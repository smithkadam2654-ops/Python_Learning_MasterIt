"""
3D Graphics Module

This module provides comprehensive 3D graphics utilities including:
- 3D vector mathematics
- Matrix operations
- 3D transformations
- Camera projection
- 3D primitives
- Ray tracing concepts
- Lighting calculations
- Texture mapping concepts
- 3D object representation
- Rendering pipeline concepts

All functions include comprehensive docstrings and type hints.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class CoordinateSystem(Enum):
    """Coordinate system types."""
    CARTESIAN = "cartesian"
    SPHERICAL = "spherical"
    CYLINDRICAL = "cylindrical"


class ProjectionType(Enum):
    """Projection types."""
    PERSPECTIVE = "perspective"
    ORTHOGRAPHIC = "orthographic"


@dataclass
class Vector3:
    """3D vector class."""
    x: float
    y: float
    z: float
    
    def __add__(self, other: 'Vector3') -> 'Vector3':
        """Add vectors."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        """Subtract vectors."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3':
        """Multiply by scalar."""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector3':
        """Divide by scalar."""
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def dot(self, other: 'Vector3') -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3') -> 'Vector3':
        """Cross product."""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def magnitude(self) -> float:
        """Calculate magnitude."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> 'Vector3':
        """Normalize vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return self / mag
    
    def distance_to(self, other: 'Vector3') -> float:
        """Calculate distance to another vector."""
        return (self - other).magnitude()
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple."""
        return (self.x, self.y, self.z)
    
    def to_list(self) -> List[float]:
        """Convert to list."""
        return [self.x, self.y, self.z]
    
    def reflect(self, normal: 'Vector3') -> 'Vector3':
        """Reflect vector around normal."""
        dot = self.dot(normal)
        return self - normal * 2.0 * dot


class Matrix4:
    """4x4 matrix for 3D transformations."""
    
    def __init__(self, values: Optional[List[List[float]]] = None):
        """Initialize matrix."""
        if values is None:
            self.values = [[0.0] * 4 for _ in range(4)]
            # Identity matrix
            for i in range(4):
                self.values[i][i] = 1.0
        else:
            self.values = values
    
    @staticmethod
    def identity() -> 'Matrix4':
        """Create identity matrix."""
        return Matrix4()
    
    @staticmethod
    def translation(x: float, y: float, z: float) -> 'Matrix4':
        """Create translation matrix."""
        matrix = Matrix4.identity()
        matrix.values[0][3] = x
        matrix.values[1][3] = y
        matrix.values[2][3] = z
        return matrix
    
    @staticmethod
    def rotation_x(angle: float) -> 'Matrix4':
        """Create rotation matrix around X axis."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        matrix = Matrix4.identity()
        matrix.values[1][1] = cos_a
        matrix.values[1][2] = -sin_a
        matrix.values[2][1] = sin_a
        matrix.values[2][2] = cos_a
        
        return matrix
    
    @staticmethod
    def rotation_y(angle: float) -> 'Matrix4':
        """Create rotation matrix around Y axis."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        matrix = Matrix4.identity()
        matrix.values[0][0] = cos_a
        matrix.values[0][2] = sin_a
        matrix.values[2][0] = -sin_a
        matrix.values[2][2] = cos_a
        
        return matrix
    
    @staticmethod
    def rotation_z(angle: float) -> 'Matrix4':
        """Create rotation matrix around Z axis."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        matrix = Matrix4.identity()
        matrix.values[0][0] = cos_a
        matrix.values[0][1] = -sin_a
        matrix.values[1][0] = sin_a
        matrix.values[1][1] = cos_a
        
        return matrix
    
    @staticmethod
    def scale(sx: float, sy: float, sz: float) -> 'Matrix4':
        """Create scale matrix."""
        matrix = Matrix4.identity()
        matrix.values[0][0] = sx
        matrix.values[1][1] = sy
        matrix.values[2][2] = sz
        return matrix
    
    def multiply(self, other: 'Matrix4') -> 'Matrix4':
        """Multiply matrices."""
        result = Matrix4([[0.0] * 4 for _ in range(4)])
        
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result.values[i][j] += self.values[i][k] * other.values[k][j]
        
        return result
    
    def transform_vector(self, vector: Vector3) -> Vector3:
        """Transform 3D vector by matrix."""
        x = vector.x
        y = vector.y
        z = vector.z
        
        new_x = self.values[0][0] * x + self.values[0][1] * y + self.values[0][2] * z + self.values[0][3]
        new_y = self.values[1][0] * x + self.values[1][1] * y + self.values[1][2] * z + self.values[1][3]
        new_z = self.values[2][0] * x + self.values[2][1] * y + self.values[2][2] * z + self.values[2][3]
        
        return Vector3(new_x, new_y, new_z)


