import library.profile
import library.hero
import library.item
import cmdline

if __name__ == '__main__':
    # Connects to the proxy
    cmdline.basic_config('127.0.0.1', 5865)

    profile = library.profile.Profile('Malcomdw#2986')
    profile.update()

    hero = profile.get_heroes()[0]
    print hero
    hero.update()

    dexterity = hero.get_stats()['dexterity']

    for pos, item in hero.get_items().iteritems():
        item.update()
        print item.get_raw_attributes()
        dexterity += item.get_raw_attr('Dexterity_Item')


    s = dexterity * 0.01 + 1



    print 'Dexterity %s' % s


