from src import *
from src.routes import *
from starlette.responses import FileResponse


@app.get("/Crawl")
async def crawl(username: str):
    result = Impl.get_json(username)

    path_file = f"{PATH_FILE}{username}.json"

    with open(path_file, "w", encoding='UTF8') as outfile:
        outfile.write(str(result))

    return FileResponse(path_file, media_type='application/octet-stream', filename=f"{username}.json")
