FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime	

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get update && \
  apt install -y tmux && \
    pip install --no-cache-dir -r requirements.txt

# CMD [ "python","run_app.py"]
#Expose server port
# EXPOSE 8080