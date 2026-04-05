import pandas as pd
from src.ingest.taxi_ingest import JourneyType
from src.config.schema_configs import SCHEMA_CONFIGS

def optimise_types(df: pd.DataFrame, journey_type: JourneyType) -> pd.DataFrame:
    config = SCHEMA_CONFIGS.get(journey_type)

    if not config:
        return df
    
    # Standardise columns to lowecase
    df.columns = [col.lower() for col in df.columns]

    # Setup local list of columns to drop and column to be created
    cols_to_drop = set(config.get("drop_cols", []))
    new_cols = []

    # Access reference data in mappings
    mappings = config.get("mappings", {})

    for col_name, mapping_dict in mappings.items():
        if col_name in df.columns:
            new_col_name = f"{col_name}_label"
            df[new_col_name] = df[col_name].map(mapping_dict).astype("category")
        
            # Add each original ID column to drop list now we have labels
            cols_to_drop.add(col_name)

            # Add each new label name to new column list
            new_cols.append(new_col_name)
    
    # Access columns to be dropped and drop them from df
    print(f"🗑️ Dropped columns {cols_to_drop} for JourneyType: {journey_type.value}")
    print(f"New columns created: {new_cols} for JourneyType: {journey_type.value}")
    df = df.drop(columns= list(cols_to_drop), errors="ignore")
    
    return df
