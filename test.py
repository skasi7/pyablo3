import library.profile
import library.hero
import library.item
import pyablo3

if __name__ == '__main__':
    # Connects to the proxy
    pyablo3.basic_config('127.0.0.1', 5865)

    profile = library.profile.Profile('Malcomdw#2986')
    profile.update()

    hero = profile.get_heroes()[0]
    print hero
    hero.update()


    for pos, item in hero.get_items().iteritems():
        item.update()
        item.



