package com.ti.lab02.repo;


import com.ti.lab02.github.dto.GitHubRepositoryQueryResponseDTO;
import com.ti.lab02.global.domain.exceptions.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RepositoryService {

    @Autowired
    private IRepositoryRepository repositoryRepository;

    @Transactional
    public void batchSave(List<Repository> repositories) {
        repositories.forEach(repository -> {
            repositoryRepository.save(repository);
        });
    }

    public List<Repository> batchBuild(List<GitHubRepositoryQueryResponseDTO> dtos) {
        List<Repository> repositories = new ArrayList<>();

        for (GitHubRepositoryQueryResponseDTO dto : dtos) {
            Repository repository = Repository.builder()
                    .url(dto.getUrl())
                    .diskUsage(dto.getDiskUsage())
                    .name(dto.getName())
                    .releaseTotalCount(dto.getReleases().getTotalCount())
                    .startgazerTotalCount(dto.getStargazers().getTotalCount())
                    .build();

            repositories.add(repository);
        }

        return repositories;
    }

    public List<Repository> findAll() {
        return repositoryRepository.findAll();
    }

    public void save(Repository repository) {
        repositoryRepository.save(repository);
    }

    public Repository findById(long id) {
        return repositoryRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Repositório não encontrado", HttpStatus.NOT_FOUND));
    }
}
