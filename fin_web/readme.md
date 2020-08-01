# Import data to db
python manage.py shell 
>>> exec(open('data_importer.py').read())

# How to connect to db
docker exec -it fin_web_db_1 psql -d bradavka -U putin

# Porblem with static files in docker
install: whitenoise