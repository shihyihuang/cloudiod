## IMPORTANT NOTICE
1. As of the current state, Docker is not operational!!!
2. The 'object_detection' and 'yolo_tiny_configs' folders have been provided by the teaching team of Monash University.


# object_detection

object_detection.py  is a Python script to perform object detection using tiny yolo weights and neural net

## Installation

The basic python packages are part of the  python installation. You also need to install python packages depending
including Flask, opencv-python, numpy, etc. Make sure you use python 3.5 or higher and upgrade your pip tool.
If any Linux dependencies are required, you shall install them based on system requirements.

# URL to the web service endpoint
http://168.138.29.44:31000/api/image

## Usage format
python Cloudiod_client.py  <input folder name> <URL> <num_threads>

## Sample run command
python3 Cloudiod_client.py  inputfolder/  http://localhost:5000/api/object_detection 4
python object_detection.py yolo_tiny_configs/ image3.jpg 
python3 object_detection/object_detection.py yolo_tiny_configs/ myenv/testimage/000000012807.jpg
