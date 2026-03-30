"""
ROLAP Storage Layer - Manages database connections and query execution.
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path
import sys
from functools import lru_cache

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import DATABASE_PATH, CACHE_ENABLED, CACHE_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ROLAPStorage:
    """
    Class for managing ROLAP data storage.
    Handles database connections, query execution, and caching.
    """
    
    def __init__(self, db_path=None):
        """
        Initialize ROLAPStorage.
        
        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path or DATABASE_PATH
        self.connection = None
        self._cache = {}
        self._cache_enabled = CACHE_ENABLED
        self._cache_size = CACHE_SIZE
    
    def connect(self):
        """
        Establish connection to the database.
        
        Returns:
            sqlite3.Connection: Database connection.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connected to database: {self.db_path}")
        return self.connection
    
    def close(self):
        """
        Close database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def execute_query(self, query, params=None):
        """
        Execute SQL query and return results as DataFrame.
        
        Args:
            query: SQL query string.
            params: Optional query parameters.
            
        Returns:
            pd.DataFrame: Query results.
        """
        # Check cache first
        cache_key = hash((query, str(params)))
        if self._cache_enabled and cache_key in self._cache:
            logger.debug(f"Cache hit for query: {query[:50]}...")
            return self._cache[cache_key].copy()
        
        # Execute query
        conn = self.connect()
        try:
            logger.debug(f"Executing query: {query[:100]}...")
            result = pd.read_sql_query(query, conn, params=params)
            
            # Update cache
            if self._cache_enabled:
                self._cache[cache_key] = result.copy()
                # Simple cache size management
                if len(self._cache) > self._cache_size:
                    # Remove oldest item (approximate)
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
            
            return result
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def get_table_info(self, table_name):
        """
        Get information about a table.
        
        Args:
            table_name: Name of the table.
            
        Returns:
            dict: Table information.
        """
        query = f"PRAGMA table_info({table_name})"
        result = self.execute_query(query)
        return result.to_dict('records')
    
    def get_dimensions(self):
        """
        Get available dimension tables and their attributes.
        
        Returns:
            dict: Dimension definitions.
        """
        dimensions = {
            'time': {
                'table': 'dim_time',
                'pk': 'time_id',
                'attributes': ['year', 'quarter', 'month', 'day_of_week', 'is_weekend', 'season'],
                'display_name': 'Время',
                'hierarchy': ['year', 'quarter', 'month', 'day_of_week']
            },
            'department': {
                'table': 'dim_department',
                'pk': 'department_id',
                'attributes': ['dept_name', 'dept_profile', 'building'],
                'display_name': 'Отделение',
                'hierarchy': ['dept_profile', 'dept_name']
            },
            'doctor': {
                'table': 'dim_doctor',
                'pk': 'doctor_id',
                'attributes': ['specialty', 'experience_years', 'qualification_category'],
                'display_name': 'Врач',
                'hierarchy': ['specialty', 'qualification_category']
            },
            'diagnosis': {
                'table': 'dim_diagnosis',
                'pk': 'diagnosis_id',
                'attributes': ['disease_class', 'icd10_name'],
                'display_name': 'Диагноз',
                'hierarchy': ['disease_class', 'icd10_name']
            },
            'patient': {
                'table': 'dim_patient',
                'pk': 'patient_id',
                'attributes': ['age_group', 'gender', 'residence_type'],
                'display_name': 'Пациент',
                'hierarchy': ['age_group', 'gender']
            }
        }
        return dimensions
    
    def get_measures(self):
        """
        Get available measures (metrics) from fact table.
        
        Returns:
            list: Measure definitions.
        """
        measures = [
            {'column': 'days_spent', 'alias': 'Койко-дни', 'agg_func': 'SUM', 'display_name': 'Койко-дни (сумма)'},
            {'column': 'days_spent', 'alias': 'avg_days', 'agg_func': 'AVG', 'display_name': 'Ср. длительность лечения'},
            {'column': 'total_cost', 'alias': 'total_cost', 'agg_func': 'SUM', 'display_name': 'Общая стоимость (сумма)'},
            {'column': 'total_cost', 'alias': 'avg_cost', 'agg_func': 'AVG', 'display_name': 'Ср. стоимость лечения'},
            {'column': 'drug_cost', 'alias': 'drug_cost', 'agg_func': 'SUM', 'display_name': 'Затраты на лекарства'},
            {'column': 'surgery_flag', 'alias': 'surgery_rate', 'agg_func': 'AVG', 'display_name': 'Доля операций', 'format': 'percent'},
            {'column': 'lethality_flag', 'alias': 'lethality_rate', 'agg_func': 'AVG', 'display_name': 'Летальность', 'format': 'percent'},
            {'column': 'readmission_30d_flag', 'alias': 'readmission_rate', 'agg_func': 'AVG', 'display_name': 'Повторные госпитализации', 'format': 'percent'},
            {'column': 'fact_id', 'alias': 'case_count', 'agg_func': 'COUNT', 'display_name': 'Количество случаев'}
        ]
        return measures
    
    def get_filter_options(self, dimension, attribute):
        """
        Get unique values for a dimension attribute for filtering.
        
        Args:
            dimension: Dimension name.
            attribute: Attribute name.
            
        Returns:
            list: Unique values.
        """
        dimensions = self.get_dimensions()
        if dimension not in dimensions:
            return []
        
        table = dimensions[dim