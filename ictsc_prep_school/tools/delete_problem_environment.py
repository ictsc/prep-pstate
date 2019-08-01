import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup


BASE_URL = "https://prep.icttoracon.net/pstate/manage/"


def delete_problem_environment(id):
    cookies = dict(sessionid='st3xa1o3vq855fle0stmbrfbk7vhgd8x', csrftoken='')
    url = BASE_URL + "problem_environments/{}/delete".format(str(id))
    response = requests.get(url=url, cookies=cookies, verify=False)
    #print(response.content.decode("utf-8"))

    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    form = soup.find("input")
    cookies = dict(sessionid='st3xa1o3vq855fle0stmbrfbk7vhgd8x', csrftoken=form.get("value"))
    delete_response = requests.post(url=url, cookies=cookies, verify=False)
    print(delete_response.status_code)


if __name__ == '__main__':
    delete_problem_environment(1834)
