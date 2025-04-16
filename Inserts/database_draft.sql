create database 3161project;
use 3161project;

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    user_role VARCHAR(20) CHECK (role IN ('admin', 'lecturer', 'student')) NOT NULL
);

CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    lecturer_id INT UNIQUE,
    FOREIGN KEY (lecturer_id) REFERENCES Users(user_id)
);

CREATE TABLE Calendar_Events (
    event_id SERIAL PRIMARY KEY,
    course_id INT,
    title VARCHAR(255),
    description TEXT,
    event_date DATE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

