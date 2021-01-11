# CardCastleAPI
This is a python library to interact with the CardCastle.co API. 

*Currently in alpha*

**This project has no affiliation with CardCastle.co and does not represent the company in any manner**

## Usage
Using the library can be done in the following ways:
```
from cardcastle impord CardCastle
...
cc = CardCastle()
cc.login(username, password)
for cards in cc.search_by_name('Llanowar'):
  for card in cards:
    print(json.dumps(card))
...

{"id": 61511399, "card_id": 184479, "foil": false, "quality": "Near Mint", "language": "en", "created_at": "2021-01-10T20:49:16.684066", "source": "app", "name": "Llanowar Elves", "set_name": "Beatdown Box Set", "release_date": "2000-10-01", "json_id": "00000000-0000-0000-0000-000000000000", "set_code": "BTD", "mana_cost": "{G}", "types": ["Creature"], "sub_type": ["Elf", "Druid"], "rarity": "Common", "converted_mana_cost": 1, "power": 1, "toughness": 1, "foreign_name": "Llanowar Elves", "price": 56.0, "quantity": 1}
```

Currently two search methods are supported, `search_by_name(str)` or `search_by_rarities(list(CardCastle.Rarities))`. Both methods return a generator that can be looped over until all cards are pulled from your account.