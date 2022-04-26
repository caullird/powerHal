DROP TABLE IF EXISTS institution;

CREATE TABLE IF NOT EXISTS institution (
    id_institution int(11) NOT NULL AUTO_INCREMENT,
    idAlex_institution varchar(100) NOT NULL,
    display_name varchar(100) NOT NULL,
    country_code varchar(100) NOT NULL,
    type_institution varchar(100) NOT NULL,
    idRor_insitution varchar(100) NOT NULL,
    PRIMARY KEY (id_institution)
);


