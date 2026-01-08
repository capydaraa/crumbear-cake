# =====================================================
# Database Connection Module for Crumbear Cake Management System
# SQL Server connection using pyodbc
# =====================================================

import pyodbc
import os
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal

# Database configuration
DB_CONFIG = {
    'server': os.environ.get('DB_SERVER', 'localhost,1433'),
    'database': os.environ.get('DB_NAME', 'CrumbearDB'),
    'username': os.environ.get('DB_USER', 'sa'),
    'password': os.environ.get('DB_PASSWORD', 'Crumbear2025!'),
    'driver': os.environ.get('DB_DRIVER', '{ODBC Driver 18 for SQL Server}')
}

# Track database availability
_db_available = None

def get_connection_string():
    """Build connection string for SQL Server"""
    return (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes;"
        f"Connection Timeout=5;"
    )

def check_db_connection():
    """Check if database connection is available"""
    global _db_available
    try:
        conn = pyodbc.connect(get_connection_string())
        conn.close()
        _db_available = True
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        _db_available = False
        print(f"⚠️ Database not available: {e}")
        return False

def is_db_available():
    """Return cached database availability status"""
    global _db_available
    if _db_available is None:
        check_db_connection()
    return _db_available

def serialize_row(row_dict):
    """Convert row values to JSON-serializable types"""
    result = {}
    for key, value in row_dict.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = float(value)
        else:
            result[key] = value
    return result

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = pyodbc.connect(get_connection_string())
        yield conn
    except pyodbc.Error as e:
        if conn:
            conn.rollback()
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None, fetch=True):
    """
    Execute a SQL query and return results
    
    Args:
        query: SQL query string
        params: Tuple of parameters for parameterized query
        fetch: If True, fetch and return results; if False, commit changes
    
    Returns:
        List of dictionaries representing rows (if fetch=True)
        Row count (if fetch=False)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                if cursor.description:
                    columns = [column[0] for column in cursor.description]
                    results = []
                    for row in cursor.fetchall():
                        row_dict = dict(zip(columns, row))
                        results.append(serialize_row(row_dict))
                    return results
                return []
            else:
                conn.commit()
                return cursor.rowcount
    except pyodbc.Error as e:
        print(f"Query execution error: {e}")
        print(f"Query: {query[:200]}...")
        raise

def execute_insert(query, params=None):
    """
    Execute an INSERT query and return the new ID
    
    Args:
        query: SQL INSERT query string
        params: Tuple of parameters for parameterized query
    
    Returns:
        The ID of the newly inserted row
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Get the last inserted ID (SQL Server SCOPE_IDENTITY)
            cursor.execute("SELECT SCOPE_IDENTITY() AS id")
            result = cursor.fetchone()
            new_id = int(result[0]) if result and result[0] else None
            
            conn.commit()
            return new_id
    except pyodbc.Error as e:
        print(f"Insert execution error: {e}")
        print(f"Query: {query[:200]}...")
        raise

def execute_many(query, params_list):
    """
    Execute multiple INSERT/UPDATE queries efficiently
    
    Args:
        query: SQL query string with placeholders
        params_list: List of parameter tuples
    
    Returns:
        Total number of affected rows
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
    except pyodbc.Error as e:
        print(f"Execute many error: {e}")
        raise

def execute_stored_procedure(proc_name, params=None):
    """
    Execute a stored procedure
    
    Args:
        proc_name: Name of the stored procedure
        params: Dictionary of parameter names and values
    
    Returns:
        List of dictionaries representing result rows
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                # Build parameter string
                param_str = ', '.join([f"@{k} = ?" for k in params.keys()])
                query = f"EXEC {proc_name} {param_str}"
                cursor.execute(query, list(params.values()))
            else:
                cursor.execute(f"EXEC {proc_name}")
            
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    results.append(serialize_row(row_dict))
                return results
            return []
    except pyodbc.Error as e:
        print(f"Stored procedure error: {e}")
        raise

def test_connection():
    """Test database connection and print status"""
    print("\n" + "=" * 50)
    print("Testing Database Connection")
    print("=" * 50)
    print(f"Server: {DB_CONFIG['server']}")
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Driver: {DB_CONFIG['driver']}")
    print("-" * 50)
    
    if check_db_connection():
        # Test a simple query
        try:
            result = execute_query("SELECT @@VERSION AS version")
            print(f"SQL Server Version:\n{result[0]['version'][:80]}...")
            
            # Check if tables exist
            tables = execute_query("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)
            if tables:
                print(f"\nTables found: {[t['TABLE_NAME'] for t in tables]}")
            else:
                print("\n⚠️ No tables found - run schema.sql to initialize")
        except Exception as e:
            print(f"Test query failed: {e}")
    
    print("=" * 50 + "\n")

# Initialize connection check on module load
if __name__ == "__main__":
    test_connection()
