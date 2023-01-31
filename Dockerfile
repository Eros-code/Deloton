FROM python:3.10

WORKDIR /app

RUN python3 -m pip install --upgrade pip

# Install the Python dependencies
ADD requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy all the application files inside of the container
COPY ./app .

CMD ["python3", "main.py"]