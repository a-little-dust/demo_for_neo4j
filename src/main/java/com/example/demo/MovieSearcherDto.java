package com.example.demo;

import lombok.Data;
@Data
public class MovieSearcherDto {
    private String actors;
    private String category;
    private String startDate;
    private String endDate;
    private String directorNames;
    private Double maxScore;
    private Double minScore;
    private String movieName;
    private Boolean positive;
}

