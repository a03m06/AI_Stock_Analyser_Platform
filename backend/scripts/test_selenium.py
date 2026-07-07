from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# configure brave
options = Options()

# Brave executable
options.binary_location = (
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
)

# YOUR existing brave profile
options.add_argument(
    r"--user-data-dir=C:\Users\Arshi Mittal\AppData\Local\BraveSoftware\Brave-Browser\User Data"
)

options.add_argument("--profile-directory=Default")

# IMPORTANT
options.add_experimental_option(
    "excludeSwitches",
    ["enable-automation"]
)

# launch brave
driver = webdriver.Chrome(options=options)

url = (
    "https://www.screener.in/"
    "screen/raw/"
    "?sort=&order=&source_id="
    "&query=Market+Capitalization+%3E+0"
    "&page=1"
)

driver.get(url)

# wait
time.sleep(10)

print("\nTITLE:")
print(driver.title)

print("\nCURRENT URL:")
print(driver.current_url)

print("\nFIRST 1000 CHARS:")
print(driver.page_source[:1000])

input("\nPress Enter to close...")

driver.quit()