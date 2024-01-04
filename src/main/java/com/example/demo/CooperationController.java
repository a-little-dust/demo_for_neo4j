package com.example.demo;

import org.neo4j.driver.*;
import org.neo4j.driver.Record;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


@RestController
@RequestMapping("/neo4j/cooperation")
public class CooperationController {
    private final Driver driver;

    public CooperationController(Driver driver) {
        this.driver = driver;
        try (Session session = driver.session()){
            //进行预热查询
            session.run("MATCH ()-[r]->() RETURN count(r)");
            System.out.println("预热查询完成");
        }
    }

    //不传参数 返回合作最多的演员和导演
/*Match (p:Person)-[r:MainAct|Act]->(m:Movie)<-[a:Direct]-(q:Person)：这是一个模式匹配语句，它指定了一个模式，其中 p 和 q 是 Person 类型的节点，m 是 Movie 类型的节点。通过关系 [r:MainAct|Act] 和 [a:Direct] 连接了这些节点，形成一个匹配模式。

    where id(p)<> id(q)：这是一个条件语句，用于过滤掉 p 和 q 是同一个节点的情况，即保证 p 和 q 是不同的人。

            return p.name,q.name,count(m)：这部分指定了查询结果要返回的内容，即 p 的姓名、q 的姓名以及合作的电影数量 m。

    order by count(m) desc：按照合作的电影数量 m 降序排序结果。

    limit 1：限制只返回排序后的第一条记录，即合作次数最多的那对人员的信息*/
    @GetMapping(path = "/actor_director_2",produces =  MediaType.APPLICATION_JSON_VALUE)
    public HashMap<String, Object> findMostCooperateActorAndDirector_origin(){
        try (Session session = driver.session())  {
            // 记录开始时间
            long startTime = System.currentTimeMillis();
            //直接返回名字和合作次数
            Result res= session.run("Match (p:Person)-[r:Act]->(m:Movie)<-[a:Direct]-(q:Person) " +
                    "where id(p)<> id(q) return p.name,q.name,count(m) order by count(m) desc limit 10");
            // 记录结束时间
            long endTime = System.currentTimeMillis();
            HashMap<String,Object> response = new HashMap<>();
            List<Record> result = res.list();//通过执行请求，返回的内容
            List<HashMap<String, Object>> relationResult = new ArrayList<>();//整理返回的关系信息
            for (Record r : result) {
                HashMap<String, Object> relation = new HashMap<>();
                relation.put("actor", r.get("p.name").asString());
                relation.put("director", r.get("q.name").asString());
                Value countValue = r.get("count(m)");
                if (!countValue.isNull()) {
                    Long count = countValue.asNumber().longValue();
                    relation.put("number", count.intValue());
                    relationResult.add(relation);
                }
                response.put("relation",relationResult);
            }
            response.put("time",endTime-startTime);
            return response;
        }
    }

    //优化：采用DirectAct关系，直接找到合作最多的演员和导演
    @GetMapping(path = "/actor_director",produces =  MediaType.APPLICATION_JSON_VALUE)
    public HashMap<String, Object> findMostCooperateActorAndDirector_2(){
        try (Session session = driver.session())  {
            // 记录开始时间
            long startTime = System.currentTimeMillis();
            //直接通过r.count找到合作最多的演员和导演
            Result res= session.run("Match (p:Person)-[r:DirectAct]->(q:Person) " +
                    "return p.name,q.name,r.count order by r.count desc limit 10");
            // 记录结束时间
            long endTime = System.currentTimeMillis();
            HashMap<String,Object> response = new HashMap<>();
            List<Record> result = res.list();//通过执行请求，返回的内容
            List<HashMap<String, Object>> relationResult = new ArrayList<>();//整理返回的关系信息
            for (Record r : result) {
                HashMap<String, Object> relation = new HashMap<>();
                relation.put("actor", r.get("p.name").asString());
                relation.put("director", r.get("q.name").asString());
                Value countValue = r.get("r.count");
                if (!countValue.isNull()) {
                    Long count = countValue.asNumber().longValue();
                    relation.put("number", count.intValue());
                    relationResult.add(relation);
                }
                response.put("relation",relationResult);
            }
            response.put("time",endTime-startTime);
            return response;
        }
    }
    //类似地，查找合作次数最多的演员
    //优化：使用>而不是<>，避免了重复
    @GetMapping(path = "/actor_actor", produces = MediaType.APPLICATION_JSON_VALUE)
    public HashMap<String, Object> findMostCooperateActors(){
        System.out.println("findMostCooperateActors");
        try (Session session = driver.session())  {
            // 记录开始时间
            long startTime = System.currentTimeMillis();
            //直接返回名字和合作次数
            Result res= session.run("Match (p:Person)-[r:Act]->(m:Movie)<-[a:Act]-(q:Person) " +
                    "where id(p)> id(q) return p.name,q.name,count(m) order by count(m) desc limit 10");
            // 记录结束时间
            long endTime = System.currentTimeMillis();
            HashMap<String,Object> response = new HashMap<>();
            List<Record> result = res.list();//通过执行请求，返回的内容
            List<HashMap<String, Object>> relationResult = new ArrayList<>();//整理返回的关系信息
            for(int i=0;i<result.size();++i){
                //首先判断是否已经存在这个关系
                String actor1 = result.get(i).get("p.name").asString();
                String actor2 = result.get(i).get("q.name").asString();
                String number = result.get(i).get("count(m)").toString();
                /*boolean flag = false;
                for(int j=0;j<relationResult.size()&& flag==false;j++)
                {
                    if(relationResult.get(j).get("actor1").equals(actor1)&&relationResult.get(j).get("actor2").equals(actor1))
                    {
                        flag = true;
                    } else if (relationResult.get(j).get("actor1").equals(actor2)&&relationResult.get(j).get("actor2").equals(actor1)) {
                        flag = true;
                    }
                }
                if(flag==true)
                    continue;*/
                HashMap<String, Object> relation = new HashMap<>();
                relation.put("actor1",actor1);
                relation.put("actor2",actor2);
                relation.put("number",number);
                relationResult.add(relation);
            }
            response.put("relation",relationResult);
            response.put("time",endTime-startTime);
            return response;
        }
    }

