
import pytesseract
from PIL import Image, ImageOps, ImageEnhance


def extract_text(image_path):
    try:
        with Image.open(image_path) as image:
            # Convert to grayscale.
            image = ImageOps.grayscale(image)

            # Improve contrast.
            image = ImageEnhance.Contrast(image).enhance(1.5)

            # Enlarge small screenshots.
            if image.width < 1500:
                scale = 1500 / image.width
                new_size = (
                    1500,
                    int(image.height * scale)
                )
                image = image.resize(
                    new_size,
                    Image.Resampling.LANCZOS
                )

            # PSM 11 works well for scattered text in screenshots.
            extracted_text = pytesseract.image_to_string(
                image,
                config="--oem 3 --psm 11"
            )

            return extracted_text.strip()

    except Exception as error:
        print(f"[ERROR] OCR failed: {error}")
        return ""

