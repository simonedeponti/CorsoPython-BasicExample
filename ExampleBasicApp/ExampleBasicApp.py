from xml.etree import ElementTree


def parseXML(xml_file):
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    assert root.tag == 'contacts'
    contacts = []
    for contact_node in root.iter('contact'):
        contact = {
            'id': contact_node.attrib['id']
        }
        for property_node in contact_node.iter():
            if property_node.tag == 'company':
                contact['company'] = {
                    'name': property_node.get('name'),
                    'roles': []
                }
                for role_node in property_node.iter('role'):
                    contact['company']['roles'].append(role_node.text)
            else:
                contact[proprty_node.tag] = property_node.text
        contacts.append(contact)
    meta = {}
    meta_node = root.find('/meta')
    if meta_node:
        for property_node in meta_node.iter():
            meta[property_node.tag] = (
                int(property_node.text.strip(), 10)
                if property_node.tag == 'txn'
                else property_node.text
            )
    return (contacts, meta)


print(parseXML('contacts.xml'))