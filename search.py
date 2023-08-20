from bs4 import BeautifulSoup
import requests
from course import Course, CourseNotFound

BASE_URL = "https://catalog.fullerton.edu"


def search(query: str) -> Course:
    URL = f"{BASE_URL}/search_advanced.php?cur_cat_oid=80&ecpage=1&cpage=1&ppage=1&pcpage=1&spage=1&tpage=1&search_database=Search&filter%5Bkeyword%5D={query}&filter%5Bexact_match%5D=1&filter%5B3%5D=1&filter%5B31%5D=1"
    soup = BeautifulSoup(requests.get(URL).content, "html.parser")

    if (element := soup.find("a", {"aria-expanded": "false"})) is None:
        raise CourseNotFound(f"Course {query} not found")

    COURSE_URL = element["href"]
    return Course(f"{BASE_URL}/{COURSE_URL}")
