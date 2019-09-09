FROM python:3
LABEL maintainer "Benny Li <dev@benny-li.de>"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME [ "/data/" ]

CMD [ "python", "./scan-reader.py" ]
