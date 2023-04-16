DROP DATABASE IF EXISTS mydb;

CREATE DATABASE mydb;

USE mydb;

CREATE TABLE companies (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    post_code VARCHAR(10) NOT NULL,
    city VARCHAR(255) NOT NULL
)ENGINE=INNODB;

CREATE TABLE people (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY ,
    lastname VARCHAR(100) NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE ON UPDATE CASCADE,
    job VARCHAR(255),
    status BOOL DEFAULT TRUE
)ENGINE=INNODB;

CREATE VIEW technicians_vw AS
    (
    SELECT *
    FROM people
    WHERE job LIKE '%Etudes'
    );

CREATE TABLE projects (
    number VARCHAR(20) NOT NULL UNIQUE PRIMARY KEY ,
    ranking VARCHAR(4) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    archive VARCHAR(10) DEFAULT NULL,
    date_archive DATE DEFAULT NULL
)ENGINE=INNODB;

CREATE VIEW archives_vw AS
    (
    SELECT *
    FROM projects
    WHERE archive IS NOT NULL
    );

CREATE VIEW current_projects_vw AS
    (
    SELECT *
    FROM projects
    WHERE archive IS NULL
    );

CREATE TABLE plans (
    number VARCHAR(10) NOT NULL,
    project_number VARCHAR(20) NOT NULL,
    version VARCHAR(4) NOT NULL,
    creation_date DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    technician_id INT NOT NULL,
    status VARCHAR(50) DEFAULT NULL,
    FOREIGN KEY (project_number) REFERENCES projects(number) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES people(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (number, name, version)
)ENGINE=INNODB;

CREATE VIEW plans_vw AS
(
    SELECT projects.name AS project,
           plans.number,
           plans.version,
           DATE_FORMAT(plans.creation_date,'%d/%m/%Y') AS date,
           plans.name,
           people.lastname AS technician
    FROM plans
    JOIN people ON plans.technician_id = people.id
    JOIN projects ON plans.project_number = projects.number
);
# Création de l'entreprise OMEXOM Nancy avec l'id = 1
INSERT INTO companies (name, address, post_code, city) VALUE ('OMEXOM Nancy', '2 Rue du Bois Jacquot', '54670', 'MILLERY');

# TEST VALUES
INSERT INTO people (lastname, firstname, company_id, job)
VALUES
    ('BARTHELEMY', 'Guillaume', 1, 'Technicien d\'Etudes'),
    ('COLLE', 'Rodolphe', 1, 'Technicien d\'Etudes'),
    ('VALENTIN', 'Franck', 1, 'Technicien d\'Etudes');

INSERT INTO projects (number, ranking, name, archive, date_archive)
VALUE
    ('P.012345.D.10', 'D25', 'Poste de MACHIN', '100', '2022-10-09');
INSERT INTO projects (number, ranking, name)
VALUE
    ('P.678910.D.11', 'D26', 'Poste de BIDULE')


