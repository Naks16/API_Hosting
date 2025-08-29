# main.py
import os
import re
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import List, Any

app = FastAPI()
def build_user_id():
    full_name = os.getenv("FULL_NAME", "nakshatra_nambiar").strip().lower()
    dob = os.getenv("DOB", "16092004").strip()
    full_name = re.sub(r"\s+", "_", full_name)
    return f"{full_name}_{dob}"
_int_re = re.compile(r"^-?\d+$")

@app.post("/bfhl")
async def bfhl(request: Request):
    user_id = build_user_id()
    email = os.getenv("EMAIL", "nikkinambiar16@gmail.com")
    roll_number = os.getenv("ROLL_NUMBER", "22BCE0401")

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={
            "is_success": False,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "message": "Invalid JSON"
        })

    data = body.get("data")
    if not isinstance(data, list):
        return JSONResponse(status_code=400, content={
            "is_success": False,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "message": "'data' field missing or not an array"
        })

    numbers_as_strings: List[str] = []
    alphabets_upper: List[str] = []
    special_chars: List[str] = []
    alpha_chars_in_order: List[str] = []  

    for item in data:
        if isinstance(item, int):
            s = str(item)
            numbers_as_strings.append(s)
        elif isinstance(item, float):
            if item.is_integer():
                s = str(int(item))
                numbers_as_strings.append(s)
            else:
                special_chars.append(str(item))
        else:
            s = str(item).strip()
            if _int_re.fullmatch(s):
                numbers_as_strings.append(s)
            elif s.isalpha():
                alphabets_upper.append(s.upper())
                alpha_chars_in_order.extend(list(s))
            else:
                special_chars.append(s)


    even_numbers: List[str] = []
    odd_numbers: List[str] = []
    total = 0
    for ns in numbers_as_strings:
        try:
            n = int(ns)
        except ValueError:
            continue
        total += n
        if n % 2 == 0:
            even_numbers.append(ns)
        else:
            odd_numbers.append(ns)


    concat_list: List[str] = []
    for i, ch in enumerate(reversed(alpha_chars_in_order)):
        if i % 2 == 0:
            concat_list.append(ch.upper())
        else:
            concat_list.append(ch.lower())
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
        "concat_string": concat_string
    }

    return JSONResponse(status_code=200, content=response)
