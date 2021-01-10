from enum import Enum

import requests


ROOT_URL = 'https://cardcastle.co/api/v3/'

class CardCastle:

    class Rarities(Enum):
        COMMON = 'common'
        UNCOMMON = 'uncommon'
        RARE = 'rare'
        MYTHIC = 'mythic rare'
        SPECIAL = 'special'

    def __init__(self):
        self._username: str = None
        self._sess = requests.Session()

    def login(self, username: str, password: str) -> bool:
        response = self._sess.post(f'{ROOT_URL}login', auth=requests.auth.HTTPBasicAuth(username, password))
        response.raise_for_status()
        self._username = response.json().get('username')
        return True

    def _verify_login(self):
        if not self._username:
            raise Exception('Not logged in')
        if not self._sess:
            raise Exception('Session closed')

    def search_all(self):
        self._verify_login()
        for cards in self._search():
            yield cards

    def search_by_rarities(self, rarities: list[Rarities]):
        self._verify_login()
        for cards in self._search(rarities=rarities):
            yield cards

    def search_by_name(self, name: str):
        self._verify_login()
        for cards in self._search(name=name):
            yield cards
        
        
    def _search(self, name:str=None, rarities: list[Rarities]=None):
        payload = {
            'group_by': 'printing',
            'order': 'desc',
            'per_page': 100,
            'set_names': {},
            'sort_by': 'date',
            'tags': {
                'with': []
            },
            'types': {}
        }

        if name:
            payload['query'] = name
        if rarities:
            payload['rarity'] = []
            for rarity in rarities:
                payload['rarity'].append(rarity.value)

        count = 0
        page = 0
        while True:
            page = page + 1
            payload['page'] = page
            cards = []
            response = self._sess.post(f'{ROOT_URL}public/{self._username}/search', json=payload)
            response.raise_for_status()
            data = response.json()
            count += data.get('page_count', 0)
            for collection in data.get('collection_items', []):
                for card in collection.get('card_users', []):
                    card['quantity'] = len(collection.get('card_users'))
                    cards.append(card)
                    # We only need each card once, so let's track quantity and
                    # not loop over all cards
                    break
            yield cards
            if count >= data.get('total_count', 0):
                break