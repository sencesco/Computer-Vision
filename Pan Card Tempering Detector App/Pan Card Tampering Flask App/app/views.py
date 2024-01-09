# Important imports
from app import app
from flask import request, render_template
import os
from skimage.metrics import structural_similarity   # pip or conda install scikit-image
import imutils
import cv2
from PIL import Image

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original'
app.config['GENERATED_FILE'] = 'app/static/generated'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Execute if request is get
    if request.method == "GET":
        return render_template("index.html")

    # Execute if request is post
    if request.method == "POST":
        # Get uploaded images
        file_upload = request.files['file_upload']
        second_file_upload = request.files['second_file_upload']

        # Resize and save the first uploaded image
        uploaded_image = Image.open(file_upload).resize((250, 160))
        uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

        # Resize and save the second uploaded image
        second_uploaded_image = Image.open(second_file_upload).resize((250, 160))
        second_uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'second_image.jpg'))

        # Resize and save the original image to ensure both uploaded and original match in size
        original_image = Image.open(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg')).resize((250, 160))
        original_image.save(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))

        # Read uploaded and original images as arrays
        original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))
        uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))
        second_uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'second_image.jpg'))

        # Convert images into grayscale
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        second_uploaded_gray = cv2.cvtColor(second_uploaded_image, cv2.COLOR_BGR2GRAY)

        # Calculate structural similarity for the first image
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")

        # Calculate structural similarity for the second image
        (score_second, diff_second) = structural_similarity(original_gray, second_uploaded_gray, full=True)
        diff_second = (diff_second * 255).astype("uint8")

        # Calculate threshold and contours for the first image
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Draw contours on the first image
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save all output images for the first image (if required)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)

        # Calculate threshold and contours for the second image
        thresh_second = cv2.threshold(diff_second, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts_second = cv2.findContours(thresh_second.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_second = imutils.grab_contours(cnts_second)

        # Draw contours on the second image
        for c in cnts_second:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(second_uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save all output images for the second image (if required)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'second_image_uploaded.jpg'), second_uploaded_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'second_image_diff.jpg'), diff_second)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'second_image_thresh.jpg'), thresh_second)

        # Combine the scores from both images or choose another method to present the results
        total_score = (score + score_second) / 2

        return render_template('index.html', similarity_result=str(round(total_score * 100, 2)) + '%' + ' that each image similarity to each other')
    
@app.route("/reload", methods=["GET"])
def reload_page():
    return render_template("index.html")

# Main function
if __name__ == '__main__':
    app.run(debug=True)
