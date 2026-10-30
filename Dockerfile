FROM python:3.11-slim

# libgl/glib are needed by OpenCV, which Ultralytics pulls in
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

# gunicorn is more robust than the Flask dev server
RUN pip install --no-cache-dir gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "--threads", "4", "--timeout", "120", "run:app"]
