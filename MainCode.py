import cv2
import numpy as np

def Gamma(image, gamma=1.0):
    # Build a lookup table mapping pixel values [0, 255] to their adjusted gamma values
    gamma_inverse = 1.0 / gamma
    table = np.array([((i / 255.0) ** gamma_inverse) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    # Apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def Equalization(image):
    return cv2.equalizeHist(image)

