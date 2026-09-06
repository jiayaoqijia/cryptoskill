#!/usr/bin/env python3
import json
import argparse
import sqlite3
import sys
from typing import Dict, Any, List, Optional

# Try importing database drivers
try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False


def format_success(data: Dict[str, Any]) -> str:
    """Format successful result as JSON."""
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    """Format error as JSON."""
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def execute_sql_query(db_type: str, connection: Dict[str, Any], query: str, params: List[Any] = None) -> Dict[str, Any]:
    """Execute SQL query with parameter binding across multiple database types.
    
    Args:
        db_type: Database type (sqlite, postgresql, mysql)
        connection: Connection parameters dict containing host, port, user, password, database
        query: SQL query with ? or %s placeholders
        params: Query parameters
        
    Returns:
        Query results as dictionary
    """
    if params is None:
        params = []
    
    if db_type == "sqlite":
        # SQLite - connection is a path string or :memory:
        db_path = connection if isinstance(connection, str) else connection.get("database", ":memory:")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            
            # Check if query returns results
            if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
                rows = cursor.fetchall()
                result = {
                    "rows": [dict(row) for row in rows],
                    "row_count": len(rows)
                }
            else:
                conn.commit()
                result = {
                    "rows": [],
                    "row_count": cursor.rowcount,
                    "affected_rows": cursor.rowcount
                }
            
            return result
        finally:
            cursor.close()
            conn.close()
    
    elif db_type == "postgresql":
        if not HAS_PSYCOPG2:
            return {"success": False, "error": "psycopg2 not installed. Run: pip install psycopg2-binary"}
        
        try:
            # Parse connection dict
            host = connection.get("host", "localhost")
            port = connection.get("port", 5432)
            user = connection.get("user", "postgres")
            password = connection.get("password", "")
            database = connection.get("database", "postgres")
            
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            try:
                # Convert ? placeholders to %s for PostgreSQL
                pg_query = query.replace("?", "%s")
                cursor.execute(pg_query, params)
                
                # Check if query returns results
                if query.strip().upper().startswith(('SELECT', 'SHOW')):
                    rows = cursor.fetchall()
                    result = {
                        "rows": [dict(row) for row in rows],
                        "row_count": len(rows)
                    }
                else:
                    conn.commit()
                    result = {
                        "rows": [],
                        "row_count": cursor.rowcount,
                        "affected_rows": cursor.rowcount
                    }
                
                return result
            finally:
                cursor.close()
                conn.close()
        
        except psycopg2.OperationalError as e:
            return {"success": False, "error": "connection_error", "message": str(e)}
        except psycopg2.Error as e:
            return {"success": False, "error": "query_error", "message": str(e)}
    
    elif db_type == "mysql":
        if not HAS_MYSQL:
            return {"success": False, "error": "mysql-connector-python not installed. Run: pip install mysql-connector-python"}
        
        try:
            # Parse connection dict
            host = connection.get("host", "localhost")
            port = connection.get("port", 3306)
            user = connection.get("user", "root")
            password = connection.get("password", "")
            database = connection.get("database", "mysql")
            
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor(dictionary=True)
            
            try:
                # Convert ? placeholders to %s for MySQL
                mysql_query = query.replace("?", "%s")
                cursor.execute(mysql_query, params)
                
                # Check if query returns results
                if query.strip().upper().startswith(('SELECT', 'SHOW')):
                    rows = cursor.fetchall()
                    result = {
                        "rows": rows,
                        "row_count": len(rows)
                    }
                else:
                    conn.commit()
                    result = {
                        "rows": [],
                        "row_count": cursor.rowcount,
                        "affected_rows": cursor.rowcount
                    }
                
                return result
            finally:
                cursor.close()
                conn.close()
        
        except mysql.connector.Error as e:
            return {"success": False, "error": "connection_error", "message": str(e)}
    
    else:
        return {"success": False, "error": "unsupported_database", "message": f"Unsupported database type: {db_type}"}


