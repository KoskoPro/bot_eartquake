FROM python:alpine
WORKDIR /app
COPY . .
RUN pip install --user aiogram
CMD ["python", "earthquake_bot.py"]
