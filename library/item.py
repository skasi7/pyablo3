import json
import library.common
import re
import urllib2

class Item(object):
    RegexObjectType = type(re.compile(''))

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

    def get_gems(self):
        return self.__item_dict['gems']

    def get_attributes(self):
        return self.__item_dict['attributes']

    def get_raw_attributes(self):
        return self.__item_dict['attributesRaw']

    def get_raw_attribute(self, attribute):
        if type(attribute) is self.RegexObjectType:
            attributes = (a for n, a in self.get_raw_attributes().iteritems() if attribute.match(n))
        else:
            attributes = (a for n, a in self.get_raw_attributes().iteritems() if attribute == n)
        result = 0.0
        for attribute_ in attributes:
            result += (attribute_['max'] + attribute_['min']) / 2
        return result

    def __repr__(self):
        return '<%s>' % (self.get_name())


if __name__ == '__main__':
    item_dict = {'attributesRaw': {
        'abc': {'min': 1, 'max': 1},
        'abcd': {'min': 2, 'max': 2},
        'abcde': {'min': 4, 'max': 4},
    }}
    item = Item(item_dict)
    # Exact string
    print item.get_raw_attribute('abcd')
    # Regular expression
    print item.get_raw_attribute(re.compile(r'abcd'))

