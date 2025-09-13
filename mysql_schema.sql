-- Table for donors

CREATE TABLE donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(100) NOT NULL,
    last_donated DATE DEFAULT NULL
);
-- Table for blood requests
CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(100) NOT NULL
);
