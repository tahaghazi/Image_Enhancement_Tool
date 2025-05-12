import cv2
import numpy as np
from PIL import Image, ImageEnhance
from skimage import io, exposure


def Gamma(image, gamma=1.0):
    image = image / 255.0
    return cv2.pow(image, gamma)


def Equalization(image):
    return exposure.equalize_hist(image)


def AdjustBrightness(image, factor=1.0):
    enhancer = ImageEnhance.Brightness(image)
    Adjusted_image = enhancer.enhance(factor)
    return Adjusted_image


def AdjustContrast(image, factor=1.0):
    enhancer = ImageEnhance.Contrast(image)
    contrast_image = enhancer.enhance(factor)
    return contrast_image


def AdjustSharpness(image, factor=1.0):
    enhancer = ImageEnhance.Sharpness(image)
    sharp_image = enhancer.enhance(factor)
    return sharp_image


def AdjustSaturation(image, factor=1.0): 
    enhancer = ImageEnhance.Color(image)
    Saturated_image = enhancer.enhance(factor)
    return Saturated_image


def AdjustExposure(image, factor=1.0):
    # Convert the image to float32 for exposure adjustment
    image_float = image.astype(np.float32) / 255.0
    
    # Apply exposure adjustment
    adjusted_image = np.clip(image_float * factor, 0, 1)
    
    # Convert back to uint8
    adjusted_image = (adjusted_image * 255).astype(np.uint8)
    
    return adjusted_image


