FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -------- Stage 2: Runtime -------- #
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn
#CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "run:app"]
CMD ["gunicorn", "--workers=1", "--timeout=120", "--bind=0.0.0.0:5000", "run:app"]