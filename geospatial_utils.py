"""
Geospatial Utilities Module

This module provides comprehensive geospatial utilities including:
- Geographic coordinate handling
- Distance calculations (Haversine, Vincenty)
- Coordinate transformations
- Geofencing and spatial queries
- GPS data processing
- Map projection utilities
- Spatial analysis
- Geocoding and reverse geocoding
- Shapefile handling
- GeoJSON processing

Note: This module uses geopy for geocoding and shapely for spatial operations.
Install with: pip install geopy shapely

All functions include comprehensive docstrings and type hints.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import json


try:
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False


try:
    from shapely.geometry import Point, Polygon, LineString
    from shapely.ops import unary_union
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False


class CoordinateSystem(Enum):
    """Coordinate system types."""
    WGS84 = "wgs84"  # World Geodetic System 1984
    NAD83 = "nad83"  # North American Datum 1983
    UTM = "utm"  # Universal Transverse Mercator
    MERCATOR = "mercator"  # Web Mercator


class DistanceUnit(Enum):
    """Distance measurement units."""
    METERS = "meters"
    KILOMETERS = "kilometers"
    MILES = "miles"
    NAUTICAL_MILES = "nautical_miles"
    FEET = "feet"
    YARDS = "yards"


@dataclass
class GeoPoint:
    """Geographic point with coordinates."""
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    timestamp: Optional[float] = None
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple (lat, lon)."""
        return (self.latitude, self.longitude)
    
    def to_3d_tuple(self) -> Tuple[float, float, Optional[float]]:
        """Convert to 3D tuple (lat, lon, alt)."""
        return (self.latitude, self.longitude, self.altitude)
    
    def is_valid(self) -> bool:
        """Check if coordinates are valid."""
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180


@dataclass
class BoundingBox:
    """Bounding box for geographic area."""
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    
    def contains(self, point: GeoPoint) -> bool:
        """Check if point is within bounding box."""
        return (self.min_lat <= point.latitude <= self.max_lat and
                self.min_lon <= point.longitude <= self.max_lon)
    
    def intersects(self, other: 'BoundingBox') -> bool:
        """Check if bounding boxes intersect."""
        return not (self.max_lat < other.min_lat or self.min_lat > other.max_lat or
                   self.max_lon < other.min_lon or self.min_lon > other.max_lon)
    
    def center(self) -> GeoPoint:
        """Get center point of bounding box."""
        center_lat = (self.min_lat + self.max_lat) / 2
        center_lon = (self.min_lon + self.max_lon) / 2
        return GeoPoint(center_lat, center_lon)
    
    def area(self) -> float:
        """Calculate approximate area in square kilometers."""
        # Simplified calculation
        lat_diff = self.max_lat - self.min_lat
        lon_diff = self.max_lon - self.min_lon
        
        # Approximate: 1 degree lat ≈ 111 km, 1 degree lon ≈ 111 km * cos(lat)
        avg_lat = (self.min_lat + self.max_lat) / 2
        lat_km = lat_diff * 111
        lon_km = lon_diff * 111 * math.cos(math.radians(avg_lat))
        
        return lat_km * lon_km


