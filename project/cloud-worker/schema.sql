CREATE TABLE IF NOT EXISTS greenhouses (
	greenhouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE,
	location TEXT
);

CREATE TABLE sensors (
	sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
	greenhouse_id INTEGER NOT NULL,
	device_name TEXT NOT NULL,
	sensor_type TEXT,

	UNIQUE (greenhouse_id, device_name),
	FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(greenhouse_id)
);

CREATE TABLE sensor_readings (
	reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
	sensor_id INTEGER NOT NULL, 
	type TEXT NOT NULL,
	value REAL NOT NULL,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

CREATE INDEX idx_sensor_time ON sensor_readings (sensor_id, timestamp);
