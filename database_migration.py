"""
Database Migration Module

This module provides comprehensive database migration utilities including:
- Migration versioning
- Schema change tracking
- Rollback functionality
- Migration execution
- Database introspection
- Schema comparison
- Migration generation
- Dependency management
- Transaction handling
- Migration logging

Note: This module uses sqlite3 for demonstration.
For production, use proper migration tools like Alembic or Flyway.

All functions include comprehensive docstrings and type hints.
"""

import sqlite3
import json
import hashlib
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import os


class MigrationStatus(Enum):
    """Migration status."""
    PENDING = "pending"
    APPLIED = "applied"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class MigrationType(Enum):
    """Types of migrations."""
    CREATE_TABLE = "create_table"
    DROP_TABLE = "drop_table"
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    ALTER_COLUMN = "alter_column"
    ADD_INDEX = "add_index"
    DROP_INDEX = "drop_index"
    ADD_FOREIGN_KEY = "add_foreign_key"
    DROP_FOREIGN_KEY = "drop_foreign_key"
    RAW_SQL = "raw_sql"


@dataclass
class Migration:
    """Database migration."""
    version: str
    name: str
    up_sql: str
    down_sql: str
    checksum: str
    type: MigrationType
    dependencies: List[str]
    applied_at: Optional[datetime] = None
    status: MigrationStatus = MigrationStatus.PENDING
    
    def __post_init__(self):
        """Calculate checksum if not provided."""
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """Calculate migration checksum."""
        content = f"{self.version}{self.name}{self.up_sql}{self.down_sql}"
        return hashlib.sha256(content.encode()).hexdigest()


