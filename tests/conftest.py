import os
import sys
import pytest
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../source')

from main import GithubCrawler

test_config = {
  "keywords": [
      "openstack",
      "nova",
      "css"
  ],
  "proxies": [
      "0.0.0.0:8080",
      "127.0.0.1:8080"
  ],
  "type": "Repositories"
}


@pytest.fixture
def git_crw():
    return GithubCrawler(**test_config)
