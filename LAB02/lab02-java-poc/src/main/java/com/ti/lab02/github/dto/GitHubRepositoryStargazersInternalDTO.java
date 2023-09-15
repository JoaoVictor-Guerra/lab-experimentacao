package com.ti.lab02.github.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class GitHubRepositoryStargazersInternalDTO {

    @JsonProperty("totalCount")
    private long totalCount;
}