class Camera:
    """Camera for 3D rendering."""
    
    def __init__(self, position: Vector3, target: Vector3, up: Vector3):
        """Initialize camera."""
        self.position = position
        self.target = target
        self.up = up
        self.fov = 60.0  # Field of view in degrees
        self.aspect_ratio = 1.0
        self.near_plane = 0.1
        self.far_plane = 100.0
    
    def get_view_matrix(self) -> Matrix4:
        """Get view matrix."""
        # Calculate camera axes
        forward = (self.target - self.position).normalize()
        right = forward.cross(self.up).normalize()
        up = right.cross(forward)
        
        # Create view matrix
        view = Matrix4.identity()
        
        view.values[0][0] = right.x
        view.values[0][1] = right.y
        view.values[0][2] = right.z
        view.values[0][3] = -right.dot(self.position)
        
        view.values[1][0] = up.x
        view.values[1][1] = up.y
        view.values[1][2] = up.z
        view.values[1][3] = -up.dot(self.position)
        
        view.values[2][0] = -forward.x
        view.values[2][1] = -forward.y
        view.values[2][2] = -forward.z
        view.values[2][3] = forward.dot(self.position)
        
        return view
    
    def get_projection_matrix(self, projection_type: ProjectionType = ProjectionType.PERSPECTIVE) -> Matrix4:
        """Get projection matrix."""
        if projection_type == ProjectionType.PERSPECTIVE:
            return self._perspective_projection()
        else:
            return self._orthographic_projection()
    
    def _perspective_projection(self) -> Matrix4:
        """Perspective projection matrix."""
        fov_rad = math.radians(self.fov)
        f = 1.0 / math.tan(fov_rad / 2.0)
        
        proj = Matrix4()
        proj.values[0][0] = f / self.aspect_ratio
        proj.values[1][1] = f
        proj.values[2][2] = (self.far_plane + self.near_plane) / (self.near_plane - self.far_plane)
        proj.values[2][3] = (2 * self.far_plane * self.near_plane) / (self.near_plane - self.far_plane)
        proj.values[3][2] = -1.0
        proj.values[3][3] = 0.0
        
        return proj
    
    def _orthographic_projection(self) -> Matrix4:
        """Orthographic projection matrix."""
        left = -self.aspect_ratio
        right = self.aspect_ratio
        bottom = -1.0
        top = 1.0
        
        proj = Matrix4()
        proj.values[0][0] = 2.0 / (right - left)
        proj.values[1][1] = 2.0 / (top - bottom)
        proj.values[2][2] = -2.0 / (self.far_plane - self.near_plane)
        proj.values[0][3] = -(right + left) / (right - left)
        proj.values[1][3] = -(top + bottom) / (top - bottom)
        proj.values[2][3] = -(self.far_plane + self.near_plane) / (self.far_plane - self.near_plane)
        
        return proj


class Vertex:
    """3D vertex with attributes."""
    
    def __init__(self, position: Vector3, normal: Optional[Vector3] = None,
                 tex_coords: Optional[Tuple[float, float]] = None):
        """Initialize vertex."""
        self.position = position
        self.normal = normal if normal else Vector3(0, 0, 1)
        self.tex_coords = tex_coords if tex_coords else (0.0, 0.0)


