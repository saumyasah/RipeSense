from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from upload import analyze_mango_ripeness

app = Flask(__name__)

@app.route('/analyze_mango', methods=['POST'])
def analyze_mango():
    try:
        data = request.json
        base64_image = data.get('image')

        if base64_image:
            # Decode the base64 image
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))

            # Analyze the mango ripeness
            fully_ripe_percentage, partially_ripe_percentage, unripe_percentage, ripeness = analyze_mango_ripeness(image)

            response = {
                "fully_ripe_percentage": fully_ripe_percentage,
                "partially_ripe_percentage": partially_ripe_percentage,
                "unripe_percentage": unripe_percentage,
                "ripeness": ripeness
            }
            return jsonify(response)
        else:
            return jsonify({"error": "No image provided in the request"})
    except Exception as e:
        return jsonify({"error": str(e)})

# create a route for the app health

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)



# python -m pip install streamlit opencv-python-headless numpy pillow Flask

