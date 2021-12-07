DROP TABLE if EXISTS albums;

CREATE TABLE recipe (
        recipeId integer PRIMARY KEY,
        title text,
        description text,
        ingredients text,
        instructions text,
        image blob,
        wantToTry boolean,
        haveTried boolean


);

CREATE TABLE recipeComment (
        commentId integer PRIMARY KEY,
        comment text,
        name text,
        commentdate date,
        FOREIGN KEY (recipeId)
                REFERENCES recipe (recipeId)
);

CREATE TABLE diet (
        dietId integer PRIMARY KEY,
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
