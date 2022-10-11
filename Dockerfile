FROM python:3.10-alpine

WORKDIR /home

ENV TG_API_TOKEN=""

COPY *.py ./
COPY requirements.txt ./
COPY quiz.db ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]