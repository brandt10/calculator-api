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