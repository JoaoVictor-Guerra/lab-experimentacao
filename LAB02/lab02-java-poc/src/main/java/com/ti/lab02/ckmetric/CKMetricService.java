package com.ti.lab02.ckmetric;


import com.github.mauricioaniche.ck.CK;
import com.github.mauricioaniche.ck.CKClassResult;
import com.github.mauricioaniche.ck.CKNotifier;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.exceptions.CsvException;
import com.ti.lab02.github.GitHubService;
import com.ti.lab02.repo.Repository;
import com.ti.lab02.repo.RepositoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

@Service
public class CKMetricService {

    @Autowired
    private ICKMetricRepository ckMetricRepository;

    @Autowired
    private RepositoryService repositoryService;

    @Autowired
    private GitHubService gitHubService;

    public void extractMetricsOfAllRepositories(){
        List<Repository> repositoryList = repositoryService.findAll();

        repositoryList.forEach(repository -> {
            CKMetric ckMetric = null;
            try {
                ckMetric = extractMetricsFromRepository(repository);
            } catch (IOException e) {
                throw new RuntimeException(e);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (CsvException e) {
                throw new RuntimeException(e);
            }
            repository.setCkMetric(ckMetric);
            repositoryService.save(repository);
        });
    }

    private CKMetric extractMetricsFromRepository(Repository repository) throws IOException, InterruptedException, CsvException {
        gitHubService.cloneGitHubRepository(repository.getUrl(), "");
        this.runCkTool(repository);
        return this.proccessCks(repository);

    }

    private CKMetric proccessCks(Repository repository) throws IOException, CsvException {
        String csvPath = "class.csv";

        try (CSVReader csvReader = new CSVReaderBuilder(new FileReader(csvPath))
                .withSkipLines(1) // Ignora a primeira linha se for um cabeçalho
                .build()) {

            List<String[]> csvData = csvReader.readAll();

            // Assumindo que as colunas lcom, loc, cbo e dit existem no CSV
            double totalLcom = csvData.stream()
                    .mapToDouble(row -> Double.parseDouble(row[1])) // Índice da coluna "lcom"
                    .average()
                    .orElse(0.0);

            int totalLoc = csvData.stream()
                    .mapToInt(row -> Integer.parseInt(row[2])) // Índice da coluna "loc"
                    .sum();

            double totalCbo = csvData.stream()
                    .mapToDouble(row -> Double.parseDouble(row[3])) // Índice da coluna "cbo"
                    .average()
                    .orElse(0.0);

            int totalDit = csvData.stream()
                    .mapToInt(row -> Integer.parseInt(row[4])) // Índice da coluna "dit"
                    .max()
                    .orElse(0);

            System.out.println("Total LCOM: " + totalLcom);
            System.out.println("Total LOC: " + totalLoc);
            System.out.println("Total CBO: " + totalCbo);
            System.out.println("Total DIT: " + totalDit);

            gitHubService.removeGitHubRepository(repository.getName());

            return CKMetric.builder()
                    .loc(totalLoc)
                    .cbo(totalCbo)
                    .dit(totalDit)
                    .lcom(totalLcom)
                    .build();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private void runCkTool(Repository repository) throws IOException, InterruptedException {
        String command = "java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar " + repository.getName() +" "+repository.getName()+"/";

        ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", command);
        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();
        int exitCode = process.waitFor();

        System.out.println("Comando a ser executado: " + command);

        if (exitCode == 0) {
            System.out.println("Métricas ck geradas para "+repository.getName());
        } else {
            System.err.println("Erro ao processar ck do repositório. Código de saída: " + exitCode);
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.err.println(line);
                }
            }
        }
    }

    public void calculateCbo(){

    }

    public void calculateLcom(){

    }

    public void calculateDit(){

    }

    public void calculateLoc(){

    }



}
