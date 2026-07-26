from pathlib import Path
from PIL import Image
from core.logger import logger

def validate_and_optimize_image(image_path: Path, max_size: int = 1920) -> bool:
    """
    Validate if file is a valid image and scale down if it exceeds max dimensions.
    """
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify it's a valid image file
        
        # Re-open for modifications since verify() closes the stream
        with Image.open(image_path) as img:
            width, height = img.size
            if width > max_size or height > max_size:
                # Maintain aspect ratio
                img.thumbnail((max_size, max_size))
                img.save(image_path)
                logger.info(f"Resized image {image_path.name} to fit within {max_size}px")
        return True
    except Exception as e:
        logger.error(f"Image validation failed for {image_path}: {str(e)}")
        return False
