"""
Computer Vision Module

This module provides comprehensive computer vision utilities including:
- Image processing basics
- Edge detection
- Color space conversion
- Image segmentation
- Feature detection
- Image transformations
- Object detection concepts
- Image filtering
- Contour detection
- Image histograms

Note: This module uses numpy for numerical operations and opencv-python for advanced features.
Install with: pip install numpy opencv-python

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

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class ColorSpace(Enum):
    """Color space types."""
    RGB = "rgb"
    GRAY = "gray"
    HSV = "hsv"
    LAB = "lab"
    YUV = "yuv"


class EdgeDetectionMethod(Enum):
    """Edge detection methods."""
    SOBEL = "sobel"
    PREWITT = "prewitt"
    LAPLACIAN = "laplacian"
    CANNY = "canny"


@dataclass
class Image:
    """Image data structure."""
    pixels: List[List[List[int]]]  # [height][width][channels]
    width: int
    height: int
    channels: int
    color_space: ColorSpace = ColorSpace.RGB
    
    def get_pixel(self, x: int, y: int) -> List[int]:
        """Get pixel at coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return [0] * self.channels
    
    def set_pixel(self, x: int, y: int, color: List[int]) -> None:
        """Set pixel at coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color


class ImageLoader:
    """Image loading utilities."""
    
    @staticmethod
    def create_blank_image(width: int, height: int, 
                          color: Tuple[int, int, int] = (0, 0, 0),
                          channels: int = 3) -> Image:
        """Create blank image."""
        pixels = [[[color[0], color[1], color[2]] for _ in range(width)] 
                 for _ in range(height)]
        
        return Image(
            pixels=pixels,
            width=width,
            height=height,
            channels=channels
        )
    
    @staticmethod
    def create_gradient_image(width: int, height: int,
                             start_color: Tuple[int, int, int],
                             end_color: Tuple[int, int, int]) -> Image:
        """Create gradient image."""
        pixels = []
        
        for y in range(height):
            row = []
            ratio = y / height
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            for x in range(width):
                row.append([r, g, b])
            
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=width,
            height=height,
            channels=3
        )
    
    @staticmethod
    def load_from_array(array: List[List[List[int]]]) -> Image:
        """Load image from array."""
        if not array or not array[0]:
            return ImageLoader.create_blank_image(1, 1)
        
        height = len(array)
        width = len(array[0])
        channels = len(array[0][0])
        
        return Image(
            pixels=array,
            width=width,
            height=height,
            channels=channels
        )


class ColorSpaceConverter:
    """Color space conversion utilities."""
    
    @staticmethod
    def rgb_to_grayscale(image: Image) -> Image:
        """Convert RGB image to grayscale."""
        pixels = []
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                pixel = image.get_pixel(x, y)
                # Luminance formula
                gray = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
                row.append([gray])
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=1,
            color_space=ColorSpace.GRAY
        )
    
    @staticmethod
    def rgb_to_hsv(image: Image) -> Image:
        """Convert RGB to HSV (simplified)."""
        pixels = []
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                pixel = image.get_pixel(x, y)
                r, g, b = pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0
                
                cmax = max(r, g, b)
                cmin = min(r, g, b)
                delta = cmax - cmin
                
                # Hue
                if delta == 0:
                    h = 0
                elif cmax == r:
                    h = 60 * (((g - b) / delta) % 6)
                elif cmax == g:
                    h = 60 * (((b - r) / delta) + 2)
                else:
                    h = 60 * (((r - g) / delta) + 4)
                
                # Saturation
                s = 0 if cmax == 0 else (delta / cmax)
                
                # Value
                v = cmax
                
                row.append([int(h), int(s * 255), int(v * 255)])
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=3,
            color_space=ColorSpace.HSV
        )


class ImageFilter:
    """Image filtering operations."""
    
    @staticmethod
    def apply_gaussian_blur(image: Image, kernel_size: int = 3) -> Image:
        """Apply Gaussian blur."""
        if not NUMPY_AVAILABLE:
            return image
        
        kernel = ImageFilter._gaussian_kernel(kernel_size)
        return ImageFilter._apply_convolution(image, kernel)
    
    @staticmethod
    def _gaussian_kernel(size: int) -> List[List[float]]:
        """Generate Gaussian kernel."""
        kernel = []
        sigma = size / 3.0
        
        for i in range(size):
            row = []
            for j in range(size):
                x = i - size // 2
                y = j - size // 2
                value = math.exp(-(x**2 + y**2) / (2 * sigma**2))
                row.append(value)
            kernel.append(row)
        
        # Normalize
        total = sum(sum(row) for row in kernel)
        kernel = [[value / total for value in row] for row in kernel]
        
        return kernel
    
    @staticmethod
    def apply_median_filter(image: Image, kernel_size: int = 3) -> Image:
        """Apply median filter for noise reduction."""
        pixels = []
        offset = kernel_size // 2
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                # Get neighborhood
                neighborhood = []
                for dy in range(-offset, offset + 1):
                    for dx in range(-offset, offset + 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < image.height and 0 <= nx < image.width:
                            pixel = image.get_pixel(nx, ny)
                            neighborhood.append(pixel[0])  # Use first channel
                
                if neighborhood:
                    median = sorted(neighborhood)[len(neighborhood) // 2]
                    row.append([median] * image.channels)
                else:
                    row.append(image.get_pixel(x, y))
            
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=image.channels
        )
    
    @staticmethod
    def apply_sharpen(image: Image) -> Image:
        """Apply sharpening filter."""
        kernel = [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]
        
        return ImageFilter._apply_convolution(image, kernel)
    
    @staticmethod
    def _apply_convolution(image: Image, kernel: List[List[float]]) -> Image:
        """Apply convolution with kernel."""
        if not NUMPY_AVAILABLE:
            return image
        
        pixels = []
        kernel_height = len(kernel)
        kernel_width = len(kernel[0])
        offset_y = kernel_height // 2
        offset_x = kernel_width // 2
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                # Apply convolution
                sum_values = [0.0] * image.channels
                
                for ky in range(kernel_height):
                    for kx in range(kernel_width):
                        ny = y + ky - offset_y
                        nx = x + kx - offset_x
                        
                        if 0 <= ny < image.height and 0 <= nx < image.width:
                            pixel = image.get_pixel(nx, ny)
                            weight = kernel[ky][kx]
                            
                            for c in range(image.channels):
                                sum_values[c] += pixel[c] * weight
                
                # Clamp values
                clamped = [max(0, min(255, int(value))) for value in sum_values]
                row.append(clamped)
            
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=image.channels
        )


class EdgeDetection:
    """Edge detection algorithms."""
    
    @staticmethod
    def sobel(image: Image) -> Image:
        """Apply Sobel edge detection."""
        # Convert to grayscale first
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        # Sobel kernels
        sobel_x = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        
        sobel_y = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
        
        # Apply both kernels
        grad_x = ImageFilter._apply_convolution(gray, sobel_x)
        grad_y = ImageFilter._apply_convolution(gray, sobel_y)
        
        # Combine gradients
        pixels = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                gx = grad_x.get_pixel(x, y)[0]
                gy = grad_y.get_pixel(x, y)[0]
                magnitude = math.sqrt(gx**2 + gy**2)
                row.append([int(magnitude)])
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=1
        )
    
    @staticmethod
    def prewitt(image: Image) -> Image:
        """Apply Prewitt edge detection."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        prewitt_x = [
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ]
        
        prewitt_y = [
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
        ]
        
        grad_x = ImageFilter._apply_convolution(gray, prewitt_x)
        grad_y = ImageFilter._apply_convolution(gray, prewitt_y)
        
        pixels = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                gx = grad_x.get_pixel(x, y)[0]
                gy = grad_y.get_pixel(x, y)[0]
                magnitude = math.sqrt(gx**2 + gy**2)
                row.append([int(magnitude)])
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=1
        )
    
    @staticmethod
    def laplacian(image: Image) -> Image:
        """Apply Laplacian edge detection."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        laplacian_kernel = [
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ]
        
        return ImageFilter._apply_convolution(gray, laplacian_kernel)


class ImageTransformation:
    """Image transformation utilities."""
    
    @staticmethod
    def resize(image: Image, new_width: int, new_height: int) -> Image:
        """Resize image using nearest neighbor."""
        pixels = []
        
        x_ratio = image.width / new_width
        y_ratio = image.height / new_height
        
        for y in range(new_height):
            row = []
            for x in range(new_width):
                src_x = int(x * x_ratio)
                src_y = int(y * y_ratio)
                pixel = image.get_pixel(src_x, src_y)
                row.append(pixel)
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=new_width,
            height=new_height,
            channels=image.channels
        )
    
    @staticmethod
    def rotate(image: Image, angle: float) -> Image:
        """Rotate image by angle (degrees)."""
        if not NUMPY_AVAILABLE:
            return image
        
        radians = math.radians(angle)
        cos_a = math.cos(radians)
        sin_a = math.sin(radians)
        
        # Calculate new dimensions
        new_width = int(abs(image.width * cos_a) + abs(image.height * sin_a))
        new_height = int(abs(image.width * sin_a) + abs(image.height * cos_a))
        
        pixels = [[[0] * image.channels for _ in range(new_width)] 
                 for _ in range(new_height)]
        
        # Rotate
        center_x = image.width / 2
        center_y = image.height / 2
        new_center_x = new_width / 2
        new_center_y = new_height / 2
        
        for y in range(new_height):
            for x in range(new_width):
                # Calculate source position
                rel_x = x - new_center_x
                rel_y = y - new_center_y
                
                src_x = int(rel_x * cos_a + rel_y * sin_a + center_x)
                src_y = int(-rel_x * sin_a + rel_y * cos_a + center_y)
                
                if 0 <= src_x < image.width and 0 <= src_y < image.height:
                    pixels[y][x] = image.get_pixel(src_x, src_y)
        
        return Image(
            pixels=pixels,
            width=new_width,
            height=new_height,
            channels=image.channels
        )
    
    @staticmethod
    def flip_horizontal(image: Image) -> Image:
        """Flip image horizontally."""
        pixels = []
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                pixel = image.get_pixel(image.width - 1 - x, y)
                row.append(pixel)
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=image.channels
        )
    
    @staticmethod
    def flip_vertical(image: Image) -> Image:
        """Flip image vertically."""
        pixels = []
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                pixel = image.get_pixel(x, image.height - 1 - y)
                row.append(pixel)
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=image.channels
        )


class ImageSegmentation:
    """Image segmentation utilities."""
    
    @staticmethod
    def threshold(image: Image, threshold: int = 128) -> Image:
        """Apply threshold segmentation."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        pixels = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                pixel = gray.get_pixel(x, y)[0]
                value = 255 if pixel > threshold else 0
                row.append([value])
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=1
        )
    
    @staticmethod
    def adaptive_threshold(image: Image, block_size: int = 11) -> Image:
        """Apply adaptive threshold."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        pixels = []
        offset = block_size // 2
        
        for y in range(image.height):
            row = []
            for x in range(image.width):
                # Calculate local threshold
                local_sum = 0
                local_count = 0
                
                for dy in range(-offset, offset + 1):
                    for dx in range(-offset, offset + 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < image.height and 0 <= nx < image.width:
                            local_sum += gray.get_pixel(nx, ny)[0]
                            local_count += 1
                
                local_threshold = local_sum / local_count if local_count > 0 else 128
                pixel = gray.get_pixel(x, y)[0]
                value = 255 if pixel > local_threshold else 0
                row.append([value])
            
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=1
        )


class ImageHistogram:
    """Image histogram utilities."""
    
    @staticmethod
    def calculate_histogram(image: Image, channel: int = 0) -> List[int]:
        """Calculate histogram for channel."""
        histogram = [0] * 256
        
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.get_pixel(x, y)
                if channel < len(pixel):
                    histogram[pixel[channel]] += 1
        
        return histogram
    
    @staticmethod
    def equalize_histogram(image: Image) -> Image:
        """Histogram equalization."""
        if image.channels != 1:
            return image
        
        histogram = ImageHistogram.calculate_histogram(image, 0)
        
        # Calculate CDF
        cdf = []
        cumulative = 0
        total = image.width * image.height
        
        for count in histogram:
            cumulative += count
            cdf.append(cumulative / total)
        
        # Apply equalization
        pixels = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                pixel = image.get_pixel(x, y)[0]
                equalized = int(cdf[pixel] * 255)
                row.append([equalized])
            pixels.append(row)
        
        return Image(
            pixels=pixels,
            width=image.width,
            height=image.height,
            channels=1
        )


class FeatureDetection:
    """Feature detection utilities."""
    
    @staticmethod
    def detect_corners(image: Image, threshold: float = 0.1) -> List[Tuple[int, int]]:
        """Detect corners using Harris corner detection (simplified)."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        # Calculate gradients
        sobel_x = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        
        sobel_y = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
        
        grad_x = ImageFilter._apply_convolution(gray, sobel_x)
        grad_y = ImageFilter._apply_convolution(gray, sobel_y)
        
        corners = []
        
        for y in range(1, image.height - 1):
            for x in range(1, image.width - 1):
                # Calculate corner response
                gx = grad_x.get_pixel(x, y)[0]
                gy = grad_y.get_pixel(x, y)[0]
                
                # Simplified corner detection
                response = abs(gx) + abs(gy)
                
                if response > threshold * 255:
                    corners.append((x, y))
        
        return corners


