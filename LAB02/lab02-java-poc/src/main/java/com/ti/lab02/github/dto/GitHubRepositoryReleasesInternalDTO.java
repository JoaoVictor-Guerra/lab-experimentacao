package com.ti.lab02.github.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class GitHubRepositoryReleasesInternalDTO {

    @JsonProperty("totalCount")
    private long totalCount;
}
