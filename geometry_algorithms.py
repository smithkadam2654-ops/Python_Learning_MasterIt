"""
Geometry Algorithms - Computational geometry operations.
Features: Points, lines, polygons, distance calculations, and geometric primitives.
"""

from typing import List, Tuple, Optional
import math


class Point:
    """2D Point class."""
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize point."""
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def distance_to_squared(self, other: 'Point') -> float:
        """Calculate squared distance (avoids sqrt)."""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


class GeometryAlgorithms:
    """Computational geometry algorithms."""
    
    @staticmethod
    def distance(p1: Point, p2: Point) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            p1: First point
            p2: Second point
            
        Returns:
            Distance
        """
        return p1.distance_to(p2)
    
    @staticmethod
    def manhattan_distance(p1: Point, p2: Point) -> float:
        """
        Calculate Manhattan distance between two points.
        
        Args:
            p1: First point
            p2: Second point
            
        Returns:
            Manhattan distance
        """
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)
    
    @staticmethod
    def point_line_distance(point: Point, line_start: Point, line_end: Point) -> float:
        """
        Calculate distance from point to line segment.
        
        Args:
            point: Point
            line_start: Line segment start
            line_end: Line segment end
            
        Returns:
            Distance to line segment
        """
        # Vector from line_start to line_end
        dx = line_end.x - line_start.x
        dy = line_end.y - line_start.y
        
        # Handle zero-length line
        if dx == 0 and dy == 0:
            return point.distance_to(line_start)
        
        # Project point onto line
        t = ((point.x - line_start.x) * dx + (point.y - line_start.y) * dy) / (dx * dx + dy * dy)
        
        # Clamp t to [0, 1] for segment
        t = max(0, min(1, t))
        
        # Find closest point on segment
        closest_x = line_start.x + t * dx
        closest_y = line_start.y + t * dy
        
        return math.sqrt((point.x - closest_x) ** 2 + (point.y - closest_y) ** 2)
    
    @staticmethod
    def cross_product(p1: Point, p2: Point, p3: Point) -> float:
        """
        Calculate cross product of vectors p1->p2 and p1->p3.
        
        Args:
            p1: Origin point
            p2: First vector end
            p3: Second vector end
            
        Returns:
            Cross product (positive = counterclockwise, negative = clockwise)
        """
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    
    @staticmethod
    def orientation(p1: Point, p2: Point, p3: Point) -> str:
        """
        Determine orientation of ordered triplet (p1, p2, p3).
        
        Args:
            p1: First point
            p2: Second point
            p3: Third point
            
        Returns:
            "collinear", "clockwise", or "counterclockwise"
        """
        cross = GeometryAlgorithms.cross_product(p1, p2, p3)
        
        if cross == 0:
            return "collinear"
        elif cross > 0:
            return "counterclockwise"
        else:
            return "clockwise"
    
    @staticmethod
    def on_segment(p1: Point, p2: Point, p3: Point) -> bool:
        """
        Check if point p3 lies on line segment p1-p2.
        
        Args:
            p1: Segment start
            p2: Segment end
            p3: Point to check
            
       _returns:
            True if p3 is on segment
        """
        return (min(p1.x, p2.x) <= p3.x <= max(p1.x, p2.x) and
                min(p1.y, p2.y) <= p3.y <= max(p1.y, p2.y))
    
    @staticmethod
    def segments_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
        """
        Check if line segments p1-p2 and p3-p4 intersect.
        
        Args:
            p1: First segment start
            p2: First segment end
            p3: Second segment start
            p4: Second segment end
            
        Returns:
            True if segments intersect
        """
        o1 = GeometryAlgorithms.orientation(p1, p2, p3)
        o2 = GeometryAlgorithms.orientation(p1, p2, p4)
        o3 = GeometryAlgorithms.orientation(p3, p4, p1)
        o4 = GeometryAlgorithms.orientation(p3, p4, p2)
        
        # General case
        if o1 != o2 and o3 != o4:
            return True
        
        # Special cases (collinear)
        if o1 == "collinear" and GeometryAlgorithms.on_segment(p1, p2, p3):
            return True
        if o2 == "collinear" and GeometryAlgorithms.on_segment(p1, p2, p4):
            return True
        if o3 == "collinear" and GeometryAlgorithms.on_segment(p3, p4, p1):
            return True
        if o4 == "collinear" and GeometryAlgorithms.on_segment(p3, p4, p2):
            return True
        
        return False
    
    @staticmethod
    def polygon_area(points: List[Point]) -> float:
        """
        Calculate area of polygon using shoelace formula.
        
        Args:
            points: List of polygon vertices in order
            
        Returns:
            Area (absolute value)
        """
        if len(points) < 3:
            return 0
        
        area = 0
        n = len(points)
        
        for i in range(n):
            j = (i + 1) % n
            area += points[i].x * points[j].y
            area -= points[j].x * points[i].y
        
        return abs(area) / 2
    
    @staticmethod
    def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
        """
        Check if point is inside polygon using ray casting.
        
        Args:
            point: Point to check
            polygon: List of polygon vertices
            
        Returns:
            True if point is inside polygon
        """
        if len(polygon) < 3:
            return False
        
        inside = False
        n = len(polygon)
        
        for i in range(n):
            j = (i + 1) % n
            
            # Check if point is on edge
            if GeometryAlgorithms.on_segment(polygon[i], polygon[j], point):
                return True
            
            # Ray casting
            if ((polygon[i].y > point.y) != (polygon[j].y > point.y)):
                x_intersect = (polygon[j].x - polygon[i].x) * (point.y - polygon[i].y) / (polygon[j].y - polygon[i].y) + polygon[i].x
                
                if point.x < x_intersect:
                    inside = not inside
        
        return inside
    
    @staticmethod
    def convex_hull(points: List[Point]) -> List[Point]:
        """
        Compute convex hull using Graham scan algorithm.
        
        Args:
            points: List of points
            
        Returns:
            Points on convex hull in counterclockwise order
        """
        if len(points) < 3:
            return points.copy()
        
        # Find lowest point (and leftmost if tie)
        start = min(points, key=lambda p: (p.y, p.x))
        
        # Sort points by polar angle with start
        def polar_angle(p: Point) -> float:
            dx = p.x - start.x
            dy = p.y - start.y
            return math.atan2(dy, dx)
        
        sorted_points = sorted(points, key=polar_angle)
        
        # Build hull
        hull = [sorted_points[0], sorted_points[1]]
        
        for point in sorted_points[2:]:
            while len(hull) >= 2:
                cross = GeometryAlgorithms.cross_product(hull[-2], hull[-1], point)
                if cross <= 0:  # Not counterclockwise
                    hul.pop()
                else:
                    break
            hull.append(point)
        
        return hull
    
    @staticmethod
    def closest_pair(points: List[Point]) -> Tuple[Point, Point]:
        """
        Find closest pair of points using divide and conquer.
        
        Args:
            points: List of points
            
        Returns:
            Tuple of two closest points
        """
        if len(points) < 2:
            raise ValueError("Need at least 2 points")
        
        # Sort by x-coordinate
        points_sorted = sorted(points, key=lambda p: p.x)
        
        return GeometryAlgorithms._closest_pair_helper(points_sorted)
    
    @staticmethod
    def _closest_pair_helper(points: List[Point]) -> Tuple[Point, Point]:
        """Helper for closest pair."""
        n = len(points)
        
        if n <= 3:
            # Brute force for small sets
            min_dist = float('inf')
            closest = (points[0], points[1])
            
            for i in range(n):
                for j in range(i + 1, n):
                    dist = points[i].distance_to_squared(points[j])
                    if dist < min_dist:
                        min_dist = dist
                        closest = (points[i], points[j])
            
            return closest
        
        mid = n // 2
        left = points[:mid]
        right = points[mid:]
        
        # Recursive calls
        left_closest = GeometryAlgorithms._closest_pair_helper(left)
        right_closest = GeometryAlgorithms._closest_pair_helper(right)
        
        # Find closer of the two
        left_dist = left_closest[0].distance_to_squared(left_closest[1])
        right_dist = right_closest[0].distance_to_squared(right_closest[1])
        
        if left_dist < right_dist:
            min_pair = left_closest
            min_dist = left_dist
        else:
            min_pair = right_closest
            min_dist = right_dist
        
        # Check strip around midline
        mid_x = points[mid].x
        strip = [p for p in points if abs(p.x - mid_x) < math.sqrt(min_dist)]
        
        strip.sort(key=lambda p: p.y)
        
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                dist = strip[i].distance_to_squared(strip[j])
                if dist < min_dist:
                    min_dist = dist
                    min_pair = (strip[i], strip[j])
        
        return min_pair
    
    @staticmethod
    def circle_center(p1: Point, p2: Point, p3: Point) -> Optional[Point]:
        """
        Find center of circle passing through three points.
        
        Args:
            p1: First point
            p2: Second point
            p3: Third point
            
        Returns:
            Center point or None if points are collinear
        """
        # Check if points are collinear
        if GeometryAlgorithms.orientation(p1, p2, p3) == "collinear":
            return None
        
        # Calculate using perpendicular bisectors
        A = p2.x - p1.x
        B = p2.y - p1.y
        C = p3.x - p1.x
        D = p3.y - p1.y
        
        E = A * (p1.x + p2.x) + B * (p1.y + p2.y)
        F = C * (p1.x + p3.x) + D * (p1.y + p3.y)
        
        G = 2 * (A * (p3.y - p1.y) - B * (p3.x - p1.x))
        
        if G == 0:
            return None
        
        center_x = (D * E - B * F) / G
        center_y = (A * F - C * E) / G
        
        return Point(center_x, center_y)
    
    @staticmethod
    def bounding_box(points: List[Point]) -> Tuple[Point, Point]:
        """
        Find axis-aligned bounding box of points.
        
        Args:
            points: List of points
            
        Returns:
            Tuple of (min_point, max_point)
        """
        if not points:
            return (Point(0, 0), Point(0, 0))
        
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)
        
        return (Point(min_x, min_y), Point(max_x, max_y))


