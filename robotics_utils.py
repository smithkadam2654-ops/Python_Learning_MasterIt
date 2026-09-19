"""
Robotics Utilities Module

This module provides comprehensive robotics utilities including:
- Robot kinematics
- Path planning and navigation
- Sensor data processing
- Motor control
- Robot state estimation
- Coordinate transformations
- PID controllers
- Robot simulation
- Vision processing for robotics
- Communication protocols

All functions include comprehensive docstrings and type hints.
"""

import math
import time
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from collections import deque


class RobotType(Enum):
    """Types of robots."""
    MOBILE = "mobile"
    MANIPULATOR = "manipulator"
    DRONE = "drone"
    HUMANOID = "humanoid"
    VEHICLE = "vehicle"


class MovementType(Enum):
    """Movement types."""
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    STOP = "stop"


class SensorType(Enum):
    """Sensor types."""
    LIDAR = "lidar"
    CAMERA = "camera"
    ULTRASONIC = "ultrasonic"
    INFRARED = "infrared"
    GYROSCOPE = "gyroscope"
    ACCELEROMETER = "accelerometer"
    COMPASS = "compass"
    GPS = "gps"


@dataclass
class Pose:
    """Robot pose (position and orientation)."""
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    
    def position(self) -> Tuple[float, float, float]:
        """Get position vector."""
        return (self.x, self.y, self.z)
    
    def orientation(self) -> Tuple[float, float, float]:
        """Get orientation angles."""
        return (self.roll, self.pitch, self.yaw)
    
    def distance_to(self, other: 'Pose') -> float:
        """Calculate Euclidean distance to another pose."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx**2 + dy**2 + dz**2)


@dataclass
class Velocity:
    """Robot velocity (linear and angular)."""
    linear_x: float
    linear_y: float
    linear_z: float
    angular_x: float
    angular_y: float
    angular_z: float
    
    def linear_magnitude(self) -> float:
        """Calculate linear velocity magnitude."""
        return math.sqrt(self.linear_x**2 + self.linear_y**2 + self.linear_z**2)
    
    def angular_magnitude(self) -> float:
        """Calculate angular velocity magnitude."""
        return math.sqrt(self.angular_x**2 + self.angular_y**2 + self.angular_z**2)


@dataclass
class SensorReading:
    """Sensor reading data."""
    sensor_type: SensorType
    value: Union[float, int, List, Dict]
    timestamp: float
    unit: str = ""
    accuracy: float = 1.0


class RobotKinematics:
    """Robot kinematics calculations."""
    
    @staticmethod
    def forward_kinematics(joint_angles: List[float],
                          link_lengths: List[float]) -> Pose:
        """Calculate end-effector pose from joint angles (2D planar)."""
        x = 0.0
        y = 0.0
        angle = 0.0
        
        for i, (joint_angle, link_length) in enumerate(zip(joint_angles, link_lengths)):
            angle += joint_angle
            x += link_length * math.cos(angle)
            y += link_length * math.sin(angle)
        
        return Pose(x=x, y=y, z=0, roll=0, pitch=0, yaw=angle)
    
    @staticmethod
    def inverse_kinematics(target: Pose, link_lengths: List[float]) -> List[float]:
        """Calculate joint angles for target pose (2D planar, simplified)."""
        # Simplified 2-link IK
        if len(link_lengths) != 2:
            return [0.0] * len(link_lengths)
        
        l1, l2 = link_lengths
        target_x, target_y = target.x, target.y
        
        # Distance to target
        distance = math.sqrt(target_x**2 + target_y**2)
        
        # Check if target is reachable
        if distance > l1 + l2:
            return [0.0, 0.0]
        
        # Calculate joint angles using law of cosines
        cos_angle2 = (distance**2 - l1**2 - l2**2) / (2 * l1 * l2)
        cos_angle2 = max(-1.0, min(1.0, cos_angle2))  # Clamp to valid range
        angle2 = math.acos(cos_angle2)
        
        cos_angle1 = (l1**2 + distance**2 - l2**2) / (2 * l1 * distance)
        cos_angle1 = max(-1.0, min(1.0, cos_angle1))
        angle1 = math.acos(cos_angle1) + math.atan2(target_y, target_x)
        
        return [angle1, angle2]
    
    @staticmethod
    def differential_drive_kinematics(v_left: float, v_right: float,
                                    wheel_base: float) -> Velocity:
        """Calculate robot velocity from wheel speeds (differential drive)."""
        linear = (v_left + v_right) / 2.0
        angular = (v_right - v_left) / wheel_base
        
        return Velocity(
            linear_x=linear,
            linear_y=0.0,
            linear_z=0.0,
            angular_x=0.0,
            angular_y=0.0,
            angular_z=angular
        )
    
    @staticmethod
    def inverse_differential_drive(linear: float, angular: float,
                                 wheel_base: float) -> Tuple[float, float]:
        """Calculate wheel speeds from robot velocity."""
        v_left = linear - (angular * wheel_base) / 2.0
        v_right = linear + (angular * wheel_base) / 2.0
        
        return v_left, v_right


class PathPlanner:
    """Path planning and navigation."""
    
    @staticmethod
    def plan_path_a_star(start: Tuple[float, float],
                        goal: Tuple[float, float],
                        obstacles: List[Tuple[float, float, float]],
                        grid_size: float = 1.0) -> List[Tuple[float, float]]:
        """Plan path using A* algorithm with obstacles."""
        # Create grid
        grid = PathPlanner._create_grid(obstacles, grid_size)
        
        # Convert to grid coordinates
        start_grid = (int(start[0] / grid_size), int(start[1] / grid_size))
        goal_grid = (int(goal[0] / grid_size), int(goal[1] / grid_size))
        
        # A* algorithm
        open_set = [(0, start_grid)]
        came_from = {}
        g_score = {start_grid: 0}
        f_score = {start_grid: PathPlanner._heuristic(start_grid, goal_grid)}
        
        while open_set:
            current = min(open_set, key=lambda x: x[0])[1]
            open_set = [item for item in open_set if item[1] != current]
            
            if current == goal_grid:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append((current[0] * grid_size, current[1] * grid_size))
                    current = came_from[current]
                path.reverse()
                return path
            
            # Check neighbors
            for neighbor in PathPlanner._get_neighbors(current, grid):
                if neighbor in grid:  # If obstacle
                    continue
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + PathPlanner._heuristic(neighbor, goal_grid)
                    open_set.append((f_score[neighbor], neighbor))
        
        return []
    
    @staticmethod
    def _create_grid(obstacles: List[Tuple[float, float, float]],
                    grid_size: float) -> set:
        """Create obstacle grid."""
        grid = set()
        for ox, oy, radius in obstacles:
            # Add obstacle cells
            cells_x = int(radius / grid_size) + 1
            cells_y = int(radius / grid_size) + 1
            
            for dx in range(-cells_x, cells_x + 1):
                for dy in range(-cells_y, cells_y + 1):
                    if dx**2 + dy**2 <= (radius / grid_size)**2:
                        grid_x = int((ox + dx * grid_size) / grid_size)
                        grid_y = int((oy + dy * grid_size) / grid_size)
                        grid.add((grid_x, grid_y))
        
        return grid
    
    @staticmethod
    def _heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Heuristic function for A*."""
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    @staticmethod
    def _get_neighbors(pos: Tuple[int, int], grid: set) -> List[Tuple[int, int]]:
        """Get valid neighboring positions."""
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            neighbor = (pos[0] + dx, pos[1] + dy)
            if neighbor not in grid:
                neighbors.append(neighbor)
        
        return neighbors
    
    @staticmethod
    def smooth_path(path: List[Tuple[float, float]],
                   smoothing_factor: float = 0.5) -> List[Tuple[float, float]]:
        """Smooth path using moving average."""
        if len(path) < 3:
            return path
        
        smoothed = [path[0]]
        
        for i in range(1, len(path) - 1):
            # Weighted average of neighbors
            prev_x, prev_y = path[i - 1]
            curr_x, curr_y = path[i]
            next_x, next_y = path[i + 1]
            
            smoothed_x = (1 - smoothing_factor) * curr_x + smoothing_factor * (prev_x + next_x) / 2
            smoothed_y = (1 - smoothing_factor) * curr_y + smoothing_factor * (prev_y + next_y) / 2
            
            smoothed.append((smoothed_x, smoothed_y))
        
        smoothed.append(path[-1])
        return smoothed


