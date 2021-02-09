# Smart Contact

## How to run project

1. Create virtual environment 
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Commit DB migrations
```bash
python manage.py migrate
```
4. Create superuser to get access to admin site
```bash
python manage.py createsuperuser
```
5. Run the server
```bash
python manage.py runserver
```
Admin page: /admin