class Mesh:
    """3D mesh composed of vertices and faces."""
    
    def __init__(self, name: str = "mesh"):
        """Initialize mesh."""
        self.name = name
        self.vertices: List[Vertex] = []
        self.indices: List[int] = []
        self.material: Optional[str] = None
    
    def add_vertex(self, vertex: Vertex) -> int:
        """Add vertex to mesh."""
        self.vertices.append(vertex)
        return len(self.vertices) - 1
    
    def add_triangle(self, v1: int, v2: int, v3: int) -> None:
        """Add triangle face."""
        self.indices.extend([v1, v2, v3])
    
    def calculate_normals(self) -> None:
        """Calculate vertex normals."""
        # Reset normals
        for vertex in self.vertices:
            vertex.normal = Vector3(0, 0, 0)
        
        # Calculate face normals
        for i in range(0, len(self.indices), 3):
            v1 = self.vertices[self.indices[i]]
            v2 = self.vertices[self.indices[i + 1]]
            v3 = self.vertices[self.indices[i + 2]]
            
            # Calculate face normal
            edge1 = v2.position - v1.position
            edge2 = v3.position - v1.position
            face_normal = edge1.cross(edge2).normalize()
            
            # Add to vertex normals
            v1.normal = v1.normal + face_normal
            v2.normal = v2.normal + face_normal
            v3.normal = v3.normal + face_normal
        
        # Normalize vertex normals
        for vertex in self.vertices:
            vertex.normal = vertex.normal.normalize()


class PrimitiveGenerator:
    """Generate 3D primitives."""
    
    @staticmethod
    def create_cube(size: float = 1.0) -> Mesh:
        """Create cube mesh."""
        mesh = Mesh("cube")
        half_size = size / 2.0
        
        # Create vertices
        vertices = [
            Vector3(-half_size, -half_size, -half_size),
            Vector3(half_size, -half_size, -half_size),
            Vector3(half_size, half_size, -half_size),
            Vector3(-half_size, half_size, -half_size),
            Vector3(-half_size, -half_size, half_size),
            Vector3(half_size, -half_size, half_size),
            Vector3(half_size, half_size, half_size),
            Vector3(-half_size, half_size, half_size),
        ]
        
        for vertex in vertices:
            mesh.add_vertex(Vertex(vertex))
        
        # Create faces
        faces = [
            (0, 1, 2), (0, 2, 3),  # Front
            (4, 5, 6), (4, 6, 7),  # Back
            (0, 4, 7), (0, 7, 3),  # Left
            (1, 5, 6), (1, 6, 2),  # Right
            (3, 2, 6), (3, 6, 7),  # Top
            (0, 1, 5), (0, 5, 4),  # Bottom
        ]
        
        for face in faces:
            mesh.add_triangle(*face)
        
        mesh.calculate_normals()
        return mesh
    
    @staticmethod
    def create_sphere(radius: float = 1.0, segments: int = 16) -> Mesh:
        """Create sphere mesh."""
        mesh = Mesh("sphere")
        
        # Create vertices
        for i in range(segments + 1):
            lat = math.pi * i / segments
            for j in range(segments + 1):
                lon = 2 * math.pi * j / segments
                
                x = radius * math.sin(lat) * math.cos(lon)
                y = radius * math.cos(lat)
                z = radius * math.sin(lat) * math.sin(lon)
                
                mesh.add_vertex(Vertex(Vector3(x, y, z)))
        
        # Create faces
        for i in range(segments):
            for j in range(segments):
                v1 = i * (segments + 1) + j
                v2 = v1 + 1
                v3 = (i + 1) * (segments + 1) + j
                v4 = v3 + 1
                
                mesh.add_triangle(v1, v2, v3)
                mesh.add_triangle(v2, v4, v3)
        
        mesh.calculate_normals()
        return mesh
    
    @staticmethod
    def create_plane(width: float = 1.0, height: float = 1.0, 
                    segments_x: int = 1, segments_y: int = 1) -> Mesh:
        """Create plane mesh."""
        mesh = Mesh("plane")
        
        half_width = width / 2.0
        half_height = height / 2.0
        
        # Create vertices
        for i in range(segments_y + 1):
            for j in range(segments_x + 1):
                x = (j / segments_x - 0.5) * width
                y = (i / segments_y - 0.5) * height
                mesh.add_vertex(Vertex(Vector3(x, 0.0, y)))
        
        # Create faces
        for i in range(segments_y):
            for j in range(segments_x):
                v1 = i * (segments_x + 1) + j
                v2 = v1 + 1
                v3 = (i + 1) * (segments_x + 1) + j
                v4 = v3 + 1
                
                mesh.add_triangle(v1, v2, v3)
                mesh.add_triangle(v2, v4, v3)
        
        mesh.calculate_normals()
        return mesh


