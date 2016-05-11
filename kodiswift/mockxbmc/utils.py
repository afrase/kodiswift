from xml.dom.minidom import parse


def load_addon_strings(addon, filename):
    """This is not an official Kodi method, it is here to facilitate
    mocking up the other methods when running outside of Kodi."""
    def get_strings(fn):
        xml = parse(fn)
        strings = {tag.getAttribute('id'): tag.firstChild.data
                   for tag in xml.getElementsByTagName('string')}
        return strings
    addon._strings = get_strings(filename)


def get_addon_id(addon_xml):
    """Parses an addon id from the given addon.xml filename."""
    xml = parse(addon_xml)
    addon_node = xml.getElementsByTagName('addon')[0]
    return addon_node.getAttribute('id')


def get_addon_name(addon_xml):
    """Parses an addon name from the given addon.xml filename."""
    xml = parse(addon_xml)
    addon_node = xml.getElementsByTagName('addon')[0]
    return addon_node.getAttribute('name')
