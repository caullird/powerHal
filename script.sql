DROP TABLE IF EXISTS institution;
DROP TABLE IF EXISTS publication;

CREATE TABLE IF NOT EXISTS institution (
    id_institution int(11) NOT NULL AUTO_INCREMENT,
    idAlex_institution varchar(100) NOT NULL,
    display_name varchar(100) NOT NULL,
    country_code varchar(100) NOT NULL,
    type_institution varchar(100) NOT NULL,
    idRor_insitution varchar(100) NOT NULL,
    PRIMARY KEY (id_institution)
);


CREATE TABLE IF NOT EXISTS publication (
    id_publication int(11) NOT NULL AUTO_INCREMENT,
    idAlex_publication varchar(100) NOT NULL,
    idDoi_publication varchar(100) NOT NULL,
    title varchar(500) NOT NULL,
    display_name varchar(500) NOT NULL,
    map varchar(100) NOT NULL,
    type_publication varchar(100) NOT NULL,
    publication_year varchar(100) NOT NULL,
    publication_date varchar(100) NOT NULL,
    updated_date varchar(100) NOT NULL,
    create_date varchar(100) NOT NULL,
    PRIMARY KEY (id_publication)
)

