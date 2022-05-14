FROM python:alpine

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.sh /
COPY cfddns.py /
CMD ["/bin/sh", "run.sh"]
