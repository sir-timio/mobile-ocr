FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime	

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get update && \
  apt install -y tmux && \
    pip install --no-cache-dir -r requirements.txt


RUN apt-get install build-essential libboost-all-dev cmake zlib1g-dev libbz2-dev liblzma-dev -y
RUN pip install https://github.com/kpu/kenlm/archive/master.zip

# CMD [ "python","run_app.py"]
#Expose server port
# EXPOSE 8080
