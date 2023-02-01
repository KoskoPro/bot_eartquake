FROM python:alpine
RUN pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip3 install --user aiogram requests
CMD ["python", "earthquake_bot.py"]
