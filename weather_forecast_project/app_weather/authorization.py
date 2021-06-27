import fake_useragent
import requests
from bs4 import BeautifulSoup

session = requests.Session()


email = "youremail"
password = "yourpassword"
user = fake_useragent.UserAgent().random
link = "https://home.openweathermap.org/users/sign_in"


header = {"user-agent": user}

data = {"user[email]": email, "user[password]": password, "commit": "Submit"}


response = session.post(link, data=data, headers=header).text
