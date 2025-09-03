#!/usr/bin/env python3
"""
Example usage of SQL generators with real data scenarios
"""

from sql_generator import SQLVariationGenerator
from advanced_sql_generator import DynamicSQLBuilder, SQLTemplateEngine, SQLVariationEngine


def ecommerce_example():
    """E-commerce database query examples"""
    print("🛒 E-COMMERCE SQL EXAMPLES")
    print("=" * 50)
    
    generator = SQLVariationGenerator()
    
    # Product queries
    print("\n📦 Product Queries:")
    product_queries = generator.generate_select_variations(
        table="products",
        columns=["id", "name", "price", "category", "stock_quantity"],
        conditions={"active": True, "stock_quantity": "> 0"}
    )
    
    for query in product_queries:
        print(f"  • {query}")
    
    # Order analytics
    print("\n📊 Order Analytics:")
    order_analytics = generator.generate_analytical_queries(
        table="orders",
        group_column="status",
        aggregate_column="total_amount"
    )
    
    for query in order_analytics:
        print(f"  • {query}")


def user_management_example():
    """User management system examples"""
    print("\n👥 USER MANAGEMENT SQL EXAMPLES")
    print("=" * 50)
    
    builder = DynamicSQLBuilder()
    
    # Different user scenarios
    scenarios = [
        {
            'name': 'Active Premium Users',
            'conditions': ['active = 1', 'subscription_type = "premium"'],
            'columns': ['id', 'username', 'email', 'subscription_expires']
        },
        {
            'name': 'New Users This Month',
            'conditions': ['created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)'],
            'columns': ['id', 'username', 'email', 'created_at']
        },
        {
            'name': 'Users with Orders',
            'conditions': [],
            'columns': ['u.username', 'u.email', 'COUNT(o.id) as order_count'],
            'joins': [('orders o', 'u.id = o.user_id', 'INNER')],
            'group_by': ['u.id', 'u.username', 'u.email']
        }
    ]
    
    for scenario in scenarios:
        builder.reset()
        query_builder = builder.select(*scenario['columns']).from_table('users', 'u')
        
        # Add joins if specified
        if 'joins' in scenario:
            for join_table, on_condition, join_type in scenario['joins']:
                query_builder.join(join_table, on_condition, join_type)
        
        # Add conditions
        for condition in scenario['conditions']:
            query_builder.where(condition)
        
        # Add group by if specified
        if 'group_by' in scenario:
            query_builder.group_by(*scenario['group_by'])
        
        query = query_builder.build()
        print(f"\n{scenario['name']}:")
        print(f"  {query}")


def reporting_dashboard_example():
    """Reporting dashboard queries"""
    print("\n📈 REPORTING DASHBOARD SQL EXAMPLES")
    print("=" * 50)
    
    template_engine = SQLTemplateEngine()
    
    # Add custom templates for reporting
    template_engine.add_template('daily_sales', 
        "SELECT DATE($date_column) as date, SUM($amount_column) as daily_total FROM $table WHERE $date_column >= DATE_SUB(NOW(), INTERVAL $days DAY) GROUP BY DATE($date_column)")
    
    template_engine.add_template('top_customers',
        "SELECT $customer_columns, SUM($amount_column) as total_spent FROM $table GROUP BY $customer_id ORDER BY total_spent DESC LIMIT $limit")
    
    template_engine.add_template('product_performance',
        "SELECT p.name, p.category, SUM(oi.quantity) as units_sold, SUM(oi.price * oi.quantity) as revenue FROM $products_table p JOIN $order_items_table oi ON p.id = oi.product_id GROUP BY p.id ORDER BY revenue DESC")
    
    # Generate reports
    reports = [
        {
            'name': 'Daily Sales (Last 30 Days)',
            'template': 'daily_sales',
            'vars': {
                'date_column': 'created_at',
                'amount_column': 'total_amount',
                'table': 'orders',
                'days': 30
            }
        },
        {
            'name': 'Top 10 Customers',
            'template': 'top_customers',
            'vars': {
                'customer_columns': 'customer_id, customer_name, customer_email',
                'amount_column': 'total_amount',
                'table': 'orders',
                'customer_id': 'customer_id',
                'limit': 10
            }
        }
    ]
    
    for report in reports:
        query = template_engine.generate_query(report['template'], report['vars'])
        print(f"\n{report['name']}:")
        print(f"  {query}")


def data_migration_example():
    """Data migration and ETL examples"""
    print("\n🔄 DATA MIGRATION SQL EXAMPLES")
    print("=" * 50)
    
    generator = SQLVariationGenerator()
    
    # Migration scenarios
    print("\n📥 Data Import Queries:")
    import_data = {
        'user_id': 123,
        'product_name': 'Wireless Headphones',
        'price': 99.99,
        'category': 'Electronics',
        'imported_at': 'NOW()'
    }
    
    import_queries = generator.generate_insert_variations('imported_products', import_data)
    for query in import_queries:
        print(f"  • {query}")
    
    print("\n🔄 Data Transformation Queries:")
    update_data = {'normalized_name': 'UPPER(product_name)', 'updated_at': 'NOW()'}
    conditions = {'category': 'Electronics'}
    
    transform_queries = generator.generate_update_variations('products', update_data, conditions)
    for query in transform_queries:
        print(f"  • {query}")


def performance_monitoring_example():
    """Performance monitoring queries"""
    print("\n⚡ PERFORMANCE MONITORING SQL EXAMPLES")
    print("=" * 50)
    
    variation_engine = SQLVariationEngine()
    
    # Performance analytics config
    config = {
        'table': 'api_logs',
        'date_column': 'timestamp',
        'group_columns': ['endpoint', 'method', 'status_code'],
        'numeric_columns': ['response_time_ms', 'request_size_bytes']
    }
    
    perf_queries = variation_engine.generate_analytical_variations(config)
    
    print("\n📊 Performance Analytics:")
    for i, query in enumerate(perf_queries[:8], 1):  # Show first 8 queries
        print(f"  {i}. {query}")


def main():
    """Run all examples"""
    examples = [
        ecommerce_example,
        user_management_example,
        reporting_dashboard_example,
        data_migration_example,
        performance_monitoring_example
    ]
    
    for example_func in examples:
        try:
            example_func()
            print("\n" + "="*70 + "\n")
        except Exception as e:
            print(f"Error in {example_func.__name__}: {e}")


if __name__ == "__main__":
    main()