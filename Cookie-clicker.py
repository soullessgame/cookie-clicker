from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Time set up to check every 5 seconds
interval_seconds = 5
start_time = time.time()

#clickable options
cookie = driver.find_element(By.CSS_SELECTOR,'#cookie')
counter =driver.find_element(By.CSS_SELECTOR,'#money')
panel = driver.find_elements(By.CSS_SELECTOR,'#store b')

#get all upgrade items in a dictionary
for items in panel:
    print(items.text)

clickable_options = {}
for n in range(len(panel)-1):
    upgrade_cost_string = panel[n].text.split('-')[-1].strip()
    upgrade_cost = int(upgrade_cost_string.replace(',', ''))

    clickable_options[n] = {
        "Upgrade name": panel[n].text.split('-')[0].strip(),
        "Upgrade cost": upgrade_cost
    }

print(clickable_options)

game_is_on = True
while game_is_on:
    cookie.click()

    #set up 5 second timer
    current_time = time.time()
    if current_time - start_time >= interval_seconds:
        print(f'current amount of cookies: {counter.text}')

        # get highest cliclable value, lower than the counter
        evaluated_counter = int(counter.text)
        filtered_items = list(filter(lambda x: x[1]['Upgrade cost'] < evaluated_counter, clickable_options.items()))
        print(filtered_items)
        highest_item = max(filtered_items)

        #use highest clickable counter to access html item and click on item
        chosen_panel_name = highest_item[1]['Upgrade name']
        print(chosen_panel_name)
        chosen_clicked_panel = driver.find_element(By.CSS_SELECTOR, f'#buy{chosen_panel_name}')
        chosen_clicked_panel.click()

        #reset 5 second timer
        start_time= current_time