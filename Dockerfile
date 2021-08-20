FROM python:3.8.5
RUN python3 -m venv venv
RUN . /venv/bin/activate
ENV FOO=/code
WORKDIR ${FOO}
COPY requirements.txt $FOO
RUN pip3 install -r ${FOO}/requirements.txt
COPY . $FOO
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000 