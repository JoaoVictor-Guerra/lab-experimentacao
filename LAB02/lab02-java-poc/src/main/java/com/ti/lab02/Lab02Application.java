package com.ti.lab02;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ti.lab02.github.GitHubService;
import okhttp3.*;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.RequestHeader;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;


@SpringBootApplication
public class Lab02Application {

    public static void main(String[] args) throws IOException {
        SpringApplication.run(Lab02Application.class, args);
    }

    @Bean
    public CommandLineRunner commandLineRunner (
            GitHubService service ) {
        return args -> {
            service.request();
        };

    };
}
