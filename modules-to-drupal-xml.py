#!/usr/bin/env python
import string as str
import sys

#static constants to be used in the xml export
class DrupalConstants(object):
    def __init__(self):
        self.category = '1' #software on RIT site is category 1
        self.type = 'software_package' #content type machine name

def main():
    risa_list = get_module_list('/opt/rit/modules')
    #condo_list = get_module_list('/home/baber/condo-modules')

    filename = create_xml()
    last_module = dict()

    for risa_module in risa_list:
        if risa_module:
            module = get_module(risa_module)
            is_duplicate = check_duplicate(module, last_module)
            if is_duplicate:
                add_version(module, filename)
            else:
                write_xml(module, filename)

            last_module = module

    prettify_xml(filename)

def check_duplicate(module, last_module):
    if last_module and (module['title'] == last_module['title']):
        #print "duplicate module"
        return True
    else:
        return False

def create_xml():
    import xml.etree.ElementTree as ET

    node_export = ET.Element('node_export')
    xml_root = ET.ElementTree(node_export)

    #todo: write some timestamped file
    filename = 'test.xml'
    xml_root.write(filename)

    return filename

def write_xml(module, filename):

    import xml.etree.ElementTree as ET
    dc = DrupalConstants()

    xml_tree = ET.parse(filename)
    xml_root = xml_tree.getroot()

    node = ET.SubElement(xml_root, 'node')

    title = ET.SubElement(node, 'title')
    title.text = module['title']

    type = ET.SubElement(node, 'type')
    type.text = dc.type

    body = ET.SubElement(node, 'body')
    und_body = ET.SubElement(body, 'und', _numeric_keys="1")
    n0_body = ET.SubElement(und_body, 'n0')
    value_body = ET.SubElement(n0_body, 'value')
    value_body.text = module['body'].decode('utf-8','xmlcharrefreplace')

    field_category = ET.SubElement(node, 'field_category')
    und_category = ET.SubElement(field_category, 'und', _numeric_keys="1")
    n0_category = ET.SubElement(und_category, 'n0')
    tid_category = ET.SubElement(n0_category, 'tid')
    tid_category.text = dc.category

    field_sp_links = ET.SubElement(node, 'field_sp_links')
    und_links = ET.SubElement(field_sp_links, 'und', _numeric_keys="1")
    n0_links = ET.SubElement(und_links, 'n0')
    url0 = ET.SubElement(n0_links, 'url')
    url0.text = module['homepage_url'].decode('utf-8','xmlcharrefreplace')
    link_title0 = ET.SubElement(n0_links, 'title')
    link_title0.text = 'Homepage'
    n1_links = ET.SubElement(und_links, 'n1')
    url1 = ET.SubElement(n1_links, 'url')
    url1.text = module['download_url'].decode('utf-8','xmlcharrefreplace')
    link_title1 = ET.SubElement(n1_links, 'title')
    link_title1.text = 'Download'

    field_versions = ET.SubElement(node, 'field_versions')
    und_versions = ET.SubElement(field_versions, 'und', _numeric_keys="1")
    n0_versions = ET.SubElement(und_versions, 'n0')
    value_versions = ET.SubElement(n0_versions, 'value')
    value_versions.text = module['version']

    xml_tree.write(filename,encoding="utf-8")

def add_version(module, filename):

    import xml.etree.ElementTree as ET
    dc = DrupalConstants()

    xml_tree = ET.parse(filename)
    xml_root = xml_tree.getroot()

    for node in xml_root.findall('node'):
        if node.find('title').text == module['title']:
            field_versions = node.find('field_versions')
            und_versions = field_versions.find('und')
            n1_versions = ET.SubElement(und_versions, 'n1')
            value_versions = ET.SubElement(n1_versions, 'value')
            value_versions.text = module['version']

    xml_tree.write(filename,encoding="utf-8")

def prettify_xml(filename):
    import xml.dom.minidom
    import codecs

    xml = xml.dom.minidom.parse(filename)
    better_xml = xml.toprettyxml()
    #better_xml.encode('utf-8','replace')

    with codecs.open(filename, encoding='utf-8', mode='w+') as file:
        file.write(better_xml)

def get_module_list(module_path):
    import os

    module_names = []

    for (dirpath, dirnames, filenames) in os.walk(module_path,followlinks=True):
        dirnames.sort()
        for name in filenames:
            if name != 'library.tcl' and name!= '.version':
                module_names.append(os.path.join(dirpath,name))

    return module_names


def get_module(infile):

    module = dict() #create an empty dictionary object to hold the module key/value pairs

    #read the file line by line, parsing each line, raise error if file can't be opened
    try:
        with open(infile) as fid:

            for line in fid:       #line by line through the file
                linelist = line.split(None,2)	#split the line string at whitespace into a list, with 3 elements at most

                if linelist :
                    if linelist[0] == "set":
                        if linelist[1] == "name":
                            module['title'] = linelist[2].strip()
                        if linelist[1] == "version":
                            module['version'] = linelist[2].strip()
                        if linelist[1] == "notes":
                            module['body'] = linelist[2].replace('"','').strip()
                        if linelist[1] == "homepage":
                            module['homepage_url'] = linelist[2].replace('"','').strip()
                        if linelist[1] == "download":
                            module['download_url'] = linelist[2].replace('"','').strip()

            fid.close()

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    return module

if __name__ == "__main__":
    main()
