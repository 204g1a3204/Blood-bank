E-blood-bank

Required softwares:
python
pycharm

Installation commands:
pip install -r requirements.txt
pip uninstall crypto
pip uninstall pycryptodome
pip install pycryptodome

Create Database based on Models:
python manage.py makemigrations
python manage.py migrate

Load initial data into database:
py manage.py loaddata init-db.json


