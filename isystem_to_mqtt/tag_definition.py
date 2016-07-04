
class TagDefinition(object):
    """ Define a tag with mqtt topic and convertion """

    def __init__(self, tag_name, convertion, needed_value=1):
        self.tag_name = tag_name
        self.convertion = convertion
        self.needed_value = needed_value

class WriteTagDefinition(object):
    """ Define a tag to write with address and convertion """

    def __init__(self, address, convertion):
        self.address = address
        self.convertion = convertion
