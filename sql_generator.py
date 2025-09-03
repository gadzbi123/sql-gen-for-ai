#!/usr/bin/env python3
"""
SQL Query Generator - Produces different SQL variations from variables
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class QueryType(Enum):
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    CREATE_TABLE = "create_table"


class JoinType(Enum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"


@dataclass
class TableConfig:
    name: str
    alias: Optional[str] = None
    columns: List[str] = None
    
    def __post_init__(self):
        if self.columns is None:
            self.columns = []


@dataclass
class JoinConfig:
    table: str
    join_type: JoinType
    on_condition: str
    alias: Optional[str] = None


class SQLGenerator:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset generator state"""
        self.table = None
        self.columns = []
        self.conditions = []
        self.joins = []
        self.group_by = []
        self.order_by = []
        self.limit_count = None
        self.values = {}
        
    def set_table(self, table_name: str, alias: str = None) -> 'SQLGenerator':
        """Set the main table"""
        self.table = TableConfig(table_name, alias)
        return self
    
    def select_columns(self, *columns: str) -> 'SQLGenerator':
        """Add columns to SELECT"""
        self.columns.extend(columns)
        return self
    
    def where(self, condition: str) -> 'SQLGenerator':
        """Add WHERE condition"""
        self.conditions.append(condition)
        return self
    
    def join(self, table: str, join_type: JoinType, on_condition: str, alias: str = None) -> 'SQLGenerator':
        """Add JOIN clause"""
        self.joins.append(JoinConfig(table, join_type, on_condition, alias))
        return self
    
    def group_by_columns(self, *columns: str) -> 'SQLGenerator':
        """Add GROUP BY columns"""
        self.group_by.extend(columns)
        return self
    
    def order_by_columns(self, *columns: str) -> 'SQLGenerator':
        """Add ORDER BY columns"""
        self.order_by.extend(columns)
        return self
    
    def limit(self, count: int) -> 'SQLGenerator':
        """Set LIMIT"""
        self.limit_count = count
        return self
    
    def set_values(self, **kwargs) -> 'SQLGenerator':
        """Set values for INSERT/UPDATE"""
        self.values.update(kwargs)
        return self


