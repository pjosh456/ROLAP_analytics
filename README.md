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

rolap-analytics-demo/
│
├── README.md                              # Основная документация проекта
├── requirements.txt                       # Список зависимостей Python
├── docker-compose.yml                     # Docker-конфигурация для контейнеризации
├── .gitignore                             # Игнорируемые файлы Git
├── .env.example                           # Пример файла с переменными окружения
│
├── config/
│   ├── __init__.py
│   └── settings.py                        # Настройки приложения (БД, кэш, логи)
│
├── data/
│   ├── __init__.py
│   ├── schema.sql                         # SQL-скрипт создания схемы «звезда»
│   ├── seed_data.py                       # Скрипт генерации тестовых данных
│   ├── rolap_demo.db                      # SQLite база данных (создаётся при запуске)
│   │
│   └── exports/                           # Директория для экспортированных CSV
│       ├── export_20260402_103000.csv
│       └── ...
│
├── src/
│   ├── __init__.py
│   ├── storage.py                         # Класс ROLAPStorage
│   ├── query_builder.py                   # Класс ROLAPQueryBuilder
│   ├── olap_operations.py                 # Класс OLAPOperations
│   └── app.py                             # Dash-веб-приложение
│
├── notebooks/
│   └── analysis.ipynb                     # Jupyter Notebook с исследовательским анализом
│
├── tests/
│   ├── __init__.py
│   ├── test_queries.py                    # Модульные тесты SQL-запросов
│   │
│   └── results/                           # Результаты тестирования
│       ├── test_log.txt                   # Лог выполнения тестов
│       └── benchmark_log.txt              # Лог производительности
│
├── docs/
│   ├── star_schema.png                    # Диаграмма схемы «звезда»
│   ├── query_examples.sql                 # Примеры OLAP-запросов с комментариями
│   ├── torchinfo_summary.txt              # Сводка архитектуры модели данных
│   ├── performance_metrics.md             # Метрики производительности
│   └── architecture.md                    # Документация архитектуры
│
├── screenshots/
│   ├── dashboard_main.png                 # Скриншот главной панели
│   ├── department_analysis.png            # Скриншот анализа по отделениям
│   ├── drill_through.png                  # Скриншот детализации
│   └── query_results.png                  # Скриншот результатов запроса
│
├── logs/
│   ├── app.log                            # Лог веб-приложения
│   └── query.log                          # Лог выполненных SQL-запросов
│
└── .github/
    └── workflows/
        └── ci.yml                         # CI/CD конфигурация GitHub Actions
