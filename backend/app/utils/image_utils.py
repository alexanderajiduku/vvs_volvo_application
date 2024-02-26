import cv2

def load_images(image_paths):
    images = []
    for fname in image_paths:
        img = cv2.imread(fname)
        if img is not None:
            images.append(img)
    return images
