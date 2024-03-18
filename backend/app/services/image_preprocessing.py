import cv2
import numpy as np
 
class Preprocessor:
    def __init__(self, blur_kernel_size=(5, 5), scale_factor=1.0, clahe_clip_limit=2.0, clahe_tile_grid_size=(8, 8)):
        self.blur_kernel_size = blur_kernel_size
        self.scale_factor = scale_factor
        self.clahe_clip_limit = clahe_clip_limit
        self.clahe_tile_grid_size = clahe_tile_grid_size
 
    def apply_clahe(self, image):
        img_y_cr_cb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(img_y_cr_cb)
        clahe = cv2.createCLAHE(clipLimit=self.clahe_clip_limit, tileGridSize=self.clahe_tile_grid_size)
        y_clahe = clahe.apply(y)
        img_y_cr_cb_clahe = cv2.merge((y_clahe, cr, cb))
        image_clahe = cv2.cvtColor(img_y_cr_cb_clahe, cv2.COLOR_YCrCb2BGR)
        return image_clahe
 
    def apply_gaussian_blur(self, image):
        variance = np.var(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        kernel_size = int(min(self.blur_kernel_size[0] + variance // 50, 31))  # Max kernel size 31, adjust as needed
        kernel_size = kernel_size + 1 if kernel_size % 2 == 0 else kernel_size  # Ensure kernel size is odd
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
 
    def adjust_brightness_contrast(self, image, brightness=0, contrast=100):
        img = np.int16(image)
        img = img * (contrast / 127 + 1) - contrast + brightness
        img = np.clip(img, 0, 255)
        img = np.uint8(img)
        return img
 
    def rescale_image(self, image):
        return cv2.resize(image, None, fx=self.scale_factor, fy=self.scale_factor, interpolation=cv2.INTER_AREA)
 
    def sharpen_image(self, image):
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
 
    def preprocess(self, image):
   
        image = self.apply_clahe(image)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = np.var(gray_image)
        variance_threshold = 500
        if variance > variance_threshold:
            image = self.apply_gaussian_blur(image)
        image = self.adjust_brightness_contrast(image)
        image = self.sharpen_image(image)  
        return image
 
 