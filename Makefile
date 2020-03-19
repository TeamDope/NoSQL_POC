DOWNLOAD_IMAGE := nosql-yelp-download
LOAD_IMAGE := nosql-loading

download:
	docker build -t $(DOWNLOAD_IMAGE) -f Dockerfile_download .
	docker run -it -v `pwd`:/app/ $(DOWNLOAD_IMAGE)

run:
	docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=root orientdb

load:
	cd load_data && docker build -t $(LOAD_IMAGE) .
	cd load_data && docker run -it --net=host -v yelp_dataset:/app/yelp_dataset $(LOAD_IMAGE)
