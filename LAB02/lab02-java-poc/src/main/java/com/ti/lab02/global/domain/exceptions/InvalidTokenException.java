package com.ti.lab02.global.domain.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.FORBIDDEN)
public class InvalidTokenException extends ForbbidenException {
    public InvalidTokenException(String message, HttpStatus status) {
        super(message, status);
    }
}