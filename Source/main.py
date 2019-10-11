#!/usr/bin/python
# -*- coding: UTF-8 -*-

from DrawIoXMLParser.DrawIoXMLParser import StateMachineInfoExtractor
from CGenerator.CCodeGenerator import CCodeGenerator


def main():
    sm_e = StateMachineInfoExtractor()
    cg = CCodeGenerator("Test")
    cg.write_c_file(sm_e.get_sm_jump_info_list_from_file("example.xml"))


if __name__ == "__main__":
    main()