def main():
    parser = argparse.ArgumentParser(
        description='Run parameterized SQL queries safely across SQLite, PostgreSQL, and MySQL'
    )
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Create demo database with SQLite
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER
                )
            """)
            
            sample_users = [
                (1, "Alice Johnson", "alice@example.com", 28),
                (2, "Bob Smith", "bob@example.com", 35),
                (3, "Charlie Brown", "charlie@example.com", 42)
            ]
            cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", sample_users)
            conn.commit()
            
            # Run demo queries
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Query 1: Select all users
            cursor.execute("SELECT * FROM users")
            all_users = [dict(row) for row in cursor.fetchall()]
            
            # Query 2: Select user by ID (parameterized)
            cursor.execute("SELECT * FROM users WHERE id = ?", [2])
            user_by_id = [dict(row) for row in cursor.fetchall()]
            
            # Query 3: Select users older than age (parameterized)
            cursor.execute("SELECT * FROM users WHERE age > ?", [30])
            users_over_30 = [dict(row) for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            result = {
                "demo": True,
                "database": "SQLite in-memory",
                "supported_databases": {
                    "sqlite": "Built-in",
                    "postgresql": "Supported" if HAS_PSYCOPG2 else "Requires: pip install psycopg2-binary",
                    "mysql": "Supported" if HAS_MYSQL else "Requires: pip install mysql-connector-python"
                },
                "queries": {
                    "all_users": {
                        "query": "SELECT * FROM users",
                        "rows": all_users,
                        "row_count": len(all_users)
                    },
                    "user_by_id": {
                        "query": "SELECT * FROM users WHERE id = ?",
                        "params": [2],
                        "rows": user_by_id,
                        "row_count": len(user_by_id)
                    },
                    "users_over_30": {
                        "query": "SELECT * FROM users WHERE age > ?",
                        "params": [30],
                        "rows": users_over_30,
                        "row_count": len(users_over_30)
                    }
                }
            }
            print(format_success(result))
        
        elif args.params:
            params_dict = json.loads(args.params)
            
            db_type = params_dict.get("db_type", "sqlite")
            connection = params_dict.get("connection", ":memory:")
            query = params_dict.get("query", "")
            query_params = params_dict.get("params", [])
            
            if not query:
                raise ValueError("Query is required")
            
            result = execute_sql_query(db_type, connection, query, query_params)
            if "success" in result and not result["success"]:
                print(format_error(result.get("error", "Unknown error"), {"details": result.get("message")}))
            else:
                print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except sqlite3.Error as e:
        print(format_error(f"Database error: {e}", {"error_type": "database"}))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}", {"error_type": "processing"}))
        sys.exit(1)


if __name__ == '__main__':
    main()


def create_demo_database() -> str:
    """Create in-memory SQLite database with sample data.
    
    Returns:
        Connection string (:memory:)
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Create sample table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER
        )
    """)
    
    # Insert sample data
    sample_users = [
        (1, "Alice Johnson", "alice@example.com", 28),
        (2, "Bob Smith", "bob@example.com", 35),
        (3, "Charlie Brown", "charlie@example.com", 42)
    ]
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", sample_users)
    conn.commit()
    cursor.close()
    conn.close()
    
    return ":memory:"


def main():
    parser = argparse.ArgumentParser(
        description='Run parameterized SQL queries safely'
    )
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Create demo database
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER
                )
            """)
            
            sample_users = [
                (1, "Alice Johnson", "alice@example.com", 28),
                (2, "Bob Smith", "bob@example.com", 35),
                (3, "Charlie Brown", "charlie@example.com", 42)
            ]
            cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", sample_users)
            conn.commit()
            
            # Run demo queries
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Query 1: Select all users
            cursor.execute("SELECT * FROM users")
            all_users = [dict(row) for row in cursor.fetchall()]
            
            # Query 2: Select user by ID (parameterized)
            cursor.execute("SELECT * FROM users WHERE id = ?", [2])
            user_by_id = [dict(row) for row in cursor.fetchall()]
            
            # Query 3: Select users older than age (parameterized)
            cursor.execute("SELECT * FROM users WHERE age > ?", [30])
            users_over_30 = [dict(row) for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            result = {
                "demo": True,
                "database": "SQLite in-memory",
                "queries": {
                    "all_users": {
                        "query": "SELECT * FROM users",
                        "rows": all_users,
                        "row_count": len(all_users)
                    },
                    "user_by_id": {
                        "query": "SELECT * FROM users WHERE id = ?",
                        "params": [2],
                        "rows": user_by_id,
                        "row_count": len(user_by_id)
                    },
                    "users_over_30": {
                        "query": "SELECT * FROM users WHERE age > ?",
                        "params": [30],
                        "rows": users_over_30,
                        "row_count": len(users_over_30)
                    }
                }
            }
            print(format_success(result))
        
        elif args.params:
            params_dict = json.loads(args.params)
            
            db_type = params_dict.get("db_type", "sqlite")
            connection = params_dict.get("connection", ":memory:")
            query = params_dict.get("query", "")
            query_params = params_dict.get("params", [])
            
            if not query:
                raise ValueError("Query is required")
            
            result = execute_sql_query(db_type, connection, query, query_params)
            print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except sqlite3.Error as e:
        print(format_error(f"Database error: {e}", {"error_type": "database"}))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}", {"error_type": "processing"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
