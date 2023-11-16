FROM python:3.10.0-slim
RUN apt update && apt-get install -y python3-opencv
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
#PYTHONPATH for web_service.py to import functions from object_detection
ENV PYTHONPATH "${PYTHONPATH}:/code:/code/object_detection"
EXPOSE 8000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "web_service:app"]
#https://stackoverflow.com/questions/43925487/how-to-run-gunicorn-on-docker

