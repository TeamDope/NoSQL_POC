VOLUME_NAME := nosql-data
DATABASE_VOLUME := nosql-database
DOWNLOAD_IMAGE := nosql-yelp-download
LOAD_IMAGE := nosql-loading

create-volume:
	docker volume create $(VOLUME_NAME)
	docker volume create $(DATABASE_VOLUME)

download-yelp: create-volume
	docker build -t $(DOWNLOAD_IMAGE) -f Dockerfile_download .
	docker run -it --mount "type=volume,src=$(VOLUME_NAME),dst=/app/data" $(DOWNLOAD_IMAGE)

download-zipcode: create-volume
	docker container create --name dummy -v $(VOLUME_NAME):/app/data hello-world
	docker cp zip_code_data dummy:/app/data/zip_code_data
	docker rm dummy

download: download-yelp download-zipcode

run: create-volume
	docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=root --mount "type=volume,src=$(DATABASE_VOLUME),dst=/orientdb/databases" orientdb

load: create-volume
	cd load_data && docker build -t $(LOAD_IMAGE) .
	# Change from --net=host to bridge network if configuration unavailable
	cd load_data && docker run -it --net=host --mount "type=volume,src=$(VOLUME_NAME),dst=/app/data" $(LOAD_IMAGE)