class Ray:
    """Ray for ray tracing."""
    
    def __init__(self, origin: Vector3, direction: Vector3):
        """Initialize ray."""
        self.origin = origin
        self.direction = direction.normalize()
    
    def at(self, t: float) -> Vector3:
        """Get point at distance t along ray."""
        return self.origin + self.direction * t


class Lighting:
    """Lighting calculations."""
    
    @staticmethod
    def calculate_phong_lighting(
        position: Vector3,
        normal: Vector3,
        view_dir: Vector3,
        light_pos: Vector3,
        light_color: Vector3,
        material_color: Vector3,
        ambient_strength: float = 0.1,
        diffuse_strength: float = 0.7,
        specular_strength: float = 0.3,
        shininess: float = 32.0
    ) -> Vector3:
        """Calculate Phong lighting."""
        # Ambient
        ambient = light_color * ambient_strength
        
        # Diffuse
        light_dir = (light_pos - position).normalize()
        diffuse_intensity = max(0.0, normal.dot(light_dir))
        diffuse = light_color * diffuse_strength * diffuse_intensity
        
        # Specular
        reflect_dir = (-light_dir).reflect(normal)
        specular_intensity = max(0.0, view_dir.dot(reflect_dir)) ** shininess
        specular = light_color * specular_strength * specular_intensity
        
        # Combine
        result = (ambient + diffuse + specular) * material_color
        return result


class Transform3D:
    """3D transformation utilities."""
    
    @staticmethod
    def apply_transform(mesh: Mesh, matrix: Matrix4) -> Mesh:
        """Apply transformation matrix to mesh."""
        transformed = Mesh(mesh.name + "_transformed")
        
        for vertex in mesh.vertices:
            new_position = matrix.transform_vector(vertex.position)
            transformed.add_vertex(Vertex(new_position, vertex.normal, vertex.tex_coords))
        
        transformed.indices = mesh.indices.copy()
        return transformed
    
    @staticmethod
    def combine_transforms(transforms: List[Matrix4]) -> Matrix4:
        """Combine multiple transformations."""
        if not transforms:
            return Matrix4.identity()
        
        result = transforms[0]
        for transform in transforms[1:]:
            result = result.multiply(transform)
        
        return result


class Texture:
    """Texture mapping concepts."""
    
    @staticmethod
    def sample_nearest(texture_data: List[List[Tuple[int, int, int]]],
                     u: float, v: float) -> Tuple[int, int, int]:
        """Sample texture using nearest neighbor."""
        height = len(texture_data)
        width = len(texture_data[0])
        
        x = int(u * (width - 1))
        y = int(v * (height - 1))
        
        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))
        
        return texture_data[y][x]
    
    @staticmethod
    def sample_bilinear(texture_data: List[List[Tuple[int, int, int]]],
                       u: float, v: float) -> Tuple[int, int, int]:
        """Sample texture using bilinear interpolation."""
        height = len(texture_data)
        width = len(texture_data[0])
        
        x = u * (width - 1)
        y = v * (height - 1)
        
        x0 = int(x)
        y0 = int(y)
        x1 = min(x0 + 1, width - 1)
        y1 = min(y0 + 1, height - 1)
        
        fx = x - x0
        fy = y - y0
        
        # Sample four corners
        c00 = texture_data[y0][x0]
        c10 = texture_data[y0][x1]
        c01 = texture_data[y1][x0]
        c11 = texture_data[y1][x1]
        
        # Interpolate
        c0 = tuple(int(c00[i] * (1 - fx) + c10[i] * fx) for i in range(3))
        c1 = tuple(int(c01[i] * (1 - fx) + c11[i] * fx) for i in range(3))
        
        result = tuple(int(c0[i] * (1 - fy) + c1[i] * fy) for i in range(3))
        return result


