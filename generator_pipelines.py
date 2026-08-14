def generate_data(num_records: int):
    """Yields dictionaries of raw data."""
    for i in range(num_records):
        yield {"id": i, "value": i * 2.5, "status": "active" if i % 2 == 0 else "inactive"}

def filter_active(records):
    """Filters only active records."""
    for record in records:
        if record.get("status") == "active":
            yield record

def scale_values(records, factor: float):
    """Scales the 'value' field by a given factor."""
    for record in records:
        record["value"] *= factor
        yield record

def calculate_sum(records) -> float:
    """Consumes the pipeline and calculates the total value."""
    total = 0.0
    for record in records:
        total += record["value"]
    return total

if __name__ == "__main__":
    print("Setting up generator pipeline...")
    # These functions don't execute immediately; they form a lazy pipeline
    raw_data = generate_data(1000)
    active_data = filter_active(raw_data)
    scaled_data = scale_values(active_data, 1.5)
    
    print("Consuming pipeline...")
    # Execution happens here
    total_value = calculate_sum(scaled_data)
    
    print(f"Total processed value: {total_value:.2f}")
