FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY . /app

COPY --from=builder /usr/local/lib/python3.11/site-packages \
                    /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ENV PATH="/usr/local/bin:$PATH"

ENV PORT=8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]
