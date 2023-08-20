from bs4 import BeautifulSoup
import requests
from catalog_post import CatalogPost
from course import Course

BASE_URL = "https://catalog.fullerton.edu"


def split_course(s: str) -> str:
    course = s.rstrip("0123456789")

    if not course:
        return "CPSC " + s
    else:
        course = course.upper()

    course_num = s[len(course) :]
    return course + course_num


def search(query: str) -> Course:
    course = split_course(query)
    URL = f"{BASE_URL}/search_advanced.php?cur_cat_oid=80&ecpage=1&cpage=1&ppage=1&pcpage=1&spage=1&tpage=1&search_database=Search&filter%5Bkeyword%5D={course}&filter%5Bexact_match%5D=1&filter%5B3%5D=1&filter%5B31%5D=1"
    soup = BeautifulSoup(requests.get(URL).content, "html.parser")

    if (COURSE_URL := soup.find("a", {"aria-expanded": "false"})["href"]) is None:
        print("Course not found")
        exit()

    RESULT_URL = f"{BASE_URL}/{COURSE_URL}"
    catalog_post = CatalogPost(RESULT_URL)
    return catalog_post.course
