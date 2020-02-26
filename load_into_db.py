import pyorient
import ijson
import json
from tqdm import tqdm

# set up connection to orient
client = pyorient.OrientDB("127.0.0.1", 2424)
session_id = client.connect("root", "root")

# open dope database
client.db_open("dope", "root", "root")


# create new clusters for each class

create_cluster_decision = input(
    "Have you created the Yelp clusters yet? (Y/N).\n N: They will be created for you \n Y: Already created ")
if create_cluster_decision == "N":
    yelp_businesses = client.data_cluster_add(
        'yelp_business', pyorient.CLUSTER_TYPE_PHYSICAL
    )
    yelp_checkins = client.data_cluster_add(
        'yelp_checkin', pyorient.CLUSTER_TYPE_PHYSICAL
    )
    yelp_reviews = client.data_cluster_add(
        'yelp_review', pyorient.CLUSTER_TYPE_PHYSICAL
    )

load_business_data_decision = input(
    "Have you loaded the Yelp business data yet? (Y/N).\n N: They will be loaded for you \n Y: Already loaded ")
if load_business_data_decision == "N":
    with open('yelp_data/business.json', 'r') as f:
        for line in tqdm(f):
            data = json.loads(line)
            business = {
                '@yelp_businesses': data
            }
            client.record_create(21, business)

load_checkin_data_decision = input(
    "Have you loaded the Yelp checkin data yet? (Y/N).\n N: They will be loaded for you \n Y: Already loaded ")
if load_checkin_data_decision == "N":
    with open('yelp_data/checkin.json', 'r') as f:
        for line in tqdm(f):
            print(line)
            data = json.loads(line)
            print(data)
            checkin = {
                '@yelp_checkins': data
            }
            client.record_create(22, checkin)

load_checkin_data_decision = input(
    "Have you loaded the Yelp review data yet? *WARNING: MAY TAKE SEVERAL MINUTES * (Y/N).\n N: They will be loaded for you \n Y: Already loaded ")
with open('yelp_data/review.json', 'r') as f:
    for line in tqdm(f):
        data = json.loads(line)
        review = {
            '@yelp_reviews': data
        }
        client.record_create(23, review)
