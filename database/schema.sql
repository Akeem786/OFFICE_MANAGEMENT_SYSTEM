-- 1) Create and use database
CREATE DATABASE IF NOT EXISTS office;
USE office;

-- 2) Schema
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  role ENUM('admin','employee') DEFAULT 'employee',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    department_id INT,
    designation VARCHAR(100),
    salary DECIMAL(10,2),
    join_date DATE,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('Not Started','In Progress','Completed') DEFAULT 'Not Started'
);

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    employee_id INT,
    title VARCHAR(255),
    description TEXT,
    due_date DATE,
    status ENUM('Pending','In Progress','Done') DEFAULT 'Pending',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    date DATE,
    status ENUM('Present','Absent','Leave') DEFAULT 'Present',
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS leaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    start_date DATE,
    end_date DATE,
    reason TEXT,
    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS assets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    purchase_date DATE,
    status VARCHAR(50) DEFAULT 'Available',
    assigned_to INT,
    assign_date DATE,
    return_date DATE,
    FOREIGN KEY (assigned_to) REFERENCES employees(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3) Seed master data

INSERT INTO departments (name, description) VALUES
('IT','Handles all IT-related tasks.'),
('HR','Manages human resources.'),
('Finance','Manages financial operations.'),
('Sales','Handles product sales.'),
('Operations','Manages daily operations.');

INSERT INTO users (username, email, password, role) VALUES
('admin_user', 'admin@example.com', 'admin123', 'admin'),
('john_doe', 'john@example.com', 'john123', 'employee'),
('jane_smith', 'jane@example.com', 'jane123', 'employee'),
('rohit_kumar', 'rohit@example.com', 'rohit123', 'employee'),
('priya_singh', 'priya@example.com', 'priya123', 'employee');


INSERT INTO employees (name, email, phone, department_id, designation, salary, join_date) VALUES
('Alice Johnson','alice.j@example.com','9123456780',1,'Software Engineer',65000.00,'2022-05-10'),
('Bob Smith','bob.s@example.com','9234567890',2,'HR Executive',55000.00,'2021-09-20'),
('Charlie Lee','charlie.l@example.com','9345678901',3,'Accountant',60000.00,'2020-06-15'),
('Diana Prince','diana.p@example.com','9456789012',4,'Sales Manager',70000.00,'2019-04-25'),
('Ethan Hunt','ethan.h@example.com','9567890123',5,'Operations Head',75000.00,'2023-01-05');

-- 4) Seed dependent data

INSERT INTO projects (title, description, start_date, end_date, status) VALUES
('Project Alpha','Internal automation project','2023-01-01','2023-06-30','Completed'),
('Project Beta','Customer-facing app','2023-03-01','2023-09-30','In Progress'),
('Project Gamma','New HR portal','2023-04-15','2023-08-15','Not Started'),
('Project Delta','CRM integration','2023-02-10','2023-07-20','In Progress'),
('Project Epsilon','Inventory System','2023-05-01','2023-11-30','Not Started');

INSERT INTO tasks (project_id, employee_id, title, description, due_date, status) VALUES
(1,1,'Setup CI/CD','Configure Jenkins pipeline.','2023-02-15','Done'),
(2,2,'Design UI','Create Figma designs.','2023-04-01','In Progress'),
(3,3,'Define Policies','List HR policies.','2023-05-10','Pending'),
(4,4,'Sales Strategy','Plan Q2 sales strategy.','2023-06-01','Pending'),
(5,5,'Vendor Onboarding','Shortlist suppliers.','2023-07-01','Pending');

INSERT INTO attendance (employee_id, date, status) VALUES
(1,'2023-04-20','Present'),
(2,'2023-04-20','Absent'),
(3,'2023-04-20','Leave'),
(4,'2023-04-20','Present'),
(5,'2023-04-20','Present');

INSERT INTO leaves (employee_id, start_date, end_date, reason, status) VALUES
(1,'2023-04-10','2023-04-12','Medical Leave','Approved'),
(2,'2023-04-15','2023-04-16','Family Function','Pending'),
(3,'2023-04-18','2023-04-19','Personal Work','Rejected'),
(4,'2023-03-25','2023-03-27','Vacation','Approved'),
(5,'2023-04-01','2023-04-02','Emergency','Pending');

INSERT INTO assets (name, description, purchase_date, status, assigned_to, assign_date, return_date) VALUES
('Laptop','Dell Latitude 7490','2022-01-15','Available',1,NULL,NULL),
('Monitor','24-inch Samsung LED','2021-11-20','Assigned',2,'2023-01-05',NULL),
('Keyboard','Mechanical Keyboard','2023-03-10','Available',NULL,NULL,NULL),
('Mouse','Wireless Mouse','2022-05-22','Returned',3,'2023-02-01','2023-02-28'),
('Headset','Noise-canceling Headset','2023-01-01','Assigned',4,'2023-03-10',NULL);

INSERT INTO notices (title, description) VALUES
('Annual Day','Annual day celebration on 30th April.'),
('New Policy','WFH policy updated for 2023.'),
('Holiday','Office will be closed on May 1st.'),
('Maintenance','Server maintenance on Sunday.'),
('Workshop','Skill workshop scheduled next week.');

INSERT INTO complaints (title, description) VALUES
('System Issue','Laptop not starting properly.'),
('AC Problem','Air conditioning not working.'),
('Chair Broken','Chair is broken and uncomfortable.'),
('Noise Issue','Construction noise disturbing work.'),
('Wi-Fi Issue','Frequent disconnections in Wi-Fi.');
ALTER TABLE assets ADD COLUMN employee_id INT;
ALTER TABLE assets ADD CONSTRAINT FK_employee_id FOREIGN KEY (employee_id) REFERENCES employees(id);
ALTER TABLE users ADD COLUMN username VARCHAR(100) NOT NULL;

DESCRIBE users;