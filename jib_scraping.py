from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import dbm
import os.path


# set absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
firefoxdriver = os.path.join(BASE_DIR, 'geckodriver')

# Run the argument with incognito
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("driver.privatebrowsing.autostart", True)
driver = webdriver.Firefox(executable_path=firefoxdriver, firefox_profile=firefox_profile)


# option.add_argument(' — incognito')
# driver = webdriver.Chrome(executable_path=chromedriver, options=option)

driver.get("https://www.jib.co.th/web/product/product_list/2/25")

# Wait 30 seconds for page to load
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "body")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()

# find_elements by class to contain element
notebook_container = driver.find_elements(By.CLASS_NAME, 'divboxpro')

# lists for contain data
notebook_name = list()
notebook_price = list()

for contain in notebook_container:
	notebook_name.append(contain.find_element(By.CLASS_NAME,'promo_name').text)
	notebook_price.append(contain.find_element(By.CLASS_NAME,'price_total').text)


# create dataframe from data
data = {'product_name': notebook_name, 'product_price': notebook_price}
df_product = pd.DataFrame.from_dict(data)

# import dataframe to database
new_df =  dbm.data_cleansing(df_product)
dbm.write_data_to_database(new_df)