import xml.parsers.expat

class XmlParser(object):
    '''a class that parses a xml string an generates a nested
    dict/list structure
    '''

    def __init__(self, text):
        '''constructor'''
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.buffer_text = True

        self.result = None
        self.stack = []
        self.current = None

        self.parser.StartElementHandler = self.start_element
        self.parser.EndElementHandler = self.end_element
        self.parser.CharacterDataHandler = self.char_data
        self.parser.Parse(text)

    def start_element(self, name, attrs):
        '''Start xml element handler'''
        if self.current != None:
            self.stack.append(self.current)

        self.current = {}

        for (key, value) in attrs.iteritems():
            self.current[str(key)] = value

        self.current['tag'] = name
        self.current['childs'] = []

    def end_element(self, name):
        '''End xml element handler'''
        if len(self.stack):
            current = self.stack.pop()
            current['childs'].append(self.current)
            self.current = current
        else:
            self.result = self.current

    def char_data(self, data):
        '''Char xml element handler.
        buffer_text is enabled, so this is the whole text element'''
        self.current['childs'].append(data)

class DictObj(dict):
    '''a class that allows to access a dict as an object
    '''

    def __init__(self, kwargs):
        '''constructor'''
        dict.__init__(self, kwargs)

    def __getattribute__(self, name):
        if name in self:
            obj = self[name]

            if type(obj) == dict:
                return DictObj(obj)
            elif type(obj) == list:
                return ListObj(obj)

            return obj
        try:
            return object.__getattribute__(self, name)
        except:
            return None


    def to_xml(self):
        xml = ''
        if self.tag:
            xml = '<%s' % self.tag
            attrs = [attr for attr in self.keys() if attr not in ['tag', 'childs']]
            for attr in attrs:
                if self[attr]:
                    xml += ' %s="%s"' % (attr, self[attr])
            xml += '>'
        for child in self.childs:
            if type(child) in (str, unicode):
                xml+=child
            else:
                xml+=child.to_xml()

        if self.tag:
            xml += '</%s>' % self.tag
        return xml


class ListObj(list):
    '''a class that allows to access dicts inside a list as objects
    '''

    def __init__(self, args):
        '''constructor'''
        list.__init__(self, args)

    def __getitem__(self, index):
        if index > len(self):
            raise IndexError('list index out of range')

        obj = list.__getitem__(self, index)

        if type(obj) == dict:
            return DictObj(obj)
        elif type(obj) == list:
            return ListObj(obj)

        return obj

    def __iter__(self):
        '''iterate over the list'''

        count = 0

        while count < len(self):
            yield self[count]
            count += 1

def raw_string(dct_):
    '''return a string containing just the string parts removing all the
    xml stuff'''

    def helper(dct):
        result = []

        if not dct.childs:
            return result

        for child in dct.childs:
            if type(child) == str or type(child) == unicode:
                result.append(str(child))
            else:
                result = result + helper(child)

        return result

    return ''.join(helper(dct_))

def parse_css(css):
    '''parse a css style string and return a dict with key values'''
    result = {}

    for token in css.split(';'):
        parts = token.split(':')
        if len(parts) == 2:
            key, value = parts
            result[key.strip().replace('-', '_')] = value.strip()

    return DictObj(result)

