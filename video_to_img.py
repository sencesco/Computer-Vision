import cv2
import os
from skimage.metrics import structural_similarity as ssim
import time

SIMILARITY_THRESHOLD = 0.9
SKIP_FRAMES = 1500  

# Function to calculate SSIM between two images
def calculate_ssim(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return ssim(gray1, gray2)

# Read the video from the specified path
cam = cv2.VideoCapture(r"C:\Users\Hp\Downloads\Video\a.mp4")

try:
    # Creating a folder for storing images
    if not os.path.exists('data_img'):
        os.makedirs('data_img')

# If not created then raise an error
except OSError:
    print('Error: Creating directory of data_img')

# Frame
currentframe = 0

# Previous frame
prev_frame = None

while True:
    # Reading from frame
    ret, frame = cam.read()

    if ret:
        # If video is still left continue creating images
        name = './data_img/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        # Check similarity with the previous frame
        if prev_frame is not None:
            similarity = calculate_ssim(frame, prev_frame)
            
            # If similarity is above threshold, skip generating the image
            if similarity > SIMILARITY_THRESHOLD:
                continue

        # Writing the extracted images
        cv2.imwrite(name, frame)

        # Update the previous frame
        prev_frame = frame.copy()

        # Increasing counter so that it will
        # show how many frames are created
        currentframe += 1

        # Skip frames to read more quickly
        for _ in range(SKIP_FRAMES):
            ret, _ = cam.read()
            if not ret:
                break
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
