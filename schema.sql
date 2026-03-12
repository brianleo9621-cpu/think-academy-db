USE think_academy;

CREATE TABLE IF NOT EXISTS students (
    student_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100),
    email        VARCHAR(100) UNIQUE,
    age          INT
);

CREATE TABLE IF NOT EXISTS sat_responses (
    response_id  INT AUTO_INCREMENT PRIMARY KEY,
    student_id   INT,
    score        INT,
    submitted_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);