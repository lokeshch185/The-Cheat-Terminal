from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Auto uses system-installed Chrome + Chromium driver
driver = webdriver.Chrome()

# Load local HTML file
driver.get("file:///home/lokesh/projects/password-test/index.html")

# Boundary test passwords
passwords = {
    "len=5": "abcde",         # Below min
    "len=6": "abcdef",        # Min valid
    "len=7": "abcdefg",       # Normal valid
    "len=12": "abcdefghijkl", # Max valid
    "len=13": "abcdefghijklm" # Above max
}

for label, pwd in passwords.items():
    pwd_box = driver.find_element(By.ID, "password")
    pwd_box.clear()
    pwd_box.send_keys(pwd)

    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)

    msg = driver.find_element(By.ID, "msg").text
    print(f"{label} -> '{pwd}' => {msg}")

time.sleep(1)
driver.quit()
