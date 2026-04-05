from src.ingest.taxi_ingest import JourneyType

def resolve_journey_type(user_input: str) -> JourneyType:
    # Return member associated with provided value.
    try:
        return JourneyType(user_input.lower().strip())
    except ValueError:
        valid_options = [jtype.value for jtype in JourneyType]
        raise ValueError(f"'{user_input}' is not a valid joruney. Choose from {valid_options}")