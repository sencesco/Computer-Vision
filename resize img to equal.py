import cv2
import os

# Resize output
RE_WIDTH_OUT = 1920 
RE_HEIGHT_OUT = 1080

# Create new folder for stor set og image
try:
    # Creating a folder for storing images
    if not os.path.exists('img_re'):
        os.makedirs('img_re')

# If not created then raise an error
except OSError:
    print('Error: Creating directory of img_rmd')

# Read image from fil oath
image_folder = r'img_dat'
img_name_ls = os.listdir(image_folder)
print(len(img_name_ls))


# Read all image in file path
for num_img in range(1,len(img_name_ls)+1):
    p_lm = r"img_dat/i{}.png".format(num_img)
    # If imag end with jpg and png
    if p_lm.endswith(('.jpg', '.png')):
        img = cv2.imread(p_lm)
        name = './img_re/img_' + str(num_img) + '.jpg'
        print('Creating...' + name)
        # Modifiend outpue of image size
        img_resized = cv2.resize(img, (RE_WIDTH_OUT, RE_HEIGHT_OUT))
        cv2.imwrite(name, img_resized)


        





