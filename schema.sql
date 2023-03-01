DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS character;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE character (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  character_name TEXT NOT NULL,
  character_class TEXT NOT NULL,
  character_race TEXT NOT NULL,
  character_strenght TEXT NOT NULL,
  character_dexterity TEXT NOT NULL,
  character_constitution TEXT NOT NULL,
  character_intelligence TEXT NOT NULL,
  character_wisdom TEXT NOT NULL,
  character_charisma TEXT NOT NULL,
  
  FOREIGN KEY (author_id) REFERENCES user (id)
);