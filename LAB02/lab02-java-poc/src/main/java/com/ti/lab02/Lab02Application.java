package com.ti.lab02;

import com.ti.lab02.ckmetric.CKMetricService;
import com.ti.lab02.github.GitHubService;
import okhttp3.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;

import java.io.IOException;

@SpringBootApplication
public class Lab02Application {

    public static void main(String[] args) throws IOException {
        SpringApplication.run(Lab02Application.class, args);
    }


}
