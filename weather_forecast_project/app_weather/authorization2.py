import base64
import os

import requests


def loginbot(login, password):
    url = "https://home.openweathermap.org/users/sign_in"
    s = requests.Session()
    token = base64.b64encode(os.urandom(24)).decode("utf-8")

    data = {
        "utf8": "✓",
        "authenticity_token": token,
        "user[email]": login,
        "user[password]": password,
        "user[remember_me]": 0,
        "commit": "Submit",
        "user[student]": "",
    }

    r = s.post(url=url, data=data)
    print(r.status_code)

    req = s.get("https://home.openweathermap.org/api_keys")
    print(req.status_code)

    with open("test.html", "w") as fi:
        fi.write(req.text)

    return r
