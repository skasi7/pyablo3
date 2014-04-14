import json
import pprint
import urllib2


if __name__ == '__main__':
    # Connects to the proxy
    proxy = urllib2.ProxyHandler({'http': 'http://127.0.0.1:3128'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    profile = Profile('Malcomdw#2986')
    profile.update()

    heroes = profile.get_heroes()
    for idx, hero in enumerate(heroes):
        print '%d: %s (%s)' % (idx, hero.get_name(), hero.get_class())

    hero_idx = int(raw_input('Select a hero> '))
    hero = heroes[hero_idx]
    hero.update()

    items = hero.get_items()
    items_idx = list()
    for idx, (position, item) in enumerate(items.iteritems()):
        items_idx.append(item)
        print '%d: %s - %s' % (idx, position, item.get_name())

    item_idx = int(raw_input('Select an item> '))
    item = items_idx[item_idx]
    item.update()

    pprint.pprint(item.get_raw_attributes())
