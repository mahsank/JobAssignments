FROM python:3.6-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install the required modules
COPY requireddeps.pip .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requireddeps.pip

# Run the application
COPY 20210319-TechnicalTask.py .
ENTRYPOINT ["python", "./20210319-TechnicalTask.py"]
