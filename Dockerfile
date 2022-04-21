
FROM python:alpine

COPY requirements.txt /requirements.txt
RUN \
  pip install -r /requirements.txt; \
  rm /requirements.txt

COPY src /app
WORKDIR /app
USER nobody

ENV \
  PROJ_TMDB_KEY=xxxxxxx \
  PROJ_MONGO_HOST=xxxxx \
  PROJ_MONGO_PORT=xxxxx \
  PROJ_MONGO_DB=xxxxxxx

CMD ["python", "flaskApp.py"]
