ECHO "Installing Docker Container"

docker run -d -p 2480:2480 -p 2424:2424 -e ORIENTDB_ROOT_PASSWORD=root orientdb
python3 load_into_db.py
