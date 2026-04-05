import os
import io
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def get_engine():
    """
    Constructs a SQLAlchemy engine using environment variables.
    Defaults to localhost if DB_HOST is not provided.
    """
    # Access values within .env
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')

    # Flexible rl
    url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    # Suppress SQL logs  with echo=False to keep console clean
    return create_engine(url, echo=False)

def initialise_schemas(engine):
    """
    Creates the Medallion architecture schemas (bronze, silver, gold).
    Uses engine.begin() to automatically commit changes.
    """
    schemas = ['bronze', 'silver', 'gold']
    
    print("🛠️  Initializing database schemas...")
    
    # .begin() starts a transaction and commits automatically at the end of the block
    with engine.begin() as conn:
        for schema in schemas:
            try:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
                print(f"  ✅ Schema '{schema}' is ready.")
            except Exception as e:
                print(f"  ❌ Error creating schema '{schema}': {e}")
    
    print("🚀 Medallion layers are fully initialized.")

def fast_postgres_upload(df, table_name, engine, schema='bronze'):
    """
    High-speed upload using PostgreSQL COPY command via memory buffer.
    """

    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False, sep='\t') # Save to CSV without index and header
    buffer.seek(0)

    raw_conn = engine.raw_connection()
    try:
        with raw_conn.cursor() as cursor:
            # COPY command, cols must be in exact order of DataFrame
            # Becomes SQL Syntax: COPY schema.tname ('col1', 'col2') FROM ...
            columns = [f'"{col}"' for col in df.columns]
            sql = f'COPY {schema}.{table_name} ({", ".join(columns)}) FROM STDIN WITH CSV DELIMITER \'\t\''
            
            cursor.copy_expert(sql=sql, file=buffer)
            raw_conn.commit()
            print(f"🚀 Bulk upload to {schema}.{table_name} completed.")
    except Exception as e:
        raw_conn.rollback()
        print(f"❌ Bulk upload failed: {e}")
        raise
    finally:
        raw_conn.close()