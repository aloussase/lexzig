from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

from lexzig import run_analysis
from lexzig.parser import ParserError


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["POST"]
)


class AnalysisRequest(BaseModel):
    code: str


@app.post("/")
async def analyse(request: AnalysisRequest) -> Any:
    try:
        result = run_analysis(request.code)
    except ParserError as parser_error:
        return HTTPException(
            status_code=400,
            detail=str(parser_error)
        )

    if result is not None:
        return {
            'data': {
                'tokens': list(map(str, result[0])),
                'ast': result[1],
            }
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Failed to analyse input"
        )
