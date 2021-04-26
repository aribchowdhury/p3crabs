from random import randint, shuffle
import requests
import hashlib
import time


def getChars():
    with open("./app/keys/key_api0.txt", "r") as keys:
        f = keys.readlines()
        public = f[0].strip()
        private = f[1].strip()

    marvel_limit = 100
    offset = randint(0, 500) * 2
    t = time.strftime("%Y%D%m%H%M%S")
    m = hashlib.md5()
    m.update("{}{}{}".format(t, private, public).encode("utf-8"))
    hash = m.hexdigest()
    response = requests.get(
        "https://gateway.marvel.com:443/v1/public/characters?apikey={}&ts={}&hash={}&limit={}&offset={}".format(
            public, t, hash, marvel_limit, offset
        )
    )
    body = response.json()["data"]["results"]
    useful = []

    for i in body:
        img = i["thumbnail"]
        if "not" not in img["path"] and img["extension"] != "gif":
            url = img["path"] + "." + img["extension"]
            useful.append((i["name"], url))

    shuffle(useful)
    return useful[:10]


print(getChars())
# print(useful[:10])
# print(len(useful))
# characters = body['name']
# img = body['thumbnail']
# for i in zip(img, characters):
#     print(i)
