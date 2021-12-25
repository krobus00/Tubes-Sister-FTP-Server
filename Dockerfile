FROM python:3.8-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
COPY .env .env
RUN pip install -r requirements.txt
EXPOSE 1818
COPY . .
CMD ["python", "server.py"]