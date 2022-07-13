# Web Hradecke sovy

Development
-----------

```
pip install virtualenv
virtualenv env
virtualenv --always-copy env (for vagrant on Windows)
```

venv/bin/activate
```
export HKSOVA_CONFIG_SECRET_KEY="CHANGE_ME"
export HKSOVA_CONFIG_SECRET_PEPPER="CHANGE_ME"
export HKSOVA_CONFIG_MYSQL_HOST="localhost"
export HKSOVA_CONFIG_MYSQL_USER="CHANGE_ME"
export HKSOVA_CONFIG_MYSQL_PASSWORD="CHANGE_ME"
export HKSOVA_CONFIG_MYSQL_DB="CHANGE_ME"
export HKSOVA_CONFIG_DIR="/vagrant/configs"
export HKSOVA_CONFIG="../configs/development.py"
```

```
. venv/bin/activate
python3 run.py
```

Deployment
----------
Rename and change
- configs/docker.py.sample
- docker-compose.yml.sample

Random key generation
```
import secrets
print (token_urlsafe(20))
```

```
sudo docker-compose up --build
docker exec -i hksova_database_1 mysql -uuser -ppassword database < database.sql
sudo docker-compose up -d
```

Side notices
------------
- `flask_mysqldb` needs `libmysqlclient-dev` package installed
- DO NOT try to install it in conda env, you'll end in dependency hell (originates in mistune pkg)