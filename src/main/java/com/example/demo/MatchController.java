package com.example.demo;

import org.neo4j.driver.Driver;
import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.Session;
import org.neo4j.driver.internal.value.NullValue;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

@RestController
@RequestMapping("/neo4j")
public class MatchController {
    private final Driver driver;

    public MatchController(Driver driver) {

        this.driver = driver;
        try (Session session = driver.session()) {
            //进行预热查询
            session.run("MATCH (n) RETURN count(n)");
        }
    }

    @PostMapping(path = "/match", produces = MediaType.APPLICATION_JSON_VALUE)
    //根据条件查找电影
    public HashMap<String, Object> getMovieByCondition(@RequestBody HashMap<String, MovieSearcherDto> MovieInfo) {
//MATCH (m:Movie {title:'Book and Sword', isPositive:'True'})-[:Belong]->(c:Category)
//RETURN COUNT(m)
        //所以需要分别找到电影、演员等需要满足什么条件
        try (Session session = driver.session()) {
            MovieSearcherDto MovieSearcher = MovieInfo.get("movieInfo");
            String query = "match (m:Movie) ";
            //首先把MovieSearcher转为我们需要的数据
            //以下几项内容需要按逗号分隔：actors,directorNames,category
            List<String> actor_list = new ArrayList<>();
            //如果不为空，就按逗号分隔
            if (MovieSearcher.getActors() != null && MovieSearcher.getActors().trim() != "") {
                String[] actors = MovieSearcher.getActors().split(",");
                for (String actor : actors) {
                    actor_list.add(actor.trim());
                }
            }
            List<String> director_list = new ArrayList<>();
            if (MovieSearcher.getDirectorNames() != null && MovieSearcher.getDirectorNames().trim() != "") {
                String[] directors = MovieSearcher.getDirectorNames().split(",");
                for (String director : directors) {
                    director_list.add(director.trim());
                }
            }
            List<String> category_list = new ArrayList<>();
            if (MovieSearcher.getCategory() != null && MovieSearcher.getCategory().trim() != "") {
                String[] categories = MovieSearcher.getCategory().split(",");
                for (String category : categories) {
                    category_list.add(category.trim());
                }
            }
            //接下来处理date，前端传来两个字符串，分别是最小日期和最大日期
            List<String> date_list = MovieSearcher.getDate();
            String start_date=null,end_date=null;
            if(date_list!=null&&date_list.size()>=1){
                start_date=date_list.get(0);
                if(date_list.size()>=2)
                    end_date=date_list.get(1);
            }
            System.out.println("MovieSearcher:"+MovieSearcher.toString());
            System.out.println("start_date:"+start_date+" end_date:"+end_date);
            //已知，start_date和end_date的格式为：yyyy-mm-ddThh:mm:ss.000Z 例如：2010-11-02T00:00:00.000Z
            //我们需要把它们转为：yyyy-mm-dd
            int start_year = 0, start_month = 0, start_day = 0, end_year = 0, end_month = 0, end_day = 0;
            if (start_date != null && start_date != "") {
                String[] start_date_list = start_date.split("T");
                String[] start_date_final_list = start_date_list[0].split("-");
                start_year = Integer.parseInt(start_date_final_list[0]);
                start_month = Integer.parseInt(start_date_final_list[1]);
                start_day = Integer.parseInt(start_date_final_list[2]);
            }
            if (end_date != null && end_date != "") {
                String[] end_date_list = end_date.split("T");
                String[] end_date_final_list = end_date_list[0].split("-");
                end_year = Integer.parseInt(end_date_final_list[0]);
                end_month = Integer.parseInt(end_date_final_list[1]);
                end_day = Integer.parseInt(end_date_final_list[2]);
            }
            //先判断它是否有连接什么关系
            //下面这些都出现在where之前
            // 类别
            if (!category_list.isEmpty()) {
                for (String category : category_list)
                    query += " , (m)-[:Belong]->(:Category{name:\"" + category + "\"})";
            }
            // 导演名称
            if (!director_list.isEmpty()) {
                for (String directorName : director_list) {
                    query += " ,(m)<-[:Direct]-(:Person{name:\"" + directorName + "\"})";
                }
            }
            // 演员名称
            if (!actor_list.isEmpty()) {
                for (String actor : actor_list) {
                    query += " ,(m)<-[:Act]-(:Person{name:\"" + actor + "\"})";
                }
            }
            //where只出现一次，后面的条件都用and连接
            Boolean whereAppear = false;
            // 电影名称 是对大小写不敏感的 支持模糊查询
            if (MovieSearcher.getMovieName() != null && MovieSearcher.getMovieName().trim() != "") {
                query += " where toLower(m.title) contains toLower(\"" + MovieSearcher.getMovieName() + "\") ";
                whereAppear = true;
            }
            //发布日期
            if (start_date != null) {
                if (whereAppear) {
                    query += " and ";
                } else {
                    query += " where ";
                    whereAppear = true;
                }
                query += " toInteger(m.year)*10000+toInteger(m.month)*100+toInteger(m.day) >= " +
                        (10000 * start_year + 100 * start_month + start_day) + " ";
            }
            if (end_date != null) {
                if (whereAppear) {
                    query += " and ";
                } else {
                    query += " where ";
                    whereAppear = true;
                }
                query += " toInteger(m.year)*10000+toInteger(m.month)*100+toInteger(m.day) <= " +
                        (10000 * end_year + 100 * end_month + end_day) + " ";
            }
            //正向评论
            if (MovieSearcher.getPositive() != null) {
                if (whereAppear) {
                    query += " and ";
                } else {
                    query += " where ";
                    whereAppear = true;
                }
                if (MovieSearcher.getPositive() == true)
                    query += " m.has_positive = \"True\" ";
                else
                    query += " m.has_positive = \"False\" ";
            }
            // 最低评分
            if (MovieSearcher.getMinScore() != null) {
                if (whereAppear) {
                    query += " and ";
                } else {
                    query += " where ";
                    whereAppear = true;
                }
                query += " toFloat(m.rating) >=" + MovieSearcher.getMinScore() + " ";
            }
            // 最高评分
            if (MovieSearcher.getMaxScore() != null) {
                if (whereAppear) {
                    query += " and ";
                } else {
                    query += " where ";
                    whereAppear = true;
                }
                query += " toFloat(m.rating) <= " + MovieSearcher.getMaxScore() + " ";
            }

            query += " return m";
            query += " limit 20";
            System.out.println("查询语句为: " + query);

            // 记录开始时间
            long startTime = System.currentTimeMillis();
            Result res = session.run(query);
//构建响应，它包括：movies num time
            HashMap<String, Object> response = new HashMap<>();
            List<Record> result = res.list();//通过执行请求，返回的内容
            List<HashMap<String, Object>> movieResult = new ArrayList<>();//整理返回的电影信息
            // 记录结束时间
            long endTime = System.currentTimeMillis();
            // 返回一部分数据
            for (int i = 0; i < result.size() && i < 20; ++i) {
                //System.out.println(result.get(i));
                if (result.get(i).get("m") == NullValue.NULL)
                    continue;
                HashMap<String, Object> movieNode = new HashMap<>();
                //找第i个结点的属性
                if (result.get(i).get("m").get("title") != NullValue.NULL) {
                    movieNode.put("movieName", result.get(i).get("m").get("title").asString());
                }
                if (result.get(i).get("m").get("format") != NullValue.NULL) {
                    String format = result.get(i).get("m").get("format").asString();
                    format = format.replaceAll("\\[|\\]|'|\"", "");  // 去除方括号、单引号和双引号
                    movieNode.put("format", format);
                }
//                if (result.get(i).get("m").get("rating") != NullValue.NULL){
//                    movieNode.put("score",String.valueOf(result.get(i).get("m").get("rating")));
//                }//目前不需要评分
                if (result.get(i).get("m").get("comment_num") != NullValue.NULL) {
                    int comment_num = Integer.parseInt(result.get(i).get("m").get("comment_num").asString());
                    movieNode.put("comment_num", String.valueOf(comment_num));
                }
                String year = null, month = null, day = null;
                if (result.get(i).get("m").get("year") != NullValue.NULL) {
                    year = result.get(i).get("m").get("year").asString();
                }
                if (result.get(i).get("m").get("month") != NullValue.NULL) {
                    month = result.get(i).get("m").get("month").asString();
                }
                if (result.get(i).get("m").get("day") != NullValue.NULL) {
                    day = result.get(i).get("m").get("day").asString();
                }
                if (year != null && month != null && day != null)
                    movieNode.put("time", year + "-" + month + "-" + day);
                else
                    movieNode.put("time", "未知");
                movieResult.add(movieNode);
            }
System.out.println("接收到的电影为："+movieResult);
            response.put("movies", movieResult);
            response.put("movieNum", result.size());//所有符合条件的电影数
            response.put("time", endTime - startTime);

            return response;
        }
    }

}



