# -*- coding: UTF-8 -*-
from SMInfoParser.StateMachineInfoParser import SMInfoParser
from SMInfoParser.DrawIoXMLParser import DrawioSMInfoExtractor
import subprocess
import os

class DrawioPngParser(SMInfoParser):
            
    def get_sm_jump_info_list_from_file(self, file_path):
        try:
            print("drawio -xuf xml -o out.xml " + file_path)
            os.system("drawio -xuf xml -o out.xml " + file_path)
            # subprocess.call(['drawio', "-x -u -f xml -o out.xml " + file_path])
        except Exception:
            raise RuntimeError("Invalid png file, make sure it contains a copy of diagram")
        
        if os.path.exists("out.xml"):
            sm_info_extractor = DrawioSMInfoExtractor()
            ret = sm_info_extractor.get_sm_jump_info_list_from_file("out.xml")
            os.system("rm out.xml")
            return ret
        else:
            raise RuntimeError("Invalid png file, make sure it contains a copy of diagram")

