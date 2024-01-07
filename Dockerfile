FROM python:3.8

WORKDIR /app

COPY . /app

RUN chmod +x wait-for-it.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9001

CMD ["./wait-for-it.sh", "mysql-db:3306", "--", "python", "app.py"]
