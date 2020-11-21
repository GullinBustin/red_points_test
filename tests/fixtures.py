

def get_search_html():
    with open("tests/search_result.html", "r") as file:
        search_html = file.read()
    return search_html


def get_repo_html():
    with open("tests/repo_result.html", "r") as file:
        repo_html = file.read()
    return repo_html
