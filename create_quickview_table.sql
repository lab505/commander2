CREATE DATABASE IF NOT EXISTS commander_db;
USE commander_db;

DROP TABLE IF EXISTS quick_view;
CREATE TABLE quick_view (
        add_into_table_time TIMESTAMP, INDEX(add_into_table_time),
        sensor_type VARCHAR(100), INDEX(sensor_type),
        sensor_id VARCHAR(100), INDEX(sensor_id),
        aircraft_id VARCHAR(100), INDEX(aircraft_id),
        aircraft_type VARCHAR(100), INDEX(aircraft_type),
        img_str_data LONGTEXT
)
