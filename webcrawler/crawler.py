import requests
from bs4 import BeautifulSoup


def crawler(url="https://devgo.com.br"):
    response = requests.get(url)
    url_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        h1_tags = soup.find_all("h1")
        for h1_tag in h1_tags:
            a_tag = h1_tag.find("a")
            href = a_tag["href"]
            text = a_tag.text
            if href and href.startswith("/"):
                href = url + href
            if href != url + "/":
                url_list.append({"url": href, "label": text})

    return url_list
