import random

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Random Shrek Pic",
    description="Get a random picture of Shrek",
    version="0.3.0",
)


@app.get("/")
@app.get("/info")
async def index():
    return {
        "Hello": "Shrek",
        "version": app.version,
    }


@app.get("/shrek")
async def get_random_shrek_picture():
    shrek_pics = [
        "https://static.wikia.nocookie.net/universalstudios/images/f/f2/Shrek2-disneyscreencaps.com-4369.jpg/revision/latest?cb=20250224023204",
        "https://sm.ign.com/t/ign_es/screenshot/default/sin-titulo-1_fmkx.1280.jpg",
        "https://media.elcomercio.com/wp-content/uploads/2025/02/Shrek-5-trailer-1024x683.jpg",
        "https://resizing.flixster.com/833TLn9JHRPgqmxIDgDHk-yE6Tw=/fit-in/705x460/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p27575_i_h10_ab.jpg",
        "https://www.rollingstone.com/wp-content/uploads/2024/04/enduring-appeal-of-shrek.jpg?w=1581&h=1054&crop=1",
        "https://www.cartoonbrew.com/wp-content/uploads/2024/07/shrek5.jpg",
        "https://images.bauerhosting.com/legacy/empire-images/articles/5be1b60cfd0c0bc844479a97/shrek.jpg?ar=16%3A9&fit=crop&crop=top&auto=format&w=1440&q=80",
        "https://static0.cbrimages.com/wordpress/wp-content/uploads/2022/04/Shrek_Swamp_Meme.jpg?w=1200&h=628&fit=crop,"
        "https://www.looper.com/img/gallery/these-things-happen-in-every-single-shrek-movie/intro-1655497837.jpg",
        "https://palomaynacho.com/wp-content/uploads/2023/11/shrek-animacion-original-1024x576.webp",
        "https://hips.hearstapps.com/hmg-prod/images/shrek-64f9ceef56099.jpg?crop=0.565xw:1.00xh;0.218xw,0&resize=1200:*",
    ]

    return RedirectResponse(random.choice(shrek_pics))


@app.get("/toilet")
async def get_random_toilet_picture():
    toilet_pics = [
        "https://static.wikia.nocookie.net/shrek/images/7/77/Shrek_outhouse.jpg",
        "https://i.ytimg.com/vi/3RvSkuKUPkg/hq720.jpg",
    ]

    return RedirectResponse(random.choice(toilet_pics))

@app.get("/swamp")
async def get_random_swap_picture():
    swamp_pics = [
        "https://static.wikia.nocookie.net/shrek/images/a/a7/Shrek%27s_Swamp_%28Shrek_Forever_After%29.jpg"
    ]

    return RedirectResponse(random.choice(swamp_pics))
