import uvicorn   #asgi server
from fastapi import FastAPI

app = FastAPI()

@app.get('/')  # home page
def index():
    return {"message": "Hello World"}

@app.get('/Welcome')  # Welcome page
def get_name(name :str):
    return{"Welcome to my page":f'{name}'}

# run the api using uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)




