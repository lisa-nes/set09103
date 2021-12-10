DROP TABLE if EXISTS albums;

DROP TABLE if EXISTS recipe;

DROP TABLE if EXISTS recipeDiet;

DROP TABLE if EXISTS diet;

DROP TABLE if EXISTS recipeComment;

CREATE TABLE recipe (
        recipeId INTEGER PRIMARY KEY AUTOINCREMENT,
        title text,
        description text,
        ingredients text,
        instructions text,
        image blob,
        wantToTry boolean,
        haveTried boolean,
	sweet boolean,
	savoury boolean,
	vegetarian boolean,
	vegan boolean,
	glutenfree boolean,
	recipetype text

);

CREATE TABLE recipeComment (
        commentId INTEGER PRIMARY KEY AUTOINCREMENT,
        comment text,
	recipeId integer,
        name text,
        commentdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (recipeId)
                REFERENCES recipe (recipeId)
);

CREATE TABLE diet (
        dietId INTEGER PRIMARY KEY AUTOINCREMENT,
        dietName text
);

CREATE TABLE recipeDiet (
        recipeId integer,
        dietId integer,
        PRIMARY KEY (recipeId,dietId),
        FOREIGN KEY (recipeId)
                REFERENCES recipe (recipeId),
        FOREIGN KEY (dietId)
                REFERENCES diet (dietId)
);
