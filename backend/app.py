import uvicorn
from src import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8090, reload=True)
