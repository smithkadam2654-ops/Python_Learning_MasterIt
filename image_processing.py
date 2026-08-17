"""
Image Processing - Basic image manipulation and processing.
Features: Image operations, filters, transformations, and analysis.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class Pixel:
    """RGB pixel representation."""
    r: int
    g: int
    b: int
    
    def to_grayscale(self) -> int:
        """Convert pixel to grayscale using luminance formula."""
        return int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
    
    def invert(self) -> 'Pixel':
        """Invert pixel colors."""
        return Pixel(255 - self.r, 255 - self.g, 255 - self.b)
    
    def __add__(self, other: 'Pixel') -> 'Pixel':
        """Add two pixels."""
        return Pixel(
            min(255, self.r + other.r),
            min(255, self.g + other.g),
            min(255, self.b + other.b)
        )
    
    def __sub__(self, other: 'Pixel') -> 'Pixel':
        """Subtract two pixels."""
        return Pixel(
            max(0, self.r - other.r),
            max(0, self.g - other.g),
            max(0, self.b - other.b)
        )


@dataclass
class Image:
    """Simple image representation."""
    width: int
    height: int
    pixels: List[List[Pixel]]
    
    @classmethod
    def create_blank(cls, width: int, height: int, color: Tuple[int, int, int] = (0, 0, 0)) -> 'Image':
        """Create a blank image with specified color."""
        pixels = [[Pixel(*color) for _ in range(width)] for _ in range(height)]
        return cls(width, height, pixels)
    
    @classmethod
    def from_pixels(cls, pixels: List[List[Pixel]]) -> 'Image':
        """Create image from pixel array."""
        height = len(pixels)
        width = len(pixels[0]) if height > 0 else 0
        return cls(width, height, pixels)
    
    def get_pixel(self, x: int, y: int) -> Optional[Pixel]:
        """Get pixel at coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None
    
    def set_pixel(self, x: int, y: int, pixel: Pixel) -> None:
        """Set pixel at coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = pixel
    
    def to_grayscale(self) -> 'Image':
        """Convert image to grayscale."""
        new_pixels = []
        for row in self.pixels:
            gray_row = []
            for pixel in row:
                gray_value = pixel.to_grayscale()
                gray_row.append(Pixel(gray_value, gray_value, gray_value))
            new_pixels.append(gray_row)
        return Image.from_pixels(new_pixels)
    
    def invert(self) -> 'Image':
        """Invert image colors."""
        new_pixels = []
        for row in self.pixels:
            new_pixels.append([pixel.invert() for pixel in row])
        return Image.from_pixels(new_pixels)
    
    def resize(self, new_width: int, new_height: int) -> 'Image':
        """Resize image using nearest neighbor interpolation."""
        if new_width == 0 or new_height == 0:
            return Image.create_blank(0, 0)
        
        new_pixels = []
        x_ratio = self.width / new_width
        y_ratio = self.height / new_height
        
        for y in range(new_height):
            row = []
            for x in range(new_width):
                src_x = int(x * x_ratio)
                src_y = int(y * y_ratio)
                row.append(self.pixels[src_y][src_x])
            new_pixels.append(row)
        
        return Image.from_pixels(new_pixels)
    
    def crop(self, x: int, y: int, width: int, height: int) -> Optional['Image']:
        """Crop image to specified rectangle."""
        if x < 0 or y < 0 or width <= 0 or height <= 0:
            return None
        
        if x + width > self.width or y + height > self.height:
            return None
        
        new_pixels = []
        for row in self.pixels[y:y + height]:
            new_pixels.append(row[x:x + width])
        
        return Image.from_pixels(new_pixels)
    
    def rotate_90(self) -> 'Image':
        """Rotate image 90 degrees clockwise."""
        new_pixels = [[None] * self.height for _ in range(self.width)]
        
        for y in range(self.height):
            for x in range(self.width):
                new_pixels[x][self.height - 1 - y] = self.pixels[y][x]
        
        return Image(self.height, self.width, new_pixels)
    
    def flip_horizontal(self) -> 'Image':
        """Flip image horizontally."""
        new_pixels = [row[::-1] for row in self.pixels]
        return Image.from_pixels(new_pixels)
    
    def flip_vertical(self) -> 'Image':
        """Flip image vertically."""
        new_pixels = self.pixels[::-1]
        return Image.from_pixels(new_pixels)
    
    def apply_brightness(self, factor: float) -> 'Image':
        """Adjust image brightness."""
        new_pixels = []
        for row in self.pixels:
            new_row = []
            for pixel in row:
                new_row.append(Pixel(
                    min(255, max(0, int(pixel.r * factor))),
                    min(255, max(0, int(pixel.g * factor))),
                    min(255, max(0, int(pixel.b * factor)))
                ))
            new_pixels.append(new_row)
        return Image.from_pixels(new_pixels)
    
    def apply_contrast(self, factor: float) -> 'Image':
        """Adjust image contrast."""
        new_pixels = []
        for row in self.pixels:
            new_row = []
            for pixel in row:
                new_row.append(Pixel(
                    min(255, max(0, int((pixel.r - 128) * factor + 128))),
                    min(255, max(0, int((pixel.g - 128) * factor + 128))),
                    min(255, max(0, int((pixel.b - 128) * factor + 128)))
                ))
            new_pixels.append(new_row)
        return Image.from_pixels(new_pixels)
    
    def get_average_color(self) -> Pixel:
        """Calculate average color of image."""
        total_r = total_g = total_b = 0
        count = self.width * self.height
        
        for row in self.pixels:
            for pixel in row:
                total_r += pixel.r
                total_g += pixel.g
                total_b += pixel.b
        
        return Pixel(total_r // count, total_g // count, total_b // count)
    
    def add_border(self, border_size: int, color: Tuple[int, int, int] = (0, 0, 0)) -> 'Image':
        """Add border around image."""
        new_width = self.width + 2 * border_size
        new_height = self.height + 2 * border_size
        
        new_pixels = [[Pixel(*color) for _ in range(new_width)] for _ in range(new_height)]
        
        for y in range(self.height):
            for x in range(self.width):
                new_pixels[y + border_size][x + border_size] = self.pixels[y][x]
        
        return Image(new_width, new_height, new_pixels)


class ImageFilters:
    """Collection of image filters."""
    
    @staticmethod
    def apply_blur(image: Image, radius: int = 1) -> Image:
        """Apply simple box blur filter."""
        if radius <= 0:
            return image
        
        new_pixels = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                r_sum = g_sum = b_sum = 0
                count = 0
                
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < image.width and 0 <= ny < image.height:
                            pixel = image.pixels[ny][nx]
                            r_sum += pixel.r
                            g_sum += pixel.g
                            b_sum += pixel.b
                            count += 1
                
                row.append(Pixel(r_sum // count, g_sum // count, b_sum // count))
            new_pixels.append(row)
        
        return Image.from_pixels(new_pixels)
    
    @staticmethod
    def apply_sharpen(image: Image) -> Image:
        """Apply sharpening filter."""
        kernel = [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]
        return ImageFilters.apply_convolution(image, kernel)
    
    @staticmethod
    def apply_edge_detection(image: Image) -> Image:
        """Apply edge detection filter."""
        kernel = [
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ]
        return ImageFilters.apply_convolution(image, kernel)
    
    @staticmethod
    def apply_convolution(image: Image, kernel: List[List[int]]) -> Image:
        """Apply convolution with given kernel."""
        k_size = len(kernel)
        offset = k_size // 2
        
        new_pixels = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                r_sum = g_sum = b_sum = 0
                
                for ky in range(k_size):
                    for kx in range(k_size):
                        nx = x + kx - offset
                        ny = y + ky - offset
                        
                        if 0 <= nx < image.width and 0 <= ny < image.height:
                            pixel = image.pixels[ny][nx]
                            weight = kernel[ky][kx]
                            r_sum += pixel.r * weight
                            g_sum += pixel.g * weight
                            b_sum += pixel.b * weight
                
                row.append(Pixel(
                    min(255, max(0, r_sum)),
                    min(255, max(0, g_sum)),
                    min(255, max(0, b_sum))
                ))
            new_pixels.append(row)
        
        return Image.from_pixels(new_pixels)
    
    @staticmethod
    def apply_sepia(image: Image) -> Image:
        """Apply sepia tone filter."""
        new_pixels = []
        for row in image.pixels:
            new_row = []
            for pixel in row:
                r = min(255, int(pixel.r * 0.393 + pixel.g * 0.769 + pixel.b * 0.189))
                g = min(255, int(pixel.r * 0.349 + pixel.g * 0.686 + pixel.b * 0.168))
                b = min(255, int(pixel.r * 0.272 + pixel.g * 0.534 + pixel.b * 0.131))
                new_row.append(Pixel(r, g, b))
            new_pixels.append(new_row)
        return Image.from_pixels(new_pixels)


def create_gradient_image(width: int, height: int, 
                         start_color: Tuple[int, int, int], 
                         end_color: Tuple[int, int, int]) -> Image:
    """Create a gradient image."""
    pixels = []
    
    for y in range(height):
        row = []
        for x in range(width):
            t = x / width if width > 0 else 0
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            
            row.append(Pixel(r, g, b))
        pixels.append(row)
    
    return Image.from_pixels(pixels)


def main() -> None:
    """Demonstrate image processing operations."""
    
    print("=== Image Creation ===")
    # Create a simple test image
    image = Image.create_blank(10, 10, (255, 0, 0))
    print(f"Created {image.width}x{image.height} red image")
    
    # Create gradient
    gradient = create_gradient_image(20, 10, (255, 0, 0), (0, 0, 255))
    print(f"Created {gradient.width}x{gradient.height} gradient image")
    
    print("\n=== Image Operations ===")
    # Test pixel operations
    pixel = Pixel(100, 150, 200)
    print(f"Original pixel: ({pixel.r}, {pixel.g}, {pixel.b})")
    print(f"Grayscale: {pixel.to_grayscale()}")
    print(f"Inverted: {pixel.invert()}")
    
    print("\n=== Image Transformations ===")
    small_image = Image.create_blank(5, 5, (128, 128, 128))
    print(f"Original: {small_image.width}x{small_image.height}")
    
    resized = small_image.resize(10, 10)
    print(f"Resized: {resized.width}x{resized.height}")
    
    rotated = small_image.rotate_90()
    print(f"Rotated: {rotated.width}x{rotated.height}")
    
    cropped = small_image.crop(1, 1, 3, 3)
    if cropped:
        print(f"Cropped: {cropped.width}x{cropped.height}")
    
    print("\n=== Color Adjustments ===")
    test_image = Image.create_blank(5, 5, (100, 100, 100))
    brightened = test_image.apply_brightness(1.5)
    contrasted = test_image.apply_contrast(1.5)
    
    avg_color = test_image.get_average_color()
    print(f"Average color: ({avg_color.r}, {avg_color.g}, {avg_color.b})")
    
    print("\n=== Image Filters ===")
    filters = ImageFilters()
    
    # Create a test pattern
    pattern_pixels = []
    for y in range(5):
        row = []
        for x in range(5):
            color = (255, 255, 255) if (x + y) % 2 == 0 else (0, 0, 0)
            row.append(Pixel(*color))
        pattern_pixels.append(row)
    
    pattern = Image.from_pixels(pattern_pixels)
    
    blurred = filters.apply_blur(pattern, radius=1)
    sharpened = filters.apply_sharpen(pattern)
    sepia = filters.apply_sepia(pattern)
    
    print(f"Applied blur, sharpen, and sepia filters")
    
    print("\n=== Border Addition ===")
    bordered = test_image.add_border(2, (0, 0, 0))
    print(f"Original: {test_image.width}x{test_image.height}")
    print(f"With border: {bordered.width}x{bordered.height}")


if __name__ == "__main__":
    main()
