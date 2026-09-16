"""
Image Processing Module

This module provides comprehensive image processing utilities including:
- Image loading and saving
- Image resizing and cropping
- Color space conversions
- Image filtering and enhancement
- Image transformation (rotate, flip, transpose)
- Image drawing and annotation
- Image analysis (histograms, statistics)
- Batch image processing
- Image format conversion
- Text watermarking

Note: This module uses Pillow library for image operations.
Install with: pip install Pillow

All functions include comprehensive docstrings and type hints.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import os


try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
    from PIL.ImageStat import Stat
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False


class ImageFormat(Enum):
    """Supported image formats."""
    JPEG = "JPEG"
    PNG = "PNG"
    GIF = "GIF"
    BMP = "BMP"
    TIFF = "TIFF"
    WEBP = "WEBP"


class ColorSpace(Enum):
    """Color space types."""
    RGB = "RGB"
    RGBA = "RGBA"
    GRAYSCALE = "L"
    CMYK = "CMYK"


@dataclass
class ImageInfo:
    """Container for image information."""
    width: int
    height: int
    format: str
    mode: str
    size_bytes: int
    has_transparency: bool


@dataclass
class ImageStats:
    """Container for image statistics."""
    mean: Tuple[float, ...]
    median: Tuple[float, ...]
    std_dev: Tuple[float, ...]
    min: Tuple[int, ...]
    max: Tuple[int, ...]


class ImageProcessor:
    """Main image processing class."""
    
    def __init__(self, image_path: Optional[str] = None):
        """Initialize image processor with optional image path."""
        if not IMAGE_PROCESSING_AVAILABLE:
            raise ImportError("Pillow library is required. Install with: pip install Pillow")
        
        self.image: Optional[Image.Image] = None
        self.image_path = image_path
        
        if image_path:
            self.load_image(image_path)
    
    def load_image(self, image_path: str) -> Image.Image:
        """Load an image from file."""
        self.image_path = image_path
        self.image = Image.open(image_path)
        return self.image
    
    def create_new_image(self, width: int, height: int, 
                         color: Union[str, Tuple[int, ...]] = "white",
                         mode: str = "RGB") -> Image.Image:
        """Create a new blank image."""
        self.image = Image.new(mode, (width, height), color)
        return self.image
    
    def save_image(self, output_path: str, format: Optional[str] = None,
                   quality: int = 95, **kwargs) -> None:
        """Save the image to file."""
        if not self.image:
            raise ValueError("No image loaded")
        
        if format is None:
            format = ImageFormat(output_path.split('.')[-1].upper()).value
        
        save_kwargs = {'quality': quality}
        save_kwargs.update(kwargs)
        
        self.image.save(output_path, format=format, **save_kwargs)
    
    def get_image_info(self) -> ImageInfo:
        """Get information about the current image."""
        if not self.image:
            raise ValueError("No image loaded")
        
        file_size = os.path.getsize(self.image_path) if self.image_path and os.path.exists(self.image_path) else 0
        
        return ImageInfo(
            width=self.image.width,
            height=self.image.height,
            format=self.image.format or "Unknown",
            mode=self.image.mode,
            size_bytes=file_size,
            has_transparency=self.image.mode in ("RGBA", "LA") or "transparency" in self.image.info
        )
    
    def close(self) -> None:
        """Close the image."""
        if self.image:
            self.image.close()
            self.image = None


class ImageTransformer:
    """Image transformation operations."""
    
    def __init__(self, processor: ImageProcessor):
        """Initialize transformer with image processor."""
        self.processor = processor
    
    def resize(self, width: int, height: int, 
               resample: int = Image.LANCZOS) -> Image.Image:
        """Resize image to specified dimensions."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.resize((width, height), resample)
        return self.processor.image
    
    def resize_by_factor(self, factor: float, 
                        resample: int = Image.LANCZOS) -> Image.Image:
        """Resize image by scaling factor."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        new_width = int(self.processor.image.width * factor)
        new_height = int(self.processor.image.height * factor)
        return self.resize(new_width, new_height, resample)
    
    def resize_to_fit(self, max_width: int, max_height: int,
                     resample: int = Image.LANCZOS) -> Image.Image:
        """Resize image to fit within max dimensions while maintaining aspect ratio."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        img = self.processor.image
        ratio = min(max_width / img.width, max_height / img.height)
        
        if ratio >= 1:
            return img  # Image already fits
        
        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)
        return self.resize(new_width, new_height, resample)
    
    def crop(self, left: int, top: int, right: int, bottom: int) -> Image.Image:
        """Crop image to specified rectangle."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.crop((left, top, right, bottom))
        return self.processor.image
    
    def crop_center(self, width: int, height: int) -> Image.Image:
        """Crop image from center to specified dimensions."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        img = self.processor.image
        left = (img.width - width) // 2
        top = (img.height - height) // 2
        right = left + width
        bottom = top + height
        
        return self.crop(left, top, right, bottom)
    
    def rotate(self, angle: float, expand: bool = False) -> Image.Image:
        """Rotate image by specified angle (degrees)."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.rotate(angle, expand=expand)
        return self.processor.image
    
    def flip_horizontal(self) -> Image.Image:
        """Flip image horizontally."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = ImageOps.mirror(self.processor.image)
        return self.processor.image
    
    def flip_vertical(self) -> Image.Image:
        """Flip image vertically."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = ImageOps.flip(self.processor.image)
        return self.processor.image
    
    def transpose(self, method: int = Image.FLIP_LEFT_RIGHT) -> Image.Image:
        """Transpose image using specified method."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.transpose(method)
        return self.processor.image
    
    def convert_color_space(self, mode: str) -> Image.Image:
        """Convert image to different color space."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.convert(mode)
        return self.processor.image


class ImageFilter:
    """Image filtering and enhancement operations."""
    
    def __init__(self, processor: ImageProcessor):
        """Initialize filter with image processor."""
        self.processor = processor
    
    def apply_blur(self, radius: float = 2) -> Image.Image:
        """Apply Gaussian blur."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.filter(ImageFilter.GaussianBlur(radius))
        return self.processor.image
    
    def apply_sharpen(self) -> Image.Image:
        """Apply sharpening filter."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.filter(ImageFilter.SHARPEN)
        return self.processor.image
    
    def apply_edge_detect(self) -> Image.Image:
        """Apply edge detection filter."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.filter(ImageFilter.FIND_EDGES)
        return self.processor.image
    
    def apply_emboss(self) -> Image.Image:
        """Apply emboss filter."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.filter(ImageFilter.EMBOSS)
        return self.processor.image
    
    def apply_smooth(self) -> Image.Image:
        """Apply smooth filter."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = self.processor.image.filter(ImageFilter.SMOOTH)
        return self.processor.image
    
    def enhance_brightness(self, factor: float = 1.0) -> Image.Image:
        """Enhance image brightness (factor > 1 brightens, < 1 darkens)."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        enhancer = ImageEnhance.Brightness(self.processor.image)
        self.processor.image = enhancer.enhance(factor)
        return self.processor.image
    
    def enhance_contrast(self, factor: float = 1.0) -> Image.Image:
        """Enhance image contrast (factor > 1 increases, < 1 decreases)."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        enhancer = ImageEnhance.Contrast(self.processor.image)
        self.processor.image = enhancer.enhance(factor)
        return self.processor.image
    
    def enhance_color(self, factor: float = 1.0) -> Image.Image:
        """Enhance image color saturation (factor > 1 increases, < 1 decreases)."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        enhancer = ImageEnhance.Color(self.processor.image)
        self.processor.image = enhancer.enhance(factor)
        return self.processor.image
    
    def enhance_sharpness(self, factor: float = 1.0) -> Image.Image:
        """Enhance image sharpness (factor > 1 sharpens, < 1 blurs)."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        enhancer = ImageEnhance.Sharpness(self.processor.image)
        self.processor.image = enhancer.enhance(factor)
        return self.processor.image
    
    def grayscale(self) -> Image.Image:
        """Convert image to grayscale."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = ImageOps.grayscale(self.processor.image)
        return self.processor.image
    
    def invert(self) -> Image.Image:
        """Invert image colors."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = ImageOps.invert(self.processor.image)
        return self.processor.image
    
    def posterize(self, bits: int = 2) -> Image.Image:
        """Reduce number of colors (posterize effect)."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = ImageOps.posterize(self.processor.image, bits)
        return self.processor.image
    
    def solarize(self, threshold: int = 128) -> Image.Image:
        """Apply solarize effect."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        self.processor.image = ImageOps.solarize(self.processor.image, threshold)
        return self.processor.image


