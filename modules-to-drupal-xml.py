#!/usr/bin/env python
import string as str
import sys

def main():
    risa_list = get_module_list('/opt/rit/modules')
    #condo_list = get_module_list('/home/baber/condo-modules')

    create_xml()

    for risa_module in risa_list:
        if risa_module:
            module = get_module(risa_module)
            #print "title is: %s" % module['title']
            #print "body is: %s" % module['body']
            write_xml(module)

def create_xml():
    import xml.etree.ElementTree as ET

    node_export = ET.Element('node_export')
    xml_root = ET.ElementTree(node_export)

    xml_root.write('test.xml')

def write_xml(module):

    import xml.etree.ElementTree as ET
    '''
    node_export = ET.Element('node_export')
    xml_root = ET.ElementTree(node_export)
    '''

    xml_tree = ET.parse('test.xml')
    xml_root = xml_tree.getroot()

    node = ET.SubElement(xml_root, 'node')

    title = ET.SubElement(node, 'title')
    title.text = module['title']

    type = ET.SubElement(node, 'type')
    type.text = 'software_package'

    body = ET.SubElement(node, 'body')
    und = ET.SubElement(body, 'und', _numeric_keys="1")
    n0 = ET.SubElement(und, 'n0')
    value = ET.SubElement(n0, 'value')
    #value.text = module['body']

    xml_tree.write('test.xml')


def get_module_list(module_path):
    import os

    module_names = []

    for (dirpath, dirnames, filenames) in os.walk(module_path,followlinks=True):
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
                            module['title'] = linelist[2]
                        if linelist[1] == "version":
                            module['version'] = linelist[2]
                        if linelist[1] == "notes":
                            module['body'] = linelist[2]
                        if linelist[1] == "homepage":
                            module['homepage_url'] = linelist[2]
                        if linelist[1] == "download":
                            module['download_url'] = linelist[2]

                    #drupal=module
                    #node_export.node.title=name
                    #node_export.node.body.und.n0.value=notes
                    #node_export.node.field_sp_links.und.n0.url=homepage
                    #node_export.node.field_sp_links.und.n1.url=download
                    #node_export.node.path.alias=name
                    #node_export.node.versions=version
                    #node_export.node.parallel_capability=parallelism
                    #module name ?

            fid.close()

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    return module

if __name__ == "__main__":
    main()
