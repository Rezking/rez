from fastapi import FastAPI
from routers.routing import router
import uvicorn


app = FastAPI()
app.include_router(router)


@app.get("/home/")
def welcome():
    return {"greetings": "welcome User"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)







