DROP TABLE IF EXISTS users, posts, post_comments;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PasswordHash BINARY(64),
    );

CREATE TABLE posts(
    username VARCHAR(50) FOREIGN KEY REFERENCES users(username),
    img_url VARCHAR(255),
    img_title VARCHAR(255),
    up_votes INTEGER,
    down_votes INTEGER, 
    post_id SERIAL PRIMARY KEY,
);

CREATE TABLE post_comments(
    post_id FOREIGN KEY REFERENCES posts(post_id),
    comment VARCHAR(255),
    username VARCHAR(255),
);