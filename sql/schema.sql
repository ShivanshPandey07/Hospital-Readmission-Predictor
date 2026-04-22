DROP TABLE IF EXISTS readmission_labels CASCADE;
DROP TABLE IF EXISTS encounters CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

CREATE TABLE patients (
    patient_nbr  BIGINT PRIMARY KEY,
    race         VARCHAR(20),
    gender       VARCHAR(10),
    age          VARCHAR(10)
);

CREATE TABLE encounters (
    encounter_id               BIGINT PRIMARY KEY,
    patient_nbr                BIGINT REFERENCES patients(patient_nbr),
    admission_type_id          INT,
    discharge_disposition_id   INT,
    admission_source_id        INT,
    time_in_hospital           INT,
    num_lab_procedures         INT,
    num_procedures             INT,
    num_medications            INT,
    number_outpatient          INT,
    number_emergency           INT,
    number_inpatient           INT,
    number_diagnoses           INT,
    diag_1                     VARCHAR(10),
    diag_2                     VARCHAR(10),
    diag_3                     VARCHAR(10),
    a1c_result                 VARCHAR(10),
    insulin                    VARCHAR(10),
    change_in_meds             VARCHAR(5),
    diabetes_med               VARCHAR(5)
);

CREATE TABLE readmission_labels (
    encounter_id   BIGINT PRIMARY KEY
                   REFERENCES encounters(encounter_id),
    readmitted_raw VARCHAR(5),
    readmitted_30d SMALLINT
);

CREATE INDEX idx_enc_patient ON encounters(patient_nbr);
CREATE INDEX idx_readmit     ON readmission_labels(readmitted_30d);