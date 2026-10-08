import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Academic Research Assistant",
    description=(
        "A FastAPI application that serves as an academic research "
        "assistant, providing tools and resources for researchers to "
        "streamline their workflow and enhance productivity."
    ),
    version="1.0.0",
    contact={
        "name": " Hans CERIL",
        "email": "hansceril.devops@gmail.com",
    },
)


@app.get("/api/v1/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
