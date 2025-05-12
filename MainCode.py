import cv2
import numpy as np
from PIL import Image, ImageEnhance
from skimage import exposure, img_as_float, img_as_ubyte


def load_image(path):
    return Image.open(path).convert('RGB')


def save_image(image, path, quality=95):
    ext = path.split('.')[-1].lower()
    opts = {}
    if ext in ('jpg', 'jpeg'):
        opts = {'quality': quality, 'optimize': True, 'subsampling': 0}
    elif ext == 'png':
        opts = {'compress_level': 1}
    image.save(path, **opts)
    print(f"Saved: {path}")


# Apply gamma correction to enhance image brightness non-linearly
def apply_gamma(image, gamma=1.0):
    arr = img_as_float(np.array(image))
    return Image.fromarray(img_as_ubyte(exposure.adjust_gamma(arr, gamma)))


# Apply histogram equalization to improve image contrast
def apply_hist_eq(image):
    arr = np.array(image)
    ycrcb = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return Image.fromarray(cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB))


# Adjust image brightness using a scaling factor
def adjust_brightness(image, factor=1.0):
    return ImageEnhance.Brightness(image).enhance(factor)


# Adjust image contrast to make differences between light and dark areas more visible
def adjust_contrast(image, factor=1.0):
    return ImageEnhance.Contrast(image).enhance(factor)


def adjust_sharpness(image, factor=1.0):
    return ImageEnhance.Sharpness(image).enhance(factor)


def adjust_saturation(image, factor=1.0):
    return ImageEnhance.Color(image).enhance(factor)


def adjust_exposure(image, gain=1.0):
    arr = img_as_float(np.array(image))
    return Image.fromarray(img_as_ubyte(exposure.adjust_log(arr, gain)))


def main():
    path = input("Path: ")
    try:
        img = load_image(path)
    except Exception as e:
        print(f"Load error: {e}")
        return

    current = img.copy()
    modified = False

    while True:
        print("\nMenu:\n"
              "1.Gamma \n2.HistEq  \n3.Brightness  \n4.Contrast\n"
              "5.Sharpness \n6.Saturation \n7.Exposure\n"
              "8.Show  \n9.Save  \n0.Exit")
        choice = input("Choose: ")

        match choice:
            case '0':
                print("Exit.")
                break

            case '1':
                g = float(input("Gamma [1.0]: ") or 1.0)
                current = apply_gamma(current, g)
                modified = True

            case '2':
                current = apply_hist_eq(current)
                modified = True

            case '3':
                f = float(input("Brightness [1.0]: ") or 1.0)
                current = adjust_brightness(current, f)
                modified = True

            case '4':
                f = float(input("Contrast [1.0]: ") or 1.0)
                current = adjust_contrast(current, f)
                modified = True

            case '5':
                f = float(input("Sharpness [1.0]: ") or 1.0)
                current = adjust_sharpness(current, f)
                modified = True

            case '6':
                f = float(input("Saturation [1.0]: ") or 1.0)
                current = adjust_saturation(current, f)
                modified = True

            case '7':
                g = float(input("Exposure [1.0]: ") or 1.0)
                current = adjust_exposure(current, g)
                modified = True

            case '8':
                current.show()

            case '9':
                if not modified:
                    print("Nothing to save.")
                    continue
                out = input("Save as: ")
                save_image(current, out)
                modified = False

            case _:
                print("Invalid.")
                continue

        if modified:
            print("Done.")
            current.show()


if __name__ == '__main__':
    main()