class SQLVariationGenerator:
    def __init__(self):
        self.generator = SQLGenerator()
    
    def generate_select_variations(self, table: str, columns: List[str], 
                                 conditions: Dict[str, Any] = None) -> List[str]:
        """Generate different SELECT query variations"""
        variations = []
        conditions = conditions or {}
        
        # Basic SELECT
        query = f"SELECT {', '.join(columns)} FROM {table}"
        if conditions:
            where_clause = " AND ".join([f"{k} = '{v}'" for k, v in conditions.items()])
            query += f" WHERE {where_clause}"
        variations.append(query)
        
        # SELECT with COUNT
        variations.append(f"SELECT COUNT(*) FROM {table}")
        
        # SELECT DISTINCT
        if columns:
            variations.append(f"SELECT DISTINCT {columns[0]} FROM {table}")
        
        # SELECT with ORDER BY
        if columns:
            query_ordered = query + f" ORDER BY {columns[0]}"
            variations.append(query_ordered)
        
        # SELECT with LIMIT
        variations.append(query + " LIMIT 10")
        
        return variations
    
    def generate_insert_variations(self, table: str, data: Dict[str, Any]) -> List[str]:
        """Generate different INSERT query variations"""
        variations = []
        columns = list(data.keys())
        values = list(data.values())
        
        # Basic INSERT
        cols_str = ", ".join(columns)
        vals_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in values])
        variations.append(f"INSERT INTO {table} ({cols_str}) VALUES ({vals_str})")
        
        # INSERT with ON DUPLICATE KEY UPDATE (MySQL)
        update_clause = ", ".join([f"{k} = VALUES({k})" for k in columns])
        variations.append(f"INSERT INTO {table} ({cols_str}) VALUES ({vals_str}) ON DUPLICATE KEY UPDATE {update_clause}")
        
        # INSERT OR REPLACE (SQLite)
        variations.append(f"INSERT OR REPLACE INTO {table} ({cols_str}) VALUES ({vals_str})")
        
        # INSERT with subquery
        variations.append(f"INSERT INTO {table} ({cols_str}) SELECT {cols_str} FROM temp_table WHERE condition = 'value'")
        
        return variations
    
    def generate_update_variations(self, table: str, data: Dict[str, Any], 
                                 conditions: Dict[str, Any]) -> List[str]:
        """Generate different UPDATE query variations"""
        variations = []
        
        # Basic UPDATE
        set_clause = ", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" 
                               for k, v in data.items()])
        where_clause = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" 
                                   for k, v in conditions.items()])
        
        basic_update = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        variations.append(basic_update)
        
        # UPDATE with JOIN
        variations.append(f"""UPDATE {table} t1 
                            JOIN other_table t2 ON t1.id = t2.ref_id 
                            SET {set_clause} 
                            WHERE {where_clause}""")
        
        # UPDATE with subquery
        variations.append(f"""UPDATE {table} 
                            SET {list(data.keys())[0]} = (SELECT value FROM lookup_table WHERE id = {table}.lookup_id) 
                            WHERE {where_clause}""")
        
        return variations
    
    def generate_delete_variations(self, table: str, conditions: Dict[str, Any]) -> List[str]:
        """Generate different DELETE query variations"""
        variations = []
        where_clause = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" 
                                   for k, v in conditions.items()])
        
        # Basic DELETE
        variations.append(f"DELETE FROM {table} WHERE {where_clause}")
        
        # DELETE with JOIN
        variations.append(f"""DELETE t1 FROM {table} t1 
                            JOIN other_table t2 ON t1.id = t2.ref_id 
                            WHERE {where_clause}""")
        
        # DELETE with subquery
        variations.append(f"""DELETE FROM {table} 
                            WHERE id IN (SELECT id FROM temp_table WHERE {where_clause})""")
        
        # TRUNCATE (removes all data)
        variations.append(f"TRUNCATE TABLE {table}")
        
        return variations
    
    def generate_analytical_queries(self, table: str, group_column: str, 
                                  aggregate_column: str) -> List[str]:
        """Generate analytical query variations"""
        variations = []
        
        # Basic aggregation
        variations.append(f"SELECT {group_column}, COUNT(*) FROM {table} GROUP BY {group_column}")
        variations.append(f"SELECT {group_column}, SUM({aggregate_column}) FROM {table} GROUP BY {group_column}")
        variations.append(f"SELECT {group_column}, AVG({aggregate_column}) FROM {table} GROUP BY {group_column}")
        
        # Window functions
        variations.append(f"""SELECT {group_column}, {aggregate_column}, 
                            ROW_NUMBER() OVER (PARTITION BY {group_column} ORDER BY {aggregate_column}) as row_num
                            FROM {table}""")
        
        variations.append(f"""SELECT {group_column}, {aggregate_column},
                            RANK() OVER (ORDER BY {aggregate_column} DESC) as rank
                            FROM {table}""")
        
        # Time-based analysis
        variations.append(f"""SELECT DATE(created_at) as date, COUNT(*) 
                            FROM {table} 
                            GROUP BY DATE(created_at) 
                            ORDER BY date DESC""")
        
        return variations


def demo_usage():
    """Demonstrate the SQL generator usage"""
    generator = SQLVariationGenerator()
    
    print("=== SELECT Variations ===")
    select_queries = generator.generate_select_variations(
        table="users",
        columns=["id", "name", "email"],
        conditions={"active": True, "role": "admin"}
    )
    for i, query in enumerate(select_queries, 1):
        print(f"{i}. {query}")
    
    print("\n=== INSERT Variations ===")
    insert_queries = generator.generate_insert_variations(
        table="products",
        data={"name": "Laptop", "price": 999.99, "category": "Electronics"}
    )
    for i, query in enumerate(insert_queries, 1):
        print(f"{i}. {query}")
    
    print("\n=== UPDATE Variations ===")
    update_queries = generator.generate_update_variations(
        table="orders",
        data={"status": "shipped", "updated_at": "NOW()"},
        conditions={"id": 123}
    )
    for i, query in enumerate(update_queries, 1):
        print(f"{i}. {query}")
    
    print("\n=== DELETE Variations ===")
    delete_queries = generator.generate_delete_variations(
        table="logs",
        conditions={"created_at": "< '2024-01-01'"}
    )
    for i, query in enumerate(delete_queries, 1):
        print(f"{i}. {query}")
    
    print("\n=== Analytical Variations ===")
    analytical_queries = generator.generate_analytical_queries(
        table="sales",
        group_column="region",
        aggregate_column="amount"
    )
    for i, query in enumerate(analytical_queries, 1):
        print(f"{i}. {query}")


if __name__ == "__main__":
    demo_usage()