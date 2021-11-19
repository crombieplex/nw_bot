FROM python:3.8
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN git clone https://github.com/Pycord-Development/pycord \
    && cd pycord \
    && git checkout groups \
    && python3 -m pip install -U . \
    && rm -rf pycord
CMD python3 main.py