class ImageUtils:
    """General image utilities."""
    
    @staticmethod
    def get_image_info(image: Image) -> Dict:
        """Get image information."""
        return {
            "width": image.width,
            "height": image.height,
            "channels": image.channels,
            "color_space": image.color_space.value,
            "total_pixels": image.width * image.height
        }
    
    @staticmethod
    def calculate_brightness(image: Image) -> float:
        """Calculate average brightness."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        total = 0
        count = 0
        
        for y in range(gray.height):
            for x in range(gray.width):
                total += gray.get_pixel(x, y)[0]
                count += 1
        
        return total / count if count > 0 else 0
    
    @staticmethod
    def calculate_contrast(image: Image) -> float:
        """Calculate image contrast (standard deviation)."""
        gray = ColorSpaceConverter.rgb_to_grayscale(image)
        
        values = []
        for y in range(gray.height):
            for x in range(gray.width):
                values.append(gray.get_pixel(x, y)[0])
        
        if not values:
            return 0
        
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        
        return math.sqrt(variance)


def demonstrate_computer_vision():
    """Demonstrate computer vision functionality."""
    print("=== Computer Vision Demonstration ===\n")
    
    # Create Test Image
    print("1. Create Test Image:")
    image = ImageLoader.create_blank_image(100, 100, (255, 255, 255))
    print(f"   Created {image.width}x{image.height} image")
    
    # Gradient Image
    print("\n2. Gradient Image:")
    gradient = ImageLoader.create_gradient_image(50, 50, (0, 0, 0), (255, 255, 255))
    print(f"   Created gradient image: {gradient.width}x{gradient.height}")
    
    # Color Space Conversion
    print("\n3. Color Space Conversion:")
    grayscale = ColorSpaceConverter.rgb_to_grayscale(image)
    print(f"   Converted to grayscale: {grayscale.channels} channel(s)")
    
    hsv = ColorSpaceConverter.rgb_to_hsv(image)
    print(f"   Converted to HSV: {hsv.color_space.value}")
    
    # Image Filtering
    print("\n4. Image Filtering:")
    blurred = ImageFilter.apply_gaussian_blur(image, kernel_size=3)
    print(f"   Applied Gaussian blur")
    
    sharpened = ImageFilter.apply_sharpen(image)
    print(f"   Applied sharpening")
    
    # Edge Detection
    print("\n5. Edge Detection:")
    edges_sobel = EdgeDetection.sobel(image)
    print(f"   Sobel edge detection: {edges_sobel.channels} channel(s)")
    
    edges_prewitt = EdgeDetection.prewitt(image)
    print(f"   Prewitt edge detection")
    
    edges_laplacian = EdgeDetection.laplacian(image)
    print(f"   Laplacian edge detection")
    
    # Image Transformation
    print("\n6. Image Transformation:")
    resized = ImageTransformation.resize(image, 50, 50)
    print(f"   Resized to: {resized.width}x{resized.height}")
    
    flipped_h = ImageTransformation.flip_horizontal(image)
    print(f"   Flipped horizontally")
    
    flipped_v = ImageTransformation.flip_vertical(image)
    print(f"   Flipped vertically")
    
    # Image Segmentation
    print("\n7. Image Segmentation:")
    thresholded = ImageSegmentation.threshold(image, threshold=128)
    print(f"   Applied threshold segmentation")
    
    adaptive = ImageSegmentation.adaptive_threshold(image, block_size=11)
    print(f"   Applied adaptive threshold")
    
    # Histogram
    print("\n8. Image Histogram:")
    histogram = ImageHistogram.calculate_histogram(grayscale, channel=0)
    print(f"   Histogram bins: {len(histogram)}")
    print(f"   Max count: {max(histogram)}")
    
    equalized = ImageHistogram.equalize_histogram(grayscale)
    print(f"   Histogram equalized")
    
    # Feature Detection
    print("\n9. Feature Detection:")
    corners = FeatureDetection.detect_corners(image, threshold=0.05)
    print(f"   Detected {len(corners)} corners")
    
    # Image Info
    print("\n10. Image Information:")
    info = ImageUtils.get_image_info(image)
    print(f"   Info: {info}")
    
    brightness = ImageUtils.calculate_brightness(image)
    print(f"   Brightness: {brightness:.2f}")
    
    contrast = ImageUtils.calculate_contrast(image)
    print(f"   Contrast: {contrast:.2f}")
    
    print("\n=== Demonstration Complete ===")
    print("\nComputer Vision Best Practices:")
    print("- Convert to grayscale for many operations")
    print("- Use appropriate kernel sizes for filtering")
    print("- Normalize images before processing")
    print("- Consider computational complexity")
    print("- Use efficient data structures for large images")
    print("- Test edge detection parameters")
    print("- Use histogram equalization for contrast enhancement")
    print("- Consider color space for specific tasks")
    print("- Handle edge cases at image boundaries")
    print("- Use built-in libraries (OpenCV) for production")
    print("- Validate input image dimensions")
    print("- Consider memory usage for large images")


if __name__ == "__main__":
    demonstrate_computer_vision()
