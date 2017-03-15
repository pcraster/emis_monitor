FROM pcraster/emis_base:latest

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY cmd.sh server.py /
COPY emis_monitor /emis_monitor
COPY test /test

CMD ["/cmd.sh"]
