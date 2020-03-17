from selenium import webdriver
import wget

URL = "https://www.yelp.com/dataset/download"
DATA_NAME = "yelp_data"
JSON_LINK_TEXT = "Download JSON"
FORM_ID = "dataset_form"
FORM_VALUES = {
    "name": "Cody",
    "email": "perak005@umn.edu",
    "signature": "CAP",
    "terms_accepted": True
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(URL)

data_form = driver.find_element_by_id(FORM_ID)
print(data_form)
for key in FORM_VALUES:
    data_instance = data_form.find_element_by_name(key)
    data_instance.click()
    if type(FORM_VALUES[key]) == str:
        data_instance.send_keys(FORM_VALUES[key])
    print(key, data_instance)
data_form.submit()
# driver.save_screenshot("test.png")

json_link = driver.find_element_by_partial_link_text(JSON_LINK_TEXT)
json_url = json_link.get_attribute("href")
wget.download(json_url)

driver.quit()