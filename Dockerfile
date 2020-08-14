FROM python:3.8

RUN apt update -y
RUN apt install -y ffmpeg

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

COPY . /

ENTRYPOINT [ "python" ]

CMD [ "src/model/main.py" ]
