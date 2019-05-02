DROP TABLE IF EXISTS yelp_resturant;
DROP TABLE IF EXISTS yelp_user;
DROP TABLE IF EXISTS yelp_review;

CREATE TABLE yelp_resturant(
    resturant_id TEXT NOT NULL PRIMARY KEY,
    name TEXT,
    rating DOUBLE,
    cuisine TEXT
);


CREATE TABLE yelp_user(
    user_id TEXT NOT NULL PRIMARY KEY,
    name TEXT
);

CREATE TABLE yelp_review(
    resturant_id TEXT,
    user_id TEXT,
    description TEXT,
    rating DOUBLE,
    date TEXT,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    FOREIGN KEY(user_id) REFERENCES yelp_user(user_id) ON DELETE CASCADE,
    FOREIGN KEY(resturant_id) REFERENCES yelp_resturant(resturant_id)  ON DELETE CASCADE
);

