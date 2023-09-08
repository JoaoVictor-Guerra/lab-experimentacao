package com.ti.lab02.github.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;


@Data
@Builder
public class GitHubRepositoryQueryResponseDTO {

    @JsonProperty("name")
    private String name;
    @JsonProperty("url")
    private String url;
    @JsonProperty("diskUsage")
    private long diskUsage;
    @JsonProperty("releases")
    private GitHubRepositoryReleasesInternalDTO releases;
}
