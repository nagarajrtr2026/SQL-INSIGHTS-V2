import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

def seed():
    # Connect to the default 'postgres' database to create the target database if needed
    default_url = "postgresql://postgres:postgres@localhost:5432/postgres"
    engine = create_engine(default_url, isolation_level="AUTOCOMMIT")
    
    db_name = "agentic_ai"
    try:
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
            if not result.fetchone():
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Could not connect/create database: {e}")
        # Continue anyway, maybe db is already created and we don't have superuser permission
        pass
    finally:
        engine.dispose()

    # Now connect to the agentic_ai database and create/seed the sales table
    target_url = f"postgresql://postgres:postgres@localhost:5432/{db_name}"
    target_engine = create_engine(target_url)
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        product_name VARCHAR(255),
        region VARCHAR(100),
        sales INTEGER,
        sale_date DATE
    );
    """
    
    mock_data = [
        ("Pro Laptop", "North", 1500, "2026-05-01"),
        ("Pro Laptop", "South", 1200, "2026-05-05"),
        ("Pro Laptop", "East", 1800, "2026-05-10"),
        ("Pro Laptop", "West", 1600, "2026-05-15"),
        ("Wireless Mouse", "North", 25, "2026-05-02"),
        ("Wireless Mouse", "South", 30, "2026-05-04"),
        ("Wireless Mouse", "East", 28, "2026-05-06"),
        ("Wireless Mouse", "West", 35, "2026-05-12"),
        ("Noise-Cancelling Headphones", "North", 350, "2026-05-03"),
        ("Noise-Cancelling Headphones", "South", 290, "2026-05-07"),
        ("Noise-Cancelling Headphones", "East", 410, "2026-05-11"),
        ("Noise-Cancelling Headphones", "West", 320, "2026-05-14"),
        ("Ergonomic Chair", "North", 450, "2026-05-04"),
        ("Ergonomic Chair", "South", 520, "2026-05-08"),
        ("Ergonomic Chair", "East", 480, "2026-05-09"),
        ("Ergonomic Chair", "West", 500, "2026-05-13"),
        ("Mechanical Keyboard", "North", 120, "2026-05-06"),
        ("Mechanical Keyboard", "South", 110, "2026-05-09"),
        ("Mechanical Keyboard", "East", 130, "2026-05-12"),
        ("Mechanical Keyboard", "West", 125, "2026-05-15"),
    ]
    
    try:
        with target_engine.begin() as conn:
            conn.execute(text(create_table_sql))
            print("Table 'sales' checked/created.")
            
            # Check if empty
            count_res = conn.execute(text("SELECT COUNT(*) FROM sales"))
            count = count_res.scalar()
            
            if count == 0:
                insert_sql = text("INSERT INTO sales (product_name, region, sales, sale_date) VALUES (:prod, :region, :sales, :date)")
                for prod, region, sales, date in mock_data:
                    conn.execute(insert_sql, {"prod": prod, "region": region, "sales": sales, "date": date})
                print("Seeded 'sales' table with mock data.")
            else:
                print(f"Table 'sales' already has {count} records. Skipping seeding.")
                
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)
    finally:
        target_engine.dispose()

if __name__ == "__main__":
    seed()
