# docker build -t thub.autohome.com.cn/ad_system/video_maker:1.0 .
docker rm video_maker
docker run --name=video_maker -v /home/aduser/data:/video_maker/data -itd thub.autohome.com.cn/ad_system/video_maker:1.0 /bin/bash

#docker exec -it video_maker /bin/bash