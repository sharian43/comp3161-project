use cms;
-- At least 100,000 students
SELECT COUNT(*) AS total_students
FROM Student;

-- At least 200 courses
SELECT COUNT(*) AS total_courses
FROM Course;

-- No student can do more than 6 courses
SELECT studentID, COUNT(courseID) AS course_count 
FROM Enrol 
GROUP BY studentID 
HAVING COUNT(courseID) > 6; 

-- Each student must be enrolled in at least 3 courses
SELECT studentID, COUNT(courseID) AS course_count 
FROM Enrol 
GROUP BY studentID 
HAVING COUNT(courseID) < 3; 

-- Each course must have at least 10 students
SELECT courseID, COUNT(studentID) AS student_count 
FROM Enrol 
GROUP BY courseID 
HAVING COUNT(studentID) < 10; 

-- No lecturer can teach more than 5 courses
SELECT lecturerID, COUNT(*) AS course_count 
FROM Course
GROUP BY lecturerID 
HAVING COUNT(*) > 5;

-- Each lecturer must teach at least 1 course
SELECT l.lecturerID, l.firstName, l.lastName
FROM Lecturer l
LEFT JOIN Course c ON l.lecturerID = c.lecturerID
GROUP BY l.lecturerID
HAVING COUNT(c.courseID) = 0;
