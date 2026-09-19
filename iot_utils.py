"""
IoT (Internet of Things) Utilities Module

This module provides comprehensive IoT utilities including:
- Device management and communication
- Sensor data processing
- MQTT client implementation
- Protocol conversion
- Device authentication
- Data aggregation and forwarding
- Edge computing utilities
- IoT device simulation
- Telemetry processing
- Fleet management

Note: This module uses paho-mqtt for MQTT communication.
Install with: pip install paho-mqtt

All functions include comprehensive docstrings and type hints.
"""

import json
import time
import threading
import queue
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import hashlib


try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False


class IoTProtocol(Enum):
    """Supported IoT protocols."""
    MQTT = "mqtt"
    HTTP = "http"
    COAP = "coap"
    WEBSOCKET = "websocket"
    AMQP = "amqp"


class DeviceStatus(Enum):
    """Device status types."""
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class SensorType(Enum):
    """Sensor types."""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    MOTION = "motion"
    LIGHT = "light"
    SOUND = "sound"
    CO2 = "co2"
    GPS = "gps"


@dataclass
class IoTDevice:
    """Represents an IoT device."""
    device_id: str
    device_type: str
    status: DeviceStatus
    last_seen: datetime
    capabilities: List[str]
    metadata: Dict[str, Any]
    sensors: List[str]


@dataclass
class SensorReading:
    """Container for sensor reading."""
    device_id: str
    sensor_type: SensorType
    value: Union[float, int, str, Dict]
    unit: str
    timestamp: datetime
    quality: float = 1.0


@dataclass
class TelemetryData:
    """Container for telemetry data."""
    device_id: str
    timestamp: datetime
    data: Dict[str, Any]
    location: Optional[Tuple[float, float]] = None
    battery_level: Optional[float] = None
    signal_strength: Optional[int] = None


