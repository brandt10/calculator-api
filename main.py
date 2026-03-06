from fastapi import FastAPI, status, HTTPException

app = FastAPI()

@app.get("/", status_code=200)
def read_root():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/add/{a}/{b}", status_code=200)
def add(a: str, b: str):
    """
    Add two numbers together.
    """
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers"
        )

    return {"result": a + b}

@app.get("/subtract/{a}/{b}")
def subtract(a: float, b: float):
    try:
        result = a - b
        return {
            "operation": "subtract",
            "a": a,
            "b": b,
            "result": result
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All arguments must be valid numbers."
        )


@app.get("/multiply/{a}/{b}")
def multiply(a: float, b: float):
    try:
        result = a * b
        return {
            "operation": "multiply",
            "a": a,
            "b": b,
            "result": result
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All arguments must be valid numbers."
        )


@app.get("/divide/{a}/{b}")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot divide by zero."
        )

    try:
        result = a / b
        return {
            "operation": "divide",
            "a": a,
            "b": b,
            "result": result
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All arguments must be valid numbers."
        )

@app.get("/average/{a}/{b}/{c}")
def average(a: float, b: float, c: float):
    """
    Calculate the average of three numbers.

    Parameters:
    - a: First number
    - b: Second number
    - c: Third number

    Returns:
    - JSON object containing the average result.
    """

    try:
        result = (a + b + c) / 3

        return {
            "operation": "average",
            "a": a,
            "b": b,
            "c": c,
            "result": result
        }

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="All arguments must be valid numbers."
        )

@app.get("/hypotenuse/{a}/{b}")
def hypotenuse(a: float, b: float):
    """
    Calculate the hypotenuse of a right triangle using the Pythagorean theorem.

    Parameters:
    - a: First side of the triangle
    - b: Second side of the triangle

    Returns:
    - JSON object containing the hypotenuse length.
    """

    if a <= 0 or b <= 0:
        raise HTTPException(
            status_code=422,
            detail="Triangle side lengths must be positive numbers."
        )

    try:
        result = (a**2 + b**2) ** 0.5

        return {
            "operation": "hypotenuse",
            "a": a,
            "b": b,
            "result": result
        }

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="All arguments must be valid numbers."
        )

@app.get("/rectangle-area/{length}/{width}")
def rectangle_area(length: float, width: float):
    """
    Calculate the area of a rectangle.

    Parameters:
    - length: Length of the rectangle
    - width: Width of the rectangle

    Returns:
    - JSON object containing the calculated area.
    """

    if length <= 0 or width <= 0:
        raise HTTPException(
            status_code=422,
            detail="Length and width must be positive numbers."
        )

    try:
        result = length * width

        return {
            "operation": "rectangle_area",
            "length": length,
            "width": width,
            "result": result
        }

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="All arguments must be valid numbers."
        )