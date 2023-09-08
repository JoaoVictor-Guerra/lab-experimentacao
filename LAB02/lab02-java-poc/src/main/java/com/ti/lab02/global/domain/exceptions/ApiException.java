package com.ti.lab02.global.domain.exceptions;

public class ApiException extends RuntimeException{
    public ApiException(String message){
        super(message);
    }
}
