import cmdline
import library.profile
import library.hero
import library.item
import re

if __name__ == '__main__':
    # Connects to the proxy
    cmdline.basic_config('127.0.0.1', 5865)

    profile = library.profile.Profile('Malcomdw#2986')
    profile.update()

    hero = profile.get_heroes()[0]
    hero.update()
    print hero.get_stats()

    dexterity = hero.get_stats()['dexterity']
    haste = 0.0  #hero.get_stats()['attackSpeed']
    critical_per = hero.get_stats()['critChance']
    critical_dmg = hero.get_stats()['critDamage']
    weapon_dmg = 0.0
    weapon_haste = 0.0

    for pos, item in hero.get_items().iteritems():
        item.update()
        print '> ', pos
        print item.get_raw_attributes()
        dexterity += item.get_raw_attribute('Dexterity_Item')
        haste += item.get_raw_attribute('Attacks_Per_Second_Percent')
        critical_per += item.get_raw_attribute('Crit_Percent_Bonus_Capped')
        critical_dmg += item.get_raw_attribute('Crit_Damage_Percent')
        weapon_dmg += item.get_raw_attribute(re.compile(r'Damage_Weapon_.*'))
        if weapon_haste == 0.0:
            weapon_haste = item.get_raw_attribute('Attacks_Per_Second_Item')

    print dexterity
    print haste
    print critical_per
    print critical_dmg
    print weapon_haste
    print weapon_dmg, weapon_dmg * weapon_haste

    s = dexterity * 0.01 + 1
    c = critical_per * critical_dmg + 1
    r = weapon_haste
    a = weapon_dmg
    m = 1.0  #Skill enhancement %

    print 'Total %d' % (s * c * r * a * m)




