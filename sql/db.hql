DROP DATABASE IF EXISTS projectbigdata CASCADE;
CREATE DATABASE projectbigdata;
USE projectbigdata;

SET mapreduce.map.output.compress = true;
SET mapreduce.map.output.compress.codec = org.apache.hadoop.io.compress.SnappyCodec;

-- Create tables

-- comments table
CREATE EXTERNAL TABLE comments STORED AS AVRO LOCATION '/project/comments' TBLPROPERTIES ('avro.schema.url'='/project/avsc/comments.avsc');


-- course table
CREATE EXTERNAL TABLE course STORED AS AVRO LOCATION '/project/course' TBLPROPERTIES ('avro.schema.url'='/project/avsc/course.avsc');

-- For checking the content of tables
SELECT * from comments LIMIT 10;
SELECT * from course LIMIT 10;

SET hive.enforce.bucketing=true;

-- EDA
-- 1. You can calculate the average rating for courses based on their payment type. This insight helps understand how different payment models affect course ratings.
INSERT OVERWRITE LOCAL DIRECTORY '/root/q1'
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
SELECT payment, AVG(rating) AS avg_rating
FROM course
GROUP BY payment;


-- 2. Identify the top courses with the highest number of subscribers. This insight can help you understand which courses are the most popular among users.
INSERT OVERWRITE LOCAL DIRECTORY '/root/q2'
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
SELECT title, subscriber
FROM course
ORDER BY subscriber DESC
LIMIT 5;


-- 3. Find course with high rates (e.g., rates greater than 4.0) and the corresponding course titles. This insight can help you identify highly praised courses.
INSERT OVERWRITE LOCAL DIRECTORY '/root/q3'
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
SELECT c.title, c.rating, c.subscriber
FROM course c
WHERE c.rating > 4.0;


-- 4. Analyze the relationship between the number of lectures in a course and the average comment rate. This insight can help you understand if longer or shorter courses receive more feedback.
INSERT OVERWRITE LOCAL DIRECTORY '/root/q4'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT num_lecture, AVG(rating) AS avg_comment_rate
FROM course
GROUP BY num_lecture;


-- 5. Explore the distribution of the number of reviews for courses. This insight can help you understand the typical review activity on the platform.
INSERT OVERWRITE LOCAL DIRECTORY '/root/q5'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT num_reviews, COUNT(*) AS num_courses
FROM course
GROUP BY num_reviews
ORDER BY num_reviews;


