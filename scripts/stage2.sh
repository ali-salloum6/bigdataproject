#!/bin/bash
hdfs dfs -rm -r /project/avsc
hdfs dfs -mkdir /project/avsc
hdfs dfs -put /project/avsc/*.avsc /project/avsc
hive -f sql/db.hql
echo "payment_status, average_rating" > output/q1.csv
cat /root/q1/* >> output/q1.csv

echo "course_title,total_subscriber" > output/q2.csv
cat /root/q2/* >> output/q2.csv

echo "course_title, rating, total_subscriber" > output/q3.csv
cat /root/q3/* >> output/q3.csv

echo "number_of_lecture, avg_rate" > output/q4.csv
cat /root/q4/* >> output/q4.csv

echo "total_reviews, total_course" > output/q5.csv
cat /root/q5/* >> output/q5.csv
