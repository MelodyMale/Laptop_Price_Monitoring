from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import dbm

# Run the argument with incognito
option = webdriver.ChromeOptions()
option.add_argument(' — incognito')
browser = webdriver.Chrome(executable_path='chromedriver', options=option)
browser.get("https://www.jib.co.th/web/product/product_list/2/25")

# Wait 30 seconds for page to load
timeout = 30
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.ID, "body")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# find_elements by class to contain element
notebook_container = browser.find_elements(By.CLASS_NAME, 'divboxpro')

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
dbm.write_data_to_database(df_product)