def main() -> None:
    """Demonstrate geometry algorithms."""
    
    print("=== Geometry Algorithms Demo ===")
    
    # Points
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    p3 = Point(1, 1)
    
    # Distance
    print("\n--- Distance ---")
    print(f"Distance {p1} to {p2}: {GeometryAlgorithms.distance(p1, p2)}")
    print(f"Manhattan distance: {GeometryAlgorithms.manhattan_distance(p1, p2)}")
    
    # Point to line
    print("\n--- Point to Line ---")
    line_start = Point(0, 0)
    line_end = Point(10, 0)
    point = Point(5, 3)
    print(f"Distance from {point} to line: {GeometryAlgorithms.point_line_distance(point, line_start, line_end)}")
    
    # Orientation
    print("\n--- Orientation ---")
    p1, p2, p3 = Point(0, 0), Point(4, 4), Point(1, 2)
    print(f"Orientation of {p1}, {p2}, {p3}: {GeometryAlgorithms.orientation(p1, p2, p3)}")
    
    # Segment intersection
    print("\n--- Segment Intersection ---")
    s1_start, s1_end = Point(0, 0), Point(4, 4)
    s2_start, s2_end = Point(0, 4), Point(4, 0)
    print(f"Segments intersect: {GeometryAlgorithms.segments_intersect(s1_start, s1_end, s2_start, s2_end)}")
    
    # Polygon area
    print("\n--- Polygon Area ---")
    square = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
    print(f"Square area: {GeometryAlgorithms.polygon_area(square)}")
    
    triangle = [Point(0, 0), Point(4, 0), Point(2, 3)]
    print(f"Triangle area: {GeometryAlgorithms.polygon_area(triangle)}")
    
    # Point in polygon
    print("\n--- Point in Polygon ---")
    point = Point(2, 2)
    print(f"Point {point} in square: {GeometryAlgorithms.point_in_polygon(point, square)}")
    print(f"Point {point} in triangle: {GeometryAlgorithms.point_in_polygon(point, triangle)}")
    
    # Convex hull
    print("\n--- Convex Hull ---")
    points = [Point(0, 0), Point(1, 1), Point(2, 0), Point(1, 2), Point(2, 2), Point(3, 1)]
    hull = GeometryAlgorithms.convex_hull(points)
    print(f"Points: {points}")
    print(f"Convex hull: {hull}")
    
    # Closest pair
    print("\n--- Closest Pair ---")
    points = [Point(0, 0), Point(3, 4), Point(1, 1), Point(2, 2), Point(5, 5)]
    closest = GeometryAlgorithms.closest_pair(points)
    print(f"Closest pair: {closest}")
    print(f"Distance: {closest[0].distance_to(closest[1])}")
    
    # Circle center
    print("\n--- Circle Center ---")
    p1, p2, p3 = Point(0, 0), Point(2, 0), Point(1, math.sqrt(3))
    center = GeometryAlgorithms.circle_center(p1, p2, p3)
    print(f"Circle center through {p1}, {p2}, {p3}: {center}")
    
    # Bounding box
    print("\n--- Bounding Box ---")
    points = [Point(1, 2), Point(5, 8), Point(3, 1), Point(6, 4)]
    min_pt, max_pt = GeometryAlgorithms.bounding_box(points)
    print(f"Bounding box: {min_pt} to {max_pt}")


if __name__ == "__main__":
    main()
