FROM python:3.10

WORKDIR /home/Documents

COPY . /home/Documents
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

#CMD ["gunicorn", "--chdir", "src", "app:server"]
CMD ["gunicorn", "-w", "8", "-b", ":7000", "--timeout", "120", "--chdir", "src", "app:server"]
#CMD ["python3", "./src/app.py"]
#CMD ["tail", "-f", "/dev/null"]
