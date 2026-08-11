# Tech Interview Prep — Backend

Django REST API for a tech interview prep community platform.

## Setup
1. `python -m venv venv && venv\Scripts\activate`
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py runserver`

## Apps
- accounts — users, auth tokens
- taxonomy — companies, job roles, tags
- questions — core content
- discussions — solutions, comments
- voting, progress, notifications, moderation