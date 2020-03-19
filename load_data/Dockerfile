FROM python:3.8
WORKDIR /app/
ADD load_into_db.py pyorient_custom /app/
RUN pip3 install pyorient ijson tqdm
CMD ["python3", "load_into_db.py"]
