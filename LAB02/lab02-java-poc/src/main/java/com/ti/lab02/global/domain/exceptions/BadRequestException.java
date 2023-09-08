package com.ti.lab02.global.domain.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST)
public class BadRequestException extends HttpException {
    public BadRequestException(String message, HttpStatus status) {
        super(message, status);
    }
}