class Renderer:
    """Simple 3D renderer concepts."""
    
    def __init__(self, camera: Camera):
        """Initialize renderer."""
        self.camera = camera
        self.meshes: List[Mesh] = []
    
    def add_mesh(self, mesh: Mesh) -> None:
        """Add mesh to scene."""
        self.meshes.append(mesh)
    
    def project_point(self, point: Vector3) -> Tuple[float, float, float]:
        """Project 3D point to 2D screen coordinates."""
        # Get view and projection matrices
        view_matrix = self.camera.get_view_matrix()
        proj_matrix = self.camera.get_projection_matrix()
        
        # Transform point
        view_pos = view_matrix.transform_vector(point)
        clip_pos = proj_matrix.transform_vector(view_pos)
        
        # Perspective divide
        if clip_pos.z != 0:
            ndc_x = clip_pos.x / clip_pos.z
            ndc_y = clip_pos.y / clip_pos.z
        else:
            ndc_x = clip_pos.x
            ndc_y = clip_pos.y
        
        # Convert to screen coordinates
        screen_x = (ndc_x + 1.0) / 2.0 * 800  # Assuming 800 width
        screen_y = (1.0 - ndc_y) / 2.0 * 600  # Assuming 600 height
        
        return screen_x, screen_y, clip_pos.z


