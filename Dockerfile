FROM python:3.8

# Fix locales
RUN apt update && apt install locales -y && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# For production, use gunicorn or nginx
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]