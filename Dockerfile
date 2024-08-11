FROM python:3.8
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1


RUN mkdir /smart_blogging_system
WORKDIR /smart_blogging_system
COPY . /smart_blogging_system
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

