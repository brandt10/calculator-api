from fastapi import FastAPI, status, HTTPException, Depends
from google.cloud import bigquery

app = FastAPI()

# Dependency method to provide a BigQuery client
# This will be used by the other endpoints where a database connection is necessary
def get_bq_client():
    # client automatically uses Cloud Run's service account credentials
    client = bigquery.Client()
    try:
        yield client
    finally:
        client.close()

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
            detail="Division by zero is not allowed. Please provide a non-zero value for b."
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

@app.get("/dbwritetest", status_code=200)
def dbwritetest(bq: bigquery.Client = Depends(get_bq_client)):
    """
    Writes a simple test row to a BigQuery table.

    Uses the `get_bq_client` dependency method to establish a connection to BigQuery.
    """
    # Define a Python list of objects that will become rows in the database table
    # In this instance, there is only a single object in the list
    row_to_insert = [
        {
            "endpoint": "/dbwritetest",
            "result": "Success",
            "status_code": 200
        }
    ]
    
    # Use the BigQuery interface to write our data to the table
    # If there are errors, store them in a list called `errors`
    # YOU MUST UPDATE YOUR PROJECT AND DATASET NAME BELOW BEFORE THIS WILL WORK!!!
    errors = bq.insert_rows_json("mgmt-545-489415.calculator.api_logs", row_to_insert)

    # If there were any errors, raise an HTTPException to inform the user
    if errors:
        # Log the full error to your Cloud Run logs for debugging
        print(f"BigQuery Insert Errors: {errors}")
        
        # Raise an exception to the API user
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to log data to BigQuery",
                "errors": errors  # Optional: return specific BQ error details
            }
        )

    # If there were NOT any errors, send a friendly response message to the API caller
    return {"message": "Log entry created successfully"}