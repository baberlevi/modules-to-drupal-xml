#!/usr/bin/env python
import string as str
import sys


def get_module_list():
    module = read_file('/home/baber/modules/modules/abyss/1.9.0')
    print "title is: %s" % module['title']

def get_module(infile):



    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

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
                        if linelist[1] == "hoempage":
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
