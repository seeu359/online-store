run:
	poetry run python ./manage.py runserver

make_migrations:
	poetry run python ./manage.py makemigrations

migrate:
	poetry run python ./manage.py migrate

shell:
	poetry run ./manage.py shell

dump_prod:
	poetry run python ./manage.py dumpdata products.Product --indent 2 > products/fixtures/products.json

dump_cat:
	poetry run python ./manage.py dumpdata products.ProductCategory --indent 2 > products/fixtures/categories.json

dump_users:
	poetry run python ./manage.py dumpdata users.User --indent 2 > users/fixtures/users.json

lint:
	poetry run flake8

sort:
	poetry run isort .

test:
	poetry run ./manage.py test