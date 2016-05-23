CREATE TABLE arts(
    Entry SMALLINT PRIMARY KEY,
	TapDate TIMESTAMP,
	FareProduct VARCHAR(50),
	TransitCard VARCHAR(30),
	TransactionType VARCHAR(100),
	Hour SMALLINT,
	Minute SMALLINT,
	Route VARCHAR(100),
	Departure TIMESTAMP,
	Arrival TIMESTAMP,
	station VARCHAR(100)
);


COPY ARTS FROM '/Users/connor/Desktop/bem150project/heatmap/data/stations.csv' DELIMITER ',' CSV HEADER;