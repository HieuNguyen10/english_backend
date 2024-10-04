from fastapi import APIRouter
from app.controller.lesson import lesson
from app.controller.word import word
from app.controller.lesson_word import lesson_word
from app.controller.file import file

router = APIRouter()

router.include_router(lesson.router, prefix="/lesson", tags=["Lesson"])
router.include_router(word.router, prefix="/word", tags=["Word"])
router.include_router(lesson_word.router,
                      prefix="/lesson_word", tags=["Lesson Word"])
router.include_router(file.router, prefix="/file", tags=["File"])
