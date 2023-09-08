package com.ti.lab02.utils;

import java.util.UUID;

public class HashUtils {

    public static String generateHash(){

        return UUID.randomUUID().toString().replaceAll("-", "");
    }
}
