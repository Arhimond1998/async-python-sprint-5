lint:
	docker-compose up file_app -d
	-docker exec -it file_app python -m flake8 --max-line-length 120 src
	docker-compose down --remove-orphans

unittest:
	docker-compose up file_app -d
	-docker exec -it file_app pytest -ra
	docker-compose down --remove-orphans

prepare:
	make lint
	make test

build:
	docker build . -t file_app

server_up:
	docker-compose up -d nginx

server_down:
	docker-compose down --remove-orphans
	
msg ?= "01_init_db"
revision:
	docker-compose up file_app -d
	docker exec -it file_app alembic revision --autogenerate -m $(msg)
	docker-compose down --remove-orphans

upgrade_rev ?= head
migration:
	docker-compose up file_app -d
	docker exec -it file_app alembic upgrade $(upgrade_rev)
	docker-compose down --remove-orphans

downgrade_rev ?= base
rollback_migration:
	docker-compose up file_app -d
	docker exec -it file_app alembic downgrade $(downgrade_rev)
	docker-compose down --remove-orphans
