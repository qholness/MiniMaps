DROP TABLE IF EXISTS stations;

CREATE TABLE stations (
    id INTEGER PRIMARY KEY,
    stationname VARCHAR,
    latitude FLOAT,
    longitude FLOAT
)