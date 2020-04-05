python3 manage.py startapp app_name
docker-compose build
docker-compose run
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py collectstatic
docker-compose run web python3 manage.py loaddata techs
docker-compose run web python3 manage.py loaddata tools
