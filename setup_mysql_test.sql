-- Script preparing MySQL server for the project

-- Database hbnb_test_db created if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- User hbnb_test created and granted all priviledges
-- on hbnb_dev and privileges selected on performance_schema
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db. * TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
