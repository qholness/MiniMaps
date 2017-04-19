BEGIN TRANSACTION;
CREATE TABLE "users" (
	`id`	INTEGER NOT NULL,
	`username`	VARCHAR(80) UNIQUE,
	`email`	VARCHAR(120),
	`password`	VARCHAR(120) NOT NULL,
	`image_url`	VARCHAR,
	`rights`	VARCHAR,
	PRIMARY KEY(`id`)
);
CREATE TABLE clients (
	id INTEGER NOT NULL, 
	name VARCHAR(80) NOT NULL, 
	import_url VARCHAR, 
	instance_url VARCHAR, assignee VARCHAR, status VARCHAR, estimated_completion VARCHAR, import_notes VARCHAR, created_timestamp VARCHAR, updated_timestamp VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE client_status (
	id INTEGER NOT NULL, 
	status VARCHAR NOT NULL, color VARCHAR, text_color VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (status)
);
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
COMMIT;
