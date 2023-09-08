package com.ti.lab02.github;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.ti.lab02.github.dto.GitHubRepositoryQueryResponseDTO;
import com.ti.lab02.github.dto.GitHubRepositoryReleasesInternalDTO;
import com.ti.lab02.repo.Repository;
import com.ti.lab02.repo.RepositoryService;
import okhttp3.*;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class GitHubService {

    @Value("${application.enviroment.github.access_token}")
    private String accessToken;

    @Autowired
    private RepositoryService repositoryService;

    private static final String QUERY = "query ($cursor: String) {\n" +
            "  search(query: \"language:Java stars:>100\", type: REPOSITORY, first: 100, after: $cursor) {\n" +
            "    edges {\n" +
            "      node {\n" +
            "        ... on Repository {\n" +
            "          name\n" +
            "          url\n" +
            "          diskUsage\n" +
            "          releases{\n" +
            "            totalCount\n" +
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

    public void request() throws IOException {
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
            List<GitHubRepositoryQueryResponseDTO> dtoList;
            dtoList = new ArrayList<>();
            for (JsonNode edgeNode : edgesNode) {
                JsonNode node = edgeNode.get("node");

                String name = node.path("name").asText();
                String url = node.path("url").asText();
                long diskUsage = node.path("diskUsage").asLong();
                int releasesTotalCount = node.path("releases").path("totalCount").asInt();

                GitHubRepositoryQueryResponseDTO dto = GitHubRepositoryQueryResponseDTO.builder()
                        .name(name)
                        .url(url)
                        .diskUsage(diskUsage)
                        .releases(GitHubRepositoryReleasesInternalDTO.builder().totalCount(releasesTotalCount).build())
                        .build();

                dtoList.add(dto);
            }

            return dtoList;

        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
