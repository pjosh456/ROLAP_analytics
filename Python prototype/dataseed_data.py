import sqlite3
import random
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import DATABASE_PATH

# =====================================================
# Configuration
# =====================================================

NUM_PATIENTS = 200
NUM_DOCTORS = 30
NUM_DEPARTMENTS = 8
NUM_DIAGNOSES = 25
NUM_FACTS = 1000

YEARS = [2022, 2023, 2024, 2025]

# =====================================================
# Helper Functions
# =====================================================

def random_date(start_year=2022, end_year=2025):
    """Generate random date within range."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def get_season(date):
    """Determine season from date."""
    month = date.month
    if month in [12, 1, 2]:
        return 'Зима'
    elif month in [3, 4, 5]:
        return 'Весна'
    elif month in [6, 7, 8]:
        return 'Лето'
    else:
        return 'Осень'

def get_age_group(age):
    """Determine age group from age."""
    if age < 18:
        return '0-17'
    elif age < 65:
        return '18-64'
    else:
        return '65+'

# =====================================================
# Generate Dimension Tables
# =====================================================

def generate_dim_time():
    """Generate time dimension table."""
    records = []
    for year in YEARS:
        for month in range(1, 13):
            for day in range(1, 29):  # Simplified: max 28 days per month
                try:
                    date = datetime(year, month, day)
                except ValueError:
                    continue
                
                records.append({
                    'time_id': len(records) + 1,
                    'date': date.strftime('%Y-%m-%d'),
                    'year': year,
                    'quarter': (month - 1) // 3 + 1,
                    'month': month,
                    'month_name': date.strftime('%B'),
                    'day_of_week': date.weekday() + 1,
                    'day_name': date.strftime('%A'),
                    'is_weekend': 1 if date.weekday() >= 5 else 0,
                    'season': get_season(date)
                })
    
    return pd.DataFrame(records)

def generate_dim_department():
    """Generate department dimension table."""
    departments = [
        {'name': 'Кардиология', 'profile': 'терапевтическое', 'beds': 60, 'building': 'Главный'},
        {'name': 'Хирургия', 'profile': 'хирургическое', 'beds': 80, 'building': 'Главный'},
        {'name': 'Терапия', 'profile': 'терапевтическое', 'beds': 100, 'building': 'Корпус А'},
        {'name': 'Неврология', 'profile': 'терапевтическое', 'beds': 50, 'building': 'Корпус Б'},
        {'name': 'Реанимация', 'profile': 'реанимационное', 'beds': 20, 'building': 'Главный'},
        {'name': 'Травматология', 'profile': 'хирургическое', 'beds': 40, 'building': 'Корпус А'},
        {'name': 'Онкология', 'profile': 'терапевтическое', 'beds': 45, 'building': 'Корпус Б'},
        {'name': 'Педиатрия', 'profile': 'педиатрическое', 'beds': 55, 'building': 'Корпус В'},
    ]
    
    records = []
    for i, dept in enumerate(departments, 1):
        records.append({
            'department_id': i,
            'dept_name': dept['name'],
            'dept_profile': dept['profile'],
            'bed_capacity': dept['beds'],
            'building': dept['building'],
            'is_active': 1
        })
    
    return pd.DataFrame(records)

def generate_dim_doctor():
    """Generate doctor dimension table."""
    specialties = ['Кардиолог', 'Хирург', 'Терапевт', 'Невролог', 'Анестезиолог', 'Травматолог', 'Онколог', 'Педиатр']
    categories = ['Вторая', 'Первая', 'Высшая']
    degrees = ['Нет', 'Кандидат наук', 'Доктор наук']
    
    records = []
    for i in range(1, NUM_DOCTORS + 1):
        records.append({
            'doctor_id': i,
            'full_name': f'Врач_{i}',
            'specialty': random.choice(specialties),
            'experience_years': random.randint(1, 35),
            'qualification_category': random.choice(categories),
            'academic_degree': random.choice(degrees)
        })
    
    return pd.DataFrame(records)

def generate_dim_diagnosis():
    """Generate diagnosis dimension table."""
    diagnoses = [
        ('I20', 'Стенокардия', 'Болезни системы кровообращения', 0),
        ('I21', 'Инфаркт миокарда', 'Болезни системы кровообращения', 0),
        ('J15', 'Пневмония', 'Болезни органов дыхания', 0),
        ('E11', 'Сахарный диабет', 'Эндокринные заболевания', 1),
        ('K80', 'Желчнокаменная болезнь', 'Болезни органов пищеварения', 0),
        ('M17', 'Гонартроз', 'Болезни костно-мышечной системы', 1),
        ('C50', 'Рак молочной железы', 'Новообразования', 0),
        ('G40', 'Эпилепсия', 'Болезни нервной системы', 1),
        ('N20', 'Мочекаменная болезнь', 'Болезни мочеполовой системы', 0),
        ('I10', 'Гипертоническая болезнь', 'Болезни системы кровообращения', 1),
        ('J44', 'ХОБЛ', 'Болезни органов дыхания', 1),
        ('K25', 'Язва желудка', 'Болезни органов пищеварения', 0),
        ('S06', 'ЧМТ', 'Травмы', 0),
        ('S72', 'Перелом шейки бедра', 'Травмы', 0),
        ('B20', 'ВИЧ-инфекция', 'Инфекционные болезни', 1),
        ('A09', 'Кишечная инфекция', 'Инфекционные болезни', 0),
        ('E10', 'Сахарный диабет 1 типа', 'Эндокринные заболевания', 1),
        ('I63', 'Ишемический инсульт', 'Болезни системы кровообращения', 0),
        ('J45', 'Бронхиальная астма', 'Болезни органов дыхания', 1),
        ('K40', 'Паховая грыжа', 'Болезни органов пищеварения', 0),
        ('L40', 'Псориаз', 'Болезни кожи', 1),
        ('M05', 'Ревматоидный артрит', 'Болезни костно-мышечной системы', 1),
        ('N18', 'ХПН', 'Болезни мочеполовой системы', 1),
        ('R10', 'Боль в животе', 'Симптомы', 0),
        ('Z00', 'Профилактический осмотр', 'Факторы здоровья', 0),
    ]
    
    records = []
    for i, (code, name, disease_class, is_chronic) in enumerate(diagnoses[:NUM_DIAGNOSES], 1):
        records.append({
            'diagnosis_id': i,
            'icd10_code': code,
            'icd10_name': name,
            'disease_class': disease_class,
            'is_chronic': is_chronic
        })
    
    return pd.DataFrame(records)

def generate_dim_patient():
    """Generate patient dimension table."""
    age_groups = ['0-17', '18-64', '65+']
    genders = ['Мужской', 'Женский']
    residence_types = ['Город', 'Село']
    social_statuses = ['Работающий', 'Пенсионер', 'Инвалид', 'Студент', 'Безработный']
    benefit_categories = ['Нет', 'Ветеран труда', 'Инвалид', 'Чернобылец']
    
    records = []
    for i in range(1, NUM_PATIENTS + 1):
        age = random.randint(0, 90)
        records.append({
            'patient_id': i,
            'age_group': get_age_group(age),
            'gender': random.choice(genders),
            'residence_type': random.choice(residence_types),
            'social_status': random.choice(social_statuses),
            'benefit_category': random.choice(benefit_categories)
        })
    
    return pd.DataFrame(records)

# =====================================================
# Generate Fact Table
# =====================================================

def generate_fact_hospitalization(dim_time, dim_department, dim_doctor, dim_diagnosis, dim_patient):
    """Generate fact table for hospitalizations."""
    records = []
    
    # Get lists of IDs
    time_ids = dim_time['time_id'].tolist()
    dept_ids = dim_department['department_id'].tolist()
    doctor_ids = dim_doctor['doctor_id'].tolist()
    diagnosis_ids = dim_diagnosis['diagnosis_id'].tolist()
    patient_ids = dim_patient['patient_id'].tolist()
    
    for i in range(1, NUM_FACTS + 1):
        # Randomly select dimensions
        time_id = random.choice(time_ids)
        dept_id = random.choice(dept_ids)
        doctor_id = random.choice(doctor_ids)
        diagnosis_id = random.choice(diagnosis_ids)
        patient_id = random.choice(patient_ids)
        
        # Generate measures with realistic distributions
        days_spent = random.choices(
            [3, 5, 7, 10, 14, 21],
            weights=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03]
        )[0]
        
        # Cost based on department and days
        dept_data = dim_department[dim_department['department_id'] == dept_id].iloc[0]
        if dept_data['dept_profile'] == 'реанимационное':
            cost_per_day = random.uniform(8000, 15000)
        elif dept_data['dept_profile'] == 'хирургическое':
            cost_per_day = random.uniform(5000, 10000)
        else:
            cost_per_day = random.uniform(3000, 7000)
        
        total_cost = round(days_spent * cost_per_day, 2)
        drug_cost = round(total_cost * random.uniform(0.2, 0.5), 2)
        
        # Flags
        surgery_flag = 1 if dept_data['dept_profile'] == 'хирургическое' and random.random() < 0.6 else 0
        
        # Lethality depends on department and diagnosis
        lethality_rate = 0.01  # base rate
        if dept_data['dept_profile'] == 'реанимационное':
            lethality_rate = 0.15
        elif dept_data['dept_profile'] == 'хирургическое':
            lethality_rate = 0.03
        
        # Higher lethality for older patients
        patient_data = dim_patient[dim_patient['patient_id'] == patient_id].iloc[0]
        if patient_data['age_group'] == '65+':
            lethality_rate *= 1.5
        
        lethality_flag = 1 if random.random() < lethality_rate else 0
        
        # Readmission flag
        readmission_rate = 0.08 if patient_data['age_group'] == '65+' else 0.05
        readmission_30d_flag = 1 if random.random() < readmission_rate else 0
        
        records.append({
            'fact_id': i,
            'time_id': time_id,
            'department_id': dept_id,
            'doctor_id': doctor_id,
            'diagnosis_id': diagnosis_id,
            'patient_id': patient_id,
            'days_spent': days_spent,
            'total_cost': total_cost,
            'drug_cost': drug_cost,
            'surgery_flag': surgery_flag,
            'lethality_flag': lethality_flag,
            'readmission_30d_flag': readmission_30d_flag
        })
    
    return pd.DataFrame(records)

# =====================================================
# Main Execution
# =====================================================

def main():
    """Generate all data and save to database."""
    print("=" * 60)
    print("ROLAP Analytics Demo - Data Generation")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Execute schema
    schema_path = Path(__file__).parent / 'schema.sql'
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    print("\n[1/6] Creating tables...")
    cursor.executescript(schema_sql)
    
    print("[2/6] Generating time dimension...")
    dim_time = generate_dim_time()
    dim_time.to_sql('dim_time', conn, if_exists='replace', index=False)
    print(f"      Generated {len(dim_time)} records")
    
    print("[3/6] Generating department dimension...")
    dim_department = generate_dim_department()
    dim_department.to_sql('dim_department', conn, if_exists='replace', index=False)
    print(f"      Generated {len(dim_department)} records")
    
    print("[4/6] Generating doctor dimension...")
    dim_doctor = generate_dim_doctor()
    dim_doctor.to_sql('dim_doctor', conn, if_exists='replace', index=False)
    print(f"      Generated {len(dim_doctor)} records")
    
    print("[5/6] Generating diagnosis dimension...")
    dim_diagnosis = generate_dim_diagnosis()
    dim_diagnosis.to_sql('dim_diagnosis', conn, if_exists='replace', index=False)
    print(f"      Generated {len(dim_diagnosis)} records")
    
    print("[6/6] Generating patient dimension...")
    dim_patient = generate_dim_patient()
    dim_patient.to_sql('dim_patient', conn, if_exists='replace', index=False)
    print(f"      Generated {len(dim_patient)} records")
    
    print("[7/6] Generating fact table (hospitalizations)...")
    fact_hospitalization = generate_fact_hospitalization(
        dim_time, dim_department, dim_doctor, dim_diagnosis, dim_patient
    )
    fact_hospitalization.to_sql('fact_hospitalization', conn, if_exists='replace', index=False)
    print(f"      Generated {len(fact_hospitalization)} records")
    
    # Create indexes
    print("\n[8/6] Creating indexes...")
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_fact_time ON fact_hospitalization(time_id)",
        "CREATE INDEX IF NOT EXISTS idx_fact_department ON fact_hospitalization(department_id)",
        "CREATE INDEX IF NOT EXISTS idx_fact_doctor ON fact_hospitalization(doctor_id)",
        "CREATE INDEX IF NOT EXISTS idx_fact_diagnosis ON fact_hospitalization(diagnosis_id)",
        "CREATE INDEX IF NOT EXISTS idx_fact_patient ON fact_hospitalization(patient_id)",
        "CREATE INDEX IF NOT EXISTS idx_dim_time_year ON dim_time(year)",
        "CREATE INDEX IF NOT EXISTS idx_dim_department_profile ON dim_department(dept_profile)",
        "CREATE INDEX IF NOT EXISTS idx_dim_patient_age ON dim_patient(age_group)",
    ]
    for idx in indexes:
        cursor.execute(idx)
    
    conn.commit()
    
    print("\n" + "=" * 60)
    print("Data generation completed successfully!")
    print(f"Database saved to: {DATABASE_PATH}")
    print("=" * 60)
    
    # Print summary
    print("\nSummary:")
    print(f"  - dim_time: {len(dim_time)} records")
    print(f"  - dim_department: {len(dim_department)} records")
    print(f"  - dim_doctor: {len(dim_doctor)} records")
    print(f"  - dim_diagnosis: {len(dim_diagnosis)} records")
    print(f"  - dim_patient: {len(dim_patient)} records")
    print(f"  - fact_hospitalization: {len(fact_hospitalization)} records")
    
    conn.close()

if __name__ == "__main__":
    main()