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
rolap-analytics-demo/
│
├── README.md                              # 📖 Основная документация проекта
├── requirements.txt                       # 📦 Список зависимостей Python
├── docker-compose.yml                     # 🐳 Docker-конфигурация
├── .gitignore                             # 🚫 Игнорируемые файлы Git
├── .env.example                           # 🔧 Пример переменных окружения
│
├── config/                                # ⚙️ Конфигурация
│   ├── __init__.py
│   └── settings.py                        # Настройки БД, кэша, логирования
│
├── data/                                  # 💾 Данные
│   ├── __init__.py
│   ├── schema.sql                         # 🗄️ SQL-схема (star schema)
│   ├── seed_data.py                       # 🌱 Генерация тестовых данных
│   ├── rolap_demo.db                      # 🗃️ SQLite БД (создаётся)
│   └── exports/                           # 📤 Экспортированные CSV
│
├── src/                                   # 🐍 Исходный код
│   ├── __init__.py
│   ├── storage.py                         # 💿 ROLAPStorage (БД + кэш)
│   ├── query_builder.py                   # 🔨 ROLAPQueryBuilder (SQL)
│   ├── olap_operations.py                 # 🔄 OLAPOperations (slice, dice, drill)
│   └── app.py                             # 🌐 Dash-веб-приложение
│
├── notebooks/                             # 📓 Jupyter ноутбуки
│   └── analysis.ipynb                     # Исследовательский анализ
│
├── tests/                                 # 🧪 Тестирование
│   ├── __init__.py
│   ├── test_queries.py                    # Модульные тесты SQL
│   └── results/                           # 📊 Результаты тестов
│       ├── test_log.txt
│       └── benchmark_log.txt
│
├── docs/                                  # 📚 Документация
│   ├── star_schema.png                    # 📐 Диаграмма схемы "звезда"
│   ├── query_examples.sql                 # 📝 Примеры OLAP-запросов
│   ├── torchinfo_summary.txt              # 📋 Сводка архитектуры
│   ├── performance_metrics.md             # 📈 Метрики производительности
│   └── architecture.md                    # 🏗️ Архитектура системы
│
├── screenshots/                           # 📸 Скриншоты
│   ├── dashboard_main.png
│   ├── department_analysis.png
│   ├── drill_through.png
│   └── query_results.png
│
├── logs/                                  # 📝 Логи
│   ├── app.log
│   └── query.log
│
└── .github/                               # 🤖 CI/CD
    └── workflows/
        └── ci.yml                         # GitHub Actions
