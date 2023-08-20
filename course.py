from bs4 import BeautifulSoup
import requests


class CourseNotFound(Exception):
    pass


def _extract_prereqs_and_coreqs(course_content):
    prereqs = None
    coreqs = None

    if "Prerequisite" in course_content[0]:
        prereqs = (
            course_content[0]
            .split("Prerequisite")[1]
            .split(":")[1]
            .split(".")[0]
            .strip()
        )

    if "Corequisite" in course_content[0]:
        coreqs = (
            course_content[0]
            .split("Corequisite")[1]
            .split(":")[1]
            .split(".")[0]
            .strip()
        )

    return prereqs, coreqs


class Course:
    def __init__(self, url: str):
        self.url = url
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        content = soup.find("td", {"class": "block_content"})

        if content is None:
            raise CourseNotFound(f"Course {url} not found")

        self.title = content.find("h1").text

        # get text before first line break
        course_content = content.get_text().split(self.title)[1].split("\n")
        self.description = course_content[0]

        self.prereqs, self.coreqs = _extract_prereqs_and_coreqs(course_content)

        if self.prereqs:
            self.description = self.description.split("Prerequisite")[0].strip()
        if self.coreqs:
            self.description = self.description.split("Corequisite")[0].strip()

    def __repr__(self) -> str:
        return str(
            {
                "title": self.title,
                "description": self.description,
                "prereqs": self.prereqs,
                "coreqs": self.coreqs,
            }
        )

    def __str__(self) -> str:
        return (
            f"Title: {self.title}\n\n"
            f"Description: {self.description}\n\n"
            f"Prerequisites: {self.prereqs}\n"
            f"Corequisites: {self.coreqs}"
        )

    def json(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "prerequisites": self.prereqs,
            "corequisites": self.coreqs,
            "url": self.url,
        }
