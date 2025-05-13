import cv2
import numpy as np
from PIL import Image, ImageEnhance
from skimage import exposure, img_as_float, img_as_ubyte


def load_image(path):
    """
    Load an image from disk and convert to RGB.
    use convert RGB to ensure the compatability of the file
    with CV2 & numpy Functions.
    """
    return Image.open(path).convert('RGB')


def save_image(image, path, quality=100):
    """
    Save image as JPEG/PNG with specified quality.
    optimize: Finds the best Huffman encoding tables to compress the
    image (Reduces file size without change in image quality)
    subsapling: Controls how color detail is compressed in JPEG and JPG
    """
    ext = path.split('.')[-1].lower()  # ['ima','ge',"jpg"] ima.ge.jpg
    options = {}
    if ext in ('jpg', 'jpeg'):
        options = {'quality': quality, 'optimize': True, 'subsampling': 0} 
    elif ext == 'png':
        options = {'compress_level': 1}
    image.save(path, **options)
    print(f"Saved: {path}")


def apply_gamma(image, gamma=1.0):
    # Non-linear mapping
    """
    Apply gamma correction and ensure values stay in [0,1] range.
    I"out" = I"in" power 1/gamma factor
    """
    arr = img_as_float(np.array(image))  # values in [0,1]
    corrected = exposure.adjust_gamma(arr, gamma)  # I_out = I_in power (1/gamma)
    corrected = np.clip(corrected, 0, 1)  # clip to valid range
    return Image.fromarray(img_as_ubyte(corrected))


"""
    didn't use the known approach of exposure.equalize_hist
    because it distort the image and doesn't keep the original colors
    unlike the cv2.equalizeHist which equalizes the histogram of the Y channel
    and keeps the original colors.

    the older approach is:  
       
        exposure.equalize_hist(image)
"""

  
def apply_hist_eq(image):
    """Equalize histogram on the Y channel."""
    arr = np.array(image)
    ycrcb = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)  # convert to YCrCb color space
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])  # image[:,:,2]
    rgb = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)  # convert back to RGB
    return Image.fromarray(rgb)


def adjust_brightness(image, factor=1.0):
    # Linear scaling
    """Scale brightness."""
    return ImageEnhance.Brightness(image).enhance(factor)


def adjust_contrast(image, factor=1.0):
    # Difference scaling
    """Adjust contrast."""
    return ImageEnhance.Contrast(image).enhance(factor)


def adjust_sharpness(image, factor=1.0):
    # Edge detection
    """Adjust sharpness."""
    return ImageEnhance.Sharpness(image).enhance(factor)


def adjust_saturation(image, factor=1.0):
    # Color component scaling
    """Adjust color saturation."""
    return ImageEnhance.Color(image).enhance(factor)

# def adjust_exposure(image: Image.Image, gain: float) -> Image.Image:
#     """Apply exposure adjustment via logarithmic mapping on each channel and return new image."""
#     arr = img_as_float(np.array(image))
#     adjusted = exposure.adjust_log(arr, gain=gain)
#     return Image.fromarray(img_as_ubyte(adjusted))


def adjust_exposure(image, gain=1.0): # Logarithmic function
    """Log exposure adjustment with clipping to avoid dtype issues."""
    arr = img_as_float(np.array(image))  # values in [0,1]
    exp = exposure.adjust_log(arr, gain) # 	I_out = log(1 + gain * I_in)
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
            try:
                g = float(input("Gamma [1]: "))
            except ValueError:
                print("Invalid gamma value. Please enter a number.")
                continue
            current = apply_gamma(current, g)
            modified = True
        elif choice == '2':
            current = apply_hist_eq(current)
            modified = True
        elif choice == '3':
            try:
                f = float(input("Brightness [1]: "))
            except ValueError:
                print("Invalid brightness value. Please enter a number.")
                continue
            current = adjust_brightness(current, f)
            modified = True
        elif choice == '4':
            try:
                f = float(input("Contrast [1]: "))
            except ValueError:
                print("Invalid contrast value. Please enter a number.")
                continue
            current = adjust_contrast(current, f)
            modified = True
        elif choice == '5':
            try:
                f = float(input("Sharpness [1]: "))
            except ValueError:
                print("Invalid sharpness value. Please enter a number.")
                continue
            current = adjust_sharpness(current, f)
            modified = True
        elif choice == '6':
            try:
                f = float(input("Saturation [1]: "))
            except ValueError:
                print("Invalid saturation value. Please enter a number.")
                continue
            current = adjust_saturation(current, f)
            modified = True
        elif choice == '7':
            try:
                g = float(input("Exposure [1]: "))
            except ValueError:
                print("Invalid exposure value. Please enter a number.")
                continue
            current = adjust_exposure(current, g)
            modified = True
        elif choice == '8':
            current.show()
        elif choice == '9':
            if modified:
                try:
                    save_image(current, input("Save as: "))
                except Exception as e:
                    print("Error saving image:", e)
                    continue
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
