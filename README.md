# Smart-Blogging-System


### For bulding container syntax
> docker build . -t <image_name>:<tag_name>

### Example For bulding container 
> docker build . -t smart_bloggin_proj:v1 

---

### Syntax for running container
> docker run -p 8000:8000 <docker_image_name>:<tag_name>

### Example for running container
> docker run -p 8000:8000 -v .:/smart_blogging_system --name smart_bloggin_project smart_bloggin_proj:v1

### For running makemigrations and migrate command and testcases
> docker exec -it smart_bloggin_project bash
> python3 manage.py makemigrations
> python3 manage.py migrate
> python3 manage.py test

---

### for running complete project test cases
> python3.8 manage.py test

### for running a specific app test cases
> python3.8 manage.py test <app_name>

### for running the testcases of a specific module in python
> python3.8 manage.py test <app_name>.<test_file_name>

### for running just one test case class
> python3.8 manage.py test <app_name>.<test_file_name>.<class_name>

### for running just one test method
> python3.8 manage.py test <app_name>.<test_file_name>.<class_name>.<method_name>