class CoordinateConverter:
    """Coordinate transformation utilities."""
    
    @staticmethod
    def dms_to_dd(degrees: float, minutes: float, seconds: float,
                  direction: str = "N") -> float:
        """Convert degrees/minutes/seconds to decimal degrees."""
        decimal = degrees + minutes / 60 + seconds / 3600
        
        if direction in ["S", "W"]:
            decimal = -decimal
        
        return decimal
    
    @staticmethod
    def dd_to_dms(decimal_degrees: float) -> Tuple[float, float, float, str]:
        """Convert decimal degrees to degrees/minutes/seconds."""
        direction = "N" if decimal_degrees >= 0 else "S"
        decimal_degrees = abs(decimal_degrees)
        
        degrees = int(decimal_degrees)
        minutes_float = (decimal_degrees - degrees) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60
        
        return degrees, minutes, seconds, direction
    
    @staticmethod
    def utm_to_zone_number(latitude: float, longitude: float) -> int:
        """Calculate UTM zone number from coordinates."""
        if 56 <= longitude < 64:
            return 32
        elif 72 <= longitude < 80:
            return 34
        elif 8 <= longitude < 16:
            return 35
        elif 112 <= longitude < 120:
            return 56
        else:
            return int((longitude + 180) / 6) + 1
    
    @staticmethod
    def lat_lon_to_mercator(latitude: float, longitude: float) -> Tuple[float, float]:
        """Convert lat/lon to Web Mercator (EPSG:3857)."""
        # Earth radius in meters
        R = 6378137.0
        
        x = R * math.radians(longitude)
        
        lat_rad = math.radians(latitude)
        y = R * math.log(math.tan(math.pi / 4 + lat_rad / 2))
        
        return x, y
    
    @staticmethod
    def mercator_to_lat_lon(x: float, y: float) -> Tuple[float, float]:
        """Convert Web Mercator to lat/lon."""
        # Earth radius in meters
        R = 6378137.0
        
        longitude = math.degrees(x / R)
        latitude = math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2)
        
        return latitude, longitude


class DistanceCalculator:
    """Distance calculation utilities."""
    
    @staticmethod
    def haversine(point1: GeoPoint, point2: GeoPoint,
                  unit: DistanceUnit = DistanceUnit.KILOMETERS) -> float:
        """Calculate distance using Haversine formula."""
        # Earth radius in different units
        earth_radii = {
            DistanceUnit.METERS: 6371000,
            DistanceUnit.KILOMETERS: 6371,
            DistanceUnit.MILES: 3959,
            DistanceUnit.NAUTICAL_MILES: 3440,
            DistanceUnit.FEET: 20903520,
            DistanceUnit.YARDS: 6967840
        }
        
        R = earth_radii[unit]
        
        # Convert to radians
        lat1, lon1 = math.radians(point1.latitude), math.radians(point1.longitude)
        lat2, lon2 = math.radians(point2.latitude), math.radians(point2.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        return distance
    
    @staticmethod
    def vincenty(point1: GeoPoint, point2: GeoPoint) -> float:
        """Calculate distance using Vincenty's formula (more accurate)."""
        if GEOPY_AVAILABLE:
            try:
                distance = geodesic(
                    (point1.latitude, point1.longitude),
                    (point2.latitude, point2.longitude)
                ).meters
                return distance
            except:
                pass
        
        # Fallback to Haversine
        return DistanceCalculator.haversine(point1, point2, DistanceUnit.METERS)
    
    @staticmethod
    def bearing(point1: GeoPoint, point2: GeoPoint) -> float:
        """Calculate bearing between two points."""
        lat1, lon1 = math.radians(point1.latitude), math.radians(point1.longitude)
        lat2, lon2 = math.radians(point2.latitude), math.radians(point2.longitude)
        
        dlon = lon2 - lon1
        
        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        
        bearing = math.atan2(x, y)
        bearing = math.degrees(bearing)
        bearing = (bearing + 360) % 360
        
        return bearing
    
    @staticmethod
    def midpoint(point1: GeoPoint, point2: GeoPoint) -> GeoPoint:
        """Calculate midpoint between two points."""
        lat1, lon1 = math.radians(point1.latitude), math.radians(point1.longitude)
        lat2, lon2 = math.radians(point2.latitude), math.radians(point2.longitude)
        
        dlon = lon2 - lon1
        
        Bx = math.cos(lat2) * math.cos(dlon)
        By = math.cos(lat2) * math.sin(dlon)
        
        lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),
                         math.sqrt((math.cos(lat1) + Bx) ** 2 + By ** 2))
        lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)
        
        return GeoPoint(math.degrees(lat3), math.degrees(lon3))
    
    @staticmethod
    def destination_point(point: GeoPoint, bearing: float,
                         distance: float, unit: DistanceUnit = DistanceUnit.KILOMETERS) -> GeoPoint:
        """Calculate destination point given bearing and distance."""
        # Convert distance to radians
        earth_radii = {
            DistanceUnit.METERS: 6371000,
            DistanceUnit.KILOMETERS: 6371,
            DistanceUnit.MILES: 3959,
            DistanceUnit.NAUTICAL_MILES: 3440
        }
        
        R = earth_radii[unit]
        d = distance / R
        bearing_rad = math.radians(bearing)
        lat1, lon1 = math.radians(point.latitude), math.radians(point.longitude)
        
        lat2 = math.asin(math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(bearing_rad))
        lon2 = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(d) * math.cos(lat1),
                                  math.cos(d) - math.sin(lat1) * math.sin(lat2))
        
        return GeoPoint(math.degrees(lat2), math.degrees(lon2))