class ImageDrawing:
    """Image drawing and annotation operations."""
    
    def __init__(self, processor: ImageProcessor):
        """Initialize drawing with image processor."""
        self.processor = processor
        self.draw: Optional[ImageDraw.Draw] = None
    
    def _get_draw(self) -> ImageDraw.Draw:
        """Get or create drawing object."""
        if self.draw is None or self.draw.im != self.processor.image:
            self.draw = ImageDraw.Draw(self.processor.image)
        return self.draw
    
    def draw_rectangle(self, coordinates: Tuple[int, int, int, int],
                       fill: Optional[str] = None, outline: Optional[str] = None,
                       width: int = 1) -> None:
        """Draw a rectangle."""
        draw = self._get_draw()
        draw.rectangle(coordinates, fill=fill, outline=outline, width=width)
    
    def draw_ellipse(self, coordinates: Tuple[int, int, int, int],
                     fill: Optional[str] = None, outline: Optional[str] = None,
                     width: int = 1) -> None:
        """Draw an ellipse."""
        draw = self._get_draw()
        draw.ellipse(coordinates, fill=fill, outline=outline, width=width)
    
    def draw_line(self, coordinates: List[Tuple[int, int]],
                  fill: str = "black", width: int = 1) -> None:
        """Draw a line."""
        draw = self._get_draw()
        draw.line(coordinates, fill=fill, width=width)
    
    def draw_text(self, position: Tuple[int, int], text: str,
                  fill: str = "black", font_size: int = 12,
                  font_path: Optional[str] = None) -> None:
        """Draw text on image."""
        draw = self._get_draw()
        
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        draw.text(position, text, fill=fill, font=font)
    
    def draw_text_centered(self, text: str, fill: str = "black",
                          font_size: int = 12, font_path: Optional[str] = None) -> None:
        """Draw text centered on image."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        img = self.processor.image
        draw = self._get_draw()
        
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate center position
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        draw.text((x, y), text, fill=fill, font=font)
    
    def add_watermark(self, text: str, position: str = "bottom-right",
                     opacity: int = 128, font_size: int = 24) -> None:
        """Add text watermark to image."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        img = self.processor.image
        
        # Create transparent overlay
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        if position == "top-left":
            x, y = 10, 10
        elif position == "top-right":
            x, y = img.width - text_width - 10, 10
        elif position == "bottom-left":
            x, y = 10, img.height - text_height - 10
        elif position == "bottom-right":
            x, y = img.width - text_width - 10, img.height - text_height - 10
        elif position == "center":
            x, y = (img.width - text_width) // 2, (img.height - text_height) // 2
        else:
            x, y = 10, img.height - text_height - 10
        
        # Draw text on overlay
        draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
        
        # Composite overlay onto original image
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        self.processor.image = Image.alpha_composite(img, overlay)


