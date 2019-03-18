#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Source.DrawIoXMLParser.DrawIoXMLParser import StateMachineInfoExtractor
from Source.CGenerator.CCodeGenerator import CCodeGenerator


def main():
    sm_e = StateMachineInfoExtractor()
    cg = CCodeGenerator("Test")
    cg.write_c_file(sm_e.get_sm_jump_info_list_from_file("example.xml"))

    # for item in sm_e.get_sm_jump_info_list_from_file("example.xml"):
    #     print("------------------------")
    #     print(item.from_state)
    #     print(item.to_state)
    #     print(item.action)
    #     print(item.condition)


if __name__ == "__main__":
    main()
