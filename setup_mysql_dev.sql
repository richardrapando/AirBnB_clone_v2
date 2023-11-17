-- Script preparing a MySQL server for the project

-- Database hbnb_dev_db created if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- User hbnb_dev created and granted all priviledges
-- on hbnb_dev and privileges selected on performance_schema
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db. * TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
