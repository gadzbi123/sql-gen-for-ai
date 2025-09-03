#!/usr/bin/env python3
"""
Advanced SQL Generator - Template-based SQL generation with variables
"""

import json
from typing import Dict, List, Any, Optional
from string import Template
from datetime import datetime, date


class SQLTemplateEngine:
    """Template-based SQL generator with variable substitution"""
    
    def __init__(self):
        self.templates = {
            'basic_select': Template("SELECT $columns FROM $table"),
            'filtered_select': Template("SELECT $columns FROM $table WHERE $conditions"),
            'joined_select': Template("SELECT $columns FROM $table $joins WHERE $conditions"),
            'aggregated_select': Template("SELECT $group_columns, $aggregates FROM $table GROUP BY $group_columns"),
            'paginated_select': Template("SELECT $columns FROM $table ORDER BY $order_by LIMIT $limit OFFSET $offset"),
            
            'basic_insert': Template("INSERT INTO $table ($columns) VALUES ($values)"),
            'bulk_insert': Template("INSERT INTO $table ($columns) VALUES $value_sets"),
            'insert_select': Template("INSERT INTO $table ($columns) SELECT $select_columns FROM $source_table WHERE $conditions"),
            
            'basic_update': Template("UPDATE $table SET $assignments WHERE $conditions"),
            'joined_update': Template("UPDATE $table $joins SET $assignments WHERE $conditions"),
            
            'basic_delete': Template("DELETE FROM $table WHERE $conditions"),
            'joined_delete': Template("DELETE $table FROM $table $joins WHERE $conditions"),
            
            'create_table': Template("CREATE TABLE $table ($column_definitions)"),
            'create_index': Template("CREATE INDEX $index_name ON $table ($columns)"),
        }
    
    def generate_query(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Generate SQL query from template and variables"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        return template.safe_substitute(**variables)
    
    def add_template(self, name: str, template_string: str):
        """Add custom template"""
        self.templates[name] = Template(template_string)


class SQLVariationEngine:
    """Generate multiple SQL variations from configuration"""
    
    def __init__(self):
        self.template_engine = SQLTemplateEngine()
    
    def generate_crud_variations(self, config: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate CRUD operation variations"""
        table = config['table']
        columns = config.get('columns', [])
        pk_column = config.get('primary_key', 'id')
        
        variations = {
            'select': [],
            'insert': [],
            'update': [],
            'delete': []
        }
        
        # SELECT variations
        variations['select'].extend([
            f"SELECT * FROM {table}",
            f"SELECT {', '.join(columns)} FROM {table}",
            f"SELECT COUNT(*) FROM {table}",
            f"SELECT * FROM {table} ORDER BY {pk_column} DESC LIMIT 10",
            f"SELECT DISTINCT {columns[0]} FROM {table}" if columns else f"SELECT * FROM {table}",
        ])
        
        # INSERT variations
        if columns:
            placeholders = ', '.join(['?' for _ in columns])
            column_list = ', '.join(columns)
            variations['insert'].extend([
                f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})",
                f"INSERT OR IGNORE INTO {table} ({column_list}) VALUES ({placeholders})",
                f"INSERT INTO {table} ({column_list}) SELECT {column_list} FROM temp_{table}",
            ])
        
        # UPDATE variations
        if columns:
            set_clause = ', '.join([f"{col} = ?" for col in columns])
            variations['update'].extend([
                f"UPDATE {table} SET {set_clause} WHERE {pk_column} = ?",
                f"UPDATE {table} SET {columns[0]} = ? WHERE {pk_column} IN (SELECT {pk_column} FROM temp_ids)",
            ])
        
        # DELETE variations
        variations['delete'].extend([
            f"DELETE FROM {table} WHERE {pk_column} = ?",
            f"DELETE FROM {table} WHERE created_at < ?",
            f"DELETE FROM {table} WHERE {pk_column} IN (?, ?, ?)",
        ])
        
        return variations
    
    def generate_analytical_variations(self, config: Dict[str, Any]) -> List[str]:
        """Generate analytical query variations"""
        table = config['table']
        date_column = config.get('date_column', 'created_at')
        group_columns = config.get('group_columns', [])
        numeric_columns = config.get('numeric_columns', [])
        
        queries = []
        
        # Time-based analytics
        queries.extend([
            f"SELECT DATE({date_column}) as date, COUNT(*) FROM {table} GROUP BY DATE({date_column})",
            f"SELECT YEAR({date_column}) as year, MONTH({date_column}) as month, COUNT(*) FROM {table} GROUP BY YEAR({date_column}), MONTH({date_column})",
            f"SELECT * FROM {table} WHERE {date_column} >= DATE_SUB(NOW(), INTERVAL 30 DAY)",
        ])
        
        # Grouping analytics
        if group_columns:
            for col in group_columns:
                queries.extend([
                    f"SELECT {col}, COUNT(*) as count FROM {table} GROUP BY {col} ORDER BY count DESC",
                    f"SELECT {col}, COUNT(*) as count FROM {table} GROUP BY {col} HAVING count > 10",
                ])
        
        # Numeric analytics
        if numeric_columns:
            for col in numeric_columns:
                queries.extend([
                    f"SELECT AVG({col}), MIN({col}), MAX({col}), SUM({col}) FROM {table}",
                    f"SELECT {col}, ROW_NUMBER() OVER (ORDER BY {col} DESC) as rank FROM {table}",
                ])
        
        # Window functions
        if group_columns and numeric_columns:
            group_col = group_columns[0]
            num_col = numeric_columns[0]
            queries.extend([
                f"SELECT {group_col}, {num_col}, AVG({num_col}) OVER (PARTITION BY {group_col}) as avg_by_group FROM {table}",
                f"SELECT {group_col}, {num_col}, RANK() OVER (PARTITION BY {group_col} ORDER BY {num_col} DESC) as rank_in_group FROM {table}",
            ])
        
        return queries
    
    def generate_join_variations(self, config: Dict[str, Any]) -> List[str]:
        """Generate JOIN query variations"""
        main_table = config['main_table']
        join_configs = config['joins']  # List of {table, on, type}
        
        queries = []
        
        for join_config in join_configs:
            join_table = join_config['table']
            on_condition = join_config['on']
            join_type = join_config.get('type', 'INNER')
            
            queries.extend([
                f"SELECT * FROM {main_table} {join_type} JOIN {join_table} ON {on_condition}",
                f"SELECT {main_table}.*, {join_table}.name FROM {main_table} {join_type} JOIN {join_table} ON {on_condition}",
                f"SELECT COUNT(*) FROM {main_table} {join_type} JOIN {join_table} ON {on_condition}",
            ])
        
        return queries


class DynamicSQLBuilder:
    """Build SQL dynamically based on runtime conditions"""
    
    def __init__(self):
        self.query_parts = {
            'select': [],
            'from': '',
            'joins': [],
            'where': [],
            'group_by': [],
            'having': [],
            'order_by': [],
            'limit': None
        }
    
    def select(self, *columns):
        """Add SELECT columns"""
        self.query_parts['select'].extend(columns)
        return self
    
    def from_table(self, table, alias=None):
        """Set FROM table"""
        self.query_parts['from'] = f"{table} {alias}" if alias else table
        return self
    
    def join(self, table, on_condition, join_type='INNER', alias=None):
        """Add JOIN"""
        table_ref = f"{table} {alias}" if alias else table
        self.query_parts['joins'].append(f"{join_type} JOIN {table_ref} ON {on_condition}")
        return self
    
    def where(self, condition):
        """Add WHERE condition"""
        self.query_parts['where'].append(condition)
        return self
    
    def group_by(self, *columns):
        """Add GROUP BY"""
        self.query_parts['group_by'].extend(columns)
        return self
    
    def order_by(self, column, direction='ASC'):
        """Add ORDER BY"""
        self.query_parts['order_by'].append(f"{column} {direction}")
        return self
    
    def limit(self, count, offset=None):
        """Add LIMIT"""
        self.query_parts['limit'] = f"LIMIT {count}"
        if offset:
            self.query_parts['limit'] += f" OFFSET {offset}"
        return self
    
    def build(self) -> str:
        """Build the final SQL query"""
        parts = []
        
        # SELECT
        select_clause = "SELECT " + (", ".join(self.query_parts['select']) or "*")
        parts.append(select_clause)
        
        # FROM
        if self.query_parts['from']:
            parts.append(f"FROM {self.query_parts['from']}")
        
        # JOINs
        if self.query_parts['joins']:
            parts.extend(self.query_parts['joins'])
        
        # WHERE
        if self.query_parts['where']:
            parts.append("WHERE " + " AND ".join(self.query_parts['where']))
        
        # GROUP BY
        if self.query_parts['group_by']:
            parts.append("GROUP BY " + ", ".join(self.query_parts['group_by']))
        
        # HAVING
        if self.query_parts['having']:
            parts.append("HAVING " + " AND ".join(self.query_parts['having']))
        
        # ORDER BY
        if self.query_parts['order_by']:
            parts.append("ORDER BY " + ", ".join(self.query_parts['order_by']))
        
        # LIMIT
        if self.query_parts['limit']:
            parts.append(self.query_parts['limit'])
        
        return " ".join(parts)
    
    def reset(self):
        """Reset builder state"""
        self.__init__()
        return self


def demo_advanced_usage():
    """Demonstrate advanced SQL generation"""
    
    print("=== Template Engine Demo ===")
    template_engine = SQLTemplateEngine()
    
    # Custom query with variables
    variables = {
        'columns': 'id, name, email',
        'table': 'users',
        'conditions': "active = 1 AND role = 'admin'"
    }
    
    query = template_engine.generate_query('filtered_select', variables)
    print(f"Generated: {query}")
    
    print("\n=== Variation Engine Demo ===")
    variation_engine = SQLVariationEngine()
    
    # CRUD variations
    config = {
        'table': 'products',
        'columns': ['name', 'price', 'category', 'description'],
        'primary_key': 'product_id'
    }
    
    crud_variations = variation_engine.generate_crud_variations(config)
    for operation, queries in crud_variations.items():
        print(f"\n{operation.upper()} Queries:")
        for i, query in enumerate(queries, 1):
            print(f"  {i}. {query}")
    
    print("\n=== Dynamic Builder Demo ===")
    builder = DynamicSQLBuilder()
    
    # Build complex query dynamically
    query = (builder
             .select('u.name', 'u.email', 'p.title', 'COUNT(o.id) as order_count')
             .from_table('users', 'u')
             .join('profiles p', 'u.id = p.user_id', 'LEFT')
             .join('orders o', 'u.id = o.user_id', 'LEFT')
             .where('u.active = 1')
             .where('u.created_at > "2024-01-01"')
             .group_by('u.id', 'u.name', 'u.email', 'p.title')
             .order_by('order_count', 'DESC')
             .limit(10)
             .build())
    
    print(f"Dynamic Query: {query}")
    
    # Generate multiple variations with different conditions
    print("\n=== Multiple Variations ===")
    base_conditions = [
        ('active users', 'active = 1'),
        ('recent users', 'created_at > "2024-01-01"'),
        ('admin users', 'role = "admin"'),
        ('premium users', 'subscription_type = "premium"')
    ]
    
    for desc, condition in base_conditions:
        builder.reset()
        query = (builder
                .select('name', 'email', 'created_at')
                .from_table('users')
                .where(condition)
                .order_by('created_at', 'DESC')
                .limit(5)
                .build())
        print(f"{desc}: {query}")


if __name__ == "__main__":
    demo_advanced_usage()