class PIDController:
    """PID controller for robot control."""
    
    def __init__(self, kp: float, ki: float, kd: float,
                 setpoint: float = 0.0):
        """Initialize PID controller."""
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint
        
        self.integral = 0.0
        self.previous_error = 0.0
        self.dt = 0.1  # Default time step
    
    def compute(self, measurement: float, dt: Optional[float] = None) -> float:
        """Compute PID control output."""
        if dt is not None:
            self.dt = dt
        
        error = self.setpoint - measurement
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / self.dt
        d_term = self.kd * derivative
        
        # Update previous error
        self.previous_error = error
        
        # Calculate output
        output = p_term + i_term + d_term
        
        return output
    
    def set_setpoint(self, setpoint: float) -> None:
        """Set target setpoint."""
        self.setpoint = setpoint
        self.integral = 0.0
        self.previous_error = 0.0
    
    def reset(self) -> None:
        """Reset controller state."""
        self.integral = 0.0
        self.previous_error = 0.0


class RobotState:
    """Robot state estimation."""
    
    def __init__(self):
        """Initialize robot state."""
        self.pose = Pose(0, 0, 0, 0, 0, 0)
        self.velocity = Velocity(0, 0, 0, 0, 0, 0)
        self.battery_level = 100.0
        self.motor_temperatures: Dict[str, float] = {}
        self.last_update = time.time()
    
    def update_pose(self, new_pose: Pose) -> None:
        """Update robot pose."""
        self.pose = new_pose
        self.last_update = time.time()
    
    def update_velocity(self, new_velocity: Velocity) -> None:
        """Update robot velocity."""
        self.velocity = new_velocity
        self.last_update = time.time()
    
    def update_battery(self, level: float) -> None:
        """Update battery level."""
        self.battery_level = max(0.0, min(100.0, level))
    
    def get_battery_status(self) -> str:
        """Get battery status."""
        if self.battery_level > 75:
            return "good"
        elif self.battery_level > 25:
            return "medium"
        else:
            return "low"
    
    def is_stale(self, timeout: float = 5.0) -> bool:
        """Check if state is stale (not updated recently)."""
        return (time.time() - self.last_update) > timeout


