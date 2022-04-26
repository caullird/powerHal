DROP TABLE IF EXISTS institution;
DROP TABLE IF EXISTS publication;

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
)

