    from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union
from mangum import Mangum
import os, re

app = FastAPI()

class InputData(BaseModel):
    data: List[Union[str, int]]

@app.post("/bfhl")
async def bfhl(body: InputData):
    return JSONResponse(content={
        "is_success": True,
        "user_id": os.getenv("FULL_NAME", "test_user") + "_" + os.getenv("DOB", "01012000"),
        "email": os.getenv("EMAIL", "test@example.com"),
        "roll_number": os.getenv("ROLL_NUMBER", "ROLL123"),
        "odd_numbers": [],
        "even_numbers": [],
        "alphabets": [],
        "special_characters": [],
        "sum": "0",
        "concat_string": ""
    })

# 👇 This is critical for Vercel/AWS Lambda
handler = Mangum(app)
