DOWNLOAD_IMAGE := nosql-yelp-download

download:
	docker build -t $(DOWNLOAD_IMAGE) -f Dockerfile_download .
	docker run -it -v `pwd`:/app/ $(DOWNLOAD_IMAGE)
