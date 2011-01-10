BEGIN TRANSACTION;
CREATE TABLE exifs (date TEXT, exposure TEXT, focal TEXT, id INTEGER PRIMARY KEY, pictureid NUMERIC, size TEXT);
CREATE TABLE pictures (thumbnail TEXT, description TEXT, filename NUMERIC, id INTEGER PRIMARY KEY, path TEXT, volumeid NUMERIC);
CREATE TABLE picturetags (id INTEGER PRIMARY KEY, pictureid NUMERIC, tagid NUMERIC);
CREATE TABLE tags (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE volumes (id INTEGER PRIMARY KEY, is_attached NUMERIC, path TEXT);
CREATE UNIQUE INDEX tags_name ON tags(name ASC);
COMMIT;