FROM python:3.9-alpine

WORKDIR /app

COPY . .

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev g++ make python3-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the model loading script
CMD ["python", "model-load.py"]
