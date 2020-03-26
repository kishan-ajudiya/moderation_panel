# Generic Moderation Panel

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://platoadmin.goibibo.com)
[![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://platoadmin.goibibo.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://platoadmin.goibibo.com)
[![forthebadge](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://platoadmin.goibibo.com)
[![forthebadge](https://forthebadge.com/images/badges/not-an-issue.svg)](https://platoadmin.goibibo.com)

#### Tech Stack Needed

1. MySQL 5.7
2. Redis
3. Mongo

#### Setup
* Clone Repo to the local system

* ``cd moderation_panel``
* Create two folder under code repo `logs` and `static`
* Create Virtual env with following command.

  `` python3 -m venv moderation_env ``
  
* Activate environment:

    ``
    source moderation_env/bin/activate
    ``
* Install all the requirements:  

    ``
    pip install -r requirement.txt
    ``

* Collect static files in static folder

    ``
    python manage.py collectstatic
    ``

* run the project

    ``
    python manage.py runserver
    ``

**Now your Moderation Panel Server is up**
