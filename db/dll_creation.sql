CREATE DATABASE bio_databases;

CREATE TABLE `pubmed_retrieval` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`filename`	TEXT NOT NULL,
	`download`	INTEGER NOT NULL,
	`download_datetime`	TEXT,
	`unzip`	TEXT NOT NULL,
	`unzip_datetime`	TEXT,
	`download_path`	TEXT,
	`unzip_path`	TEXT
);

CREATE TABLE `pubmed_articles` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`pmid`	INTEGER NOT NULL UNIQUE,
	`filename`	TEXT NOT NULL,
	`json`	INTEGER NOT NULL,
	`json_datetime`	TEXT,
	`json_path`	TEXT,
	`txt`	INTEGER NOT NULL,
	`txt_datetime`	TEXT,
	`txt_path`	TEXT
);

CREATE TABLE `pmc_articles` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`pmid`	INTEGER NOT NULL UNIQUE,
	`filename`	TEXT NOT NULL,
	`download`	INTEGER NOT NULL,
	`download_datetime`	TEXT,
	`download_path`	TEXT,
	`json`	INTEGER NOT NULL,
	`json_datetime`	TEXT,
	`json_path`	TEXT,
	`txt`	INTEGER NOT NULL,
	`txt_datetime`	TEXT,
	`txt_path`	TEXT
);
