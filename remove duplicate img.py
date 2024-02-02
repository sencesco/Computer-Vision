import cv2
import os
from skimage.metrics import structural_similarity as ssim

SIMILARITY_THRESHOLD = 0.85

# Resize or processing
WIDTH_PROCESSING = 893
HEIGHT_PROCESSING = 500

# Resize output
RE_WIDTH_OUT = 1920 
RE_HEIGHT_OUT = 1080

# Function to calculate SSIM between two images
def calculate_ssim(img1, img2):
    # Resize images if image size very large
    img1 = cv2.resize(img1, (WIDTH_PROCESSING, HEIGHT_PROCESSING))
    img2 = cv2.resize(img2, (WIDTH_PROCESSING, HEIGHT_PROCESSING))
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Reduce a noise
    blurred1 = cv2.GaussianBlur(gray1, (5, 5), 0)
    blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)

    # Edge detection 
    edges1 = cv2.Canny(blurred1, 50, 150)
    edges2 = cv2.Canny(blurred2, 50, 150)

    # Calculate SSIM on the edge-detected images
    return ssim(edges1, edges2)

# Create new folder for stor set og image
try:
    # Creating a folder for storing images
    if not os.path.exists('img_rmd'):
        os.makedirs('img_rmd')

# If not created then raise an error
except OSError:
    print('Error: Creating directory of img_rmd')

# Read image from fil oath
image_folder = r'img'
img_name_ls = os.listdir(image_folder)
print(len(img_name_ls))

# For new order name file
i = 1
# Read all image in file path
for num_img in range(1,len(img_name_ls)):
    p_lm = r"img/0-mathematics-for-ai-statisticalpng_Page{}.png".format(num_img)
    # If imag end with jpg and png
    if p_lm.endswith(('.jpg', '.png')):
        img = cv2.imread(p_lm)
        # if index > 1 will compare similarity of image to skip current image that same as image before
        if num_img > 1:
            p_lm_prev = r"img/0-mathematics-for-ai-statisticalpng_Page{}.png".format(num_img-1)
            img_prev = cv2.imread(p_lm_prev)
            similarity = calculate_ssim(img_prev, img)
            if similarity > SIMILARITY_THRESHOLD:
                continue
            i += 1
            name = './img_rmd/img_' + str(i) + '.jpg'
            print('Creating...' + name)
            # Modifiend outpue of image size
            img_resized = cv2.resize(img, (RE_WIDTH_OUT, RE_HEIGHT_OUT))
            cv2.imwrite(name, img_resized)
        else:
            name = './img_rmd/img_' + str(num_img) + '.jpg'
            print('Creating...' + name)
            img_resized = cv2.resize(img, (RE_WIDTH_OUT, RE_HEIGHT_OUT))
            cv2.imwrite(name, img_resized)

        





