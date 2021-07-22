import requests, urllib, json, discord
from discord.utils import get
import asyncio
from datetime import datetime

CURRENT_NAME = ""
with open('config.json') as data:
    settings = json.loads(data.read())

COOKIE = settings['session']

client = discord.Client()

COOKIES = { "osu_session": COOKIE }
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "X-CSRF-Token": settings['xcsrf'],
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
}

with open('osume.txt', 'r') as f:
    contents = f.read()

#contents = urllib.parse.quote(contents)


@client.event
async def on_ready():
    global CURRENT_NAME
    global contents
    while True:
        user = await client.fetch_user(settings['your_id'])
        print("UPDATE")
        if CURRENT_NAME != str(user):
            print("CHANGED")
            CURRENT_NAME = str(user)
            now = datetime.utcnow()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            _tempCont = urllib.parse.quote(contents.replace("%PLACEHERE%", CURRENT_NAME).replace("%UPDTIMEHERE%", date_time))
            _x = requests.put(
                "https://osu.ppy.sh/users/"+settings['your_osu_id']+"/page",
                headers=HEADERS,
                data="body={0}".format(_tempCont),
                cookies=COOKIES
            )
        print("WAIT")
        await asyncio.sleep(180)
        print("NEXT")

client.run(settings['bot_token'])