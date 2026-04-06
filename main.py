
# main.py 

import argparse
import sys
from src.utils.install_config import install_requirements
from src.utils.db_tools import get_engine, initialise_schemas, fast_postgres_upload
from src.ingest.taxi_ingest import fetch_taxi_data, JourneyType
from src.config.settings import resolve_journey_type
from src.transform.taxi_transformer import optimise_types
from src.transform.taxi_validation import validate_tripdata

def run_pipeline(journey_type, year, month):

    # Ingestion layer: handles imports and conenction to database
    install_requirements()
    engine = get_engine()
    initialise_schemas(engine) 

    df_bronze = fetch_taxi_data(journey_type, year, month)

    if df_bronze is not None:
        # Transformation layer
        df_silver = optimise_types(df_bronze, journey_type)

        # Validation layer
        df_gold, df_quarantine = validate_tripdata(df_silver)
        if not df_quarantine.empty:
            # Generate empty logging table for fast upload
            df_quarantine.head(0).to_sql("erroneous_tripdata", engine, schema="logging", if_exists="append", index=False)
            fast_postgres_upload(df_quarantine, "erroneous_tripdata", engine, schema="logging")
            print(f"⚠️ {len(df_quarantine)} rows labelled as erroneous and moved to 'logging'.")
        
        # Upload Layer
        table_name = f"{journey_type.value}_tripdata_gold"
        # Generate empty gold table ready for fast upload
        df_gold.head(0).to_sql(table_name, engine, schema="gold", if_exists="replace", index=False)
        fast_postgres_upload(df_gold, table_name, engine =engine, schema="gold")

if __name__ == "__main__":
    # Initialise Parser: handle command line strings to python objects 
    parser = argparse.ArgumentParser(description="NYC Taxi Medallion Pipeline")

    parser.add_argument("--type", type=str, required=True, help="Journey Type: (yellow, green, fhv, fhvhv)")

    parser.add_argument("--year", type=int, required=True, help="Year (i.e. 2026)")

    parser.add_argument("--month", type=int, required=True, help="Month (i.e. 1)")

    # Parse arguments
    args = parser.parse_args()

    try:
        # Pass type argument to function to resolve
        resolved_type = resolve_journey_type(args.type)

    except Exception as e:
        print(f"Failed to parse journey type. Valid journey types include: {[journey_type.value for journey_type in JourneyType]}")

    try:
        # Execute data pipeline using passed arguments
        run_pipeline(journey_type=resolved_type, year=args.year, month=args.month)

    except Exception as e:
        print(f"❌ Pipeline Failed: {e}")
        sys.exit(1) # Signal a failure to the OS

"""
Example usage:
    
    Python main.py --type green -- year 2026 --month 1

    http://localhost:5050
"""