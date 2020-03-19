from pyorient_custom import pyorient
from datetime import datetime
import ijson
import json
import csv
from tqdm import tqdm


class OrientDataLoader():
    def __init__(self):
        self.client = None
        self.session_id = None
        self.zip_income = {}

    def establish_connection(self, host, port, user, password):
        try:
            # attempt toset up connection to orient
            client = pyorient.OrientDB(host, port)
            session_id = client.connect(user, password)
            self.client = client
            self.session_id = session_id
        except Exception as e:
            print("Cannot establish connection to database. Aborting...")
            print(e)
            print("Make sure to run the orient database with port 2424 open.")
            exit()

        print("Database connected!")

    def connect_db(self, db, user, password):
        if not self.client.db_exists(db):
            print("Createing databse {}".format(db))
            self.client.db_create(db)
        print("Opening database {}".format(db))
        self.client.db_open(db, user, password)

    def create_cluster(self):
        try:
            self.client.data_cluster_add(
                'yelp_business', pyorient.CLUSTER_TYPE_PHYSICAL
            )
            print("Created yelp_business cluster!")
        except:
            print("Business cluster already created")

        try:
            self.client.data_cluster_add(
                'yelp_checkin', pyorient.CLUSTER_TYPE_PHYSICAL
            )
            print("Created yelp_checkin cluster!")
        except:
            print("Checkin cluster already created")

        try:
            self.client.data_cluster_add(
                'yelp_review', pyorient.CLUSTER_TYPE_PHYSICAL
            )
            print("Created yelp_review cluster")
        except:
            print("Review cluster already created")

        try:
            self.client.data_cluster_add(
                'yelp_business_income', pyorient.CLUSTER_TYPE_PHYSICAL
            )
            print("Created yelp_business_income cluster!")
        except:
            print("Business/income denormalized cluster already created")

    # create an efficient hash table to store zipcodes and average incomes

    def income_zip_hash(self):
        print("Hashing income/zipcode data...\n")
        with open('zip_code_data/2013-zipcode-income.csv') as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader):
                zc = row['zipcode']
                income = float(row['avg'])
                self.zip_income[zc] = income

    # load data into orientdb database
    def load_data(self):
        # business data
        load_business_data_decision = input(
            "Do you want to load/reload the Yelp Business Data? (Y/N): ").upper()
        if load_business_data_decision == "Y":
            with open('yelp_dataset/business.json', 'r') as f:
                for line in tqdm(f):
                    data = json.loads(line)
                    data['loaded_at'] = datetime.utcnow().strftime("%Y%m%d") # current time of loaded data (provenance)
                    business = {
                        '@yelp_businesses': data
                    }
                    self.client.record_create(17, business)

        # checkin data
        load_checkin_data_decision = input(
            "Do you want to load/reload the Yelp Checkin Data? (Y/N): ").upper()
        if load_checkin_data_decision == "Y":
            with open('yelp_dataset/checkin.json', 'r') as f:
                for line in tqdm(f):
                    data = json.loads(line)
                    data['loaded_at'] = datetime.utcnow().strftime("%Y%m%d") # current time of loaded data (provenance)
                    checkin = {
                        '@yelp_checkins': data
                    }
                    self.client.record_create(18, checkin)

        # review data (HEAVY)
        load_review_data_decision = input(
            "Do you want to load/reload the Yelp Review Data? (Y/N): ").upper()
        if (load_review_data_decision == "Y"):
            with open('yelp_dataset/review.json', 'r') as f:
                for line in tqdm(f):
                    data = json.loads(line)
                    data['loaded_at'] = datetime.utcnow().strftime("%Y%m%d") # current time of loaded data (provenance)
                    review = {
                        '@yelp_reviews': data
                    }
                    self.client.record_create(23, review)

        # denormalized business data (HEAVY)
        load_denormalized_business_data_decision = input(
            "Do you want to load the denormalized Yelp Review data? (Y/N): "
        ).upper()
        if (load_denormalized_business_data_decision == "Y"):
            self.income_zip_hash()  # load zip code income data
            with open('yelp_dataset/business.json', 'r') as f1:
                print("Denormalizing data...")
                for line in tqdm(f1):
                    data = json.loads(line)
                    if data['postal_code'] not in self.zip_income:
                        pass  # don't add business if income isn't associated with area
                    else:
                        # add income field to business (no need for JOIN)
                        data['average_zip_income'] = self.zip_income[data['postal_code']]
                        data['loaded_at'] = datetime.utcnow # current time of loaded data (provenance)
                        business = {
                            '@yelp_business_income': data
                        }
                        self.client.record_create(24, business)

        print("Finished loading data.")

loader = OrientDataLoader()
loader.establish_connection("127.0.0.1", 2424, "root", "root")
loader.connect_db("dope", "root", "root")
loader.create_cluster()
loader.load_data()
