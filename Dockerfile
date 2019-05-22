FROM thub.autohome.com.cn/ad_system/anaconda3:1.0
MAINTAINER xiaorongtao
LABEL version="1.0"
RUN apt-get update
RUN apt-get install ffmpeg
WORKDIR /video_maker
ADD . /video_maker
RUN cd /video_maker 
RUN /root/anaconda3/bin/pip install -r requirements.txt
CMD ["/root/anaconda3/bin/python", "pipline.py"]