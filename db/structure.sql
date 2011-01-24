BEGIN TRANSACTION;
CREATE TABLE pictures (thumbnail TEXT, description TEXT, filename NUMERIC, id INTEGER PRIMARY KEY, path TEXT, volumeid NUMERIC, raw_exif TEXT);
CREATE TABLE picturetags (id INTEGER PRIMARY KEY, pictureid NUMERIC, tagid NUMERIC);
CREATE TABLE tags (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE volumes (id INTEGER PRIMARY KEY, is_attached NUMERIC, path TEXT);
CREATE UNIQUE INDEX pictures_path ON pictures(path ASC);
CREATE UNIQUE INDEX tags_name ON tags(name ASC);
COMMIT;