class CoordinateTransform:
    """Coordinate transformation utilities."""
    
    @staticmethod
    def rotate_point(point: Tuple[float, float],
                    angle: float,
                    center: Tuple[float, float] = (0, 0)) -> Tuple[float, float]:
        """Rotate point around center by angle (radians)."""
        x, y = point
        cx, cy = center
        
        # Translate to origin
        x -= cx
        y -= cy
        
        # Rotate
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        # Translate back
        new_x += cx
        new_y += cy
        
        return (new_x, new_y)
    
    @staticmethod
    def transform_point(point: Tuple[float, float],
                       translation: Tuple[float, float],
                       rotation: float = 0.0) -> Tuple[float, float]:
        """Transform point with translation and rotation."""
        # First rotate
        rotated = CoordinateTransform.rotate_point(point, rotation)
        
        # Then translate
        transformed = (rotated[0] + translation[0], rotated[1] + translation[1])
        
        return transformed
    
    @staticmethod
    def polar_to_cartesian(r: float, theta: float) -> Tuple[float, float]:
        """Convert polar coordinates to Cartesian."""
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return (x, y)
    
    @staticmethod
    def cartesian_to_polar(x: float, y: float) -> Tuple[float, float]:
        """Convert Cartesian coordinates to polar."""
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        return (r, theta)


