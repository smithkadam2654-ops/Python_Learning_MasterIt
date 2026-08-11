"""
Advanced Python - Lesson 11: File I/O & Serialization
======================================================
Serialization converts objects to storable/transmittable formats.
Python supports JSON, CSV, pickle, and more.

Topics Covered:
- JSON serialization (json module)
- CSV reading and writing (csv module)
- Pickle for Python-specific serialization
- Working with binary files
- Custom JSON encoders/decoders
- Streaming large files
- Configuration files (INI with configparser)
- File path operations (pathlib)
"""

import json
import csv
import pickle
import io
import tempfile
import os
from pathlib import Path
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import Any


# ============================================================
# 1. JSON SERIALIZATION
# ============================================================
def demonstrate_json():
    """JSON: the universal data interchange format."""
    
    # Basic serialization
    data = {
        "name": "Alice",
        "age": 30,
        "scores": [95, 87, 92],
        "active": True,
        "address": {"city": "NYC", "zip": "10001"},
    }
    
    # dumps: object -> string
    json_str = json.dumps(data, indent=2)
    print("JSON string:")
    print(json_str)
    
    # loads: string -> object
    parsed = json.loads(json_str)
    print(f"\nParsed back: {parsed['name']}, scores: {parsed['scores']}")
    
    # Writing to file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f, indent=2)
        tmp_path = f.name
    
    # Reading from file
    with open(tmp_path, "r") as f:
        loaded = json.load(f)
    print(f"Loaded from file: {loaded['name']}")
    
    os.unlink(tmp_path)


# ============================================================
# 2. CUSTOM JSON ENCODER
# ============================================================
class CustomEncoder(json.JSONEncoder):
    """Custom JSON encoder for Python-specific types."""
    
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return {"__type__": "datetime", "value": obj.isoformat()}
        if isinstance(obj, set):
            return {"__type__": "set", "value": list(obj)}
        if isinstance(obj, bytes):
            return {"__type__": "bytes", "value": obj.hex()}
        if hasattr(obj, "to_json"):
            return obj.to_json()
        return super().default(obj)


def custom_decoder(dct: dict) -> Any:
    """Custom JSON decoder hook for restoring special types."""
    if "__type__" in dct:
        if dct["__type__"] == "datetime":
            return datetime.fromisoformat(dct["value"])
        if dct["__type__"] == "set":
            return set(dct["value"])
        if dct["__type__"] == "bytes":
            return bytes.fromhex(dct["value"])
    return dct


@dataclass
class UserProfile:
    """User profile with custom serialization."""
    username: str
    email: str
    created_at: datetime
    tags: set

    def to_json(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "tags": list(self.tags),
        }


def demonstrate_custom_json():
    """Handle types that json doesn't support by default."""
    
    data = {
        "timestamp": datetime(2024, 6, 15, 10, 30, 0),
        "unique_ids": {1, 2, 3, 4, 5},
        "raw_data": b"\x48\x65\x6c\x6c\x6f",
    }
    
    # Encode with custom encoder
    json_str = json.dumps(data, cls=CustomEncoder, indent=2)
    print("Custom encoded:")
    print(json_str)
    
    # Decode with custom decoder
    restored = json.loads(json_str, object_hook=custom_decoder)
    print(f"\nRestored types:")
    print(f"  timestamp: {type(restored['timestamp']).__name__} = {restored['timestamp']}")
    print(f"  unique_ids: {type(restored['unique_ids']).__name__} = {restored['unique_ids']}")
    print(f"  raw_data: {type(restored['raw_data']).__name__} = {restored['raw_data']}")

    # Dataclass serialization
    print()
    user = UserProfile("alice", "alice@example.com", datetime.now(), {"admin", "editor"})
    user_json = json.dumps(user, cls=CustomEncoder, indent=2)
    print(f"UserProfile JSON:\n{user_json}")


