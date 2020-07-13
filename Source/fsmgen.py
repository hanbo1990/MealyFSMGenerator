#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys, getopt
import os

from CodeGenerator.CGenerator.CCodeGenerator import CCodeGenerator

allowed_type = {
    "drawio" : "drawio",
       "dot" : "dot",
}
default_type = "drawio"

def main(argv):

    try:
       opts, args = getopt.getopt(argv, ":t:i:n:")
    except getopt.GetoptError:
       print('fsmgen.py -t <inputtype> -i <pathToInputFile> -n <StateMachineName>')
       sys.exit(2)

    i_exist = False
    n_exist = False

    t_type = default_type

    for opt, arg in opts:
        if opt == '-h':
            print('fsmgen.py -t <input type> -i <pathToInputFile> -n <StateMachineName>')
            sys.exit()
        elif opt in ("-t", "--type"):
            if arg in allowed_type.keys():
                t_type = allowed_type[arg]
            else:
                raise ValueError("input type not valid, currently only support " + str(list(allowed_type.keys())))
        elif opt in ("-i", "--ifile"):
            i_exist = True
            xml_path = arg
            if os.path.isfile(xml_path) is False:
                raise ValueError("input is not a file")
        elif opt in ("-n", "--sm_name"):
            n_exist = True
            sm_name = arg
    
    if i_exist is not True or n_exist is not True:
        print('fsmgen.py -i <pathToInputFile> -n <StateMachineName>')
        sys.exit(2)

    if t_type == "drawio":
        from SMInfoParser.DrawIoXMLParser import DrawioSMInfoExtractor
        sm_info_extractor = DrawioSMInfoExtractor()
    elif t_type == "dot":
        from SMInfoParser.GraphvizParser import GraphvizSMInfoExtractor
        sm_info_extractor = GraphvizSMInfoExtractor()
    else:
        RuntimeError("Should not come here! Please contact to fix this!")

    sm_transitions = sm_info_extractor.get_sm_jump_info_list_from_file(xml_path)
    c_code_generator = CCodeGenerator(sm_name)
        
    c_code_generator.write_file(sm_transitions)


if __name__ == "__main__":
    main(sys.argv[1:])
