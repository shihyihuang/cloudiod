from flask import Flask
from flask import request
import object_detection.object_detection as object_detection
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import json


 #create a Flask app by calling the Flask constructor
app = Flask(__name__)

@app.route('/api/image', methods =['post'])
def detect_image():
    # retrieves HTTP request in JSON format
    request_json = request.get_json()
    request_dictionary = json.loads(request_json)
    image_base64 = request_dictionary["image"]
    detected_item = object_detection.detect_image(image_base64) #function shows as below
    return detected_item

"""
    def detect_image(image_base64):

    try:
        # decodes the base64-encoded image 
        image_bytes = base64.b64decode(image_base64)
        # convert the bytes object to a NumPy array of unsigned integers
        image_nparray = np.frombuffer(image_bytes, np.uint8)
        image_copy=image_nparray.copy()
        # decode np array into an OpenCV image obj with color info
        image_opencv = cv2.imdecode(image_copy, cv2.IMREAD_COLOR)
        # convert color space of the image from BGR to RGB
        image_opencv_cvtvolor=cv2.cvtColor(image_opencv, cv2.COLOR_BGR2RGB)
        # loads a neural network model as the parameter to call do_prediction to predict the image
        nets = load_model(CFG, Weights)
        return do_prediction(image_opencv_cvtvolor, nets, Lables)
    except Exception as e:
        return {"error" : "Error : {}".format(e)}
"""


#if __name__ == "__main__":
    #app.run(debug = True, host='0.0.0.0', port=8000, threaded=True)
    # threaded=True enables multi-threading to handle multiple clients concurrently


