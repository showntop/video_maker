FROM python:3
MAINTAINER xiaorongtao
LABEL version="1.0"
RUN apt-get update
RUN apt-get install ffmpeg -y
WORKDIR /video_maker
ADD . /video_maker
RUN cd /video_maker 
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p data/output
RUN mkdir -p data/videos
CMD ["python", "pipline.py"]