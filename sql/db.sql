-- switch to the database
\c project;

-- Optional
START TRANSACTION;

-- Add tables

CREATE TABLE course (
    course_id integer NOT NULL PRIMARY KEY,
    title VARCHAR (250) NOT NULL,
    payment VARCHAR (10) NOT NULL,
    price FLOAT,
    subscriber FLOAT,
    rating FLOAT,
    num_reviews FLOAT,
    num_comments FLOAT,
    num_lecture FLOAT
);
-- comments table
CREATE TABLE comments (
    course_id integer NOT NULL,
    id integer NOT NULL,
    rate FLOAT
);


\COPY comments FROM 'data/comments_df.csv' DELIMITER E'\t' CSV HEADER NULL AS 'null';

\COPY course FROM 'data/course_df.csv' DELIMITER E'\t' CSV HEADER NULL AS 'null';

-- optional
COMMIT;

-- For checking the content of tables
SELECT * from comments LIMIT 10;
SELECT * from course LIMIT 10;
SELECT DISTINCT c.course_id
FROM comments c
WHERE EXISTS (
    SELECT 1
    FROM course cr
    WHERE cr.course_id = c.course_id
);