class Geofencing:
    """Geofencing and spatial query utilities."""
    
    @staticmethod
    def point_in_circle(point: GeoPoint, center: GeoPoint, radius: float,
                       unit: DistanceUnit = DistanceUnit.KILOMETERS) -> bool:
        """Check if point is within a circular geofence."""
        distance = DistanceCalculator.haversine(point, center, unit)
        return distance <= radius
    
    @staticmethod
    def point_in_polygon(point: GeoPoint, polygon: List[GeoPoint]) -> bool:
        """Check if point is within a polygon (ray casting algorithm)."""
        if not polygon:
            return False
        
        x, y = point.longitude, point.latitude
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0].longitude, polygon[0].latitude
        for i in range(n + 1):
            p2x, p2y = polygon[i % n].longitude, polygon[i % n].latitude
            
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            
            p1x, p1y = p2x, p2y
        
        return inside
    
    @staticmethod
    def points_in_polygon(points: List[GeoPoint], polygon: List[GeoPoint]) -> List[GeoPoint]:
        """Find all points within a polygon."""
        return [point for point in points if Geofencing.point_in_polygon(point, polygon)]
    
    @staticmethod
    def create_circle_geofence(center: GeoPoint, radius: float,
                              unit: DistanceUnit = DistanceUnit.KILOMETERS) -> Dict:
        """Create circular geofence definition."""
        return {
            "type": "circle",
            "center": center.to_tuple(),
            "radius": radius,
            "unit": unit.value
        }
    
    @staticmethod
    def create_polygon_geofence(vertices: List[GeoPoint]) -> Dict:
        """Create polygon geofence definition."""
        return {
            "type": "polygon",
            "vertices": [v.to_tuple() for v in vertices]
        }


class Geocoder:
    """Geocoding and reverse geocoding utilities."""
    
    @staticmethod
    def geocode(address: str, timeout: int = 10) -> Optional[GeoPoint]:
        """Convert address to coordinates."""
        if not GEOPY_AVAILABLE:
            raise ImportError("geopy library is required. Install with: pip install geopy")
        
        try:
            geolocator = Nominatim(user_agent="python_geospatial_utils")
            location = geolocator.geocode(address, timeout=timeout)
            
            if location:
                return GeoPoint(location.latitude, location.longitude)
            
            return None
        except GeocoderTimedOut:
            print("Geocoding request timed out")
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    @staticmethod
    def reverse_geocode(latitude: float, longitude: float,
                       timeout: int = 10) -> Optional[str]:
        """Convert coordinates to address."""
        if not GEOPY_AVAILABLE:
            raise ImportError("geopy library is required")
        
        try:
            geolocator = Nominatim(user_agent="python_geospatial_utils")
            location = geolocator.reverse((latitude, longitude), timeout=timeout)
            
            if location:
                return location.address
            
            return None
        except GeocoderTimedOut:
            print("Reverse geocoding request timed out")
            return None
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None
    
    @staticmethod
    def batch_geocode(addresses: List[str], delay: float = 1.0) -> Dict[str, Optional[GeoPoint]]:
        """Geocode multiple addresses with delay between requests."""
        import time
        
        results = {}
        
        for address in addresses:
            results[address] = Geocoder.geocode(address)
            time.sleep(delay)
        
        return results


