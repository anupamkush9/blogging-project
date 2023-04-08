FROM python:3.8
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN mkdir /smart_blogging_system
WORKDIR /smart_blogging_system
COPY . /smart_blogging_system
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# docker run -p 8989:8989 <docker_image_name>:<tag_name>
# docker build . -t <image_name>:<tag_name> 
# docker build . -t anupam:1058 
# docker run -p 8989:8000 -v .:/smart_blogging_system anupam:1058