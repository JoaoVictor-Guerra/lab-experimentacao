package com.ti.lab02.github;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.ti.lab02.github.dto.GitHubRepositoryQueryResponseDTO;
import com.ti.lab02.github.dto.GitHubRepositoryReleasesInternalDTO;
import com.ti.lab02.github.dto.GitHubRepositoryStargazersInternalDTO;
import com.ti.lab02.repo.Repository;
import com.ti.lab02.repo.RepositoryService;
import okhttp3.*;
import org.eclipse.jgit.api.Git;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

@Service
public class GitHubService {

    @Value("${application.enviroment.github.access_token}")
    private String accessToken;

    @Autowired
    private RepositoryService repositoryService;

    private String cursor = null;

    private String QUERY = "query {\n" +
            "  search(query: \"language:Java stars:>100\", type: REPOSITORY, first: 2, after: " + this.cursor + ") {\n" +
            "    edges {\n" +
            "      node {\n" +
            "        ... on Repository {\n" +
            "          nameWithOwner\n" +
            "          name\n" +
            "          url\n" +
            "          diskUsage\n" +
            "          releases(orderBy: {field: CREATED_AT, direction: DESC}) {\n" +
            "              totalCount\n" +
            "          }\n" +
            "          stargazers{\n" +
            "               totalCount\n" +
            "          }\n" +
            "        }\n" +
            "      }\n" +
            "    }\n" +
            "    pageInfo {\n" +
            "      endCursor\n" +
            "      hasNextPage\n" +
            "    }\n" +
            "  }\n" +
            "}";

    public void request(int repeat) throws IOException {
        for (int i = 0 ; i < repeat ; i++){
            request();
        }
    }

    private void request()  throws IOException{
        OkHttpClient client = new OkHttpClient();

        JSONObject jsonRequest = new JSONObject();
        jsonRequest.put("query", QUERY);

        RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), jsonRequest.toString());
        Request request = new Request.Builder()
                .url("https://api.github.com/graphql")
                .header("Authorization", "Bearer " + accessToken)
                .post(requestBody)
                .build();

        Response response = client.newCall(request).execute();

        if (response.isSuccessful()) {
            String responseBody = response.body().string();

            List<GitHubRepositoryQueryResponseDTO> repositoryQueryResponseDTOs = processJsonResponse(responseBody);
            List<Repository> repositories = repositoryService.batchBuild(repositoryQueryResponseDTOs);
            repositoryService.batchSave(repositories);

        } else {
            System.out.println("Falha na solicitação GraphQL");
            System.out.println(response.code() + " " + response.message());
        }
    }

    private List<GitHubRepositoryQueryResponseDTO> processJsonResponse(String jsonResponse) {

        ObjectMapper objectMapper = new ObjectMapper();

        try {
            JsonNode rootNode = objectMapper.readTree(jsonResponse);
            JsonNode dataNode = rootNode.get("data");
            JsonNode searchNode = dataNode.get("search");
            JsonNode edgesNode = searchNode.get("edges");
            JsonNode pageInfoNode = searchNode.path("pageInfo");
            this.cursor = pageInfoNode.path("endCursor").asText();

            List<GitHubRepositoryQueryResponseDTO> dtoList;
            dtoList = new ArrayList<>();
            for (JsonNode edgeNode : edgesNode) {
                JsonNode node = edgeNode.get("node");

                String name = node.path("name").asText();
                String url = node.path("url").asText();
                long diskUsage = node.path("diskUsage").asLong();
                int releasesTotalCount = node.path("releases").path("totalCount").asInt();
                int startgazerTotalCount = node.path("startgazers").path("totalCount").asInt();


                GitHubRepositoryQueryResponseDTO dto = GitHubRepositoryQueryResponseDTO.builder()
                        .name(name)
                        .url(url)
                        .diskUsage(diskUsage)
                        .releases(GitHubRepositoryReleasesInternalDTO.builder().totalCount(releasesTotalCount).build())
                        .stargazers(GitHubRepositoryStargazersInternalDTO.builder().totalCount(startgazerTotalCount).build())
                        .build();

                dtoList.add(dto);
            }

            return dtoList;

        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void cloneGitHubRepository(String repositoryUrl, String destinationPath) throws IOException, InterruptedException {
        String command = "git clone " + repositoryUrl + " " + destinationPath;

        ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", command);
        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();
        int exitCode = process.waitFor();

        if (exitCode == 0) {
            System.out.println("Repositório clonado com sucesso em: " + destinationPath);
        } else {
            System.err.println("Erro ao clonar o repositório. Código de saída: " + exitCode);
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.err.println(line);
                }
            }
        }
    }

    public void removeGitHubRepository(String repoName) throws IOException, InterruptedException {
        String command = "rm -rf "+repoName;

        ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", command);
        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();
        int exitCode = process.waitFor();

        if (exitCode == 0) {
            System.out.println("Repositório removido com sucesso: " + repoName);
        } else {
            System.err.println("Erro ao remover o repositório. Código de saída: " + exitCode);
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.err.println(line);
                }
            }
        }
    }

//    public void cloneGitHubRepository(String repositoryUrl, String destinationPath) throws IOException, InterruptedException {
//        try {
//            // Obter o diretório de recursos como um Resource
//            Resource resource = new ClassPathResource("");
//            File resourcesDir = resource.getFile();
//
//            // Construir o caminho completo para o diretório de destino dentro dos recursos
//            String fullPath = new File(resourcesDir, destinationPath).getPath();
//
//            // Construir o comando git clone
//            String command = "git clone " + repositoryUrl + " " + fullPath;
//
//            ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", command);
//            processBuilder.redirectErrorStream(true);
//
//            Process process = processBuilder.start();
//            int exitCode = process.waitFor();
//
//            if (exitCode == 0) {
//                System.out.println("Repositório clonado com sucesso em: " + fullPath);
//            } else {
//                System.err.println("Erro ao clonar o repositório. Código de saída: " + exitCode);
//                // Tratar erros como necessário
//            }
//        } catch (IOException e) {
//            // Tratar exceções de E/S, por exemplo, se o diretório de recursos não existe
//            e.printStackTrace();
//        }
//    }
}
