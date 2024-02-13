FROM python:3.10

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "main.py"]