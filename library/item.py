import json
import library.common
import urllib2

class Item(object):
    def __init__(self, item_dict):
        object.__init__(self)
        self.__item_dict = item_dict

    def get_name(self):
        return self.__item_dict['name']

    def update(self):
        url = urllib2.urlopen('http://%s/api/d3/data/%s' % (
            library.common.BATTLE_NET_HOST, self.__item_dict['tooltipParams']))
        result = json.loads(url.read())
        # pprint.pprint(result)
        self.__item_dict.update(result)

    def get_type(self):
        return self.__item_dict['type']['id']

    def get_attributes(self):
        return self.__item_dict['attributes']

    def get_raw_attributes(self):
        return self.__item_dict['attributesRaw']

    def __repr__(self):
        return '<%s>' % (self.get_name())

