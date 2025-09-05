FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

COPY libs/python-common /tmp/python-common
RUN pip install /tmp/python-common && rm -rf /tmp/python-common

COPY services/cart-service/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY services/cart-service/app /app/app

EXPOSE 8000
CMD ["gunicorn", "app.main:create_app()", "-b", "0.0.0.0:8000", "-w", "2", "-k", "gthread"]

