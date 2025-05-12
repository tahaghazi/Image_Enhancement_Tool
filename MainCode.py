import cv2
import numpy as np
from PIL import Image, ImageEnhance
from skimage import exposure, img_as_float, img_as_ubyte


def load_image(path: str) -> Image.Image:
    """Load an image from disk and convert it to RGB."""
    return Image.open(path).convert('RGB')


def save_image(image: Image.Image, path: str, quality: int = 95) -> None:
    """
    Save the image with minimal compression artifacts.
    - JPEG: set quality, optimize, and disable subsampling.
    - PNG: set low compression level.
    """
    extension = path.split('.')[-1].lower()
    options = {}
    if extension in ('jpg', 'jpeg'):
        options = {'quality': quality, 'optimize': True, 'subsampling': 0}
    elif extension == 'png':
        options = {'compress_level': 1}

    image.save(path, **options)
    print(f"Image saved to {path}")


def apply_gamma(image: Image.Image, gamma: float) -> Image.Image:
    """Return a gamma-corrected copy of the image."""
    float_arr = img_as_float(np.array(image))
    corrected = exposure.adjust_gamma(float_arr, gamma)
    return Image.fromarray(img_as_ubyte(corrected))


def apply_histogram_equalization(image: Image.Image) -> Image.Image:
    """Apply histogram equalization on the luminance channel, preserving color."""
    arr = np.array(image)
    ycrcb = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    equalized = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
    return Image.fromarray(equalized)


def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Brightness(image).enhance(factor)


def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Contrast(image).enhance(factor)


def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Sharpness(image).enhance(factor)


def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Color(image).enhance(factor)


def adjust_exposure(image: Image.Image, gain: float) -> Image.Image:
    """Apply exposure adjustment via logarithmic mapping on each channel and return new image."""
    arr = img_as_float(np.array(image))
    adjusted = exposure.adjust_log(arr, gain=gain)
    return Image.fromarray(img_as_ubyte(adjusted))


def display_menu(options: dict) -> None:
    """Print the numbered menu from the options dict."""
    print("\nImage Processing Menu:")
    for key, (label, *_ ) in options.items():
        print(f"  {key}. {label}")
    print("  8. Show Current Image")
    print("  9. Save Modified Image")
    print("  0. Exit")


def prompt_parameters(params: dict) -> dict:
    """Prompt user for parameter values, using defaults if no input."""
    for name, default in params.items():
        user_input = input(f"Enter {name} (default={default}): ")
        params[name] = float(user_input) if user_input else default
    return params


def main():
    image_path = input("Enter image path: ")
    try:
        original = load_image(image_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    current = original.copy()
    modified = False

    operations = {
        '1': ('Gamma Correction', apply_gamma, {'gamma': 1.0}),
        '2': ('Histogram Equalization', apply_histogram_equalization, {}),
        '3': ('Adjust Brightness', adjust_brightness, {'factor': 1.0}),
        '4': ('Adjust Contrast', adjust_contrast, {'factor': 1.0}),
        '5': ('Adjust Sharpness', adjust_sharpness, {'factor': 1.0}),
        '6': ('Adjust Saturation', adjust_saturation, {'factor': 1.0}),
        '7': ('Adjust Exposure', adjust_exposure, {'gain': 1.0}),
    }

    while True:
        display_menu(operations)
        choice = input("Choose an option (0-9): ")

        if choice == '0':
            print("Goodbye!")
            break

        if choice == '8':
            current.show()
            continue

        if choice == '9':
            if not modified:
                print("No changes to save.")
                continue
            save_path = input("Output filename (e.g., result.jpg or result.png): ")
            try:
                save_image(current, save_path)
                modified = False
            except Exception as e:
                print(f"Failed to save: {e}")
            continue

        if choice in operations:
            label, func, params = operations[choice]
            params = prompt_parameters(params)
            try:
                current = func(current, **params)
                modified = True
                print(f"{label} applied successfully.")
                current.show()
            except Exception as e:
                print(f"Error during {label}: {e}")
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()