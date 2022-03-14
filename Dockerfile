FROM python:3.9

RUN apt update && apt install -y stress-ng && pip install pyyaml

ADD main.py /app/main.py

CMD python /app/main.py