package com.ti.lab02.start;

import com.ti.lab02.ckmetric.CKMetricService;
import com.ti.lab02.github.GitHubService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class Start {

    @Autowired
    private GitHubService gitHubService;

    @Autowired
    private CKMetricService ckMetricService;

    @EventListener(ApplicationReadyEvent.class)
    public void letsGo() throws IOException {
        gitHubService.request(10);
        ckMetricService.extractMetricsOfAllRepositories();

    }
}