# ============================================================
# 3. CSV READING AND WRITING
# ============================================================
def demonstrate_csv():
    """CSV: simple tabular data format."""
    
    # Writing CSV
    employees = [
        {"name": "Alice", "dept": "Engineering", "salary": 95000},
        {"name": "Bob", "dept": "Marketing", "salary": 78000},
        {"name": "Charlie", "dept": "Engineering", "salary": 102000},
        {"name": "Diana", "dept": "Design", "salary": 85000},
    ]
    
    output = io.StringIO()
    
    writer = csv.DictWriter(output, fieldnames=["name", "dept", "salary"])
    writer.writeheader()
    writer.writerows(employees)
    
    csv_content = output.getvalue()
    print("CSV output:")
    print(csv_content)
    
    # Reading CSV
    output.seek(0)
    reader = csv.DictReader(output)
    print("Parsed CSV:")
    for row in reader:
        print(f"  {row['name']:10} | {row['dept']:12} | ${int(row['salary']):>7,}")
    
    # CSV with custom delimiter
    print("\nTSV (tab-separated):")
    tsv_output = io.StringIO()
    writer = csv.writer(tsv_output, delimiter="\t")
    writer.writerow(["Name", "Score", "Grade"])
    writer.writerow(["Alice", 95, "A"])
    writer.writerow(["Bob", 82, "B"])
    print(tsv_output.getvalue())


# ============================================================
# 4. PICKLE (Python-Specific Serialization)
# ============================================================
class MLModel:
    """Simulated ML model that can be serialized with pickle."""
    
    def __init__(self, name: str):
        self.name = name
        self.weights = [0.1, 0.5, -0.3, 0.8]
        self.trained = False

    def train(self, data: list):
        self.weights = [w * 1.1 for w in self.weights]
        self.trained = True
        print(f"  Model '{self.name}' trained on {len(data)} samples")

    def predict(self, x: float) -> float:
        return sum(w * x for w in self.weights)

    def __repr__(self):
        return f"MLModel(name={self.name!r}, trained={self.trained}, weights={self.weights})"


def demonstrate_pickle():
    """Pickle serializes Python objects to bytes (including custom classes).
    
    WARNING: Never unpickle data from untrusted sources!
    Pickle can execute arbitrary code during deserialization.
    """
    
    # Create and train a model
    model = MLModel("neural_net_v1")
    model.train([1, 2, 3, 4, 5])
    print(f"Original: {model}")
    prediction = model.predict(2.5)
    print(f"Prediction: {prediction:.4f}")
    
    # Serialize (pickle)
    pickled = pickle.dumps(model)
    print(f"\nPickled size: {len(pickled)} bytes")
    
    # Deserialize (unpickle)
    restored_model = pickle.loads(pickled)
    print(f"Restored: {restored_model}")
    print(f"Prediction matches: {restored_model.predict(2.5) == prediction}")
    
    # Save to file
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
        pickle.dump(model, f)
        tmp_path = f.name
    
    # Load from file
    with open(tmp_path, "rb") as f:
        loaded_model = pickle.load(f)
    print(f"Loaded from file: {loaded_model}")
    
    os.unlink(tmp_path)


# ============================================================
# 5. STREAMING LARGE FILES
# ============================================================
def demonstrate_streaming():
    """Process large files line-by-line to save memory."""
    
    # Create a temporary file with simulated data
    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
        tmp_path = f.name
        for i in range(1000):
            level = ["INFO", "WARNING", "ERROR"][i % 3]
            f.write(f"2024-06-15 10:{i//60:02d}:{i%60:02d} [{level}] Message #{i+1}\n")
    
    # Stream and process line by line
    print("Streaming log file (showing first 5 ERROR lines):")
    error_count = 0
    total_lines = 0
    
    with open(tmp_path, "r") as f:
        for line in f:  # Iterates line by line (memory efficient)
            total_lines += 1
            if "[ERROR]" in line and error_count < 5:
                print(f"  {line.strip()}")
                error_count += 1
    
    print(f"\n  Total lines: {total_lines}")
    print(f"  Total errors: {sum(1 for line in open(tmp_path) if '[ERROR]' in line)}")
    
    os.unlink(tmp_path)