class MotorController:
    """Motor control utilities."""
    
    def __init__(self, num_motors: int):
        """Initialize motor controller."""
        self.num_motors = num_motors
        self.motor_speeds: List[float] = [0.0] * num_motors
        self.motor_directions: List[int] = [1] * num_motors
        self.pid_controllers: List[PIDController] = []
    
    def add_pid_controller(self, motor_index: int, pid: PIDController) -> None:
        """Add PID controller to motor."""
        if 0 <= motor_index < self.num_motors:
            while len(self.pid_controllers) <= motor_index:
                self.pid_controllers.append(None)
            self.pid_controllers[motor_index] = pid
    
    def set_motor_speed(self, motor_index: int, speed: float) -> bool:
        """Set motor speed (-1.0 to 1.0)."""
        if 0 <= motor_index < self.num_motors:
            speed = max(-1.0, min(1.0, speed))
            self.motor_speeds[motor_index] = speed
            return True
        return False
    
    def get_motor_speed(self, motor_index: int) -> float:
        """Get motor speed."""
        if 0 <= motor_index < self.num_motors:
            return self.motor_speeds[motor_index]
        return 0.0
    
    def stop_all_motors(self) -> None:
        """Stop all motors."""
        self.motor_speeds = [0.0] * self.num_motors
    
    def emergency_stop(self) -> None:
        """Emergency stop - cut power to all motors."""
        self.stop_all_motors()
        # In real implementation, this would cut power immediately


