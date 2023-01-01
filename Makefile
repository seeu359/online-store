run:
	poetry run python ./manage.py runserver

make_migrations:
	poetry run python ./manage.py makemigrations

migrate:
	poetry run python ./manage.py migrate

shell:
	poetry run ./manage.py shell

dump_prod:
	poetry run python ./manage.py dumpdata products.Product --indent 2 > fixtures/products.json

dump_cat:
	poetry run python ./manage.py dumpdata products.ProductCategory --indent 2 > fixtures/categories.json

lint:
	poetry run flake8

sort:
	poetry run isort .