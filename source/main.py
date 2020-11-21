import re
import json
import random
import logging
import requests

from bs4 import BeautifulSoup
from requests.exceptions import ProxyError, Timeout


def get_config():
    with open('config.yml', 'r') as file:
        config = json.load(file)
    return config


class GithubCrawler:

    GITHUB_SEARCH_URL = "https://github.com/search?q={keywords}&type={type}"
    GITHUB_OWNER_REGEX = r"https://github.com/(.+)/.*"

    def __init__(self, keywords, proxies, type):
        self.keywords = keywords
        self.proxies = proxies
        self.type = type

    def _call_url_with_proxy(self, url):
        random.shuffle(self.proxies)
        proxy_list = self.proxies.copy()
        while True:
            try:
                rand_proxy = proxy_list.pop()
                proxies = {
                    "http": rand_proxy,
                    "https": rand_proxy
                }
                r = requests.get(url, proxies=proxies, timeout=5)
                r.raise_for_status()
            except (ProxyError, Timeout) as e:
                logging.warning(e)
                continue
            except IndexError:
                raise ProxyError("No proxy is available")
            break
        return r

    def get_search_html(self):
        keywords = "+".join(self.keywords)
        search_url = self.GITHUB_SEARCH_URL.format(keywords=keywords, type=self.type)
        response = self._call_url_with_proxy(search_url)
        return response.text

    def parse_search_html(self, html_str):
        git_html = BeautifulSoup(html_str, "html.parser")
        repo_list_html = git_html.find_all("li", attrs={"class": "repo-list-item"})
        results = []
        for repo_item_html in repo_list_html:
            json_data = json.loads(repo_item_html.a["data-hydro-click"])
            repo_url = json_data["payload"]["result"]["url"]
            response_json = {"url": repo_url}
            results.append(response_json)
        return results

    def get_user_from_url(self, url):
        m = re.search(self.GITHUB_OWNER_REGEX, url)
        return m.group(1)

    def get_extra_from_url(self, url):
        response = self._call_url_with_proxy(url)
        return {"owner": self.get_user_from_url(url),
                "language_stats": self.parse_language_html(response.text)}

    def parse_language_html(self, html_str):
        git_html = BeautifulSoup(html_str, "html.parser")
        languages_list = git_html.find_all("span", attrs={"class": "Progress-item",
                                                          "itemprop": "keywords"})
        lang_dict = {}
        for lang in languages_list:
            attr_split = lang["aria-label"].split()
            lang_dict[attr_split[0]] = float(attr_split[1])
        return lang_dict


def main():
    config = get_config()
    git_crw = GithubCrawler(**config)
    search_html = git_crw.get_search_html()
    json_response = git_crw.parse_search_html(search_html)
    for item in json_response:
        item["extra"] = git_crw.get_extra_from_url(item["url"])
    print(json.dumps(json_response))


if __name__ == "__main__":
    main()
