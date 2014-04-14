import json
import pprint
import urllib2

BATTLE_NET_HOST = 'eu.battle.net'

class Item(object):

  def __init__(self, item_dict):
    object.__init__(self)
    self.__item_dict = item_dict

  def get_name(self):
    return self.__item_dict['name']

  def update(self):
    pprint.pprint(self.__item_dict)
    url = urllib2.urlopen('http://%s/api/d3/data/%s' % (
      BATTLE_NET_HOST, self.__item_dict['tooltipParams']))
    result = json.loads(url.read())
    pprint.pprint(result)
    self.__item_dict.update(result)

  def get_raw_attributes(self):
    return self.__item_dict['attributesRaw']

  def __repr__(self):
    return '<Item %s>' % (self.get_name())


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

  def __repr__(self):
    return '<Hero %s: level %d %s>' % (self.get_name(), self.get_level(), self.get_class())

  def update(self):
    url = urllib2.urlopen('http://%s/api/d3/profile/%s/hero/%d' % (
      BATTLE_NET_HOST, self.__profile.get_battle_tag(), self.get_id()))
    result = json.loads(url.read())
    self.__hero_dict.update(result)

    self.__items = self.__hero_dict.pop('items')
    for item_key, item_value in self.__items.iteritems():
      self.__items[item_key] = Item(item_value)

  def get_stats(self):
    return self.__hero_dict['stats']

  def get_skills(self):
    return self.__hero_dict['skills']

  def get_items(self):
    return self.__items


class Profile(object):

  def __init__(self, battle_tag):
    object.__init__(self)
    self.__battle_tag = battle_tag.replace('#', '-')
    self.__heroes = list()

  def get_battle_tag(self):
    return self.__battle_tag

  def update(self):
    url = urllib2.urlopen('http://%s/api/d3/profile/%s/' % (
      BATTLE_NET_HOST, self.__battle_tag))
    result = json.loads(url.read())
    self.__heroes = list()
    for hero_dict in result['heroes']:
      self.__heroes.append(Hero(self, hero_dict))

  def get_heroes(self):
    return self.__heroes


if __name__ == '__main__':
  # Connects to the proxy
  proxy = urllib2.ProxyHandler({'http': 'http://127.0.0.1:3128'})
  opener = urllib2.build_opener(proxy)
  urllib2.install_opener(opener)

  profile = Profile('Malcomdw#2986')
  profile.update()

  for hero in profile.get_heroes():
    print hero
  hero.update()

  for item in hero.get_items().values():
    pass
  item.update()

  # item = Item('CnYI1prOpQ8SBwgEFVX89CQdhyPHTh3tcAetHdSUxQkddCjasB1FtflLHW6Ld_AiCwgAFar-AQAYNCAIMIkCON4DQABID1AQYN4DaisKDAgAEP3Z3diAgICgChIbCN3v4fMNEgcIBBVo9YtfMIsCOABAAVgEkAEAGKrxp88EUAZYAA')
  # item.update()

