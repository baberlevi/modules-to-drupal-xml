#!/usr/bin/env python
import string as str
import sys

#static constants to be used in the xml export
class DrupalConstants(object):
    def __init__(self):
        self.category = '1' #software on RIT site is category 1
        self.type = 'software_package' #content type machine name
        self.risa_version_field = 'field_risa_versions'
        self.condo_version_field = 'field_condo_versions'

def main():

    from operator import itemgetter

    dc = DrupalConstants()

    risa_list = get_module_list('/opt/rit/modules')
    condo_list = get_module_list('/home/baber/condo-modules')

    filename = create_xml()
    last_module = dict()

    modlist = []

    for risa_module in risa_list:
        if risa_module:
            module = get_module(risa_module)
        modlist.append(module)

    for condo_module in condo_list:
        if condo_module:
            module = get_module(condo_module)
        modlist.append(module)

    #for module in modlist:
    #    print module


    sortedlist = sorted(modlist, key=itemgetter('title'))

    for module in sortedlist:
        print module['title']

    '''
    for risa_module in risa_list:
        if risa_module:
            module = get_module(risa_module)

            #this is terrible and needs to be redone
            #probably get a list of lists, then merge them, sort by name, then check for dups, and write_xml and add versions
            #in that flow - how to differentiate condo/risa ?
            if module in condo_list:
                print "this never happens"
                condo_module = get_module(module)
                add_version(condo_module, dc.condo_version_field, filename)

            is_duplicate = check_duplicate(module, last_module)
            if is_duplicate:
                add_version(module, dc.risa_version_field, filename)
            else:
                write_xml(module, filename)

            last_module = module.
    '''

    '''
    for condo_module in condo_list:
        if condo_module:
            module = get_module(condo_module)
            is_duplicate = check_duplicate(module, last_module)
            if is_duplicate:
                add_version(module, filename)
            else:
                write_xml(module, filename)

            last_module = module
    '''

    prettify_xml(filename)

def check_duplicate(module, last_module):
    if last_module and (module['title'] == last_module['title']):
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

    # Software Title
    title = ET.SubElement(node, 'title')
    title.text = module['title']

    #Set content type to software_package
    type = ET.SubElement(node, 'type')
    type.text = dc.type

    #Body holds description of Software functionality
    body = ET.SubElement(node, 'body')
    und_body = ET.SubElement(body, 'und', _numeric_keys="1")
    n0_body = ET.SubElement(und_body, 'n0')
    value_body = ET.SubElement(n0_body, 'value')
    value_body.text = module['body'].decode('utf-8','xmlcharrefreplace')

    #Category taxonomy term, currently hard set to 'Software'
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

    field_versions = ET.SubElement(node, dc.risa_version_field)
    und_versions = ET.SubElement(field_versions, 'und', _numeric_keys="1")
    n0_versions = ET.SubElement(und_versions, 'n0')
    value_versions = ET.SubElement(n0_versions, 'value')
    value_versions.text = module['version']

    if 'parallel_capability' in module:
        field_parallel_capability = ET.SubElement(node, 'field_parallel_capability')
        und_parallel = ET.SubElement(field_parallel_capability, 'und', _numeric_keys="1")
        n0_parallel = ET.SubElement(und_parallel, 'n0')
        value_parallel = ET.SubElement(n0_parallel, 'value')
        value_parallel.text = module['parallel_capability']

    xml_tree.write(filename,encoding="utf-8")

def add_version(module, version_field, filename):

    import xml.etree.ElementTree as ET
    dc = DrupalConstants()

    xml_tree = ET.parse(filename)
    xml_root = xml_tree.getroot()

    for node in xml_root.findall('node'):
        if node.find('title').text == module['title']:
            if node.find(version_field):
                field_versions = node.find(version_field)
                und_versions = field_versions.find('und')
                n1_versions = ET.SubElement(und_versions, 'n1')
                value_versions = ET.SubElement(n1_versions, 'value')
                value_versions.text = module['version']
            else:
                field_versions = ET.SubElement(node, version_field)
                und_versions = ET.SubElement(field_versions,'und')
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
        if '.git' in dirnames:
            dirnames.remove('.git')
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
                        if linelist[1] == "parallelism":
                            module['parallel_capability'] = linelist[2].replace('"','').strip()

            fid.close()

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    return module

if __name__ == "__main__":
    main()
