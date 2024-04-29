FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install pandas numpy
RUN mkdir -p so_output && chmod 777 so_output  # Create and set permissions
CMD ["python", "main.py"]
