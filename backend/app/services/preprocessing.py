import cv2
import numpy as np




def preprocess_frame(frame, USE_GRAYSCALE, USE_GAUSSIAN_BLUR, USE_HISTOGRAM_EQUALIZATION, USE_EDGE_ENHANCEMENT, USE_NORMALIZATION):
    preprocessed_frame = frame.copy()
    frame_height, frame_width, _ = frame.shape

    if USE_GRAYSCALE:
        preprocessed_frame = cv2.cvtColor(preprocessed_frame, cv2.COLOR_BGR2GRAY)
        preprocessed_frame = cv2.cvtColor(preprocessed_frame, cv2.COLOR_GRAY2BGR)

    if USE_GAUSSIAN_BLUR:
        preprocessed_frame = cv2.GaussianBlur(preprocessed_frame, (5, 5), 0)

    if USE_HISTOGRAM_EQUALIZATION:
        gray_frame = cv2.cvtColor(preprocessed_frame, cv2.COLOR_BGR2GRAY) if not USE_GRAYSCALE else preprocessed_frame
        equalized_frame = cv2.equalizeHist(gray_frame)
        preprocessed_frame = cv2.cvtColor(equalized_frame, cv2.COLOR_GRAY2BGR)

    if USE_EDGE_ENHANCEMENT:
        laplacian = cv2.Laplacian(preprocessed_frame, cv2.CV_64F)
        preprocessed_frame = cv2.convertScaleAbs(preprocessed_frame - laplacian)

    if USE_NORMALIZATION:
        preprocessed_frame = preprocessed_frame / 255.0

    return preprocessed_frame, frame_width, frame_height


preprocess_frame_func = lambda frame: preprocess_frame(frame, USE_GRAYSCALE=True, USE_GAUSSIAN_BLUR=True, USE_HISTOGRAM_EQUALIZATION=False, USE_EDGE_ENHANCEMENT=True, USE_NORMALIZATION=False)  