INSERT INTO dim_date VALUES
(1, '2024-01-10', 10, 1, 'January', 1, 2024),
(2, '2024-02-15', 15, 2, 'February', 1, 2024),
(3, '2024-03-20', 20, 3, 'March', 1, 2024),
(4, '2024-04-12', 12, 4, 'April', 2, 2024),
(5, '2025-01-05', 5, 1, 'January', 1, 2025),
(6, '2025-02-18', 18, 2, 'February', 1, 2025);

INSERT INTO dim_patient VALUES
(1, 'Male', 34),
(2, 'Female', 28),
(3, 'Male', 45),
(4, 'Female', 51),
(5, 'Male', 60),
(6, 'Female', 39);

INSERT INTO dim_doctor VALUES
(1, 'Dr. Ivanov', 'Cardiologist'),
(2, 'Dr. Petrova', 'Neurologist'),
(3, 'Dr. Sidorov', 'Therapist');

INSERT INTO dim_department VALUES
(1, 'Cardiology'),
(2, 'Neurology'),
(3, 'Therapy');

INSERT INTO dim_disease VALUES
(1, 'Hypertension', 'Cardiovascular'),
(2, 'Migraine', 'Neurological'),
(3, 'Flu', 'General');

INSERT INTO dim_region VALUES
(1, 'North'),
(2, 'South'),
(3, 'Central');

INSERT INTO fact_visits VALUES
(1, 1, 1, 1, 1, 1, 1, 150.0, 5),
(2, 2, 2, 2, 2, 2, 2, 200.0, 3),
(3, 3, 3, 3, 3, 3, 3, 100.0, 2),
(4, 4, 4, 1, 1, 1, 1, 170.0, 6),
(5, 5, 5, 2, 2, 2, 2, 210.0, 4),
(6, 6, 6, 3, 3, 3, 3, 120.0, 2),
(7, 1, 2, 1, 1, 1, 1, 160.0, 4),
(8, 2, 3, 2, 2, 2, 2, 220.0, 5),
(9, 3, 4, 3, 3, 3, 3, 110.0, 3),
(10, 4, 5, 1, 1, 1, 1, 180.0, 7);