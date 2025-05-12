import cv2
import numpy as np
from PIL import Image, ImageEnhance
from skimage import exposure, img_as_float, img_as_ubyte


def load_image(path):
    """Load an image from disk and convert to RGB."""
    return Image.open(path).convert('RGB')


def save_image(image, path, quality=100):
    """Save image as JPEG/PNG with specified quality."""
    ext = path.split('.')[-1].lower()
    options = {}
    if ext in ('jpg', 'jpeg'):
        options = {'quality': quality, 'optimize': True, 'subsampling': 0}
    elif ext == 'png':
        options = {'compress_level': 1}
    image.save(path, **options)
    print(f"Saved: {path}")


def apply_gamma(image, gamma=1.0):
    """Apply gamma correction and ensure values stay in [0,1] range."""
    arr = img_as_float(np.array(image))  # values in [0,1]
    corrected = exposure.adjust_gamma(arr, gamma)
    corrected = np.clip(corrected, 0, 1)  # clip to valid range
    return Image.fromarray(img_as_ubyte(corrected))


def apply_hist_eq(image):
    """Equalize histogram on the Y channel."""
    arr = np.array(image)
    ycrcb = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    rgb = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
    return Image.fromarray(rgb)


def adjust_brightness(image, factor=1.0):
    """Scale brightness."""
    return ImageEnhance.Brightness(image).enhance(factor)


def adjust_contrast(image, factor=1.0):
    """Adjust contrast."""
    return ImageEnhance.Contrast(image).enhance(factor)


def adjust_sharpness(image, factor=1.0):
    """Adjust sharpness."""
    return ImageEnhance.Sharpness(image).enhance(factor)


def adjust_saturation(image, factor=1.0):
    """Adjust color saturation."""
    return ImageEnhance.Color(image).enhance(factor)


def adjust_exposure(image, gain=1.0):
    """Log exposure adjustment with clipping to avoid dtype issues."""
    arr = img_as_float(np.array(image))  # values in [0,1]
    exp = exposure.adjust_log(arr, gain)
    exp = np.clip(exp, 0, 1)  # clip to valid range
    return Image.fromarray(img_as_ubyte(exp))


def main():
    path = input("Path: ")
    try:
        img = load_image(path)
    except Exception as e:
        print("Error loading image:", e)
        return

    current = img.copy()
    modified = False

    while True:
        print("\n1: Gamma \n2: HistEq \n3: Brightness \n4: Contrast \
              \n5: Sharpness \n6: Saturation \n7: Exposure \n8: Show \n9: Save \n0: Exit")
        choice = input("Choose: ")
        if choice == '0':
            break
        elif choice == '1':
            g = float(input("Gamma [1]: "))
            current = apply_gamma(current, g)
            modified = True
        elif choice == '2':
            current = apply_hist_eq(current)
            modified = True
        elif choice == '3':
            f = float(input("Brightness [1]: "))
            current = adjust_brightness(current, f)
            modified = True
        elif choice == '4':
            f = float(input("Contrast [1]: "))
            current = adjust_contrast(current, f)
            modified = True
        elif choice == '5':
            f = float(input("Sharpness [1]: "))
            current = adjust_sharpness(current, f)
            modified = True
        elif choice == '6':
            f = float(input("Saturation [1]: "))
            current = adjust_saturation(current, f)
            modified = True
        elif choice == '7':
            g = float(input("Exposure [1]: "))
            current = adjust_exposure(current, g)
            modified = True
        elif choice == '8':
            current.show()
        elif choice == '9':
            if modified:
                save_image(current, input("Save as: "))
                modified = False
            else:
                print("Nothing to save.")
        else:
            print("Invalid.")

        if modified:
            print("Applied.")
            current.show()

if __name__ == '__main__':
    main()