class ImageAnalyzer:
    """Image analysis and statistics operations."""
    
    def __init__(self, processor: ImageProcessor):
        """Initialize analyzer with image processor."""
        self.processor = processor
    
    def get_statistics(self) -> ImageStats:
        """Get image statistics."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        stat = Stat(self.processor.image)
        
        return ImageStats(
            mean=stat.mean,
            median=stat.median,
            std_dev=stat.stddev,
            min=stat.extrema[0],
            max=stat.extrema[1]
        )
    
    def get_histogram(self) -> Dict[str, List[int]]:
        """Get image histogram."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        histogram = self.processor.image.histogram()
        mode = self.processor.image.mode
        
        if mode == "RGB":
            return {
                "red": histogram[0:256],
                "green": histogram[256:512],
                "blue": histogram[512:768]
            }
        elif mode == "L":
            return {"grayscale": histogram}
        else:
            return {"channel_0": histogram}
    
    def get_dominant_colors(self, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Get dominant colors using quantization."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        # Convert to RGB if necessary
        img = self.processor.image.convert("RGB")
        
        # Quantize image
        quantized = img.quantize(colors=num_colors)
        
        # Get palette
        palette = quantized.getpalette()
        colors = []
        
        for i in range(num_colors):
            r = palette[i * 3]
            g = palette[i * 3 + 1]
            b = palette[i * 3 + 2]
            colors.append((r, g, b))
        
        return colors
    
    def find_edges(self) -> Image.Image:
        """Find edges in image."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        return self.processor.image.filter(ImageFilter.FIND_EDGES)
    
    def calculate_brightness(self) -> float:
        """Calculate average brightness of image."""
        if not self.processor.image:
            raise ValueError("No image loaded")
        
        stat = Stat(self.processor.image.convert("L"))
        return stat.mean[0]


class BatchImageProcessor:
    """Batch processing operations for multiple images."""
    
    def __init__(self):
        """Initialize batch processor."""
        self.operations: List[callable] = []
    
    def add_operation(self, operation: callable) -> None:
        """Add an operation to the batch."""
        self.operations.append(operation)
    
    def process_directory(self, input_dir: str, output_dir: str,
                          pattern: str = "*.jpg") -> List[str]:
        """Process all images in a directory."""
        if not IMAGE_PROCESSING_AVAILABLE:
            raise ImportError("Pillow library is required")
        
        import glob
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        processed_files = []
        
        for input_path in glob.glob(os.path.join(input_dir, pattern)):
            try:
                # Load image
                processor = ImageProcessor(input_path)
                
                # Apply all operations
                for operation in self.operations:
                    operation(processor)
                
                # Save processed image
                filename = os.path.basename(input_path)
                output_path = os.path.join(output_dir, filename)
                processor.save_image(output_path)
                
                processed_files.append(output_path)
                processor.close()
                
            except Exception as e:
                print(f"Error processing {input_path}: {e}")
        
        return processed_files
    
    def convert_format(self, input_dir: str, output_dir: str,
                      input_format: str = "jpg", output_format: str = "png") -> List[str]:
        """Convert all images from one format to another."""
        if not IMAGE_PROCESSING_AVAILABLE:
            raise ImportError("Pillow library is required")
        
        import glob
        
        os.makedirs(output_dir, exist_ok=True)
        
        converted_files = []
        
        for input_path in glob.glob(os.path.join(input_dir, f"*.{input_format}")):
            try:
                processor = ImageProcessor(input_path)
                
                # Change output extension
                filename = os.path.basename(input_path)
                output_filename = os.path.splitext(filename)[0] + f".{output_format}"
                output_path = os.path.join(output_dir, output_filename)
                
                processor.save_image(output_path, format=output_format.upper())
                converted_files.append(output_path)
                processor.close()
                
            except Exception as e:
                print(f"Error converting {input_path}: {e}")
        
        return converted_files


def create_sample_image(output_path: str = "sample_image.png") -> None:
    """Create a sample image for demonstration."""
    if not IMAGE_PROCESSING_AVAILABLE:
        print("Pillow library is required. Install with: pip install Pillow")
        return
    
    processor = ImageProcessor()
    processor.create_new_image(400, 300, color="lightblue")
    
    transformer = ImageTransformer(processor)
    drawing = ImageDrawing(processor)
    
    # Draw some shapes
    drawing.draw_rectangle((50, 50, 150, 150), fill="red", outline="black")
    drawing.draw_ellipse((200, 50, 350, 150), fill="green", outline="black")
    drawing.draw_line([(50, 200), (350, 200)], fill="blue", width=3)
    
    # Add text
    drawing.draw_text_centered("Sample Image", fill="white", font_size=24)
    
    processor.save_image(output_path)
    processor.close()
    
    print(f"Sample image created: {output_path}")


def demonstrate_image_processing():
    """Demonstrate image processing functionality."""
    print("=== Image Processing Demonstration ===\n")
    
    if not IMAGE_PROCESSING_AVAILABLE:
        print("Pillow library is required. Install with: pip install Pillow")
        return
    
    # Create sample image
    print("1. Creating sample image...")
    create_sample_image("demo_image.png")
    
    # Load and analyze
    print("\n2. Loading and analyzing image...")
    processor = ImageProcessor("demo_image.png")
    info = processor.get_image_info()
    print(f"   Image info: {info.width}x{info.height}, {info.format}, {info.mode}")
    
    # Transformations
    print("\n3. Image transformations...")
    transformer = ImageTransformer(processor)
    
    print("   Resizing to 200x150...")
    transformer.resize(200, 150)
    
    print("   Rotating 45 degrees...")
    transformer.rotate(45)
    
    print("   Converting to grayscale...")
    transformer.convert_color_space("L")
    
    # Filters
    print("\n4. Image filters...")
    img_filter = ImageFilter(processor)
    
    print("   Applying blur...")
    img_filter.apply_blur(radius=1)
    
    print("   Enhancing contrast...")
    img_filter.enhance_contrast(1.5)
    
    # Drawing
    print("\n5. Image drawing...")
    processor.create_new_image(300, 200, color="white")
    drawing = ImageDrawing(processor)
    
    drawing.draw_rectangle((50, 50, 100, 100), fill="blue", outline="black")
    drawing.draw_ellipse((150, 50, 250, 100), fill="red", outline="black")
    drawing.draw_text((50, 150), "Hello World!", fill="black", font_size=16)
    
    processor.save_image("demo_drawn.png")
    print("   Drawn image saved")
    
    # Statistics
    print("\n6. Image statistics...")
    processor.load_image("demo_drawn.png")
    analyzer = ImageAnalyzer(processor)
    
    stats = analyzer.get_statistics()
    print(f"   Mean brightness: {stats.mean[0]:.2f}")
    
    brightness = analyzer.calculate_brightness()
    print(f"   Average brightness: {brightness:.2f}")
    
    # Watermark
    print("\n7. Adding watermark...")
    drawing.add_watermark("Demo Watermark", position="bottom-right", opacity=180)
    processor.save_image("demo_watermarked.png")
    print("   Watermarked image saved")
    
    # Cleanup
    processor.close()
    
    try:
        os.remove("demo_image.png")
        os.remove("demo_drawn.png")
        os.remove("demo_watermarked.png")
        print("\n8. Cleanup: Removed demo files")
    except:
        pass
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_image_processing()