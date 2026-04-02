# ROLAP Analytics System

## Тема проекта
**Использование технологии ROLAP при разработке информационно-аналитических систем на базе многомерного подхода**

## Описание проекта
Данный проект представляет собой прототип информационно-аналитической системы, реализующей многомерный анализ данных с использованием технологии **ROLAP (Relational Online Analytical Processing)**.

Система демонстрирует, как реляционная база данных может использоваться для хранения аналитических данных, построения многомерной модели и выполнения OLAP-операций:
- **Slice**
- **Dice**
- **Drill-down**
- **Roll-up**

В качестве предметной области в прототипе используется **анализ медицинских данных**.

## Основной функционал
- хранение данных в реляционной базе данных;
- реализация многомерной схемы типа **«звезда»**;
- таблица фактов и таблицы измерений;
- аналитические SQL-запросы;
- фильтрация по измерениям;
- drill-down / roll-up анализ;
- визуализация результатов;
- базовый веб-интерфейс на Flask.

## Технологический стек
- Python 3.11+
- Flask
- SQLite (или PostgreSQL)
- SQLAlchemy
- Pandas
- Bootstrap 5
- Chart.js

## Структура многомерной модели

### Таблица фактов
- `fact_visits`

### Таблицы измерений
- `dim_date`
- `dim_patient`
- `dim_doctor`
- `dim_department`
- `dim_disease`
- `dim_region`

## Структура проекта

```bash
rolap-analytics-system/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── dashboard.html
│   ├── routes.py
│   ├── analytics.py
│   ├── db.py
│   └── models.py
│
├── sql/
│   ├── schema.sql
│   ├── seed.sql
│   └── queries.sql
│
├── screenshots/
│   ├── dashboard.png
│   ├── filters.png
│   ├── drilldown.png
│   └── logs.png
│
├── tests/
│   └── test_queries.py
│
├── requirements.txt
├── run.py
└── README.md/
   
