import uvicorn

if __name__ == "__main__":
    uvicorn.run("src:app", port=7777, reload=True, debug=True)