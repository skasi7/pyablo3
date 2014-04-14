import json
import library.common
import urllib2
import hero

class Profile(object):
    def __init__(self, battle_tag):
        object.__init__(self)
        self.__battle_tag = battle_tag.replace('#', '-')
        self.__heroes = list()

    def get_battle_tag(self):
        return self.__battle_tag

    def update(self):
        url = urllib2.urlopen('http://%s/api/d3/profile/%s/' % (
            library.common.BATTLE_NET_HOST, self.__battle_tag))
        result = json.loads(url.read())
        # pprint.pprint(result)
        self.__heroes = list()
        for hero_dict in result['heroes']:
            self.__heroes.append(hero.Hero(self, hero_dict))

    def get_heroes(self):
        return self.__heroes