class MigrationTracker:
    """Track applied migrations."""
    
    def __init__(self, db_path: str):
        """Initialize migration tracker."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._ensure_migration_table()
    
    def _ensure_migration_table(self) -> None:
        """Ensure migration table exists."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                checksum TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_time REAL,
                status TEXT DEFAULT 'applied'
            )
        """)
        self.conn.commit()
    
    def record_migration(self, migration: Migration, execution_time: float) -> bool:
        """Record applied migration."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO schema_migrations 
                (version, name, checksum, applied_at, execution_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                migration.version,
                migration.name,
                migration.checksum,
                datetime.now(),
                execution_time,
                MigrationStatus.APPLIED.value
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def remove_migration(self, version: str) -> bool:
        """Remove migration record."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM schema_migrations WHERE version = ?", (version,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_applied_migrations(self) -> List[Dict]:
        """Get list of applied migrations."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT version, name, checksum, applied_at, execution_time, status
            FROM schema_migrations
            ORDER BY applied_at
        """)
        
        return [
            {
                "version": row[0],
                "name": row[1],
                "checksum": row[2],
                "applied_at": row[3],
                "execution_time": row[4],
                "status": row[5]
            }
            for row in cursor.fetchall()
        ]
    
    def get_applied_version(self, version: str) -> Optional[Dict]:
        """Get specific applied migration."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT version, name, checksum, applied_at, execution_time, status
            FROM schema_migrations
            WHERE version = ?
        """, (version,))
        
        row = cursor.fetchone()
        if row:
            return {
                "version": row[0],
                "name": row[1],
                "checksum": row[2],
                "applied_at": row[3],
                "execution_time": row[4],
                "status": row[5]
            }
        return None
    
    def close(self) -> None:
        """Close database connection."""
        self.conn.close()


class MigrationExecutor:
    """Execute database migrations."""
    
    def __init__(self, db_path: str):
        """Initialize migration executor."""
        self.db_path = db_path
        self.tracker = MigrationTracker(db_path)
    
    def execute_up(self, migration: Migration) -> Tuple[bool, float]:
        """Execute migration up."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_time = datetime.now()
        
        try:
            cursor.execute(migration.up_sql)
            conn.commit()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.tracker.record_migration(migration, execution_time)
            
            return True, execution_time
        except Exception as e:
            conn.rollback()
            print(f"Migration failed: {e}")
            return False, 0.0
        finally:
            conn.close()
    
    def execute_down(self, migration: Migration) -> Tuple[bool, float]:
        """Execute migration down (rollback)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_time = datetime.now()
        
        try:
            cursor.execute(migration.down_sql)
            conn.commit()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.tracker.remove_migration(migration.version)
            
            return True, execution_time
        except Exception as e:
            conn.rollback()
            print(f"Rollback failed: {e}")
            return False, 0.0
        finally:
            conn.close()
    
    def close(self) -> None:
        """Close executor."""
        self.tracker.close()


class SchemaIntrospector:
    """Database schema introspection."""
    
    def __init__(self, db_path: str):
        """Initialize introspector."""
        self.db_path = db_path
    
    def get_tables(self) -> List[str]:
        """Get list of tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return tables
    
    def get_table_schema(self, table_name: str) -> Dict:
        """Get table schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        
        conn.close()
        
        return {
            "columns": [
                {
                    "name": col[1],
                    "type": col[2],
                    "not_null": col[3],
                    "default_value": col[4],
                    "primary_key": col[5]
                }
                for col in columns
            ],
            "foreign_keys": foreign_keys,
            "indexes": indexes
        }
    
    def get_schema_hash(self) -> str:
        """Get hash of current schema."""
        tables = self.get_tables()
        schema_data = {}
        
        for table in tables:
            schema_data[table] = self.get_table_schema(table)
        
        return hashlib.sha256(json.dumps(schema_data, sort_keys=True).encode()).hexdigest()


class SchemaComparator:
    """Compare database schemas."""
    
    @staticmethod
    def compare_schemas(schema1: Dict, schema2: Dict) -> Dict:
        """Compare two schemas."""
        tables1 = set(schema1.keys())
        tables2 = set(schema2.keys())
        
        added_tables = tables2 - tables1
        removed_tables = tables1 - tables2
        common_tables = tables1 & tables2
        
        differences = {
            "added_tables": list(added_tables),
            "removed_tables": list(removed_tables),
            "modified_tables": []
        }
        
        for table in common_tables:
            if schema1[table] != schema2[table]:
                differences["modified_tables"].append(table)
        
        return differences
    
    @staticmethod
    def generate_migration_from_diff(diff: Dict) -> List[Migration]:
        """Generate migrations from schema differences."""
        migrations = []
        
        # Generate migrations for added tables
        for table in diff["added_tables"]:
            # This would need full schema details
            pass
        
        # Generate migrations for removed tables
        for table in diff["removed_tables"]:
            down_sql = f"DROP TABLE IF EXISTS {table};"
            up_sql = f"-- Recreate {table}"
            
            migration = Migration(
                version=f"drop_{table}",
                name=f"Drop table {table}",
                up_sql=up_sql,
                down_sql=down_sql,
                checksum="",
                type=MigrationType.DROP_TABLE,
                dependencies=[]
            )
            migrations.append(migration)
        
        return migrations


class MigrationGenerator:
    """Generate migration files."""
    
    @staticmethod
    def generate_create_table_migration(table_name: str, columns: Dict) -> Migration:
        """Generate create table migration."""
        column_defs = []
        for col_name, col_type in columns.items():
            column_defs.append(f"{col_name} {col_type}")
        
        up_sql = f"CREATE TABLE {table_name} (\n    " + ",\n    ".join(column_defs) + "\n);"
        down_sql = f"DROP TABLE {table_name};"
        
        return Migration(
            version=f"create_{table_name}",
            name=f"Create table {table_name}",
            up_sql=up_sql,
            down_sql=down_sql,
            checksum="",
            type=MigrationType.CREATE_TABLE,
            dependencies=[]
        )
    
    @staticmethod
    def generate_add_column_migration(table_name: str, column_name: str, 
                                      column_type: str) -> Migration:
        """Generate add column migration."""
        up_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
        down_sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        
        return Migration(
            version=f"add_{column_name}_to_{table_name}",
            name=f"Add column {column_name} to {table_name}",
            up_sql=up_sql,
            down_sql=down_sql,
            checksum="",
            type=MigrationType.ADD_COLUMN,
            dependencies=[]
        )
    
    @staticmethod
    def generate_add_index_migration(table_name: str, column_name: str,
                                    index_name: Optional[str] = None) -> Migration:
        """Generate add index migration."""
        idx_name = index_name or f"idx_{table_name}_{column_name}"
        up_sql = f"CREATE INDEX {idx_name} ON {table_name}({column_name});"
        down_sql = f"DROP INDEX {idx_name};"
        
        return Migration(
            version=f"add_index_{idx_name}",
            name=f"Add index {idx_name}",
            up_sql=up_sql,
            down_sql=down_sql,
            checksum="",
            type=MigrationType.ADD_INDEX,
            dependencies=[]
        )
    
    @staticmethod
    def generate_raw_sql_migration(version: str, name: str, 
                                  up_sql: str, down_sql: str) -> Migration:
        """Generate raw SQL migration."""
        return Migration(
            version=version,
            name=name,
            up_sql=up_sql,
            down_sql=down_sql,
            checksum="",
            type=MigrationType.RAW_SQL,
            dependencies=[]
        )


class MigrationManager:
    """Manage database migrations."""
    
    def __init__(self, db_path: str, migrations_dir: str = "migrations"):
        """Initialize migration manager."""
        self.db_path = db_path
        self.migrations_dir = migrations_dir
        self.executor = MigrationExecutor(db_path)
        self.migrations: Dict[str, Migration] = {}
        
        # Create migrations directory
        os.makedirs(migrations_dir, exist_ok=True)
    
    def add_migration(self, migration: Migration) -> None:
        """Add migration to manager."""
        self.migrations[migration.version] = migration
    
    def load_migrations_from_dir(self) -> None:
        """Load migrations from directory."""
        for filename in os.listdir(self.migrations_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.migrations_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    
                    migration = Migration(
                        version=data["version"],
                        name=data["name"],
                        up_sql=data["up_sql"],
                        down_sql=data["down_sql"],
                        checksum=data.get("checksum", ""),
                        type=MigrationType(data.get("type", "raw_sql")),
                        dependencies=data.get("dependencies", [])
                    )
                    self.add_migration(migration)
    
    def save_migration(self, migration: Migration) -> None:
        """Save migration to file."""
        filepath = os.path.join(self.migrations_dir, f"{migration.version}.json")
        
        data = {
            "version": migration.version,
            "name": migration.name,
            "up_sql": migration.up_sql,
            "down_sql": migration.down_sql,
            "checksum": migration.checksum,
            "type": migration.type.value,
            "dependencies": migration.dependencies
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_pending_migrations(self) -> List[Migration]:
        """Get pending migrations."""
        applied = self.executor.tracker.get_applied_migrations()
        applied_versions = {m["version"] for m in applied}
        
        pending = []
        for version, migration in self.migrations.items():
            if version not in applied_versions:
                pending.append(migration)
        
        # Sort by version
        pending.sort(key=lambda m: m.version)
        
        return pending
    
    def migrate_up(self, target_version: Optional[str] = None) -> Dict:
        """Migrate up to target version."""
        pending = self.get_pending_migrations()
        
        if target_version:
            pending = [m for m in pending if m.version <= target_version]
        
        results = {
            "successful": [],
            "failed": [],
            "skipped": []
        }
        
        for migration in pending:
            # Check dependencies
            if not self._check_dependencies(migration):
                results["skipped"].append(migration.version)
                continue
            
            success, exec_time = self.executor.execute_up(migration)
            
            if success:
                results["successful"].append({
                    "version": migration.version,
                    "execution_time": exec_time
                })
            else:
                results["failed"].append(migration.version)
                break
        
        return results
    
    def migrate_down(self, target_version: Optional[str] = None) -> Dict:
        """Migrate down to target version."""
        applied = self.executor.tracker.get_applied_migrations()
        
        if target_version:
            to_rollback = [m for m in applied if m["version"] > target_version]
        else:
            to_rollback = applied[-1:] if applied else []
        
        results = {
            "successful": [],
            "failed": []
        }
        
        for migration_data in reversed(to_rollback):
            version = migration_data["version"]
            if version in self.migrations:
                migration = self.migrations[version]
                success, exec_time = self.executor.execute_down(migration)
                
                if success:
                    results["successful"].append({
                        "version": version,
                        "execution_time": exec_time
                    })
                else:
                    results["failed"].append(version)
                    break
        
        return results
    
    def _check_dependencies(self, migration: Migration) -> bool:
        """Check if migration dependencies are satisfied."""
        applied = self.executor.tracker.get_applied_migrations()
        applied_versions = {m["version"] for m in applied}
        
        for dep in migration.dependencies:
            if dep not in applied_versions:
                return False
        
        return True
    
    def get_status(self) -> Dict:
        """Get migration status."""
        applied = self.executor.tracker.get_applied_migrations()
        pending = self.get_pending_migrations()
        
        return {
            "applied_count": len(applied),
            "pending_count": len(pending),
            "applied_versions": [m["version"] for m in applied],
            "pending_versions": [m.version for m in pending]
        }
    
    def close(self) -> None:
        """Close manager."""
        self.executor.close()


class DataMigrator:
    """Migrate data between schemas."""
    
    @staticmethod
    def migrate_data(source_db: str, target_db: str, 
                    table_mapping: Dict[str, str],
                    column_mapping: Dict[str, Dict[str, str]]) -> int:
        """Migrate data between databases."""
        source_conn = sqlite3.connect(source_db)
        target_conn = sqlite3.connect(target_db)
        
        rows_migrated = 0
        
        for source_table, target_table in table_mapping.items():
            # Get columns for mapping
            col_map = column_mapping.get(source_table, {})
            
            # Read from source
            cursor = source_conn.cursor()
            cursor.execute(f"SELECT * FROM {source_table}")
            rows = cursor.fetchall()
            
            # Write to target
            target_cursor = target_conn.cursor()
            
            for row in rows:
                # Map columns
                if col_map:
                    mapped_data = {}
                    for src_col, tgt_col in col_map.items():
                        # Simple column mapping
                        mapped_data[tgt_col] = row[0]  # Simplified
                    
                    placeholders = ", ".join(["?"] * len(mapped_data))
                    target_cursor.execute(
                        f"INSERT INTO {target_table} VALUES ({placeholders})",
                        list(mapped_data.values())
                    )
                else:
                    target_cursor.execute(
                        f"INSERT INTO {target_table} VALUES ({', '.join(['?'] * len(row))})",
                        row
                    )
                
                rows_migrated += 1
            
            target_conn.commit()
        
        source_conn.close()
        target_conn.close()
        
        return rows_migrated


def demonstrate_database_migration():
    """Demonstrate database migration functionality."""
    print("=== Database Migration Demonstration ===\n")
    
    # Create test database
    test_db = "test_migration.db"
    
    # Migration Manager
    print("1. Migration Manager:")
    manager = MigrationManager(test_db, "test_migrations")
    
    # Generate migrations
    print("\n2. Generating Migrations:")
    
    create_users = MigrationGenerator.generate_create_table_migration(
        "users",
        {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE"
        }
    )
    
    add_column = MigrationGenerator.generate_add_column_migration(
        "users",
        "age",
        "INTEGER"
    )
    
    add_index = MigrationGenerator.generate_add_index_migration(
        "users",
        "email"
    )
    
    manager.add_migration(create_users)
    manager.add_migration(add_column)
    manager.add_migration(add_index)
    
    print(f"   Generated migrations: {len(manager.migrations)}")
    
    # Save migrations
    print("\n3. Saving Migrations:")
    for migration in manager.migrations.values():
        manager.save_migration(migration)
    print(f"   Saved {len(manager.migrations)} migrations")
    
    # Get status
    print("\n4. Migration Status:")
    status = manager.get_status()
    print(f"   Applied: {status['applied_count']}")
    print(f"   Pending: {status['pending_count']}")
    print(f"   Pending versions: {status['pending_versions']}")
    
    # Migrate up
    print("\n5. Migrating Up:")
    results = manager.migrate_up()
    print(f"   Successful: {len(results['successful'])}")
    print(f"   Failed: {len(results['failed'])}")
    
    # Check applied migrations
    print("\n6. Applied Migrations:")
    applied = manager.executor.tracker.get_applied_migrations()
    for m in applied:
        print(f"   {m['version']}: {m['name']}")
    
    # Schema introspection
    print("\n7. Schema Introspection:")
    introspector = SchemaIntrospector(test_db)
    tables = introspector.get_tables()
    print(f"   Tables: {tables}")
    
    if tables:
        schema = introspector.get_table_schema(tables[0])
        print(f"   Columns in {tables[0]}: {[col['name'] for col in schema['columns']]}")
    
    # Schema hash
    print("\n8. Schema Hash:")
    schema_hash = introspector.get_schema_hash()
    print(f"   Schema hash: {schema_hash[:16]}...")
    
    # Generate more migration
    print("\n9. Additional Migration:")
    create_posts = MigrationGenerator.generate_create_table_migration(
        "posts",
        {
            "id": "INTEGER PRIMARY KEY",
            "user_id": "INTEGER",
            "title": "TEXT NOT NULL",
            "content": "TEXT"
        }
    )
    
    create_posts.dependencies = ["create_users"]
    manager.add_migration(create_posts)
    manager.save_migration(create_posts)
    
    # Migrate again
    print("\n10. Second Migration:")
    results = manager.migrate_up()
    print(f"   Successful: {len(results['successful'])}")
    
    # Rollback
    print("\n11. Rollback:")
    rollback_results = manager.migrate_down(target_version="create_users")
    print(f"   Rolled back: {len(rollback_results['successful'])}")
    
    # Cleanup
    manager.close()
    
    # Remove test files
    import os
    import shutil
    if os.path.exists(test_db):
        os.remove(test_db)
    if os.path.exists("test_migrations"):
        shutil.rmtree("test_migrations")
    
    print("\n12. Cleanup complete")
    
    print("\n=== Demonstration Complete ===")
    print("\nDatabase Migration Best Practices:")
    print("- Always include rollback migrations (down SQL)")
    print("- Use version numbers to order migrations")
    print("- Test migrations in development first")
    print("- Never modify applied migrations")
    print("- Use transactions for atomic operations")
    print("- Document schema changes in migrations")
    print("- Check dependencies before applying")
    print("- Back up database before major migrations")
    print("- Use proper migration tools (Alembic, Flyway) in production")
    print("- Keep migration files in version control")
    print("- Review generated migrations before applying")


if __name__ == "__main__":
    demonstrate_database_migration()