class MQTTClient:
    """MQTT client for IoT communication."""
    
    def __init__(self, broker: str, port: int = 1883,
                 client_id: Optional[str] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        """Initialize MQTT client."""
        if not MQTT_AVAILABLE:
            raise ImportError("paho-mqtt library is required. Install with: pip install paho-mqtt")
        
        self.broker = broker
        self.port = port
        self.client_id = client_id or f"iot_client_{int(time.time())}"
        self.username = username
        self.password = password
        
        self.client = mqtt.Client(client_id=self.client_id)
        self.connected = False
        self.subscriptions: Dict[str, Callable] = {}
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
    
    def _on_connect(self, client, userdata, flags, rc):
        """Handle connection callback."""
        if rc == 0:
            self.connected = True
            print(f"Connected to MQTT broker")
        else:
            print(f"Connection failed with code {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnection callback."""
        self.connected = False
        print(f"Disconnected from MQTT broker")
    
    def _on_message(self, client, userdata, msg):
        """Handle incoming message."""
        topic = msg.topic
        payload = msg.payload.decode()
        
        if topic in self.subscriptions:
            try:
                self.subscriptions[topic](topic, payload)
            except Exception as e:
                print(f"Error in message handler: {e}")
    
    def connect(self) -> bool:
        """Connect to MQTT broker."""
        try:
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            
            # Wait for connection
            time.sleep(1)
            
            return self.connected
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish(self, topic: str, payload: Any, qos: int = 0, retain: bool = False) -> bool:
        """Publish message to MQTT topic."""
        if not self.connected:
            return False
        
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            elif not isinstance(payload, str):
                payload = str(payload)
            
            self.client.publish(topic, payload, qos=qos, retain=retain)
            return True
        except Exception as e:
            print(f"Publish error: {e}")
            return False
    
    def subscribe(self, topic: str, callback: Callable, qos: int = 0) -> bool:
        """Subscribe to MQTT topic."""
        if not self.connected:
            return False
        
        try:
            self.client.subscribe(topic, qos=qos)
            self.subscriptions[topic] = callback
            return True
        except Exception as e:
            print(f"Subscribe error: {e}")
            return False
    
    def unsubscribe(self, topic: str) -> bool:
        """Unsubscribe from MQTT topic."""
        if not self.connected:
            return False
        
        try:
            self.client.unsubscribe(topic)
            if topic in self.subscriptions:
                del self.subscriptions[topic]
            return True
        except Exception as e:
            print(f"Unsubscribe error: {e}")
            return False


class DeviceManager:
    """IoT device management."""
    
    def __init__(self):
        """Initialize device manager."""
        self.devices: Dict[str, IoTDevice] = {}
        self.device_groups: Dict[str, List[str]] = {}
    
    def register_device(self, device: IoTDevice) -> None:
        """Register a new IoT device."""
        self.devices[device.device_id] = device
        device.last_seen = datetime.now()
    
    def unregister_device(self, device_id: str) -> bool:
        """Unregister an IoT device."""
        if device_id in self.devices:
            del self.devices[device_id]
            return True
        return False
    
    def get_device(self, device_id: str) -> Optional[IoTDevice]:
        """Get device by ID."""
        return self.devices.get(device_id)
    
    def update_device_status(self, device_id: str, status: DeviceStatus) -> bool:
        """Update device status."""
        device = self.devices.get(device_id)
        if device:
            device.status = status
            device.last_seen = datetime.now()
            return True
        return False
    
    def get_devices_by_type(self, device_type: str) -> List[IoTDevice]:
        """Get all devices of a specific type."""
        return [device for device in self.devices.values() 
                if device.device_type == device_type]
    
    def get_devices_by_status(self, status: DeviceStatus) -> List[IoTDevice]:
        """Get all devices with specific status."""
        return [device for device in self.devices.values() 
                if device.status == status]
    
    def create_device_group(self, group_name: str, device_ids: List[str]) -> bool:
        """Create a device group."""
        valid_devices = [device_id for device_id in device_ids if device_id in self.devices]
        
        if valid_devices:
            self.device_groups[group_name] = valid_devices
            return True
        return False
    
    def get_device_group(self, group_name: str) -> List[IoTDevice]:
        """Get devices in a group."""
        device_ids = self.device_groups.get(group_name, [])
        return [self.devices[device_id] for device_id in device_ids if device_id in self.devices]
    
    def send_command(self, device_id: str, command: str, parameters: Dict = None) -> bool:
        """Send command to device."""
        device = self.devices.get(device_id)
        if not device:
            return False
        
        # In real implementation, this would send via MQTT or other protocol
        print(f"Command '{command}' sent to device {device_id}")
        print(f"Parameters: {parameters}")
        
        return True


class SensorProcessor:
    """Sensor data processing utilities."""
    
    @staticmethod
    def process_reading(reading: SensorReading) -> SensorReading:
        """Process and validate sensor reading."""
        # Validate value range based on sensor type
        if reading.sensor_type == SensorType.TEMPERATURE:
            if isinstance(reading.value, (int, float)):
                # Temperature should be reasonable (-50 to 100 Celsius)
                if reading.value < -50 or reading.value > 100:
                    reading.quality = 0.5  # Lower quality for out-of-range values
        
        elif reading.sensor_type == SensorType.HUMIDITY:
            if isinstance(reading.value, (int, float)):
                # Humidity should be 0-100%
                if reading.value < 0 or reading.value > 100:
                    reading.quality = 0.5
        
        elif reading.sensor_type == SensorType.PRESSURE:
            if isinstance(reading.value, (int, float)):
                # Pressure should be reasonable (800-1200 hPa)
                if reading.value < 800 or reading.value > 1200:
                    reading.quality = 0.5
        
        return reading
    
    @staticmethod
    def aggregate_readings(readings: List[SensorReading], 
                          aggregation: str = "average") -> float:
        """Aggregate multiple sensor readings."""
        if not readings:
            return 0.0
        
        values = [r.value for r in readings if isinstance(r.value, (int, float))]
        
        if not values:
            return 0.0
        
        if aggregation == "average":
            return sum(values) / len(values)
        elif aggregation == "sum":
            return sum(values)
        elif aggregation == "min":
            return min(values)
        elif aggregation == "max":
            return max(values)
        elif aggregation == "median":
            sorted_values = sorted(values)
            return sorted_values[len(sorted_values) // 2]
        else:
            return sum(values) / len(values)
    
    @staticmethod
    def detect_anomalies(readings: List[SensorReading],
                         threshold: float = 2.0) -> List[SensorReading]:
        """Detect anomalous readings using statistical methods."""
        if len(readings) < 3:
            return []
        
        values = [r.value for r in readings if isinstance(r.value, (int, float))]
        
        if not values:
            return []
        
        # Calculate mean and standard deviation
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std_dev = variance ** 0.5 if variance > 0 else 0
        
        # Find anomalies (values beyond threshold standard deviations)
        anomalies = []
        for reading in readings:
            if isinstance(reading.value, (int, float)):
                z_score = abs((reading.value - mean) / std_dev) if std_dev > 0 else 0
                if z_score > threshold:
                    anomalies.append(reading)
        
        return anomalies


class TelemetryProcessor:
    """Telemetry data processing."""
    
    @staticmethod
    def parse_telemetry(data: str) -> Optional[TelemetryData]:
        """Parse telemetry data from string."""
        try:
            parsed_data = json.loads(data)
            
            return TelemetryData(
                device_id=parsed_data.get("device_id", ""),
                timestamp=datetime.fromisoformat(parsed_data.get("timestamp", datetime.now().isoformat())),
                data=parsed_data.get("data", {}),
                location=tuple(parsed_data.get("location", [])) if "location" in parsed_data else None,
                battery_level=parsed_data.get("battery_level"),
                signal_strength=parsed_data.get("signal_strength")
            )
        except Exception as e:
            print(f"Error parsing telemetry: {e}")
            return None
    
    @staticmethod
    def format_telemetry(telemetry: TelemetryData) -> str:
        """Format telemetry data for transmission."""
        data = {
            "device_id": telemetry.device_id,
            "timestamp": telemetry.timestamp.isoformat(),
            "data": telemetry.data,
            "location": list(telemetry.location) if telemetry.location else None,
            "battery_level": telemetry.battery_level,
            "signal_strength": telemetry.signal_strength
        }
        
        return json.dumps(data)
    
    @staticmethod
    def aggregate_telemetry(telemetry_list: List[TelemetryData],
                               device_id: str) -> Dict[str, Any]:
        """Aggregate telemetry data for a device."""
        device_telemetry = [t for t in telemetry_list if t.device_id == device_id]
        
        if not device_telemetry:
            return {}
        
        # Calculate statistics
        battery_levels = [t.battery_level for t in device_telemetry if t.battery_level is not None]
        signal_strengths = [t.signal_strength for t in device_telemetry if t.signal_strength is not None]
        
        return {
            "device_id": device_id,
            "total_readings": len(device_telemetry),
            "first_reading": min(t.timestamp for t in device_telemetry),
            "last_reading": max(t.timestamp for t in device_telemetry),
            "average_battery": sum(battery_levels) / len(battery_levels) if battery_levels else None,
            "average_signal": sum(signal_strengths) / len(signal_strengths) if signal_strengths else None,
            "data_points": sum(len(t.data) for t in device_telemetry)
        }


class ProtocolConverter:
    """Protocol conversion utilities."""
    
    @staticmethod
    def mqtt_to_http(mqtt_topic: str, mqtt_payload: str) -> Tuple[str, Dict]:
        """Convert MQTT message to HTTP request."""
        # Parse MQTT topic to HTTP endpoint
        parts = mqtt_topic.split('/')
        endpoint = "/" + "/".join(parts[1:])  # Skip first part (usually device ID)
        
        # Parse payload
        try:
            data = json.loads(mqtt_payload)
        except:
            data = {"value": mqtt_payload}
        
        return endpoint, data
    
    @staticmethod
    def http_to_mqtt(endpoint: str, data: Dict) -> Tuple[str, str]:
        """Convert HTTP request to MQTT message."""
        # Convert HTTP endpoint to MQTT topic
        parts = endpoint.strip('/').split('/')
        topic = "/".join(parts)
        
        # Convert data to JSON payload
        payload = json.dumps(data)
        
        return topic, payload
    
    @staticmethod
    def convert_units(value: float, from_unit: str, to_unit: str) -> float:
        """Convert units for sensor data."""
        conversions = {
            ("celsius", "fahrenheit"): lambda v: (v * 9/5) + 32,
            ("fahrenheit", "celsius"): lambda v: (v - 32) * 5/9,
            ("celsius", "kelvin"): lambda v: v + 273.15,
            ("kelvin", "celsius"): lambda v: v - 273.15,
            ("hpa", "atm"): lambda v: v / 1013.25,
            ("atm", "hpa"): lambda v: v * 1013.25,
            ("meters", "feet"): lambda v: v * 3.28084,
            ("feet", "meters"): lambda v: v / 3.28084
        }
        
        conversion = conversions.get((from_unit, to_unit))
        if conversion:
            return conversion(value)
        
        return value


class DeviceSimulator:
    """IoT device simulation for testing."""
    
    def __init__(self, device_id: str, device_type: str):
        """Initialize device simulator."""
        self.device_id = device_id
        self.device_type = device_type
        self.running = False
        self.sensors: Dict[str, Any] = {}
        self.metrics: Dict[str, float] = {}
    
    def add_sensor(self, sensor_type: SensorType, 
                   initial_value: Union[float, int] = 0,
                   unit: str = "") -> None:
        """Add a sensor to the device."""
        self.sensors[sensor_type.value] = {
            "value": initial_value,
            "unit": unit,
            "timestamp": datetime.now()
        }
    
    def generate_reading(self, sensor_type: SensorType) -> SensorReading:
        """Generate a sensor reading."""
        import random
        
        sensor_data = self.sensors.get(sensor_type.value)
        if not sensor_data:
            raise ValueError(f"Sensor {sensor_type} not found")
        
        # Simulate sensor variation
        base_value = sensor_data["value"]
        if isinstance(base_value, (int, float)):
            variation = random.uniform(-0.1, 0.1) * base_value
            value = base_value + variation
        else:
            value = base_value
        
        return SensorReading(
            device_id=self.device_id,
            sensor_type=sensor_type,
            value=value,
            unit=sensor_data["unit"],
            timestamp=datetime.now()
        )
    
    def simulate(self, duration: float, interval: float = 1.0) -> List[SensorReading]:
        """Simulate device operation for specified duration."""
        readings = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for sensor_type in self.sensors.keys():
                reading = self.generate_reading(SensorType(sensor_type))
                readings.append(reading)
            
            time.sleep(interval)
        
        return readings


class DataAggregator:
    """IoT data aggregation and forwarding."""
    
    def __init__(self):
        """Initialize data aggregator."""
        self.data_buffer: Dict[str, List[TelemetryData]] = {}
        self.aggregation_rules: Dict[str, Dict] = {}
    
    def add_data(self, telemetry: TelemetryData) -> None:
        """Add telemetry data to buffer."""
        device_id = telemetry.device_id
        
        if device_id not in self.data_buffer:
            self.data_buffer[device_id] = []
        
        self.data_buffer[device_id].append(telemetry)
        
        # Keep buffer size manageable
        if len(self.data_buffer[device_id]) > 1000:
            self.data_buffer[device_id] = self.data_buffer[device_id][-1000:]
    
    def aggregate_device_data(self, device_id: str) -> Dict[str, Any]:
        """Aggregate data for a specific device."""
        if device_id not in self.data_buffer:
            return {}
        
        return TelemetryProcessor.aggregate_telemetry(
            self.data_buffer[device_id], device_id
        )
    
    def aggregate_all_devices(self) -> Dict[str, Dict[str, Any]]:
        """Aggregate data for all devices."""
        results = {}
        
        for device_id in self.data_buffer:
            results[device_id] = self.aggregate_device_data(device_id)
        
        return results
    
    def set_aggregation_rule(self, device_id: str, rule: Dict) -> None:
        """Set aggregation rule for a device."""
        self.aggregation_rules[device_id] = rule
    
    def apply_aggregation_rules(self) -> Dict[str, Any]:
        """Apply aggregation rules to buffered data."""
        results = {}
        
        for device_id, rule in self.aggregation_rules.items():
            device_data = self.data_buffer.get(device_id, [])
            
            if device_data:
                # Apply rule-based aggregation
                if rule.get("function") == "average":
                    values = [d.data.get(rule.get("field", "value"), 0) for d in device_data]
                    results[device_id] = {
                        "aggregation": "average",
                        "value": sum(values) / len(values) if values else 0
                    }
                elif rule.get("function") == "count":
                    results[device_id] = {
                        "aggregation": "count",
                        "value": len(device_data)
                    }
        
        return results


class EdgeComputing:
    """Edge computing utilities for IoT."""
    
    @staticmethod
    def process_locally(data: List[TelemetryData], 
                        processing_function: Callable) -> Any:
        """Process data locally at the edge."""
        return processing_function(data)
    
    @staticmethod
    def filter_data(data: List[TelemetryData], 
                     filter_function: Callable) -> List[TelemetryData]:
        """Filter data based on criteria."""
        return [d for d in data if filter_function(d)]
    
    @staticmethod
    def compress_data(data: List[TelemetryData]) -> Dict:
        """Compress data for transmission."""
        # Simple compression: aggregate by device
        compressed = {}
        
        for telemetry in data:
            device_id = telemetry.device_id
            
            if device_id not in compressed:
                compressed[device_id] = {
                    "count": 0,
                    "latest": None,
                    "battery_levels": [],
                    "signal_strengths": []
                }
            
            compressed[device_id]["count"] += 1
            compressed[device_id]["latest"] = telemetry.timestamp.isoformat()
            
            if telemetry.battery_level is not None:
                compressed[device_id]["battery_levels"].append(telemetry.battery_level)
            
            if telemetry.signal_strength is not None:
                compressed[device_id]["signal_strengths"].append(telemetry.signal_strength)
        
        return compressed
    
    @staticmethod
    def decide_transmission(data: List[TelemetryData],
                           bandwidth_limit: int) -> Tuple[List[TelemetryData], List[TelemetryData]]:
        """Decide which data to transmit based on bandwidth."""
        # Prioritize critical data
        prioritized = []
        deferred = []
        
        for telemetry in data:
            # Simple priority: recent data and low battery warnings
            is_critical = (
                telemetry.battery_level is not None and telemetry.battery_level < 20 or
                (datetime.now() - telemetry.timestamp).total_seconds() < 3600  # Last hour
            )
            
            if is_critical:
                prioritized.append(telemetry)
            else:
                deferred.append(telemetry)
        
        # Apply bandwidth limit
        return prioritized[:bandwidth_limit], deferred


class FleetManager:
    """IoT fleet management."""
    
    def __init__(self):
        """Initialize fleet manager."""
        self.fleets: Dict[str, List[str]] = {}
        self.device_manager = DeviceManager()
    
    def create_fleet(self, fleet_name: str, device_ids: List[str]) -> bool:
        """Create a device fleet."""
        valid_devices = [device_id for device_id in device_ids 
                       if device_id in self.device_manager.devices]
        
        if valid_devices:
            self.fleets[fleet_name] = valid_devices
            return True
        return False
    
    def get_fleet_status(self, fleet_name: str) -> Dict[str, Any]:
        """Get fleet status information."""
        if fleet_name not in self.fleets:
            return {}
        
        device_ids = self.fleets[fleet_name]
        devices = [self.device_manager.devices[device_id] for device_id in device_ids 
                   if device_id in self.device_manager.devices]
        
        online = sum(1 for d in devices if d.status == DeviceStatus.ONLINE)
        offline = sum(1 for d in devices if d.status == DeviceStatus.OFFLINE)
        error = sum(1 for d in devices if d.status == DeviceStatus.ERROR)
        
        return {
            "fleet_name": fleet_name,
            "total_devices": len(devices),
            "online": online,
            "offline": offline,
            "error": error,
            "device_types": {}
        }
    
    def fleet_command(self, fleet_name: str, command: str, parameters: Dict = None) -> Dict[str, bool]:
        """Send command to all devices in fleet."""
        if fleet_name not in self.fleets:
            return {}
        
        results = {}
        for device_id in self.fleets[fleet_name]:
            results[device_id] = self.device_manager.send_command(device_id, command, parameters)
        
        return results


def demonstrate_iot_utils():
    """Demonstrate IoT utilities functionality."""
    print("=== IoT Utilities Demonstration ===\n")
    
    # Device Management
    print("1. Device Management:")
    device_manager = DeviceManager()
    
    device = IoTDevice(
        device_id="sensor_001",
        device_type="temperature_sensor",
        status=DeviceStatus.ONLINE,
        last_seen=datetime.now(),
        capabilities=["temperature", "humidity"],
        metadata={"location": "Building A", "floor": 1},
        sensors=["temperature", "humidity"]
    )
    
    device_manager.register_device(device)
    print(f"   Registered device: {device.device_id}")
    print(f"   Device status: {device.status.value}")
    
    # Sensor Processing
    print("\n2. Sensor Processing:")
    reading = SensorReading(
        device_id="sensor_001",
        sensor_type=SensorType.TEMPERATURE,
        value=25.5,
        unit="C",
        timestamp=datetime.now()
    )
    
    processed = SensorProcessor.process_reading(reading)
    print(f"   Processed reading quality: {processed.quality}")
    
    readings = [
        SensorReading("sensor_001", SensorType.TEMPERATURE, 20.0, "C", datetime.now()),
        SensorReading("sensor_001", SensorType.TEMPERATURE, 22.0, "C", datetime.now()),
        SensorReading("sensor_001", SensorType.TEMPERATURE, 21.0, "C", datetime.now()),
        SensorReading("sensor_001", SensorType.TEMPERATURE, 50.0, "C", datetime.now())  # Anomaly
    ]
    
    average = SensorProcessor.aggregate_readings(readings, "average")
    print(f"   Average temperature: {average}")
    
    anomalies = SensorProcessor.detect_anomalies(readings)
    print(f"   Anomalies detected: {len(anomalies)}")
    
    # MQTT Client
    print("\n3. MQTT Client:")
    if MQTT_AVAILABLE:
        print("   MQTT client available")
        print("   - Connect to broker")
        print("   - Publish/subscribe to topics")
        print("   - QoS levels and retained messages")
    else:
        print("   Install paho-mqtt: pip install paho-mqtt")
    
    # Telemetry Processing
    print("\n4. Telemetry Processing:")
    telemetry_data = {
        "device_id": "sensor_001",
        "timestamp": datetime.now().isoformat(),
        "data": {"temperature": 25.5, "humidity": 60.0},
        "battery_level": 85.0,
        "signal_strength": -45
    }
    
    telemetry = TelemetryProcessor.parse_telemetry(json.dumps(telemetry_data))
    print(f"   Parsed telemetry device: {telemetry.device_id if telemetry else 'None'}")
    
    if telemetry:
        formatted = TelemetryProcessor.format_telemetry(telemetry)
        print(f"   Formatted telemetry length: {len(formatted)}")
    
    # Device Simulation
    print("\n5. Device Simulation:")
    simulator = DeviceSimulator("sim_device_001", "weather_station")
    simulator.add_sensor(SensorType.TEMPERATURE, 25.0, "C")
    simulator.add_sensor(SensorType.HUMIDITY, 60.0, "%")
    
    print(f"   Simulated device: {simulator.device_id}")
    print(f"   Sensors: {list(simulator.sensors.keys())}")
    
    reading = simulator.generate_reading(SensorType.TEMPERATURE)
    print(f"   Generated reading: {reading.value} {reading.unit}")
    
    # Protocol Conversion
    print("\n6. Protocol Conversion:")
    converter = ProtocolConverter()
    
    temp_f = converter.convert_units(25.0, "celsius", "fahrenheit")
    print(f"   25°C = {temp_f}°F")
    
    temp_k = converter.convert_units(25.0, "celsius", "kelvin")
    print(f"   25°C = {temp_k}K")
    
    # Data Aggregation
    print("\n7. Data Aggregation:")
    aggregator = DataAggregator()
    
    for i in range(5):
        telemetry = TelemetryData(
            device_id="sensor_001",
            timestamp=datetime.now(),
            data={"temperature": 20.0 + i, "humidity": 60.0 - i},
            battery_level=80.0 - i * 2,
            signal_strength=-50 - i
        )
        aggregator.add_data(telemetry)
    
    aggregated = aggregator.aggregate_device_data("sensor_001")
    print(f"   Total readings: {aggregated.get('total_readings')}")
    print(f"   Average battery: {aggregated.get('average_battery')}")
    
    # Edge Computing
    print("\n8. Edge Computing:")
    print("   Edge computing capabilities:")
    print("   - Local data processing")
    print("   - Data filtering and compression")
    print("   - Bandwidth-aware transmission")
    print("   - Real-time analytics")
    
    # Fleet Management
    print("\n9. Fleet Management:")
    fleet_manager = FleetManager()
    
    # Register more devices
    device2 = IoTDevice(
        device_id="sensor_002",
        device_type="humidity_sensor",
        status=DeviceStatus.ONLINE,
        last_seen=datetime.now(),
        capabilities=["humidity"],
        metadata={"location": "Building A", "floor": 2},
        sensors=["humidity"]
    )
    
    device_manager.register_device(device2)
    fleet_manager.device_manager = device_manager
    
    fleet_manager.create_fleet("building_a_sensors", ["sensor_001", "sensor_002"])
    fleet_status = fleet_manager.get_fleet_status("building_a_sensors")
    print(f"   Fleet status: {fleet_status}")
    
    print("\n=== Demonstration Complete ===")
    print("\nIoT Best Practices:")
    print("- Use secure communication protocols (MQTT over TLS)")
    print("- Implement proper device authentication")
    print("- Process data at the edge when possible")
    print("- Monitor device health and battery levels")
    print("- Use data aggregation to reduce bandwidth")
    print("- Implement proper error handling and retry logic")
    print("- Consider device constraints (memory, processing power)")
    print("- Use appropriate data rates and quality settings")


if __name__ == "__main__":
    demonstrate_iot_utils()