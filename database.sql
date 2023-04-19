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
    project_number VARCHAR(20) NOT NULL,
    plan_number VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    id INT AUTO_INCREMENT NOT NULL UNIQUE,
    FOREIGN KEY (project_number) REFERENCES projects(number) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (project_number, plan_number)
)ENGINE=INNODB;

CREATE TABLE versions (
    version VARCHAR(5) NOT NULL,
    plan_id INT NOT NULL,
    creation_date DATE NOT NULL,
    modification VARCHAR(150) NOT NULL,
    technician_id INT NOT NULL,
    status VARCHAR(10),
    id INT AUTO_INCREMENT NOT NULL UNIQUE,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES people(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (version, plan_id)
)ENGINE=INNODB;

CREATE TABLE dispatch_notes (
    dispatch_id INT NOT NULL AUTO_INCREMENT,
    dispatch_number VARCHAR(20) NOT NULL,
    project_number VARCHAR(20) NOT NULL,
    sender INT NOT NULL,
    recipient INT NOT NULL,
    sending_date DATE NOT NULL,
    sending_status VARCHAR(10) NOT NULL,
    FOREIGN KEY (project_number) REFERENCES projects(number) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (sender) REFERENCES people(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (recipient) REFERENCES people(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (dispatch_id)
)ENGINE=INNODB;

CREATE TABLE versions_dispatch_notes (
    version_id INT NOT NULL,
    dispatch_note_id INT NOT NULL,
    FOREIGN KEY (version_id) REFERENCES versions(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dispatch_note_id) REFERENCES  dispatch_notes(dispatch_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (version_id, dispatch_note_id)
)ENGINE=INNODB;

CREATE VIEW versions_dispatch_notes_vw AS
    (
    SELECT *
    FROM versions
    JOIN versions_dispatch_notes ON versions.id = versions_dispatch_notes.version_id
    JOIN dispatch_notes ON dispatch_notes.dispatch_id = versions_dispatch_notes.dispatch_note_id
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
VALUES
    ('P.678910.D.11', 'D26', 'Poste de BIDULE'),
    ('P.678910.D.12', 'D27', 'Poste de LABAS'),
    ('P.678910.D.13', 'D28', 'Poste de TRUC');

INSERT INTO plans (project_number, plan_number, title)
VALUES
    ('P.678910.D.12', 100, 'Vue en plan Génie Civil'),
    ('P.678910.D.12', 300, 'Vue en plan Electrique'),
    ('P.678910.D.12', 1500, 'Tranche Automatismes');

INSERT INTO versions (version, plan_id, creation_date, modification, technician_id)
VALUES
    ('A1', 1, '2023-04-01', 'Création du document', 1),
    ('A1', 2, '2023-04-01', 'Création du document', 1),
    ('A1', 3, '2023-04-01', 'Création du document', 1),
    ('A2', 1, '2023-04-02', 'Màj suite avancement', 1);

INSERT INTO dispatch_notes (dispatch_number, project_number, sender, recipient, sending_date, sending_status)
VALUE
    ('0001-BE/OMX_NCY', 'P.678910.D.12', 1, 3, '2023-04-02', 'BPE');