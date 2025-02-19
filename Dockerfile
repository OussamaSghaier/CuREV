FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH="/app:$PYTHONPATH"

COPY . .

RUN pip install --no-cache-dir --no-build-isolation -r requirements.txt

CMD ["/bin/bash"]