# ============================================================
# 6. PATHLIB - MODERN PATH OPERATIONS
# ============================================================
def demonstrate_pathlib():
    """pathlib provides an object-oriented approach to file paths."""
    
    # Current directory
    cwd = Path.cwd()
    print(f"Current directory: {cwd}")
    
    # Path construction (cross-platform!)
    config_path = Path.home() / ".config" / "myapp" / "settings.json"
    print(f"Config path: {config_path}")
    
    # Path components
    sample = Path("/home/user/documents/report.pdf")
    print(f"\nPath: {sample}")
    print(f"  Parent:    {sample.parent}")
    print(f"  Name:      {sample.name}")
    print(f"  Stem:      {sample.stem}")
    print(f"  Suffix:    {sample.suffix}")
    print(f"  Is absolute: {sample.is_absolute()}")
    
    # Path operations
    print("\nPath joining:")
    base = Path("project")
    paths = [
        base / "src" / "main.py",
        base / "tests" / "test_main.py",
        base / "README.md",
    ]
    for p in paths:
        print(f"  {p}")
    
    # Glob patterns
    workspace = Path(__file__).parent
    py_files = list(workspace.glob("*.py"))
    print(f"\nPython files in workspace: {len(py_files)}")
    for f in sorted(py_files)[:5]:
        print(f"  {f.name}")
    
    # File info
    if py_files:
        sample_file = py_files[0]
        stat = sample_file.stat()
        print(f"\nFile info for {sample_file.name}:")
        print(f"  Size: {stat.st_size:,} bytes")
        print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime)}")


# ============================================================
# 7. INI CONFIGURATION FILES
# ============================================================
import configparser


def demonstrate_configparser():
    """configparser reads and writes INI configuration files."""
    
    # Create a configuration
    config = configparser.ConfigParser()
    
    config["database"] = {
        "host": "localhost",
        "port": "5432",
        "name": "myapp_db",
        "user": "admin",
    }
    
    config["server"] = {
        "host": "0.0.0.0",
        "port": "8080",
        "debug": "false",
        "workers": "4",
    }
    
    config["logging"] = {
        "level": "INFO",
        "file": "/var/log/myapp.log",
        "max_size": "10MB",
    }
    
    # Write to string (for demo)
    output = io.StringIO()
    config.write(output)
    config_str = output.getvalue()
    print("Generated INI config:")
    print(config_str)
    
    # Read back
    config2 = configparser.ConfigParser()
    config2.read_string(config_str)
    
    print("Parsed values:")
    print(f"  Database host: {config2['database']['host']}")
    print(f"  Server port:   {config2.getint('server', 'port')}")
    print(f"  Debug mode:    {config2.getboolean('server', 'debug')}")
    print(f"  Log level:     {config2['logging']['level']}")


# ============================================================
# 8. BINARY FILE OPERATIONS
# ============================================================
def demonstrate_binary():
    """Read and write binary data."""
    
    # Create binary data
    header = b"MYFILE\x01\x00"  # Magic bytes + version
    payload = bytes(range(256))  # All byte values
    
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
        tmp_path = f.name
        f.write(header)
        f.write(len(payload).to_bytes(4, "big"))  # Length as 4-byte int
        f.write(payload)
    
    # Read binary data
    with open(tmp_path, "rb") as f:
        magic = f.read(6)
        version = int.from_bytes(f.read(2), "big")
        length = int.from_bytes(f.read(4), "big")
        data = f.read(length)
    
    print(f"Magic:   {magic}")
    print(f"Version: {version}")
    print(f"Length:  {length}")
    print(f"Data:    {data[:20]}... ({len(data)} bytes total)")
    
    os.unlink(tmp_path)


# ============================================================
# DEMO / MAIN
# ============================================================
def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    separator("1. JSON Serialization")
    demonstrate_json()

    separator("2. Custom JSON Encoder/Decoder")
    demonstrate_custom_json()

    separator("3. CSV Operations")
    demonstrate_csv()

    separator("4. Pickle Serialization")
    demonstrate_pickle()

    separator("5. Streaming Large Files")
    demonstrate_streaming()

    separator("6. Pathlib")
    demonstrate_pathlib()

    separator("7. INI Configuration")
    demonstrate_configparser()

    separator("8. Binary File Operations")
    demonstrate_binary()


if __name__ == "__main__":
    main()
