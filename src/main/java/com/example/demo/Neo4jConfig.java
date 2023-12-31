package com.example.demo;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@Configuration
@EnableTransactionManagement
public class Neo4jConfig {
    @Value("${org.neo4j.driver.uri}")
    private String url;
    @Value("${org.neo4j.driver.authentication.username}")
    private String userName;
    @Value("${org.neo4j.driver.authentication.password}")
    private String password;
    @Bean(name = "session")
    public Session neo4jSession() {
        Driver driver = GraphDatabase.driver(url, AuthTokens.basic(userName, password));
        return driver.session();
    }
    @Bean
    public Driver neo4jDriver() {
        return GraphDatabase.driver(url, AuthTokens.basic(userName, password));
    }
//    @Bean
//    public CooperationController cooperationController(@Qualifier("session") Session session) {
//        return new CooperationController(session);
//    }
}
