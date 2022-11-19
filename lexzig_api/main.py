from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

from lexzig import run_analysis


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["POST"]
)


class AnalysisRequest(BaseModel):
    code: str


@app.post("/")
async def analyse(request: AnalysisRequest):
    result = run_analysis(request.code)
    if result is not None:
        return {'data': result}
    else:
        raise HTTPException(
            status_code=400,
            detail="Failed to analyse input"
        )
