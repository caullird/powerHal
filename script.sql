-- Création des tables primaires
DROP TABLE IF EXISTS institution;
DROP TABLE IF EXISTS publication;
DROP TABLE IF EXISTS conceptpublication;
DROP TABLE IF EXISTS conceptauthor;
DROP TABLE IF EXISTS author;

-- Création des relations entre les tables
DROP TABLE IF EXISTS authorinstitution;
DROP TABLE IF EXISTS authorpublication;

CREATE TABLE IF NOT EXISTS institution (
    id_institution int(11) NOT NULL AUTO_INCREMENT,
    idAlex_institution varchar(100),
    display_name varchar(100),
    country_code varchar(100),
    type_institution varchar(100),
    idRor_insitution varchar(100),
    PRIMARY KEY (id_institution)
);


CREATE TABLE IF NOT EXISTS publication (
    id_publication int(11) NOT NULL AUTO_INCREMENT,
    idAlex_publication varchar(100),
    idDoi_publication varchar(100),
    title varchar(500),
    display_name varchar(500),
    mag varchar(100),
    type_publication varchar(100),
    publication_year varchar(100),
    publication_date varchar(100),
    updated_date varchar(100),
    created_date varchar(100),
    PRIMARY KEY (id_publication)
);

CREATE TABLE IF NOT EXISTS conceptpublication (
    id_conceptpublication int(11) NOT NULL AUTO_INCREMENT,
    idAlex_conceptpublication varchar(100),
    wikidata varchar(100),
    display_name varchar(500),
    level_concept varchar(100),
    score varchar(100),
    PRIMARY KEY (id_conceptpublication)
);

CREATE TABLE IF NOT EXISTS conceptauthor (
    id_conceptauthor int(11) NOT NULL AUTO_INCREMENT,
    idAlex_conceptauthor varchar(100),
    wikidata varchar(100),
    display_name varchar(500),
    PRIMARY KEY (id_conceptauthor)
);

CREATE TABLE IF NOT EXISTS author (
    id_author int(11) NOT NULL AUTO_INCREMENT,
    idsAlex_author varchar(2000),
    orcid_id varchar(2000),
    display_name varchar(2000),
    display_name_alternatives varchar(2000),
    works_count varchar(500),
    cited_by_count varchar(500),
    PRIMARY KEY (id_author)
);

CREATE TABLE IF NOT EXISTS authorinstitution (
    id_authorinstitution int(11) NOT NULL AUTO_INCREMENT,
    id_author int(11) NOT NULL,
    id_institution int(11) NOT NULL,
    PRIMARY KEY (id_authorinstitution),
    FOREIGN KEY (id_author) REFERENCES author(id_author),
    FOREIGN KEY (id_institution) REFERENCES institution(id_institution)
);

CREATE TABLE IF NOT EXISTS authorpublication (
    id_authorpublication int(11) NOT NULL AUTO_INCREMENT,
    id_author int(11) NOT NULL,
    id_publication int(11) NOT NULL,
    PRIMARY KEY (id_authorpublication),
    FOREIGN KEY (id_author) REFERENCES author(id_author),
    FOREIGN KEY (id_publication) REFERENCES publication(id_publication)
);



