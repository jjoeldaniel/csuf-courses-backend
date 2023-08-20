from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from course import Course
from search import search, CourseNotFound

app = FastAPI()


class NoCollegeFound(Exception):
    pass


def split_course(s: str) -> str:
    course = s.rstrip("0123456789")

    if not course:
        raise NoCollegeFound
    else:
        course = course.upper()

    course_num = s[len(course) :]
    return course + course_num


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/ping/")
async def ping():
    return {"message": "pong"}


@app.get("/api/course/{course}")
async def get_course(course: str):
    try:
        course = split_course(course)
    except NoCollegeFound:
        return RedirectResponse(url="/api/course/CPSC" + course)

    try:
        course_model: Course = search(course)
    except CourseNotFound:
        return {"error": "Course not found"}

    return course_model.json()
