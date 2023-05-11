# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /clubpro_back

COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 uninstall -y jwt
RUN pip3 uninstall -y pyjwt
RUN pip3 install pyjwt

COPY api api/
COPY services services/
COPY *.py ./

CMD ["python3", "main.py"]
