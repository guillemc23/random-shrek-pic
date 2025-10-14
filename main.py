import random
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Random Shrek Pic",
    description="Get a random picture of Shrek",
    version="0.4.0",
)

SHREK_DATABASE = Path("data/shrek.txt")
CURSED_DATABASE = Path("data/cursed.txt")
TOILET_DATABASE = Path("data/toilet.txt")
SWAMP_DATABASE = Path("data/swamp.txt")


def random_line(file_path: Path) -> str:
    with Path.open(file_path, "r", encoding="utf-8") as f:
        line = None
        new_line = None
        # Reading with reservoir sampling should be more efficient for big files, since it avoids loading everything onto memory
        for i, new_line in enumerate(f, 1):
            # If the chosen line includes a trailing newline ("\n" or "\r\n"), strip it
            # so that RedirectResponse doesn't end up with a URL containing an encoded newline (%0A).
            if random.randint(1, i) == 1:
                line = new_line.strip()
                return line
        if new_line is not None:
            return new_line.strip()
        else:
            raise ValueError(f"No lines found in file: {file_path}")


@app.get("/info")
async def index():
    return {
        "Hello": "Shrek",
        "version": app.version,
    }


@app.get("/")
@app.get("/shrek")
async def get_random_shrek_picture():
    return RedirectResponse(random_line(SHREK_DATABASE))


@app.get("/toilet")
async def get_random_toilet_picture():
    return RedirectResponse(random_line(TOILET_DATABASE))


@app.get("/swamp")
async def get_random_swamp_picture():
    return RedirectResponse(random_line(SWAMP_DATABASE))


@app.get("/cursed")
async def get_random_cursed_picture():
    return RedirectResponse(random_line(CURSED_DATABASE))
