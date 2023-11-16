# import the necessary packages
import numpy as np
import base64
import sys
import time
import cv2
import os

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1

def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    lpath=os.path.sep.join([yolo_path, labels_path])

    print(yolo_path)
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weights_path])
    return weightsPath

def get_config(config_path):
    configPath = os.path.sep.join([yolo_path, config_path])
    return configPath

def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

def get_image_base64(image_path):
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return image_base64

image_folder = 'cloudiod/3ppl.jpeg'

# def main():
#     with open('cloudiod/3ppl.jpeg', 'rb') as image_file:
#         image_bytes = image_file.read()
#         image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#     with open('output.txt', 'w') as output_file:
#         output_file.write(image_base64)


def do_prediction(image,net,LABELS):

    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # TODO Prepare the output as required to the assignment specification
    # ensure at least one detection exists
    detected_item = []
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            item_data = {
                "label" : LABELS[classIDs[i]],
                "accuracy" : confidences[i],
                "rectangle":{
                    "height" :boxes[i][3],
                    "left": boxes[i][0],
                    "top": boxes[i][1],
                    "width": boxes[i][2]
                }
            }
            detected_item.append(item_data)
    return detected_item


#yolo_path  = str(sys.argv[1])
yolo_path  = "yolo_tiny_configs"

## Yolov3-tiny versrion
labelsPath= "coco.names"
cfgpath= "yolov3-tiny.cfg"
wpath= "yolov3-tiny.weights"

Lables=get_labels(labelsPath)
CFG=get_config(cfgpath)
Weights=get_weights(wpath)

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


#TODO, you should  make this console script into webservice using Flask
def main():
    ## argument
    if len(sys.argv) != 3:
        raise ValueError("Argument list is wrong. Please use the following format:  {} {} {}".
                     format("python iWebLens_server.py", "<yolo_config_folder>", "<Image file path>"))
    try:
        imagefile = str(sys.argv[2])
        img = cv2.imread(imagefile)
        npimg=np.array(img)
        image=npimg.copy()
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # load the neural net.  Should be local to this method as its multi-threaded endpoint
        nets = load_model(CFG, Weights)
        do_prediction(image, nets, Lables)
        #print(do_prediction(image, nets, Lables))
    except Exception as e:
        print("Exception  {}".format(e))



if __name__ == '__main__':
    main()


