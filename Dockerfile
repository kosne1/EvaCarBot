FROM python

WORKDIR /EvaCarBot

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]