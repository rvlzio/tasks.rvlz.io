FROM python:3.10.0-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt
RUN rm -rf /requirements

RUN mkdir /src
COPY ./src /src

COPY ./start_server.sh /start_server.sh
RUN chmod +x /start_server.sh

CMD ["/start_server.sh"]
