FROM python:3.11-slim

COPY . .

COPY requirements.txt ./ 

RUN pip install -U pip

RUN pip install -r ./requirements.txt --no-cache-dir --no-input 