class SensorProcessor:
    """Sensor data processing."""
    
    @staticmethod
    def filter_readings(readings: List[SensorReading],
                       window_size: int = 5) -> List[SensorReading]:
        """Apply moving average filter to sensor readings."""
        if len(readings) < window_size:
            return readings
        
        filtered = []
        
        for i in range(len(readings)):
            start = max(0, i - window_size // 2)
            end = min(len(readings), i + window_size // 2 + 1)
            window = readings[start:end]
            
            if window and isinstance(window[0].value, (int, float)):
                avg_value = sum(r.value for r in window) / len(window)
                filtered_reading = SensorReading(
                    sensor_type=window[0].sensor_type,
                    value=avg_value,
                    timestamp=window[0].timestamp,
                    unit=window[0].unit,
                    accuracy=window[0].accuracy
                )
                filtered.append(filtered_reading)
            else:
                filtered.append(readings[i])
        
        return filtered
    
    @staticmethod
    def detect_anomalies(readings: List[SensorReading],
                        threshold: float = 2.0) -> List[SensorReading]:
        """Detect anomalous sensor readings."""
        if len(readings) < 3:
            return []
        
        values = [r.value for r in readings if isinstance(r.value, (int, float))]
        
        if not values:
            return []
        
        # Calculate mean and standard deviation
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std_dev = math.sqrt(variance) if variance > 0 else 0
        
        # Find anomalies
        anomalies = []
        for reading in readings:
            if isinstance(reading.value, (int, float)):
                z_score = abs((reading.value - mean) / std_dev) if std_dev > 0 else 0
                if z_score > threshold:
                    anomalies.append(reading)
        
        return anomalies
    
    @staticmethod
    def calibrate_sensor(readings: List[SensorReading],
                        reference_value: float) -> float:
        """Calculate calibration offset."""
        if not readings:
            return 0.0
        
        values = [r.value for r in readings if isinstance(r.value, (int, float))]
        
        if not values:
            return 0.0
        
        mean_value = sum(values) / len(values)
        offset = reference_value - mean_value
        
        return offset


class RobotSimulator:
    """Simple robot simulator for testing."""
    
    def __init__(self, robot_type: RobotType = RobotType.MOBILE):
        """Initialize robot simulator."""
        self.robot_type = robot_type
        self.state = RobotState()
        self.world_size = (100.0, 100.0)
        self.obstacles: List[Tuple[float, float, float]] = []
    
    def add_obstacle(self, x: float, y: float, radius: float) -> None:
        """Add circular obstacle to world."""
        self.obstacles.append((x, y, radius))
    
    def update(self, delta_time: float) -> None:
        """Update robot simulation."""
        # Update position based on velocity
        self.state.pose.x += self.state.velocity.linear_x * delta_time
        self.state.pose.y += self.state.velocity.linear_y * delta_time
        self.state.pose.yaw += self.state.velocity.angular_z * delta_time
        
        # Keep within world bounds
        self.state.pose.x = max(0, min(self.world_size[0], self.state.pose.x))
        self.state.pose.y = max(0, min(self.world_size[1], self.state.pose.y))
        
        # Update battery
        speed = self.state.velocity.linear_magnitude()
        self.state.battery_level -= speed * delta_time * 0.01
        self.state.battery_level = max(0.0, self.state.battery_level)
    
    def get_distance_to_obstacle(self) -> float:
        """Get distance to nearest obstacle."""
        min_distance = float('inf')
        
        for ox, oy, radius in self.obstacles:
            distance = math.sqrt((self.state.pose.x - ox)**2 + (self.state.pose.y - oy)**2)
            distance -= radius
            min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else float('inf')
    
    def set_velocity(self, linear: float, angular: float) -> None:
        """Set robot velocity."""
        self.state.velocity.linear_x = linear
        self.state.velocity.angular_z = angular


class RobotCommunication:
    """Robot communication protocols."""
    
    @staticmethod
    def encode_command(command: str, parameters: Dict = None) -> str:
        """Encode robot command for transmission."""
        message = {
            "command": command,
            "parameters": parameters or {},
            "timestamp": time.time()
        }
        
        return json.dumps(message)
    
    @staticmethod
    def decode_command(message: str) -> Optional[Dict]:
        """Decode robot command from transmission."""
        try:
            return json.loads(message)
        except:
            return None
    
    @staticmethod
    def encode_telemetry(state: RobotState) -> str:
        """Encode robot telemetry for transmission."""
        telemetry = {
            "pose": {
                "x": state.pose.x,
                "y": state.pose.y,
                "z": state.pose.z,
                "roll": state.pose.roll,
                "pitch": state.pose.pitch,
                "yaw": state.pose.yaw
            },
            "velocity": {
                "linear_x": state.velocity.linear_x,
                "linear_y": state.velocity.linear_y,
                "linear_z": state.velocity.linear_z,
                "angular_x": state.velocity.angular_x,
                "angular_y": state.velocity.angular_y,
                "angular_z": state.velocity.angular_z
            },
            "battery": state.battery_level,
            "timestamp": state.last_update
        }
        
        return json.dumps(telemetry)
    
    @staticmethod
    def decode_telemetry(message: str) -> Optional[RobotState]:
        """Decode robot telemetry from transmission."""
        try:
            data = json.loads(message)
            
            state = RobotState()
            state.pose = Pose(
                x=data["pose"]["x"],
                y=data["pose"]["y"],
                z=data["pose"]["z"],
                roll=data["pose"]["roll"],
                pitch=data["pose"]["pitch"],
                yaw=data["pose"]["yaw"]
            )
            state.velocity = Velocity(
                linear_x=data["velocity"]["linear_x"],
                linear_y=data["velocity"]["linear_y"],
                linear_z=data["velocity"]["linear_z"],
                angular_x=data["velocity"]["angular_x"],
                angular_y=data["velocity"]["angular_y"],
                angular_z=data["velocity"]["angular_z"]
            )
            state.battery_level = data["battery"]
            state.last_update = data["timestamp"]
            
            return state
        except:
            return None


class RobotFleet:
    """Fleet management for multiple robots."""
    
    def __init__(self):
        """Initialize robot fleet."""
        self.robots: Dict[str, RobotState] = {}
        self.fleet_formation: str = "free"
    
    def add_robot(self, robot_id: str, robot_state: RobotState) -> None:
        """Add robot to fleet."""
        self.robots[robot_id] = robot_state
    
    def remove_robot(self, robot_id: str) -> bool:
        """Remove robot from fleet."""
        if robot_id in self.robots:
            del self.robots[robot_id]
            return True
        return False
    
    def get_robot_state(self, robot_id: str) -> Optional[RobotState]:
        """Get state of specific robot."""
        return self.robots.get(robot_id)
    
    def get_fleet_center(self) -> Optional[Tuple[float, float]]:
        """Calculate fleet center position."""
        if not self.robots:
            return None
        
        x_sum = sum(state.pose.x for state in self.robots.values())
        y_sum = sum(state.pose.y for state in self.robots.values())
        
        return (x_sum / len(self.robots), y_sum / len(self.robots))
    
    def broadcast_command(self, command: str, parameters: Dict = None) -> int:
        """Broadcast command to all robots."""
        encoded = RobotCommunication.encode_command(command, parameters)
        # In real implementation, this would send to all robots
        return len(self.robots)


def demonstrate_robotics_utils():
    """Demonstrate robotics utilities functionality."""
    print("=== Robotics Utilities Demonstration ===\n")
    
    # Robot Kinematics
    print("1. Robot Kinematics:")
    joint_angles = [math.pi/4, math.pi/6]
    link_lengths = [10.0, 8.0]
    
    end_effector = RobotKinematics.forward_kinematics(joint_angles, link_lengths)
    print(f"   Forward kinematics: x={end_effector.x:.2f}, y={end_effector.y:.2f}")
    
    target_pose = Pose(x=15.0, y=10.0, z=0, roll=0, pitch=0, yaw=0)
    joint_angles = RobotKinematics.inverse_kinematics(target_pose, link_lengths)
    print(f"   Inverse kinematics: {[f'{a:.2f}' for a in joint_angles]}")
    
    # Differential Drive
    v_left, v_right = 2.0, 3.0
    wheel_base = 0.5
    
    velocity = RobotKinematics.differential_drive_kinematics(v_left, v_right, wheel_base)
    print(f"   Robot velocity: linear={velocity.linear_x:.2f}, angular={velocity.angular_z:.2f}")
    
    linear, angular = 2.5, 1.0
    wheel_speeds = RobotKinematics.inverse_differential_drive(linear, angular, wheel_base)
    print(f"   Wheel speeds: left={wheel_speeds[0]:.2f}, right={wheel_speeds[1]:.2f}")
    
    # Path Planning
    print("\n2. Path Planning:")
    start = (10.0, 10.0)
    goal = (90.0, 90.0)
    obstacles = [(30.0, 30.0, 10.0), (50.0, 50.0, 15.0), (70.0, 30.0, 8.0)]
    
    path = PathPlanner.plan_path_a_star(start, goal, obstacles)
    print(f"   Path points: {len(path)}")
    if path:
        print(f"   Start: {path[0]}, End: {path[-1]}")
    
    smoothed_path = PathPlanner.smooth_path(path)
    print(f"   Smoothed path points: {len(smoothed_path)}")
    
    # PID Controller
    print("\n3. PID Controller:")
    pid = PIDController(kp=1.0, ki=0.1, kd=0.5, setpoint=10.0)
    
    for i in range(10):
        measurement = 5.0 + i * 0.5
        output = pid.compute(measurement)
        print(f"   Measurement: {measurement:.2f}, Output: {output:.2f}")
    
    # Robot State
    print("\n4. Robot State:")
    state = RobotState()
    state.update_pose(Pose(10.0, 20.0, 0.0, 0.0, 0.0, math.pi/4))
    state.update_velocity(Velocity(1.0, 0.0, 0.0, 0.0, 0.0, 0.5))
    state.update_battery(75.0)
    
    print(f"   Position: ({state.pose.x:.2f}, {state.pose.y:.2f})")
    print(f"   Orientation: {state.pose.yaw:.2f} rad")
    print(f"   Battery: {state.battery_level:.1f}%")
    print(f"   Battery status: {state.get_battery_status()}")
    
    # Coordinate Transform
    print("\n5. Coordinate Transform:")
    point = (5.0, 5.0)
    rotated = CoordinateTransform.rotate_point(point, math.pi/4)
    print(f"   Original: {point}")
    print(f"   Rotated 45°: ({rotated[0]:.2f}, {rotated[1]:.2f})")
    
    polar = CoordinateTransform.cartesian_to_polar(3.0, 4.0)
    print(f"   Cartesian (3, 4) to polar: r={polar[0]:.2f}, θ={polar[1]:.2f}")
    
    cartesian = CoordinateTransform.polar_to_cartesian(5.0, math.pi/3)
    print(f"   Polar (5, π/3) to Cartesian: ({cartesian[0]:.2f}, {cartesian[1]:.2f})")
    
    # Motor Control
    print("\n6. Motor Control:")
    motor_controller = MotorController(num_motors=4)
    
    motor_controller.set_motor_speed(0, 0.8)
    motor_controller.set_motor_speed(1, 0.6)
    motor_controller.set_motor_speed(2, -0.4)
    motor_controller.set_motor_speed(3, 0.7)
    
    print(f"   Motor speeds: {[motor_controller.get_motor_speed(i) for i in range(4)]}")
    
    # Sensor Processing
    print("\n7. Sensor Processing:")
    readings = [
        SensorReading(SensorType.LIDAR, 10.0, time.time(), "m"),
        SensorReading(SensorType.LIDAR, 10.5, time.time(), "m"),
        SensorReading(SensorType.LIDAR, 10.2, time.time(), "m"),
        SensorReading(SensorType.LIDAR, 15.0, time.time(), "m"),  # Anomaly
        SensorReading(SensorType.LIDAR, 10.3, time.time(), "m")
    ]
    
    filtered = SensorProcessor.filter_readings(readings)
    print(f"   Original readings: {len(readings)}")
    print(f"   Filtered readings: {len(filtered)}")
    
    anomalies = SensorProcessor.detect_anomalies(readings)
    print(f"   Anomalies detected: {len(anomalies)}")
    
    # Robot Simulation
    print("\n8. Robot Simulation:")
    simulator = RobotSimulator(RobotType.MOBILE)
    simulator.add_obstacle(30.0, 30.0, 5.0)
    simulator.add_obstacle(60.0, 60.0, 8.0)
    
    simulator.set_velocity(2.0, 0.5)
    simulator.update(1.0)
    
    print(f"   Position after 1s: ({simulator.state.pose.x:.2f}, {simulator.state.pose.y:.2f})")
    print(f"   Battery: {simulator.state.battery_level:.1f}%")
    
    distance = simulator.get_distance_to_obstacle()
    print(f"   Distance to obstacle: {distance:.2f}")
    
    # Robot Communication
    print("\n9. Robot Communication:")
    command = RobotCommunication.encode_command("move", {"distance": 5.0, "angle": 0.5})
    print(f"   Encoded command: {command[:50]}...")
    
    telemetry = RobotCommunication.encode_telemetry(state)
    print(f"   Encoded telemetry length: {len(telemetry)}")
    
    # Fleet Management
    print("\n10. Fleet Management:")
    fleet = RobotFleet()
    
    for i in range(3):
        robot_state = RobotState()
        robot_state.update_pose(Pose(i * 10.0, i * 10.0, 0.0, 0.0, 0.0, 0.0))
        fleet.add_robot(f"robot_{i}", robot_state)
    
    fleet_center = fleet.get_fleet_center()
    print(f"   Fleet center: ({fleet_center[0]:.2f}, {fleet_center[1]:.2f})")
    
    broadcast_count = fleet.broadcast_command("stop")
    print(f"   Broadcast to {broadcast_count} robots")
    
    print("\n=== Demonstration Complete ===")
    print("\nRobotics Best Practices:")
    print("- Use proper coordinate transformations for multi-robot systems")
    print("- Implement safety limits and emergency stops")
    print("- Use appropriate control algorithms (PID, MPC, etc.)")
    print("- Validate sensor data and handle anomalies")
    print("- Plan paths considering kinematic constraints")
    print("- Monitor battery levels and power consumption")
    print("- Use robust communication protocols")
    print("- Test thoroughly in simulation before deployment")
    print("- Implement proper calibration procedures")
    print("- Consider real-time requirements and latency")


if __name__ == "__main__":
    import json
    demonstrate_robotics_utils()