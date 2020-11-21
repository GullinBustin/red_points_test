import requests
from requests.exceptions import ProxyError
import json
from bs4 import BeautifulSoup
import random
import logging
import re

GITHUB_SEARCH_URL = "https://github.com/search?q={keywords}&type={type}"
GITHUB_OWNER_REGEX = r"https://github.com/(.+)/.*"


def get_config():
    config = {
        "keywords": [
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [
            "51.75.147.43:3128",
            "51.75.147.41:3128",
            "136.243.254.196:80",
            "62.23.15.92:3128"
        ],
        "type": "Repositories"
    }
    return config


def get_html(config):
    keywords = "+".join(config["keywords"])
    proxy_list = config["proxies"].copy()
    random.shuffle(proxy_list)
    search_url = GITHUB_SEARCH_URL.format(keywords=keywords, type=config["type"])
    response = call_url_with_proxy(search_url, proxy_list)
    return response.text


def call_url_with_proxy(url, proxy_list):
    while True:
        try:
            rand_proxy = proxy_list.pop()
            proxies = {
                "http": rand_proxy,
                "https": rand_proxy
            }
            r = requests.get(url, proxies=proxies)
        except ProxyError as e:
            logging.warning(e)
            continue
        except IndexError:
            raise ProxyError("No proxy is available")
        break
    return r


def get_user_from_url(url):
    m = re.search(GITHUB_OWNER_REGEX, url)
    return m.group(1)


def get_language_stats_from_url(url, config):
    proxy_list = config["proxies"].copy()
    random.shuffle(proxy_list)
    response = call_url_with_proxy(url, proxy_list)
    git_html = BeautifulSoup(response.text, "html.parser")
    languages_list = git_html.find_all("span", attrs={"class": "Progress-item",
                                                      "itemprop": "keywords"})
    lang_dict = {}
    for lang in languages_list:
        attr_split = lang["aria-label"].split()
        lang_dict[attr_split[0]] = float(attr_split[1])
    return lang_dict


def parse_html(html_str):
    git_html = BeautifulSoup(html_str, "html.parser")
    repo_list_html = git_html.find_all("li", attrs={"class": "repo-list-item"})

    results = []
    for repo_item_html in repo_list_html:
        json_data = json.loads(repo_item_html.a["data-hydro-click"])
        repo_url = json_data["payload"]["result"]["url"]
        repo_user = get_user_from_url(repo_url)
        response_json = {"url": repo_url,
                         "extra": {"owner": repo_user}}
        results.append(response_json)
    return results


def main():
    config = get_config()
    response_html = get_html(config)
    json_response = parse_html(response_html)
    for item in json_response:
        item["extra"]["language_stats"] = get_language_stats_from_url(item["url"], config)
    print(json.dumps(json_response))


if __name__ == "__main__":
    main()
