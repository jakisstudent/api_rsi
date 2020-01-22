CREATE TABLE highscores
(
    id SERIAL,
    name character varying(100) NOT NULL,
    score integer NOT NULL,
    PRIMARY KEY (id)
);