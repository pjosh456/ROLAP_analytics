DROP TABLE IF EXISTS fact_visits;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_patient;
DROP TABLE IF EXISTS dim_doctor;
DROP TABLE IF EXISTS dim_department;
DROP TABLE IF EXISTS dim_disease;
DROP TABLE IF EXISTS dim_region;

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL,
    day INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    year INTEGER
);

CREATE TABLE dim_patient (
    patient_id INTEGER PRIMARY KEY,
    gender TEXT,
    age INTEGER
);

CREATE TABLE dim_doctor (
    doctor_id INTEGER PRIMARY KEY,
    doctor_name TEXT,
    specialization TEXT
);

CREATE TABLE dim_department (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT
);

CREATE TABLE dim_disease (
    disease_id INTEGER PRIMARY KEY,
    disease_name TEXT,
    disease_category TEXT
);

CREATE TABLE dim_region (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT
);

CREATE TABLE fact_visits (
    visit_id INTEGER PRIMARY KEY,
    date_id INTEGER,
    patient_id INTEGER,
    doctor_id INTEGER,
    department_id INTEGER,
    disease_id INTEGER,
    region_id INTEGER,
    cost REAL,
    treatment_days INTEGER,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (patient_id) REFERENCES dim_patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES dim_doctor(doctor_id),
    FOREIGN KEY (department_id) REFERENCES dim_department(department_id),
    FOREIGN KEY (disease_id) REFERENCES dim_disease(disease_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);