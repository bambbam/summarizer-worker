FROM python:3.8
RUN pip3 install poetry
COPY . /code
WORKDIR /code
RUN apt install ffmpeg -y
RUN pip install cmake
RUN poetry install --no-root
CMD ["poetry", "run", "poe", "app"]
