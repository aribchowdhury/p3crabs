import hashlib
from random import randint, shuffle
import time
import requests


# character name, and their img
def getChars() -> list:
    with open("./app/keys/key_api0.txt", "r") as keys:
        f = keys.readlines()
        public = f[0].strip()
        private = f[1].strip()

    marvel_limit = 100
    offset = randint(0, 500)
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
        path = i["thumbnail"]["path"]
        extension = i["thumbnail"]["extension"]
        if "not" not in path and extension != "gif":
            name = i["name"]
            # print(name, len(name))
            if "(" in name:
                name = name[: name.find("(")].strip()
            url = path + "/portrait_xlarge." + extension
            length = len(name)
            useful.append((name, url, length))

    shuffle(useful)
    return useful


if __name__ == "__main__":
    print(getChars())


# print(useful[:10])
# print(len(useful))
# characters = body['name']
# img = body['thumbnail']
# for i in zip(img, characters):
#     print(i)
