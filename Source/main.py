#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys, getopt

from SMInfoParser.DrawIoXMLParser import StateMachineInfoExtractor
from CodeGenerator.CGenerator.CCodeGenerator import CCodeGenerator


def main(argv):

    try:
       opts, args = getopt.getopt(argv,"hi:n", ["ifile=", "sm_name="])
    except getopt.GetoptError:
       print('main.py -i <pathToXML> -n <StateMachineName>')
       sys.exit(2)

    i_exist = False
    n_exist = False
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <pathToXML> -n <StateMachineName>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            i_exist = True
            xml_path = arg
        elif opt in ("-n", "--sm_name"):
            n_exist = True
            sm_name = arg
    
    if i_exist is not True or n_exist is not True:
        print('main.py -i <pathToXML> -n <StateMachineName>')
        sys.exit(2)

    sm_info_extractor = StateMachineInfoExtractor()
    sm_transitions = sm_info_extractor.get_sm_jump_info_list_from_file(xml_path)
    c_code_generator = CCodeGenerator(sm_name)
        
    c_code_generator.write_file(sm_transitions)


if __name__ == "__main__":
    main(sys.argv[1:])
