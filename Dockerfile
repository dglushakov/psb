FROM python:alpine

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python3", "-m" , "flask", "--app=src/app", "run", "--host=0.0.0.0"]