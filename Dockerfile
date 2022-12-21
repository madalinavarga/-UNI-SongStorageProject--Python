FROM python:3.10

WORKDIR /usr/src/app

COPY Main.py . 
COPY features.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "./Main.py" ]