### **IMPORTANT NOTICE**
1. As of the current state, Docker is not operational!!!
2. The 'object_detection' and 'yolo_tiny_configs' folders have been provided by the teaching team of Monash University.

### **Performance Experimental Result**

**Average response time of the web service versus the number of pods for different number of threads for the local client** 
![local.png](img%2Flocal.png)

**Average response time of the web service versus the number of pods for different number of threads for the Nectar client** 
![nectar.png](img%2Fnectar.png)

**Explanation and Justification of the experimental results**

The above two plots illustrate the result of two sets of experiments conducted on a web-based system, Cloudiod. 
One experiment was carried out with the client locally on the master node of Kubernetes, while the other was conducted on a VM instance in Nectar. 
In both experiments, the system was evaluated under varying numbers of threads in the client, with varying numbers of pods in the cluster.

First, both experiments demonstrate that the average response time tends to decrease as the number of threads increases. 
The shortest average response time occurred when both the number of threads in the client and the pods in the cluster were 16, 
while the longest average response time occurred when both were set to 1. However, beyond a certain threshold, 
increasing the number of threads in the client may not significantly improve the response time and could even result in slower response times.
Take the Nectar client experiment result as an instance, when the cluster has 16 pods, the response time is 0.65 and 0.545 when the client has 2 and 8 threads, respectively. 
The response time, however, increased to 0.546 when the client was configured to use 16 threads (as shown in Plot 2).
Increasing more pods in the cluster can improve response time by handling concurrent requests since the workload is distributed. 
Likewise, adding more threads allows parallel requests, enhancing throughput and decreasing response time. 
However, as more threads are added to the client, the number of requests sent to the remote server increases, 
and the system load could surpass its capacity when the number of requests goes beyond a certain point. 
Basically, as the number of requests sent to the server increases, so does the workload it needs to handle. 
If the server is unable to cope with the workload, the system can become overloaded, leading to poor performance or system crashes. 
Simply, using too few or too many threads or pods can diminish performance by being unable to manage a substantial number of requests, encountering resource contention, or generating additional overhead.

Secondly, upon the comparison of the two plots, it can be observed that the response time of the Nectar client is marginally slower than that of the local client. 
More detailed results are provided in Appendix A. This could be attributed to the increased latency caused by requests traveling over the network, 
which can lead to slower response times for remote clients, depending on network bandwidth and the amount of data being transferred. 
Conversely, if the client and server are on the same machine, they communicate through the same network stack, minimizing network latency. 
Resources are shared and used more efficiently, resulting in better performance.
Thirdly, prior to implementing Gunicorn for performance optimization, the web server running within the pod was unable to handle incoming requests, 
which caused the pod to continually crash and restart, resulting in a CrashLoopBackOff state (Refer to Appendix B for information on the successful response rate of the Flask Application on the Built-in Server). 
Gunicorn serves as a proxy server that mediates between the web application and the client, 
capable of managing numerous requests at once and distributing them to the appropriate worker process without consuming excessive resources (Shaw, 2021). 
By implementing Gunicorn, the web server can handle numerous client requests without crashing or becoming unresponsive, which leads to more stable and efficient system performance.
Conclusively, increasing the number of threads and pods can improve performance up to a certain point, 
but beyond that point, the system capacity will be exceeded, and performance will thus degrade, or the system may fail. 
Finding the optimal balance between the number of threads and pods is important to maximize performance without overloading the system.


### **Reference**

Shaw, S. (2021, September 8). Usage of Gunicorn for deploying Python web applications. GitConnected. https://levelup.gitconnected.com/usage-of-gunicorn-for-deploying- python-web-applications-1e296618e1ab


### **Appendix A**
Average response time of the web service versus the number of pods for different number of threads for the local client and Nectar client
![appendixA.png](img%2FappendixA.png)

**Appendix B**
Successful Response Rate of the request from the Nectar Cloud Client with Flask Application on Built-in Server
![appendixB.png](img%2FappendixB.png)

Average response time of the Flask Application on the Built-in Server versus the number of pods for different numbers of threads for the Nectar client
![appendixB2.png](img%2FappendixB2.png)

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
