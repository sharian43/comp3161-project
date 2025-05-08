CREATE DATABASE cms;

USE cms;

-- USER Table
CREATE TABLE User (
    userID SERIAL PRIMARY KEY UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    userPassword VARCHAR(255) NOT NULL
);

-- ACCOUNT Table
CREATE TABLE Account(
    accountID SERIAL PRIMARY KEY,
    userID BIGINT UNSIGNED UNIQUE NOT NULL,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    acc_contact_info VARCHAR(255),
    accRole VARCHAR(20) CHECK (accRole IN ('ADMIN', 'LECTURER', 'STUDENT')) NOT NULL,
    accPassword VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (userID) REFERENCES User(userID)
    -- build contraints for admin only to create account at application level.
);


-- LOGIN Table (tracks the period they were logged in for)
CREATE TABLE Login(
    sessionID SERIAL PRIMARY KEY,
    userID BIGINT UNSIGNED NOT NULL,
    session_period TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID)
);

-- ADMIN Table (subtype of ACCOUNT)
CREATE TABLE Admin(
    adminID SERIAL PRIMARY KEY,
    accountID BIGINT UNSIGNED UNIQUE,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    FOREIGN KEY (accountID) REFERENCES Account(accountID)
);

-- STUDENT Table (subtype of ACCOUNT)
CREATE TABLE Student(
    studentID SERIAL PRIMARY KEY,
    accountID BIGINT UNSIGNED UNIQUE NOT NULL,
    firstName VARCHAR (255),
    lastName VARCHAR(255),
    department VARCHAR(255),
    gpa DECIMAL(3,2),
    CHECK (gpa >= 0.00 AND gpa <= 4.00), -- constraint to enforce valid GPA range
    FOREIGN KEY (accountID) REFERENCES Account(accountID)
);

-- LECTURER Table (subtype of ACCOUNT)
CREATE TABLE Lecturer(
    lecturerID SERIAL PRIMARY KEY,
    accountID BIGINT UNSIGNED UNIQUE NOT NULL,
    firstName VARCHAR (255),
    lastName VARCHAR(255),
    department VARCHAR(255),
    schedule VARCHAR(255),
    FOREIGN KEY (accountID) REFERENCES Account(accountID)
);

-- COURSE Table
CREATE TABLE Course (
    courseID SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL, 
    lecturerID BIGINT UNSIGNED  NOT NULL,
    created_by BIGINT UNSIGNED  NOT NULL, -- enforce via application logic: only Admin-created accounts can assign courses.
    FOREIGN KEY (lecturerID) REFERENCES Lecturer(lecturerID),
    FOREIGN KEY (created_by) REFERENCES Admin(adminID)
);


-- CALENDER EVENT Table
CREATE TABLE CalendarEvent(
    eventID SERIAL PRIMARY KEY,
    courseID BIGINT UNSIGNED UNIQUE NOT NULL,
    title VARCHAR(255),
    description TEXT,
    event_date DATE,
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

-- SECTIONS Table
CREATE TABLE Section(
    sectionID SERIAL PRIMARY KEY,
    courseID BIGINT UNSIGNED NOT NULL, --removed unique constraint
    section_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

-- SECTION ITEM Table
CREATE TABLE SectionItem(
    itemID SERIAL PRIMARY KEY,
    sectionID BIGINT UNSIGNED NOT NULL, -- removed unique constraint
    item_type VARCHAR(50) CHECK (item_type IN ('LECTURE_SLIDE', 'ASSIGNMENT', 'FILE', 'LINK')) NOT NULL, --added File and Link
    FOREIGN KEY (sectionID) REFERENCES Section(sectionID)
);

-- LECTURE SLIDES Table (subtype of SECTION ITEM)
CREATE TABLE LectureSlide(
    slideID SERIAL PRIMARY KEY,
    itemID BIGINT UNSIGNED UNIQUE NOT NULL,
    slide_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (itemID) REFERENCES SectionItem(itemID)
);

-- ASSIGNMENT Table (subtype of SECTION ITEM)
-- Added maxPoints and weight 
-- Removed assignmentGrade, studentID 
CREATE TABLE Assignment(
    assignmentID SERIAL PRIMARY KEY,
    itemID BIGINT UNSIGNED UNIQUE NOT NULL,
    assignmentName VARCHAR(255) NOT NULL,
    maxPoints DECIMAL(5,2) DEFAULT 100.00,
    weight DECIMAL(5,2) DEFAULT 1.00,
    FOREIGN KEY (itemID) REFERENCES SectionItem(itemID)
);

-- DISCUSSION FORUMS Table
CREATE TABLE DiscussionForum(
    forumID SERIAL PRIMARY KEY,
    courseID BIGINT UNSIGNED NOT NULL, -- removed unique constraint
    topic VARCHAR(255) NOT NULL,
    creator BIGINT UNSIGNED NOT NULL, -- removed unique constraint
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    FOREIGN KEY (creator) REFERENCES User(userID)
);

-- DISCUSSION THREADS Table (child of DISCUSSION FORUMS)
CREATE TABLE DiscussionThread(
    threadID SERIAL PRIMARY KEY,
    forumID BIGINT UNSIGNED NOT NULL, -- removed unique constraint
    userID BIGINT UNSIGNED NOT NULL, -- removed unique constraint
    title VARCHAR(255),                -- Added title field
    content TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parentThreadID BIGINT UNSIGNED, -- if NULL it's a top level thread else a reply to another thread
    FOREIGN KEY (forumID) REFERENCES DiscussionForum(forumID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (parentThreadID) REFERENCES DiscussionThread(threadID) ON DELETE CASCADE -- If a parent thread is deleted, all its replies (children) are also deleted automatically
);
 
-- STUDENT to COURSE (A student is assigned to a course)
CREATE TABLE Enrol (
    studentID BIGINT UNSIGNED  NOT NULL,--removed unique constraint
    courseID BIGINT UNSIGNED NOT NULL, --removed unique constraint
    PRIMARY KEY (studentID, courseID),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

-- Added ASSIGNMENT SUBMISSION Table
CREATE TABLE AssignmentSubmission(
    submissionID SERIAL PRIMARY KEY,
    assignmentID BIGINT UNSIGNED NOT NULL,
    studentID BIGINT UNSIGNED NOT NULL,
    submissionContent TEXT,
    submissionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade DECIMAL(5,2) NULL,
    FOREIGN KEY (assignmentID) REFERENCES Assignment(assignmentID),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    UNIQUE (assignmentID, studentID)
);

-- Added FILE Table 
CREATE TABLE File(
    fileID SERIAL PRIMARY KEY,
    itemID BIGINT UNSIGNED UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (itemID) REFERENCES SectionItem(itemID)
);

-- Added LINK Table 
CREATE TABLE Link(
    linkID SERIAL PRIMARY KEY,
    itemID BIGINT UNSIGNED UNIQUE NOT NULL,
    link_title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (itemID) REFERENCES SectionItem(itemID)
);

