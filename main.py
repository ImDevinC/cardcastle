import os
import argparse
import logging
import json
import csv

from cardcastle import CardCastle

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-U', '--username')
    parser.add_argument('-P', '--password')
    parser.add_argument('-c', '--common', action='store_true')
    parser.add_argument('-u', '--uncommon', action='store_true')
    parser.add_argument('-r', '--rare', action='store_true')
    parser.add_argument('-m', '--mythic', action='store_true')
    parser.add_argument('-s', '--special', action='store_true')
    parser.add_argument('-o', '--output-file')
    args = parser.parse_args()
    return {'username': args.username, 'password': args.password, 'common': args.common, 'uncommon': args.uncommon, 'rare': args.rare, 'mythic': args.mythic, 'special': args.special, 'all': (not args.common and not args.uncommon and not args.rare and not args.mythic and not args.special), 'output_file': args.output_file}

def write_cards_to_file(cards, file):
    columns = ['name', 'set', 'foil', 'quantity']
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(cards)

def main():
    logging.basicConfig(level=logging.INFO)
    args = get_args()
    username = args.get('username') if args.get('username') else os.environ.get('CC_USERNAME')
    password = args.get('password') if args.get('password') else os.environ.get('CC_PASSWORD')
    if not username or not password:
        logging.error('No username or password supplied')
        return
    
    cc = CardCastle()
    if not cc.login(username, password):
        logging.error('Failed to login')
        return

    final_cards = []
    # for cards in cc.search_by_name('Llanowar Elves'):
    #     final_cards.extend([
    #         {
    #             'name': card.get('name'),
    #             'set': card.get('set_name'),
    #             'foil': card.get('foil'),
    #             'quantity': card.get('quantity')
    #         }
    #     for card in cards])
    
    rarities: list(CardCastle.Rarities) = []
    if args.get('common'):
        rarities.append(CardCastle.Rarities.COMMON)
    if args.get('uncommon'):
        rarities.append(CardCastle.Rarities.UNCOMMON)
    if args.get('rare'):
        rarities.append(CardCastle.Rarities.RARE)
    if args.get('mythic'):
        rarities.append(CardCastle.Rarities.MYTHIC)
    if args.get('special'):
        rarities.append(CardCastle.Rarities.SPECIAL)
    
    for cards in cc.search_by_rarities(rarities):
        final_cards.extend([
            {
                'name': card.get('name'),
                'set': card.get('set_name'),
                'foil': card.get('foil', False),
                'quantity': card.get('quantity')
            }
        for card in cards])

    if args.get('output_file'):
        write_cards_to_file(final_cards, args.get('output_file'))
    else:
        print(json.dumps(final_cards))
    
    total_count = 0
    for card in final_cards:
        total_count = total_count + card.get('quantity')
    print(f'Total Cards: {total_count}')


if __name__ == '__main__':
    main()