CREATE TABLE members (
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    account TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE histories (
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    memberid INTEGER,
    time DATETIME DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (memberid) REFERENCES members(id)
);

CREATE TABLE test (
    id INTEGER NOT NULL,
    actual_1 INT,
    actual_2 INT,
    actual_3 INT,
    actual_4 INT,
    actual_5 INT,
    guess_1 INT,
    guess_2 INT,
    guess_3 INT,
    guess_4 INT,
    guess_5 INT,
    FOREIGN KEY (id) REFERENCES histories(id)
);

CREATE TABLE temp (
    id INTEGER NOT NULL,
    temp_0 REAL,
    temp_1 REAL,
    temp_2 REAL,
    temp_3 REAL,
    temp_4 REAL,
    temp_5 REAL,
    temp_6 REAL,
    temp_7 REAL,
    temp_8 REAL,
    temp_9 REAL,
    FOREIGN KEY (id) REFERENCES histories(id)
);
