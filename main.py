from bs4 import BeautifulSoup
import requests

BASE_URL = "https://catalog.fullerton.edu"


def split_course(s: str) -> str:
    course = s.rstrip("0123456789")

    if not course:
        return "CPSC " + s
    else:
        course = course.upper()

    course_num = s[len(course) :]
    return course + course_num


course = split_course(input("Enter course: "))
URL = f"{BASE_URL}/search_advanced.php?cur_cat_oid=80&ecpage=1&cpage=1&ppage=1&pcpage=1&spage=1&tpage=1&search_database=Search&filter%5Bkeyword%5D={course}&filter%5Bexact_match%5D=1&filter%5B3%5D=1&filter%5B31%5D=1"
soup = BeautifulSoup(requests.get(URL).content, "html.parser")

if (COURSE_URL := soup.find("a", {"aria-expanded": "false"})["href"]) is None:
    print("Course not found")
    exit()

RESULT_URL = f"{BASE_URL}/{COURSE_URL}"
soup = BeautifulSoup(requests.get(RESULT_URL).content, "html.parser")

content = soup.find("td", {"class": "block_content"})
title = content.find("h1").text

# get text before first line break
course_content = content.get_text().split(title)[1].split("\n")
description = course_content[0]

prereqs: str | None = None
coreqs: str | None = None

if "Prerequisite" in course_content[0]:
    prereqs = (
        course_content[0].split("Prerequisite")[1].split(":")[1].split(".")[0].strip()
    )
if "Corequisite" in course_content[0]:
    coreqs = (
        course_content[0].split("Corequisite")[1].split(":")[1].split(".")[0].strip()
    )

print("\n" + title + "\n")
print(description + "\n\n")

if prereqs:
    print("Prerequisites: " + prereqs)
if coreqs:
    print("Corequisites: " + coreqs)
