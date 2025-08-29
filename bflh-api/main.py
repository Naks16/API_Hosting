import os
import re
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

# Define the request body model
class InputData(BaseModel):
    data: List[Union[str, int]]

# Helper: build user_id from FULL_NAME and DOB environment variables
def build_user_id():
    full_name = os.getenv("FULL_NAME", "nakhsatra nambiar").strip().lower()
    dob = os.getenv("DOB", "16092004").strip()   # ddmmyyyy
    full_name = re.sub(r"\s+", "_", full_name)   # replace spaces with _
    return f"{full_name}_{dob}"

# Utility regex for integers
_int_re = re.compile(r"^-?\d+$")

@app.post("/bfhl")
async def bfhl(body: InputData):
    user_id = build_user_id()
    email = os.getenv("EMAIL", "nikkinambiar16@gmail.com")
    roll_number = os.getenv("ROLL_NUMBER", "22BCE0401")

    data = body.data

    numbers_as_strings = []
    alphabets_upper = []
    special_chars = []
    alpha_chars_in_order = []

    for item in data:
        s = str(item).strip()
        # integer string?
        if _int_re.fullmatch(s):
            numbers_as_strings.append(s)
        elif s.isalpha():
            alphabets_upper.append(s.upper())
            alpha_chars_in_order.extend(list(s))
        else:
            special_chars.append(s)

    even_numbers, odd_numbers = [], []
    total = 0
    for ns in numbers_as_strings:
        n = int(ns)
        total += n
        if n % 2 == 0:
            even_numbers.append(ns)
        else:
            odd_numbers.append(ns)

    # Build concat_string
    concat_list = []
    for i, ch in enumerate(reversed(alpha_chars_in_order)):
        concat_list.append(ch.upper() if i % 2 == 0 else ch.lower())
    concat_string = "".join(concat_list)

    response = {
        "is_success": True,
        "user_id": user_id,
        "email": email,
        "roll_number": roll_number,
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets_upper,
        "special_characters": special_chars,
        "sum": str(total),
        "concat_string": concat_string,
    }

    return JSONResponse(status_code=200, content=response)


