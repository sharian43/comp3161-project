CREATE DATABASE cms;

USE cms;

--USER Table
CREATE TABLE User (
    userID SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    userPassword VARCHAR(255) NOT NULL,
    userRole VARCHAR(20) CHECK (userRole IN ('ADMIN', 'LECTURER', 'STUDENT')) NOT NULL
);

--ACCOUNT Table
CREATE TABLE Account(
    accountID SERIAL PRIMARY KEY,
    acc_name VARCHAR(100) UNIQUE NOT NULL,
    acc_contact_info VARCHAR(255),
    accRole VARCHAR(20) CHECK (userRole IN ('ADMIN', 'LECTURER', 'STUDENT')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    created_by INT NOT NULL,
    FOREIGN KEY (created_by) REFERENCES User(userID),
    FOREIGN KEY (accRole) REFERENCES User(userRole)
);

--LOGIN Table (tracks the period they were logged in for)
CREATE TABLE Login(
    sessionID SERIAL PRIMARY KEY,
    userID INT NOT NULL,
    session_period TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID)
);

--ADMIN Table (subtype of USER)
CREATE TABLE Admin(
    adminID SERIAL PRIMARY KEY,
    userID INT NOT NULL UNIQUE,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    FOREIGN KEY (userID) REFERENCES User(userID)
);

--STUDENT Table (subtype of USER)
CREATE TABLE Student(
    studentID SERIAL PRIMARY KEY,
    userID INT NOT NULL,
    firstName VARCHAR (255),
    lastName VARCHAR(255),
    department VARCHAR(255),
    gpa DECIMAL(3,2),
    CHECK (gpa >= 0.00 AND gpa <= 4.00), --constraint to enforce valid GPA range
    FOREIGN KEY (userID) REFERENCES User (userID)
);

--LECTURER Table (subtype of USER)
CREATE TABLE Lecturer(
    lecturerID SERIAL PRIMARY KEY,
    userID INT NOT NULL UNIQUE,
    firstName VARCHAR (255),
    lastName VARCHAR(255),
    department VARCHAR(255),
    schedule VARCHAR(255),
    FOREIGN KEY (userID) REFERENCES User(userID)
);

--COURSE Table
CREATE TABLE Course (
    courseID SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL, 
    lecturerID INT UNIQUE,
    created_by INT NOT NULL, -- aid with contraint on application level to ensure that the acc was made by an admin
    FOREIGN KEY (lecturerID) REFERENCES Lecturer(lecturerID),
    FOREIGN KEY (created_by) REFERENCES Admin(adminID)
);


--CALENDER EVENT Table
CREATE TABLE CalendarEvent(
    eventID SERIAL PRIMARY KEY,
    courseID INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    event_date DATE,
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

--SECTIONS Table
CREATE TABLE Section(
    sectionID SERIAL PRIMARY KEY,
    courseID INT NOT NULL,
    section_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

--SECTION ITEM Table
CREATE TABLE SectionItem(
    itemID SERIAL PRIMARY KEY,
    sectionID INT NOT NULL,
    item_type VARCHAR(50) CHECK (item_type IN ('LECTURE_SLIDE', 'ASSIGNMENT')) NOT NULL,
    FOREIGN KEY (sectionID) REFERENCES Section(sectionID)
);

--LECTURE SLIDES Table (subtype of SECTION ITEM)
CREATE TABLE LectureSlide(
    slideID SERIAL PRIMARY KEY,
    itemID INT NOT NULL UNIQUE,
    slide_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (itemID) REFERENCES SectionItem(itemID)
);

--ASSIGNMENT Table (subtype of SECTION ITEM)
CREATE TABLE Assignment(
    assignmentID SERIAL PRIMARY KEY,
    itemID INT NOT NULL,
    assignmentName VARCHAR(255) NOT NULL,
    assignmentGrade DECIMAL(5,2),
    studentID INT NOT NULL,
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (itemID) REFERENCES SectionItem(itemID)
);

--DISCUSSION FORUMS Table
CREATE TABLE DiscussionForum(
    forumID SERIAL PRIMARY KEY,
    courseID INT NOT NULL,
    topic VARCHAR(255) NOT NULL,
    creator INT NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    FOREIGN KEY (creator) REFERENCES User(userID)
);

--DISCUSSION THREADS Table (child of DISCUSSION FORUMS)
CREATE TABLE DiscussionThread(
    threadID SERIAL PRIMARY KEY,
    forumID INT NOT NULL,
    userID INT NOT NULL,
    content TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parentThreadID INT, --if NULL it's a top level thread else a reply to another thread
    FOREIGN KEY (forumID) REFERENCES DiscussionForum(forumID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (parentThreadID) REFERENCES DiscussionThread(threadID) ON DELETE CASCADE --If a parent thread is deleted, all its replies (children) are also deleted automatically
);
 
-- STUDENT to COURSE (A student is assigned to a course)
CREATE TABLE Enrol (
    studentID INT NOT NULL,
    courseID INT NOT NULL,
    PRIMARY KEY (studentID, courseID),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