def demonstrate_3d_graphics():
    """Demonstrate 3D graphics functionality."""
    print("=== 3D Graphics Demonstration ===\n")
    
    # Vector Operations
    print("1. Vector Operations:")
    v1 = Vector3(1.0, 2.0, 3.0)
    v2 = Vector3(4.0, 5.0, 6.0)
    
    v_sum = v1 + v2
    v_diff = v1 - v2
    v_scaled = v1 * 2.0
    
    print(f"   v1 + v2: {v_sum.to_tuple()}")
    print(f"   v1 - v2: {v_diff.to_tuple()}")
    print(f"   v1 * 2: {v_scaled.to_tuple()}")
    
    dot_product = v1.dot(v2)
    cross_product = v1.cross(v2)
    
    print(f"   Dot product: {dot_product}")
    print(f"   Cross product: {cross_product.to_tuple()}")
    
    magnitude = v1.magnitude()
    normalized = v1.normalize()
    
    print(f"   Magnitude: {magnitude:.4f}")
    print(f"   Normalized: {normalized.to_tuple()}")
    
    # Matrix Operations
    print("\n2. Matrix Operations:")
    trans_matrix = Matrix4.translation(1.0, 2.0, 3.0)
    rot_matrix = Matrix4.rotation_x(math.pi / 4)
    scale_matrix = Matrix4.scale(2.0, 2.0, 2.0)
    
    combined = trans_matrix.multiply(rot_matrix)
    print(f"   Combined matrix applied to (1,0,0): {combined.transform_vector(Vector3(1, 0, 0)).to_tuple()}")
    
    # Camera
    print("\n3. Camera:")
    camera = Camera(
        position=Vector3(0, 0, 5),
        target=Vector3(0, 0, 0),
        up=Vector3(0, 1, 0)
    )
    
    view_matrix = camera.get_view_matrix()
    proj_matrix = camera.get_projection_matrix()
    
    print(f"   Camera position: {camera.position.to_tuple()}")
    print(f"   FOV: {camera.fov} degrees")
    
    # Primitives
    print("\n4. 3D Primitives:")
    cube = PrimitiveGenerator.create_cube(2.0)
    sphere = PrimitiveGenerator.create_sphere(1.0, segments=8)
    plane = PrimitiveGenerator.create_plane(4.0, 4.0, segments_x=2, segments_y=2)
    
    print(f"   Cube vertices: {len(cube.vertices)}")
    print(f"   Cube faces: {len(cube.indices) // 3}")
    print(f"   Sphere vertices: {len(sphere.vertices)}")
    print(f"   Plane vertices: {len(plane.vertices)}")
    
    # Transformations
    print("\n5. 3D Transformations:")
    transforms = [
        Matrix4.translation(1.0, 0.0, 0.0),
        Matrix4.rotation_y(math.pi / 6),
        Matrix4.scale(1.5, 1.5, 1.5)
    ]
    
    combined_transform = Transform3D.combine_transforms(transforms)
    transformed_cube = Transform3D.apply_transform(cube, combined_transform)
    
    print(f"   Transformed cube vertices: {len(transformed_cube.vertices)}")
    
    # Lighting
    print("\n6. Lighting Calculations:")
    position = Vector3(0, 0, 0)
    normal = Vector3(0, 1, 0)
    view_dir = Vector3(0, 0, -1)
    light_pos = Vector3(2, 2, 2)
    
    light_color = Vector3(1.0, 1.0, 1.0)
    material_color = Vector3(0.8, 0.2, 0.2)
    
    lighting = Lighting.calculate_phong_lighting(
        position, normal, view_dir, light_pos, light_color, material_color
    )
    
    print(f"   Phong lighting result: {lighting.to_tuple()}")
    
    # Ray
    print("\n7. Ray Tracing Concepts:")
    ray = Ray(Vector3(0, 0, 0), Vector3(1, 1, 1))
    point_at_t = ray.at(2.0)
    
    print(f"   Ray origin: {ray.origin.to_tuple()}")
    print(f"   Ray direction: {ray.direction.to_tuple()}")
    print(f"   Point at t=2: {point_at_t.to_tuple()}")
    
    # Texture
    print("\n8. Texture Sampling:")
    texture_data = [
        [(255, 0, 0), (0, 255, 0)],
        [(0, 0, 255), (255, 255, 0)]
    ]
    
    nearest = Texture.sample_nearest(texture_data, 0.5, 0.5)
    bilinear = Texture.sample_bilinear(texture_data, 0.5, 0.5)
    
    print(f"   Nearest sample: {nearest}")
    print(f"   Bilinear sample: {bilinear}")
    
    # Rendering
    print("\n9. Rendering Concepts:")
    renderer = Renderer(camera)
    renderer.add_mesh(cube)
    renderer.add_mesh(sphere)
    
    point = Vector3(1, 1, 1)
    screen_x, screen_y, depth = renderer.project_point(point)
    
    print(f"   Projected point (1,1,1): ({screen_x:.2f}, {screen_y:.2f}), depth: {depth:.4f}")
    
    print("\n=== Demonstration Complete ===")
    print("\n3D Graphics Best Practices:")
    print("- Use appropriate coordinate systems for your application")
    print("- Normalize vectors before lighting calculations")
    print("- Use efficient data structures for large meshes")
    print("- Consider using GPU acceleration for rendering")
    print("- Implement proper culling for performance")
    print("- Use appropriate projection for your use case")
    print("- Handle edge cases in matrix operations")
    print("- Use consistent winding order for faces")
    print("- Implement proper texture filtering")
    print("- Consider LOD (Level of Detail) for distant objects")
    print("- Use frustum culling to eliminate off-screen objects")
    print("- Implement proper z-buffering for depth sorting")
    print("- Consider using existing graphics libraries (OpenGL, DirectX)")


if __name__ == "__main__":
    demonstrate_3d_graphics()
