import pytest
import requests
from tests import fixtures
from main import GithubCrawler
from requests.exceptions import ProxyError


def test_parse_search_html(git_crw):
    url_list = git_crw.parse_search_html(fixtures.get_search_html())
    assert url_list == [{"url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage"},
                        {"url": "https://github.com/michealbalogun/Horizon-dashboard"}]


def test_parse_language_html(git_crw):
    url_list = git_crw.parse_language_html(fixtures.get_repo_html())
    assert url_list == {"CSS": 52, "JavaScript": 47.2, "HTML": 0.8}


def test_get_user_from_url(git_crw):
    owner = git_crw.get_user_from_url("https://github.com/atuldjadhav/DropBox-Cloud-Storage")
    assert owner == "atuldjadhav"


def test_get_search_html_url_generator(mocker, git_crw):
    call_url_patch = mocker.patch.object(GithubCrawler, '_call_url_with_proxy', autospec=True)
    git_crw.get_search_html()
    call_url_patch.assert_called_with(git_crw, "https://github.com/search?q=openstack+nova+css&type=Repositories")


def test_get_extra_from_url(git_crw):
    git_crw._call_url_with_proxy = lambda x: type('FalseResponse', (), {'text': fixtures.get_repo_html()})
    result = git_crw.get_extra_from_url("https://github.com/atuldjadhav/DropBox-Cloud-Storage")
    assert result == {"owner": "atuldjadhav",
                      "language_stats": {"CSS": 52, "JavaScript": 47.2, "HTML": 0.8}}


def test_create_github_crawler():
    test_config = {
        "keywords": [
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [
            "0.0.0.0:8080"
        ],
        "type": "Repositories"
    }
    git_crw = GithubCrawler(**test_config)
    assert git_crw.keywords == ["openstack", "nova", "css"]
    assert git_crw.proxies == ["0.0.0.0:8080"]
    assert git_crw.type == "Repositories"


def test_call_url_with_proxy(mocker, git_crw):
    mocker.patch('random.shuffle')
    fake_response = requests.Response()
    fake_response.status_code = 200
    get_mock = mocker.patch('requests.get', return_value=fake_response)
    git_crw._call_url_with_proxy("https://myurl")
    get_mock.assert_called_with("https://myurl",
                                proxies={"http": "127.0.0.1:8080",
                                         "https": "127.0.0.1:8080"},
                                timeout=5)


def test_call_url_with_proxy_error(mocker, git_crw):
    def raise_(e):
        raise e
    mocker.patch('requests.get', new=lambda x, **args: raise_(ProxyError()))
    git_crw.proxies.copy()
    with pytest.raises(ProxyError, match="No proxy is available"):
        git_crw._call_url_with_proxy("https://myurl")
