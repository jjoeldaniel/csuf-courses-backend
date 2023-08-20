from fastapi import FastAPI, Request
from course import Course
from search import search, CourseNotFound

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/course/{course}")
async def get_course(request: Request, course: str):
    try:
        course_model: Course = search(course)
    except CourseNotFound:
        return {"error": "Course not found"}

    return {
        "title": course_model.title,
        "description": course_model.description,
        "prerequisites": course_model.prereqs,
        "corequisites": course_model.coreqs,
        "url": course_model.url,
    }
