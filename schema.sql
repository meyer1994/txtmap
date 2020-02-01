

CREATE TABLE item (
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    char CHAR(1) NOT NULL DEFAULT ' ',

    PRIMARY KEY (x, y)
);
