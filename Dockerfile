# Python 3.13 base (slim Debian)
FROM python:3.13-slim

# Avoid .pyc and enable unbuffered logs; use headless matplotlib
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

# System deps for Pillow/Matplotlib/NumPy and GEOS
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev zlib1g-dev \
    libpng-dev libfreetype6-dev \
    libgeos-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Upgrade pip first
RUN python -m pip install --upgrade pip

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app /app

# If you kept root and want port 80, leave these two lines:
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
