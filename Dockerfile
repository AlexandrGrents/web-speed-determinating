FROM nvidia/cuda:11.0-devel-ubuntu18.04-rc
WORKDIR /home/app

RUN export TZ=Asia/Yekaterinburg
RUN export MPLBACKEND=TKAgg
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-tk 
RUN apt-get install -y python3-matplotlib python3-numpy python3-pil python3-scipy
RUN apt-get install -y python3-opencv
RUN pip3 install scikit-build
RUN pip3 install cmake
RUN pip3 install torch==1.7
RUN pip3 install --upgrade setuptools pip
RUN pip3 install opencv-python==4.4.0.46
RUN pip3 install gunicorn
COPY . .
RUN pip3 install -r requirements.txt
RUN python3 -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu110/torch1.7/index.html

RUN export LC_ALL=en_US.utf-8
RUN export LANG=en_US.utf-8
RUN export FLASK_APP=app:app
RUN pip3 list

