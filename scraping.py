from selenium.webdriver import Chrome 
from instascrape import Profile, scrape_posts
from webdriver_manager.chrome import ChromeDriverManager
import os

chrome_driver_path = os.path.join('/Users/yuvvvvv/Downloads/chromedriver-mac-arm64', "chromedriver")

webdriver = Chrome(chrome_driver_path)
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid='43637400127%3AB74sGjt18MZIf0%3A3%3AAYfHwFxgjCjFRg0fcwVo1Dt51OQtCnOoA5JDvwNFHQ;"
}
joe = Profile("joebiden")
joe.scrape(headers=headers)