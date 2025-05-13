# Image Processing Application

This is a command-line application for performing various image processing operations on an input image. The application allows users to load an image, apply transformations such as gamma correction, histogram equalization, brightness adjustment, and more, and then save the modified image.

## Features

- Load an image from a specified path.
- Apply the following operations:
  - Gamma Correction
  - Histogram Equalization
  - Adjust Brightness
  - Adjust Contrast
  - Adjust Sharpness
  - Adjust Saturation
  - Adjust Exposure
- Display the current image.
- Save the modified image with minimal compression artifacts.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Pillow (`PIL`)
- scikit-image (`skimage`)

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required libraries using pip:

```bash
pip install opencv-python numpy pillow scikit-image
```

## Usage

1. Run the script:

```bash
python image_processing.py
```

2. When prompted, enter the path to the image you want to process.
3. Use the menu to select an operation:
   - Enter the number corresponding to the operation you want to apply.
   - For operations that require parameters, you will be prompted to enter the values. If you press Enter without typing a value, the default will be used.
   - Choose option 8 to display the current image.
   - Choose option 9 to save the modified image. You will be asked to provide a filename (e.g., `result.jpg` or `result.png`).
   - Choose option 0 to exit the application.

## Operations

- **Gamma Correction**: Adjusts the gamma value of the image. A gamma value less than 1 makes the image brighter, while a value greater than 1 makes it darker.
- **Histogram Equalization**: Enhances the contrast of the image by equalizing the histogram of the luminance channel.
- **Adjust Brightness**: Increases or decreases the brightness of the image.
- **Adjust Contrast**: Increases or decreases the contrast of the image.
- **Adjust Sharpness**: Sharpens or blurs the image.
- **Adjust Saturation**: Increases or decreases the color saturation of the image.
- **Adjust Exposure**: Adjusts the exposure of the image using logarithmic mapping.

## Saving Images

When saving the image, the application attempts to minimize compression artifacts:
- For JPEG images, it uses high quality (default 95), optimizes the image, and disables subsampling.
- For PNG images, it uses a low compression level to preserve quality.

## Notes

- The image must be in a supported format like JPG, PNG, or BMP.
- All transformations are cumulative — each operation applies on top of the previous one.
- It's recommended to keep a backup of the original image before saving.
- When adjusting brightness, contrast, etc., values around 1.0 mean no change.
- Histogram Equalization works best with grayscale or low-contrast images.


- The application converts the image to RGB format upon loading.
- All operations are applied to a copy of the original image, so the original remains unchanged unless saved.
- If you try to save without making any modifications, you will be notified that there are no changes to save.
## Reviewed By
MR. President Abdallah Haider
## Reviewed By
Ahmed Maher Plus
