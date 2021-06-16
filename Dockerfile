FROM python:3.9-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY paycom.py main.py /app/

CMD ["python", "main.py"]