    //查找指定种类，且合作热度最高的演员
    @GetMapping(path = "/high_heat_actors_2", produces = MediaType.APPLICATION_JSON_VALUE)
    public HashMap<String, Object> findHighestHeatActors_origin(@RequestParam String category){
        try (Session session = driver.session())  {
            // 记录开始时间
            long startTime = System.currentTimeMillis();
            //直接返回名字和评论数量
            String query= new String("MATCH (p:Person)-[r:Act]->(m:Movie)<-[a:Act]-(q:Person) " );
            if(category!=null && category!="")
                query +=" , (m)-[:Belong]->(c:Category WHERE toLower(c.name) CONTAINS toLower(\'"+category+"\'))";

            query+= (" WHERE id(p) > id(q) RETURN p.name, q.name, sum(toInteger( m.comment_num)) AS totalHeat " +
                    "ORDER BY totalHeat DESC " +
                    "LIMIT 10");
            System.out.println(query);
            Result res= session.run(query);
            // 记录结束时间
            long endTime = System.currentTimeMillis();
            HashMap<String,Object> response = new HashMap<>();
            List<Record> result = res.list();//通过执行请求，返回的内容
            List<HashMap<String, Object>> relationResult = new ArrayList<>();//整理返回的关系信息
            for(int i=0;i<result.size();++i){
                //首先判断是否已经存在这个关系
                String actor1 = result.get(i).get("p.name").asString();
                String actor2 = result.get(i).get("q.name").asString();
                String heat = result.get(i).get("totalHeat").toString();
//                boolean flag = false;
//                for(int j=0;j<relationResult.size()&& flag==false;j++)
//                {
//                    if(relationResult.get(j).get("actor1").equals(actor1)&&relationResult.get(j).get("actor2").equals(actor1))
//                    {
//                        flag = true;
//                    } else if (relationResult.get(j).get("actor1").equals(actor2)&&relationResult.get(j).get("actor2").equals(actor1)) {
//                        flag = true;
//                    }
//                }
//                if(flag==true)
//                    continue;
                HashMap<String, Object> relation = new HashMap<>();
                relation.put("actor1",actor1);
                relation.put("actor2",actor2);
                relation.put("heat",heat);
                relationResult.add(relation);
            }
            response.put("relation",relationResult);
            response.put("time",endTime-startTime);
            return response;
        }
    }

    @GetMapping(path = "/high_heat_actors", produces = MediaType.APPLICATION_JSON_VALUE)
    //优化1 使用了with，避免了笛卡尔积
    //优化2 先查找指定种类的电影，再查找合作热度最高的演员
    public HashMap<String, Object> findHighestHeatActors_2(@RequestParam String category){
        try (Session session = driver.session())  {
            // 记录开始时间
            long startTime = System.currentTimeMillis();
            //直接返回名字和评论数量
            String query=new String("");
            if(category!=null && category!="")
            query+=("Match (m:Movie)-[:Belong]->(c:Category WHERE toLower(c.name) CONTAINS toLower(\'"+category+"\')) "+
                    "MATCH (p:Person)-[:Act]->(m)<-[:Act]-(q:Person) ");
            else
                query+="MATCH (p:Person)-[:Act]->(m:Movie)<-[:Act]-(q:Person) ";
            query+=(" WHERE id(p) > id(q) RETURN p.name, q.name, sum(toInteger( m.comment_num)) AS totalHeat " +
                    "ORDER BY totalHeat DESC " +
                    "LIMIT 10");
            System.out.println(query);
            Result res= session.run(query);
            // 记录结束时间
            long endTime = System.currentTimeMillis();
            HashMap<String,Object> response = new HashMap<>();
            List<Record> result = res.list();//通过执行请求，返回的内容
            List<HashMap<String, Object>> relationResult = new ArrayList<>();//整理返回的关系信息
            for(int i=0;i<result.size();++i){
                String actor1 = result.get(i).get("p.name").asString();
                String actor2 = result.get(i).get("q.name").asString();
                String heat = result.get(i).get("totalHeat").toString();
                HashMap<String, Object> relation = new HashMap<>();
                relation.put("actor1",actor1);
                relation.put("actor2",actor2);
                relation.put("heat",heat);
                relationResult.add(relation);
            }
            response.put("relation",relationResult);
            response.put("time",endTime-startTime);
            return response;
        }
    }
}


