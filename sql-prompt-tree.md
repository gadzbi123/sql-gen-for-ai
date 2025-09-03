# SQL Prompt Tree Structure

## 📊 Database Operations
### 🔍 Query Operations
#### Basic Queries
- **SELECT**: Retrieve data from tables
  - `SELECT * FROM table_name`
  - `SELECT column1, column2 FROM table_name WHERE condition`
- **DISTINCT**: Get unique values
  - `SELECT DISTINCT column_name FROM table_name`
- **COUNT**: Count records
  - `SELECT COUNT(*) FROM table_name`
  - `SELECT COUNT(DISTINCT column_name) FROM table_name`

#### Advanced Queries
- **JOINs**: Combine data from multiple tables
  - `INNER JOIN`: Records matching in both tables
  - `LEFT JOIN`: All records from left table
  - `RIGHT JOIN`: All records from right table
  - `FULL OUTER JOIN`: All records from both tables
- **Subqueries**: Nested queries
  - `SELECT * FROM table1 WHERE id IN (SELECT id FROM table2)`
- **Window Functions**: Advanced analytics
  - `ROW_NUMBER() OVER (PARTITION BY column ORDER BY column)`
  - `RANK() OVER (ORDER BY column)`

### ✏️ Data Modification
#### Insert Operations
- **INSERT**: Add new records
  - `INSERT INTO table_name (col1, col2) VALUES (val1, val2)`
  - `INSERT INTO table_name SELECT * FROM other_table WHERE condition`

#### Update Operations
- **UPDATE**: Modify existing records
  - `UPDATE table_name SET column1 = value1 WHERE condition`
  - `UPDATE table1 SET col1 = (SELECT col2 FROM table2 WHERE condition)`

#### Delete Operations
- **DELETE**: Remove records
  - `DELETE FROM table_name WHERE condition`
  - `TRUNCATE TABLE table_name` (faster, removes all)

### 🏗️ Schema Operations
#### Table Management
- **CREATE TABLE**: Define new tables
  ```sql
  CREATE TABLE table_name (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
  ```
- **ALTER TABLE**: Modify table structure
  - `ALTER TABLE table_name ADD COLUMN new_column datatype`
  - `ALTER TABLE table_name DROP COLUMN column_name`
- **DROP TABLE**: Remove tables
  - `DROP TABLE table_name`

#### Index Management
- **CREATE INDEX**: Improve query performance
  - `CREATE INDEX idx_name ON table_name (column_name)`
- **DROP INDEX**: Remove indexes
  - `DROP INDEX idx_name`

## 🎯 Common Use Cases
### 📈 Analytics & Reporting
#### Aggregations
- **GROUP BY**: Group data for calculations
  - `SELECT category, COUNT(*) FROM products GROUP BY category`
  - `SELECT DATE(created_at), SUM(amount) FROM orders GROUP BY DATE(created_at)`
- **HAVING**: Filter grouped results
  - `SELECT category, COUNT(*) FROM products GROUP BY category HAVING COUNT(*) > 10`

#### Time-based Analysis
- **Date Functions**: Work with dates
  - `SELECT * FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)`
  - `SELECT YEAR(created_at), MONTH(created_at), COUNT(*) FROM orders GROUP BY YEAR(created_at), MONTH(created_at)`

### 🔗 Data Relationships
#### Foreign Keys
- **REFERENCES**: Link tables
  ```sql
  CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
  )
  ```

#### Many-to-Many Relationships
- **Junction Tables**: Handle complex relationships
  ```sql
  CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
  )
  ```

## 🛠️ Performance & Optimization
### 🚀 Query Optimization
#### Indexing Strategies
- **Single Column Index**: `CREATE INDEX idx_email ON users (email)`
- **Composite Index**: `CREATE INDEX idx_name_date ON orders (customer_id, created_at)`
- **Partial Index**: `CREATE INDEX idx_active_users ON users (email) WHERE active = true`

#### Query Hints
- **EXPLAIN**: Analyze query execution
  - `EXPLAIN SELECT * FROM large_table WHERE indexed_column = 'value'`
- **LIMIT**: Restrict result size
  - `SELECT * FROM table_name ORDER BY created_at DESC LIMIT 10`

### 📊 Data Types & Constraints
#### Common Data Types
- **Numeric**: `INT`, `BIGINT`, `DECIMAL(10,2)`, `FLOAT`
- **Text**: `VARCHAR(255)`, `TEXT`, `CHAR(10)`
- **Date/Time**: `DATE`, `TIMESTAMP`, `DATETIME`
- **Boolean**: `BOOLEAN`, `TINYINT(1)`

#### Constraints
- **PRIMARY KEY**: Unique identifier
- **UNIQUE**: Ensure uniqueness
- **NOT NULL**: Require value
- **CHECK**: Custom validation
- **DEFAULT**: Set default value

## 🔧 Database-Specific Features
### MySQL
- **AUTO_INCREMENT**: Auto-generating IDs
- **ENGINE**: Storage engine selection (InnoDB, MyISAM)
- **CHARSET**: Character set specification

### PostgreSQL
- **SERIAL**: Auto-incrementing integers
- **JSONB**: JSON data type with indexing
- **ARRAY**: Array data types
- **ENUM**: Custom enumerated types

### SQLite
- **INTEGER PRIMARY KEY**: Auto-increment without AUTOINCREMENT
- **WITHOUT ROWID**: Optimize table structure
- **PRAGMA**: Database configuration

## 📝 Best Practices
### 🎯 Query Writing
- Use meaningful table and column aliases
- Always specify column names in INSERT statements
- Use parameterized queries to prevent SQL injection
- Add appropriate WHERE clauses to limit data
- Use LIMIT for large result sets

### 🏗️ Schema Design
- Normalize data to reduce redundancy
- Use appropriate data types and sizes
- Add indexes on frequently queried columns
- Use foreign keys to maintain referential integrity
- Document your schema with comments

### 🔒 Security
- Use least privilege principle for database users
- Validate and sanitize all inputs
- Use stored procedures when appropriate
- Regular backups and recovery testing
- Monitor for suspicious query patterns