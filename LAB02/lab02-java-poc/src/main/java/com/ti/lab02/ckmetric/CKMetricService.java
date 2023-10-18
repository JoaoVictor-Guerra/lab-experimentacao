package com.ti.lab02.ckmetric;

import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.exceptions.CsvException;
import com.ti.lab02.github.GitHubService;
import com.ti.lab02.repo.Repository;
import com.ti.lab02.repo.RepositoryService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class CKMetricService {

    @Autowired
    private ICKMetricRepository ckMetricRepository;

    @Autowired
    private RepositoryService repositoryService;

    @Autowired
    private GitHubService gitHubService;


    public void extractMetricsOfAllRepositories() {
        List<Repository> repositoryList = repositoryService.findAll();

        int startingPoint = 0;
        for (int i = startingPoint ; i <= 1000 ; i++){
            extractMetricsFromRepository(repositoryList.get(i));
            gitHubService.removeGitHubRepository(repositoryList.get(i).getName());
        }
    }

    public void extractMetricsFromRepository(Repository repository) {
        try {
            gitHubService.cloneGitHubRepository(repository.getUrl(), "");
            runCkTool(repository);
            CKMetric collectedCKMetric = processCks(repository);
            collectedCKMetric.setRepository(repository);
            ckMetricRepository.save(collectedCKMetric);
        } catch (IOException | InterruptedException | CsvException e) {
            throw new RuntimeException("Erro ao extrair métricas do repositório: " + repository.getName(), e);
        }
    }

    public CKMetric processCks(Repository repository) throws IOException, CsvException {
        String csvPath = "class.csv";

        try (CSVReader csvReader = new CSVReaderBuilder(new FileReader(csvPath))
                .withSkipLines(1)
                .build()) {

            List<String[]> csvData = csvReader.readAll();

            // Extrair valores das colunas relevantes
            List<Double> cboValues = csvData.stream()
                    .map(row -> Double.parseDouble(row[3])) // Índice da coluna "cbo"
                    .collect(Collectors.toList());

            List<Integer> locValues = csvData.stream()
                    .map(row -> Integer.parseInt(row[32])) // Índice da coluna "loc"
                    .collect(Collectors.toList());

            List<Integer> ditValues = csvData.stream()
                    .map(row -> Integer.parseInt(row[7])) // Índice da coluna "dit"
                    .collect(Collectors.toList());

            List<Double> lcomValues = csvData.stream()
                    .map(row -> Double.parseDouble(row[11])) // Índice da coluna "lcom"
                    .collect(Collectors.toList());

            // Calcular métricas
            double cboMedian = calculateMedian(cboValues);
            int locSum = locValues.stream().mapToInt(Integer::intValue).sum();
            int ditMax = ditValues.stream().mapToInt(Integer::intValue).max().orElse(0);
            double lcomMedian = calculateMedian(lcomValues);

            System.out.println("Mediana CBO: " + cboMedian);
            System.out.println("Soma LOC: " + locSum);
            System.out.println("Maior DIT: " + ditMax);
            System.out.println("Mediana LCOM: " + lcomMedian);

            return CKMetric.builder()
                    .loc(locSum)
                    .cbo(cboMedian)
                    .dit(ditMax)
                    .lcom(lcomMedian)
                    .build();
        }
    }

    private double calculateMedian(List<Double> values) {
        if (!values.isEmpty()) {
            values.sort(Double::compareTo);
            int size = values.size();
            if (size % 2 == 0) {
                int middleIndex1 = (size - 1) / 2;
                int middleIndex2 = middleIndex1 + 1;
                return (values.get(middleIndex1) + values.get(middleIndex2)) / 2.0;
            } else {
                int middleIndex = size / 2;
                return values.get(middleIndex);
            }
        }
        return 0;
    }

    private void runCkTool(Repository repository) {
        String command = "java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar " + repository.getName() + "/";

        ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", command);
        processBuilder.redirectErrorStream(true);

        try {
            Process process = processBuilder.start();
            int exitCode = process.waitFor();

            System.out.println("Comando a ser executado: " + command);

            if (exitCode == 0) {
                System.out.println("Métricas CK geradas para " + repository.getName());
            } else {
                System.err.println("Erro ao processar métricas CK do repositório. Código de saída: " + exitCode);
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        System.err.println(line);
                    }
                }
            }
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException("Erro ao executar a ferramenta CK para o repositório: " + repository.getName(), e);
        }
    }

}
