from src.ingest.taxi_ingest import JourneyType

# Create reference data for numeric data fields - see NYC TLC web resources for full details
PAYMENT_MAP = {0: "Flex Fare Trip", 1: "Credit Card", 2: "Cash", 3: "No Charge", 4: "Dispute", 5: "Unkown", 6: "Voided"}
RATE_MAP = {1: "Standard", 2: "JFK", 3: "Newark", 4: "Nassau/Westchester", 5: "Negotiated", 6: "Group", 99: "Null/Unknown"}
VENDOR_MAP = {1: "Creative Mobile Technologies", 2: "Curb Mobility", 6: "Myle Technologies", 7: "Helix"}
TRIP_TYPE_MAP = {1: "Street-hail", 2: "Dispatch"}
LICENCE_BUSINESS_MAP = {"HV0002": "Juno", "HV0003": "Uber", "HV0004": "Via", "HV0005": "Lyft"}

# Define each JourneyType schema - data dictionaries to be accessed using "mappings" key
# Each "mapping" level describes a col_name: ref_data relationship
SCHEMA_CONFIGS = {

    JourneyType.YELLOW: {
    "mappings": {
        "payment_type": PAYMENT_MAP,
        "ratecodeid": RATE_MAP,
        "vendorid": VENDOR_MAP
        },
    "drop_cols": []
    },
    JourneyType.GREEN: {
    "mappings": {
        "payment_type": PAYMENT_MAP,
        "ratecodeid": RATE_MAP,
        "vendorid": VENDOR_MAP,
        "trip_type": TRIP_TYPE_MAP
        },
    "drop_cols": []
    },
     JourneyType.FHVHV: {
    "mappings": {
        "hvfhs_license_num": LICENCE_BUSINESS_MAP
        },
    "drop_cols": []
    }
}