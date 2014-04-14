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

    def get_raw_attribute(self, attr, exact=True):
        if exact:
            if attr in self.get_raw_attributes():
                return (self.get_raw_attributes()[attr]['max'] + self.get_raw_attributes()[attr]['min']) / 2
            else:
                return 0
        else:
            acc = 0
            for value in (x for x in self.get_raw_attributes().iterkeys() if attr in x):
                acc += (value['max'] + value['min']) / 2
            return acc

    def __repr__(self):
        return '<%s>' % (self.get_name())

