DROP TABLE IF EXISTS users, posts, post_comments;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PasswordHash VARCHAR(255)
    );

CREATE TABLE posts(
    user_id INTEGER,
    img_url VARCHAR(255),
    img_title VARCHAR(255),
    comment_date 
    up_votes INTEGER,
    down_votes INTEGER, 
    post_id SERIAL PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE post_comments(
    post_id SERIAL PRIMARY KEY,
    comment VARCHAR(255),
    username VARCHAR(255),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
    
);

