from pathlib import Path
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--start-maximized')

BROWSER = {
    'browser_type': 'Chrome'
}