class GeoJSONHandler:
    """GeoJSON processing utilities."""
    
    @staticmethod
    def create_point_feature(geometry: GeoPoint, properties: Dict = None) -> Dict:
        """Create GeoJSON Point feature."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [geometry.longitude, geometry.latitude]
            },
            "properties": properties or {}
        }
    
    @staticmethod
    def create_line_feature(points: List[GeoPoint], properties: Dict = None) -> Dict:
        """Create GeoJSON LineString feature."""
        coordinates = [[p.longitude, p.latitude] for p in points]
        
        return {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": properties or {}
        }
    
    @staticmethod
    def create_polygon_feature(vertices: List[GeoPoint], properties: Dict = None) -> Dict:
        """Create GeoJSON Polygon feature."""
        coordinates = [[v.longitude, v.latitude] for v in vertices]
        
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            },
            "properties": properties or {}
        }
    
    @staticmethod
    def create_feature_collection(features: List[Dict]) -> Dict:
        """Create GeoJSON FeatureCollection."""
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    @staticmethod
    def parse_geojson(geojson_string: str) -> Dict:
        """Parse GeoJSON string."""
        return json.loads(geojson_string)
    
    @staticmethod
    def extract_features(geojson: Dict) -> List[Dict]:
        """Extract features from GeoJSON."""
        if geojson.get("type") == "FeatureCollection":
            return geojson.get("features", [])
        elif geojson.get("type") == "Feature":
            return [geojson]
        return []
    
    @staticmethod
    def get_bbox(features: List[Dict]) -> Optional[BoundingBox]:
        """Calculate bounding box from GeoJSON features."""
        if not features:
            return None
        
        all_coords = []
        
        for feature in features:
            geometry = feature.get("geometry", {})
            geom_type = geometry.get("type")
            coords = geometry.get("coordinates", [])
            
            if geom_type == "Point":
                all_coords.append(coords)
            elif geom_type == "LineString":
                all_coords.extend(coords)
            elif geom_type == "Polygon":
                all_coords.extend(coords[0])
            elif geom_type == "MultiPoint":
                all_coords.extend(coords)
            elif geom_type == "MultiLineString":
                for line in coords:
                    all_coords.extend(line)
            elif geom_type == "MultiPolygon":
                for polygon in coords:
                    all_coords.extend(polygon[0])
        
        if not all_coords:
            return None
        
        lons = [coord[0] for coord in all_coords]
        lats = [coord[1] for coord in all_coords]
        
        return BoundingBox(
            min_lat=min(lats),
            max_lat=max(lats),
            min_lon=min(lons),
            max_lon=max(lons)
        )


class GPSProcessor:
    """GPS data processing utilities."""
    
    @staticmethod
    def calculate_speed(point1: GeoPoint, point2: GeoPoint,
                      time_diff: float, unit: DistanceUnit = DistanceUnit.KILOMETERS) -> float:
        """Calculate speed between two GPS points."""
        distance = DistanceCalculator.haversine(point1, point2, unit)
        
        if time_diff > 0:
            return distance / time_diff  # distance per second
        return 0.0
    
    @staticmethod
    def calculate_heading(point1: GeoPoint, point2: GeoPoint) -> float:
        """Calculate heading between two GPS points."""
        return DistanceCalculator.bearing(point1, point2)
    
    @staticmethod
    def smooth_track(track: List[GeoPoint], window_size: int = 3) -> List[GeoPoint]:
        """Smooth GPS track using moving average."""
        if len(track) < window_size:
            return track
        
        smoothed = []
        
        for i in range(len(track)):
            start = max(0, i - window_size // 2)
            end = min(len(track), i + window_size // 2 + 1)
            window = track[start:end]
            
            avg_lat = sum(p.latitude for p in window) / len(window)
            avg_lon = sum(p.longitude for p in window) / len(window)
            
            avg_alt = None
            if all(p.altitude is not None for p in window):
                avg_alt = sum(p.altitude for p in window) / len(window)
            
            smoothed.append(GeoPoint(avg_lat, avg_lon, avg_alt))
        
        return smoothed
    
    @staticmethod
    def calculate_track_distance(track: List[GeoPoint],
                               unit: DistanceUnit = DistanceUnit.KILOMETERS) -> float:
        """Calculate total distance of GPS track."""
        if len(track) < 2:
            return 0.0
        
        total_distance = 0.0
        
        for i in range(len(track) - 1):
            distance = DistanceCalculator.haversine(track[i], track[i + 1], unit)
            total_distance += distance
        
        return total_distance
    
    @staticmethod
    def filter_points_by_accuracy(track: List[GeoPoint],
                                  max_accuracy: float) -> List[GeoPoint]:
        """Filter GPS points by accuracy threshold."""
        # This would use altitude as a proxy for accuracy in real implementation
        return [point for point in track if point.altitude is not None and point.altitude <= max_accuracy]


class SpatialAnalysis:
    """Spatial analysis utilities."""
    
    @staticmethod
    def calculate_area_polygon(vertices: List[GeoPoint]) -> float:
        """Calculate area of polygon using shoelace formula (simplified)."""
        if len(vertices) < 3:
            return 0.0
        
        # Convert to Cartesian coordinates (simplified, assumes small area)
        avg_lat = sum(v.latitude for v in vertices) / len(vertices)
        lat_scale = 111.32  # km per degree latitude
        lon_scale = 111.32 * math.cos(math.radians(avg_lat))  # km per degree longitude
        
        x_coords = [v.longitude * lon_scale for v in vertices]
        y_coords = [v.latitude * lat_scale for v in vertices]
        
        # Shoelace formula
        n = len(vertices)
        area = 0.0
        
        for i in range(n):
            j = (i + 1) % n
            area += x_coords[i] * y_coords[j]
            area -= x_coords[j] * y_coords[i]
        
        area = abs(area) / 2
        return area
    
    @staticmethod
    def calculate_centroid(vertices: List[GeoPoint]) -> GeoPoint:
        """Calculate centroid of polygon."""
        if not vertices:
            return GeoPoint(0, 0)
        
        avg_lat = sum(v.latitude for v in vertices) / len(vertices)
        avg_lon = sum(v.longitude for v in vertices) / len(vertices)
        
        return GeoPoint(avg_lat, avg_lon)
    
    @staticmethod
    def buffer_point(point: GeoPoint, distance: float,
                    unit: DistanceUnit = DistanceUnit.KILOMETERS) -> List[GeoPoint]:
        """Create buffer around point (simplified circle)."""
        center = point
        radius = distance
        
        # Create circle points
        points = []
        num_points = 36  # 10-degree increments
        
        for i in range(num_points):
            angle = math.radians(i * 360 / num_points)
            dest = DistanceCalculator.destination_point(center, math.degrees(angle), radius, unit)
            points.append(dest)
        
        return points
    
    @staticmethod
    def nearest_neighbor(query_point: GeoPoint, candidates: List[GeoPoint]) -> Optional[GeoPoint]:
        """Find nearest neighbor from candidates."""
        if not candidates:
            return None
        
        nearest = candidates[0]
        min_distance = DistanceCalculator.haversine(query_point, nearest)
        
        for candidate in candidates[1:]:
            distance = DistanceCalculator.haversine(query_point, candidate)
            if distance < min_distance:
                min_distance = distance
                nearest = candidate
        
        return nearest
    
    @staticmethod
    def find_points_within_distance(center: GeoPoint, points: List[GeoPoint],
                                    max_distance: float,
                                    unit: DistanceUnit = DistanceUnit.KILOMETERS) -> List[GeoPoint]:
        """Find all points within max distance of center."""
        return [point for point in points 
                if DistanceCalculator.haversine(center, point, unit) <= max_distance]


class MapProjection:
    """Map projection utilities."""
    
    @staticmethod
    def equirectangular_proj(latitude: float, longitude: float,
                            width: int, height: int) -> Tuple[int, int]:
        """Equirectangular projection to pixel coordinates."""
        # Simple equirectangular projection
        x = int((longitude + 180) / 360 * width)
        y = int((90 - latitude) / 180 * height)
        
        return x, y
    
    @staticmethod
    def inverse_equirectangular(x: int, y: int,
                                width: int, height: int) -> Tuple[float, float]:
        """Inverse equirectangular projection."""
        longitude = (x / width) * 360 - 180
        latitude = 90 - (y / height) * 180
        
        return latitude, longitude
    
    @staticmethod
    def web_mercator_proj(latitude: float, longitude: float,
                         width: int, height: int) -> Tuple[int, int]:
        """Web Mercator projection to pixel coordinates."""
        # Convert to Web Mercator
        x_merc, y_merc = CoordinateConverter.lat_lon_to_mercator(latitude, longitude)
        
        # World extent in Web Mercator
        x_min, x_max = -20037508.34, 20037508.34
        y_min, y_max = -20037508.34, 20037508.34
        
        # Normalize to pixel coordinates
        x = int((x_merc - x_min) / (x_max - x_min) * width)
        y = int((y_max - y_merc) / (y_max - y_min) * height)
        
        return x, y


def demonstrate_geospatial_utils():
    """Demonstrate geospatial utilities functionality."""
    print("=== Geospatial Utilities Demonstration ===\n")
    
    # Geographic Points
    print("1. Geographic Points:")
    point1 = GeoPoint(40.7128, -74.0060)  # New York
    point2 = GeoPoint(51.5074, -0.1278)   # London
    point3 = GeoPoint(35.6762, 139.6503)  # Tokyo
    
    print(f"   New York: {point1.to_tuple()}")
    print(f"   London: {point2.to_tuple()}")
    print(f"   Tokyo: {point3.to_tuple()}")
    
    # Distance Calculations
    print("\n2. Distance Calculations:")
    distance_ny_london = DistanceCalculator.haversine(point1, point2)
    print(f"   NYC to London: {distance_ny_london:.2f} km")
    
    distance_ny_tokyo = DistanceCalculator.haversine(point1, point3)
    print(f"   NYC to Tokyo: {distance_ny_tokyo:.2f} km")
    
    bearing = DistanceCalculator.bearing(point1, point2)
    print(f"   Bearing NYC to London: {bearing:.2f}°")
    
    midpoint = DistanceCalculator.midpoint(point1, point2)
    print(f"   Midpoint: {midpoint.to_tuple()}")
    
    # Coordinate Conversion
    print("\n3. Coordinate Conversion:")
    dms = CoordinateConverter.dd_to_dms(40.7128)
    print(f"   NYC in DMS: {dms}")
    
    dd = CoordinateConverter.dms_to_dd(40, 42, 46, "N")
    print(f"   Back to DD: {dd:.4f}")
    
    mercator = CoordinateConverter.lat_lon_to_mercator(40.7128, -74.0060)
    print(f"   Web Mercator: ({mercator[0]:.0f}, {mercator[1]:.0f})")
    
    # Geofencing
    print("\n4. Geofencing:")
    center = GeoPoint(40.7128, -74.0060)
    test_point = GeoPoint(40.75, -74.05)
    
    in_circle = Geofencing.point_in_circle(test_point, center, 50)
    print(f"   Point in 50km circle: {in_circle}")
    
    polygon = [
        GeoPoint(40.70, -74.00),
        GeoPoint(40.70, -74.05),
        GeoPoint(40.75, -74.05),
        GeoPoint(40.75, -74.00)
    ]
    
    in_polygon = Geofencing.point_in_polygon(test_point, polygon)
    print(f"   Point in polygon: {in_polygon}")
    
    # Geocoding
    print("\n5. Geocoding:")
    if GEOPY_AVAILABLE:
        location = Geocoder.geocode("Times Square, New York")
        if location:
            print(f"   Times Square: {location.to_tuple()}")
        
        address = Geocoder.reverse_geocode(40.7128, -74.0060)
        if address:
            print(f"   Reverse geocode: {address[:50]}...")
    else:
        print("   Install geopy: pip install geopy")
    
    # GeoJSON
    print("\n6. GeoJSON Processing:")
    point_feature = GeoJSONHandler.create_point_feature(point1, {"name": "NYC"})
    print(f"   Point feature: {point_feature['geometry']['type']}")
    
    line_feature = GeoJSONHandler.create_line_feature([point1, point2], {"route": "NYC-London"})
    print(f"   Line feature: {line_feature['geometry']['type']}")
    
    polygon_feature = GeoJSONHandler.create_polygon_feature(polygon, {"area": "downtown"})
    print(f"   Polygon feature: {polygon_feature['geometry']['type']}")
    
    # GPS Processing
    print("\n7. GPS Processing:")
    track = [
        GeoPoint(40.7128, -74.0060, 10.0, 0.0),
        GeoPoint(40.7130, -74.0065, 12.0, 1.0),
        GeoPoint(40.7135, -74.0070, 15.0, 2.0),
        GeoPoint(40.7140, -74.0075, 14.0, 3.0)
    ]
    
    track_distance = GPSProcessor.calculate_track_distance(track)
    print(f"   Track distance: {track_distance:.4f} km")
    
    smoothed = GPSProcessor.smooth_track(track)
    print(f"   Smoothed track: {len(smoothed)} points")
    
    speed = GPSProcessor.calculate_speed(track[0], track[1], 1.0)
    print(f"   Speed between first two points: {speed:.4f} km/s")
    
    # Spatial Analysis
    print("\n8. Spatial Analysis:")
    area = SpatialAnalysis.calculate_area_polygon(polygon)
    print(f"   Polygon area: {area:.4f} km²")
    
    centroid = SpatialAnalysis.calculate_centroid(polygon)
    print(f"   Centroid: {centroid.to_tuple()}")
    
    nearest = SpatialAnalysis.nearest_neighbor(point1, [point2, point3])
    print(f"   Nearest to NYC: {nearest.to_tuple()}")
    
    buffer = SpatialAnalysis.buffer_point(point1, 10)
    print(f"   Buffer circle: {len(buffer)} points")
    
    # Map Projection
    print("\n9. Map Projection:")
    x, y = MapProjection.equirectangular_proj(40.7128, -74.0060, 800, 400)
    print(f"   Equirectangular: ({x}, {y})")
    
    mx, my = MapProjection.web_mercator_proj(40.7128, -74.0060, 800, 400)
    print(f"   Web Mercator: ({mx}, {my})")
    
    # Bounding Box
    print("\n10. Bounding Box:")
    bbox = BoundingBox(40.70, 40.75, -74.05, -74.00)
    print(f"   Bounding box: {bbox}")
    
    in_bbox = bbox.contains(test_point)
    print(f"   Test point in bbox: {in_bbox}")
    
    bbox_center = bbox.center()
    print(f"   Bbox center: {bbox_center.to_tuple()}")
    
    bbox_area = bbox.area()
    print(f"   Bbox area: {bbox_area:.4f} km²")
    
    print("\n=== Demonstration Complete ===")
    print("\nGeospatial Best Practices:")
    print("- Use appropriate coordinate system for your application")
    print("- Consider accuracy requirements when choosing distance calculation")
    print("- Haversine is sufficient for most applications")
    print("- Vincenty provides higher accuracy for long distances")
    print("- Respect rate limits when using geocoding APIs")
    print("- Handle edge cases (poles, antimeridian)")
    print("- Consider projection distortions for large areas")
    print("- Use appropriate spatial indexes for large datasets")
    print("- Validate coordinate ranges before processing")
    print("- Consider performance vs. accuracy trade-offs")


if __name__ == "__main__":
    demonstrate_geospatial_utils()