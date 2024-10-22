from ..extension import db
from ..models.core import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class ImageService:
    def add_image(self, user_id, filename, filepath):
        new_image = Image(user_id=user_id, filename=filename, filepath=filepath)
        db.session.add(new_image)
        db.session.commit()
        return new_image

    def generate_histogram(self, image_id, user_id):
        image = Image.query.filter_by(id=image_id, user_id=user_id).first()
        if not image:
            return {"error": "Image not found"}, 404

        img = cv2.imread(image.filepath)
        color = ('b', 'g', 'r')
        histogram_data = {}

        for i, col in enumerate(color):
            histogram = cv2.calcHist([img], [i], None, [256], [0, 256])
            histogram_data[col] = histogram.flatten().tolist()

        return histogram_data

    def generate_segmentation_mask(self, image_id, user_id):
        image = Image.query.filter_by(id=image_id, user_id=user_id).first()
        if not image:
            return {"error": "Image not found"}, 404

        img = cv2.imread(image.filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        mask_filename = f"mask_{image.filename}"
        mask_filepath = os.path.join('uploads', mask_filename)
        cv2.imwrite(mask_filepath, mask)

        return mask_filename

    def manipulate_image(self, image_id, data, user_id):
        image = Image.query.filter_by(id=image_id, user_id=user_id).first()
        if not image:
            return {"error": "Image not found"}, 404

        img = cv2.imread(image.filepath)

        if 'resize' in data:
            width, height = data['resize']
            img = cv2.resize(img, (width, height))

        if 'crop' in data:
            x, y, w, h = data['crop']
            img = img[y:y+h, x:x+w]

        manipulated_filename = f"manipulated_{image.filename}"
        manipulated_filepath = os.path.join('uploads', manipulated_filename)
        cv2.imwrite(manipulated_filepath, img)

        return Image(user_id=user_id, filename=manipulated_filename, filepath=manipulated_filepath)

    def get_user_images(self, user_id):
        # Query the database to get all images for the user
        return Image.query.filter_by(user_id=user_id).all()
