import pandas as pd

def validate_tripdata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies a matrix of constraints to taxi df, ensuring that only valid data is
    uploaded to the database.  
    """
    
    # Define dictionary of headers and constraints to be used as filters
    constraints = {
        "passenger_count": df["passenger_count"] > 0,
        "total_amount": df["total_amount"] > 0,
        "trip_distance": df["trip_distance"] > 0
    }

    # Locate and return rows which pass constraints
    constraints_matrix = pd.concat(constraints, axis=1)
    failed_rows = df[~constraints_matrix.all(axis=1)]
    return df.drop(failed_rows.index)