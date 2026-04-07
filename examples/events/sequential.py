import urllib.request
import json

junk_foods = [
  'Pizza',
  'Popcorn',
  'Hamburger',
  'Pepsi',
  'Potato_chip',
  'Cake',
]

for food in junk_foods:
    url = f"https://en.wikipedia.org/w/api.php?action=parse&format=json&page={food}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "EventExample/1.0"}
    )

    with urllib.request.urlopen(req) as response:
        contents = response.read()
        data = json.loads(contents)
        print(f"{food}: {data['parse']['properties'][0]['*']}")
