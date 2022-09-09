FROM python:3.6
RUN mkdir /app
WORKDIR /app
COPY app /app

RUN pip install --no-cache-dir -r requirements.txt
RUN dvc pull
# RUN chmod a+x ./run.sh

# EXPOSE 5000
# ENTRYPOINT ["./run.sh"]
