import cmdline
import library.profile
import library.hero
import library.item
import re


def process_items(items, main_stat, elemental_bonus):
    stat = main_stat[1]
    haste = 0.0  # hero.get_stats()['attackSpeed']
    critical_per = 0.0  # hero.get_stats()['critChance']
    critical_dmg = 0.0  # hero.get_stats()['critDamage']
    weapon_dmg = 0.0
    weapon_haste = 0.0

    for pos, item in items.iteritems():
        item.update()
        # print '> ', pos
        # print item.get_raw_attributes()
        stat += item.get_raw_attribute(re.compile(r'.*' + main_stat[0][1:] + '.*'))
        haste += item.get_raw_attribute('Attacks_Per_Second_Percent')
        critical_per += item.get_raw_attribute('Crit_Percent_Bonus_Capped')
        critical_dmg += item.get_raw_attribute('Crit_Damage_Percent')

        # Look for elemental bonus, just one
        for element in elemental_bonus:
            value = item.get_raw_attribute('Damage_Dealt_Percent_Bonus#%s' % element)
            if value != 0.0:
                elemental_bonus[element] += value
                break

        # Just once
        if weapon_dmg == 0.0:
            weapon_dmg += item.get_raw_attribute(re.compile(r'Damage_Weapon.*Min.*')) * 2
            weapon_dmg += item.get_raw_attribute(re.compile(r'Damage_Weapon.*Delta.*'))
            weapon_dmg /= 2

        # Just once
        if weapon_haste == 0.0:
            weapon_haste = item.get_raw_attribute('Attacks_Per_Second_Item') * (
                1 + item.get_raw_attribute('Attacks_Per_Second_Item_Percent'))

        gems = item.get_gems()
        for gem in gems:
            # print '>> gem: ', gem
            item_gem = library.item.Item(gem)
            weapon_dmg += item_gem.get_raw_attribute(re.compile(r'Damage_Weapon.*'))
            stat += item_gem.get_raw_attribute(re.compile(r'.*' + main_stat[0][1:] + '.*'))
            critical_dmg += item_gem.get_raw_attribute('Crit_Damage_Percent')

    # print 'Main stat    %d' % stat
    # print 'Haste        %.2f' % haste
    # print 'Critical     %.2f' % critical_per
    # print 'Critical dmg %.2f' % critical_dmg
    # print 'Weapon spd   %.2f' % weapon_haste
    # print 'Weapon dmg   %.2f' % weapon_dmg
    # print 'Weapon avg   %.2f' % (weapon_dmg * weapon_haste)

    s = stat * 0.01 + 1
    c = critical_per * critical_dmg + 1
    r = weapon_haste * (1 + haste)
    a = weapon_dmg
    m = 1.0  # Skill enhancement %

    return max(1, s) * max(1, c) * max(1, r) * max(10, a) * max(1, m)
    # print 'Total %d' % result


if __name__ == '__main__':
    # Connects to the proxy
    cmdline.basic_config('127.0.0.1', 5865)

    profile = library.profile.Profile('Malcomdw#2986')
    profile.update()

    for hero in [profile.get_heroes()[0]]:
        # for hero in profile.get_heroes():
        hero.update()

        elemental_bonus = {'Fire': 1.0, 'Cold': 1.0, 'Lightning': 1.0, 'Poison': 1.0, 'Holy': 1.0, 'Physical': 1.0}
        hero_info = (hero.get_main_stat(), hero.get_stats()[hero.get_main_stat()])
        total = process_items(hero.get_items(), hero_info, elemental_bonus)
        print
        print '%s - Damage %d' % (hero.get_name(), total)

        # Calculate skills damage
        skills = hero.get_skills()
        for skill in skills['active']:
            print skill['skill']['name']

            tokens = skill['rune']['description'].split()
            # Guess damage type
            t = [x for x in tokens if x in elemental_bonus]
            if len(t):
                dmg_type = set(t).pop()
                print '> Type', dmg_type
            else:
                dmg_type = 'Physical'
                print '> Type N/A (Physical?)'

            # Guess damage increment
            tokens.append(skill['skill']['description'].split())
            t = [float(x[:x.find('%')]) for x in tokens if '%' in x]
            if len(t):
                print '+ Damage %d (%d%% + %d%%)' % (
                    (total * max(t) / 100) * elemental_bonus[dmg_type], max(t), ((elemental_bonus[dmg_type] - 1) * 100))
            else:
                print '+ Damage N/A'

        # Calculate item damage contribution
        for k, v in hero.get_items().iteritems():
            items = hero.get_items().copy()
            del items[k]
            result = process_items(items, hero_info, dict())
            print '> %-11s %.2f' % (k, (total - result) / total * 100)
