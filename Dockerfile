FROM python:3.9-alpine

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the model loading script
CMD ["python", "model-load.py"]
