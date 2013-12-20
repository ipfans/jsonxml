#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import simplejson as json
except:
    import json
try:
    from lxml import etree
except:
    import xml.etree.cElementTree as etree


def strip_tag(tag):
    strip_ns_tag = tag
    split_array = tag.split('}')
    print split_array
    strip_ns_tag = split_array[1]
    tag = strip_ns_tag
    return tag


def elem_to_internal(elem, strip_ns=1, strip=1):
    """Convert an Element into an internal dictionary (not JSON!)."""
    d = {}
    elem_tag = elem.tag
    if strip_ns:
        elem_tag = strip_tag(elem.tag)
    else:
        for key, value in list(elem.attrib.items()):
            d['@' + key] = value

    # loop over subelements to merge them
    for subelem in elem:
        v = elem_to_internal(subelem, strip_ns=strip_ns, strip=strip)

        tag = subelem.tag
        if strip_ns:
            tag = strip_tag(subelem.tag)

        value = v[tag]

        try:
            # add to existing list for this tag
            d[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            d[tag] = [d[tag], value]
        except KeyError:
            # add a new non-list entry
            d[tag] = value
    text = elem.text
    tail = elem.tail
    if strip:
        # ignore leading and trailing whitespace
        if text:
            text = text.strip()
        if tail:
            tail = tail.strip()

    if tail:
        d['#tail'] = tail

    if d:
        # use #text element if other attributes exist
        if text:
            d["#text"] = text
    else:
        # text is the value if no attributes
        d = text or None
    return {elem_tag: d}


def internal_to_elem(pfsh, factory=etree.Element):
    """Convert an internal dictionary (not JSON!) into an Element."""
    attribs = {}
    text = None
    tail = None
    sublist = []
    tag = list(pfsh.keys())
    if len(tag) != 1:
        raise ValueError("Illegal structure with multiple tags: %s" % tag)
    tag = tag[0]
    value = pfsh[tag]
    if isinstance(value, dict):
        for k, v in list(value.items()):
            if k[:1] == "@":
                attribs[k[1:]] = v
            elif k == "#text":
                text = v
            elif k == "#tail":
                tail = v
            elif isinstance(v, list):
                for v2 in v:
                    sublist.append(internal_to_elem({k: v2}, factory=factory))
            else:
                sublist.append(internal_to_elem({k: v}, factory=factory))
    else:
        text = value
    e = factory(tag, attribs)
    for sub in sublist:
        e.append(sub)
    e.text = text
    e.tail = tail
    return e


def elem2json(elem, options, strip_ns=1, strip=1):
    """Convert an ElementTree or Element into a JSON string."""
    if hasattr(elem, 'getroot'):
        elem = elem.getroot()

    if options:
        return json.dumps(elem_to_internal(elem, strip_ns=strip_ns, strip=strip), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        return json.dumps(elem_to_internal(elem, strip_ns=strip_ns, strip=strip))


def json2elem(json_data, factory=etree.Element):
    """
    Convert a JSON string into an Element.
    If you want to use something else, pass the Element class
    as the factory parameter.
    """
    return internal_to_elem(json.loads(json_data), factory)


def xml2json(xmlstring, pretty=False, strip_ns=1, strip=1):
    """Convert an XML string into a JSON string."""
    elem = etree.fromstring(xmlstring)
    return elem2json(elem, pretty, strip_ns=strip_ns, strip=strip)


def json2xml(json_data, factory=etree.Element):
    """
    Convert a JSON string into an XML string.
    Warning:
        All value in json_data must be string !!
    If you want to use something else, pass the Element class
    as the factory parameter.
    """
    elem = internal_to_elem(json.loads(json_data), factory)
    return etree.tostring(elem)


def main():
    data = {
        "data": {
            "a": "1",
            "b": "2",
        },
    }
    json_data = json.dumps(data)
    xml_data = json2xml(json_data)
    print xml_data
    json_data = xml2json(xml_data, True, 0)
    print json_data
    pass

if __name__ == '__main__':
    main()
