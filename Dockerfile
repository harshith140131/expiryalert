
FROM python:3.9-slim

WORKDIR /app
# COPY requirements.txt requirements.txt

COPY . .
# RUN git clone https://github.com/streamlit/streamlit-example.git .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5004




ENTRYPOINT ["streamlit", "run", "invoice.py", "--server.port=5004", "--server.address=0.0.0.0"]