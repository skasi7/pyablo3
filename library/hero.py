import json
import library.common
import library.item
import urllib2


class Hero(object):
    def __init__(self, profile, hero_dict):
        object.__init__(self)
        self.__profile = profile
        self.__hero_dict = hero_dict
        self.__items = dict()

    def get_class(self):
        return self.__hero_dict['class']

    def get_name(self):
        return self.__hero_dict['name']

    def get_id(self):
        return int(self.__hero_dict['id'])

    def get_level(self):
        return int(self.__hero_dict['level'])

    def update(self):
        url = urllib2.urlopen('http://%s/api/d3/profile/%s/hero/%d' % (
            library.common.BATTLE_NET_HOST, self.__profile.get_battle_tag(), self.get_id()))
        result = json.loads(url.read())
        # pprint.pprint(result)
        self.__hero_dict.update(result)

        self.__items = self.__hero_dict.pop('items')
        for item_key, item_value in self.__items.iteritems():
            self.__items[item_key] = library.item.Item(item_value)

    def get_stats(self):
        return self.__hero_dict['stats']

    def get_skills(self):
        return self.__hero_dict['skills']

    def get_items(self):
        return self.__items

    def __repr__(self):
        return '<%s: %s (lv %d)>' % (self.get_class(), self.get_name(), self.get_level())
