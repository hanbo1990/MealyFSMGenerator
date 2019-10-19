#!/usr/bin/python
# -*- coding: UTF-8 -*-

from SMInfoParser.DrawIoXMLParser import StateMachineInfoExtractor
from CodeGenerator.CGenerator.CCodeGenerator import CCodeGenerator


def main():
    sm_e = StateMachineInfoExtractor()
    cg = CCodeGenerator("Test")
    sm_transitions = sm_e.get_sm_jump_info_list_from_file("/home/bo/Desktop/example.xml")
            
    # for item in sm_transitions:
    #     item.print()
        
    cg.write_file(sm_transitions)


if __name__ == "__main__":
    main()
