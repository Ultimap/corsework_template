FROM python:3.10

WORKDIR /backend

COPY req.txt /backend/req.txt

RUN pip install --no-cache-dir --upgrade -r /backend/req.txt

COPY . /backend/.

CMD sh -c "uvicorn main:app --host 0.0.0.0 --port 80"


