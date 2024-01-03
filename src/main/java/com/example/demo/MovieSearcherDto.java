package com.example.demo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
@AllArgsConstructor
@NoArgsConstructor
@Data
public class MovieSearcherDto {
    private String actors;
    private String category;
    private List<String> date;
    private String directorNames;
    private Double maxScore;
    private Double minScore;
    private String movieName;
    private Boolean positive;
}

