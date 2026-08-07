from fastapi import FastAPI

from app.api.papers import router as papers_router


app = FastAPI(
    title="Research Radar API",
    version="1.0.0"
)


app.include_router(
    papers_router
)



@app.get("/")
def health_check():

    return {
        "status": "UP",
        "service": "Research Radar"
    }