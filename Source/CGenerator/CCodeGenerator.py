import os
import errno
from Source.DrawIoXMLParser.StateMachineInfo import StateJumpInfo
import re

SM_SHORT = "Reset"

RESULT_PATH = ".." + os.sep + "Result"
LICENSE = "/**\n\n" \
           "This File is generated automatically.\n\n\n\n"\
           "Copyright <2019> <hanbo1990@gmail.com>\n" \
           "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and \n" \
           "associated documentation files (the \"Software\"), to deal in the Software without restriction, including\n"\
           "without limitation the rights to use, copy,modify, merge, publish, distribute, sublicense, and/or sell \n" \
           "copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the\n"\
           "following conditions:\n\n" \
           "The above copyright notice and this permission notice shall be included in all copies or substantial \n" \
           "portions of the Software.\n\n" \
           "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT \n"\
           "LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO\n"\
           "EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\n"\
           "IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR \n"\
           "THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n" \
           "*/ \n\n"

INCLUDE = "/***************************************************************************************************\n" \
          "           INCLUDE\n" \
          "*/\n\n"

ENUM_DEF = "/***************************************************************************************************\n" \
           "           ENUMERATION\n" \
           "*/\n\n"

PRIV_FUNC = "/***************************************************************************************************\n" \
            "           PRIVATE FUNCTION DECLARATION\n" \
            "*/\n\n"


TRANS_STATE = "/***************************************************************************************************\n" \
              "           STATE MACHINE VARIABLES\n" \
              "*/\n\n"

SM_STATE_COMMON = SM_SHORT.upper() + "_STATE__"
SM_CONDI_COMMON = SM_SHORT.upper() + "_CONDITION__"

state_enum_def = SM_SHORT + "State_e"
condi_enum_def = SM_SHORT + "Condition_e"

trans_name_s = SM_SHORT + "Transition_t"
SM_BASIC_CODE = "typedef void (*ActionType) ( void );\n\n" \
                "typedef struct{\n" \
                "    ActionType pActFunc;\n" \
                "    " + state_enum_def + " nextState;\n" \
                "}" + trans_name_s + ";\n\n"

sm_handler_name = SM_SHORT + "Handle"
sm_handler_s = "typedef struct{\n" \
             "    void (*process) (void);\n" \
             "    void (*reset) (void);\n" \
             "    uint32_t currentCondition;\n" \
             "    uint32_t currentState;\n" \
             "}StateMachineHandle_t;\n" \
             "\n"

LOCAL_VAR = "/***************************************************************************************************\n" \
            "           LOCAL VAR\n" \
            "*/\n\n"

sm_handler_var = "static StateMachineHandle_t " + sm_handler_name + " = {\n" \
                 "    .process = private_Process,\n" \
                 "    .reset = private_Reset,\n" \
                 "    .currentState = " + SM_STATE_COMMON + "IDLE,\n" \
                 "    .currentCondition = " + SM_CONDI_COMMON + "NONE\n" \
                 "};\n\n"

PUB_FNC = "/***************************************************************************************************\n" \
          "           PUBLIC FUNCTION\n" \
          "*/\n\n"


class CCodeGenerator:
    """
    This file help generates .c and .h code for the state machine
    """

    _h_file_writer = None
    _c_file_writer = None
    _priv_func_name_list = []
    _priv_condi_name_list = []
    _priv_state_name_list = []

    def __init__(self, state_machine_name=None):
        if "." in state_machine_name:
            raise ValueError("PLease only input the state machine name without .\n")
        elif state_machine_name is None:
            state_machine_name = "DefaultSM"

        if not os.path.exists(RESULT_PATH):
            try:
                os.makedirs(RESULT_PATH)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise RuntimeError("Cannot create the folder now")

        self._h_file_writer = open(RESULT_PATH + os.sep + state_machine_name + ".h", 'w')
        self._c_file_writer = open(RESULT_PATH + os.sep + state_machine_name + ".c", 'w')

    def write_c_file(self, st_list):
        """
        Write to the generated c file
        :param st_list:
        :return:
        """
        # check input
        assert isinstance(st_list, list)
        for item in st_list:
            assert isinstance(item, StateJumpInfo)
            if item.action is not None:
                if "NULL" not in item.action:
                    item.action = "private_SM_" + item.action
                    if item.action not in self._priv_func_name_list:
                        self._priv_func_name_list.append(item.action)
                item.from_state = SM_STATE_COMMON + self.__get_str_without_nr(item.from_state)
                item.to_state = SM_STATE_COMMON + self.__get_str_without_nr(item.to_state)
                if item.from_state not in self._priv_state_name_list:
                    self._priv_state_name_list.append(item.from_state)
                if item.condition not in self._priv_condi_name_list:
                    self._priv_condi_name_list.append(item.condition)
                    item.condition = SM_CONDI_COMMON + self.__get_str_without_nr(item.condition)

        self._priv_condi_name_list.sort(key=lambda x: int(re.findall(r"^\d*", x)[0]))
        for i in range(0, len(self._priv_condi_name_list)):
            self._priv_condi_name_list[i] = SM_CONDI_COMMON + self.__get_str_without_nr(self._priv_condi_name_list[i])

        self._c_file_writer.write(LICENSE)
        self._c_file_writer.write(INCLUDE)

        # --------------------------------------->Enumerations
        self._c_file_writer.write(ENUM_DEF)

        list_nr = len(self._priv_state_name_list)
        self._c_file_writer.write("typedef enum{\n")
        for i in range(0, list_nr):
            self._c_file_writer.write("    " + self._priv_state_name_list[i] + ",\n")
        self._c_file_writer.write("    " + SM_STATE_COMMON + "END,\n")
        self._c_file_writer.write("} " + state_enum_def + ";\n\n")

        list_nr = len(self._priv_condi_name_list)
        self._c_file_writer.write("typedef enum{\n")
        for i in range(0, list_nr):
            self._c_file_writer.write("    " + self._priv_condi_name_list[i] + ",\n")
        self._c_file_writer.write("    " + SM_CONDI_COMMON + "END,\n")
        self._c_file_writer.write("} " + condi_enum_def + ";\n\n")

        # --------------------------------------->Private Functions Declarations
        self._c_file_writer.write(PRIV_FUNC)

        self._c_file_writer.write("static void private_Process( void );\n")
        self._c_file_writer.write("static void private_Reset( void );\n")
        # adding function names into the file
        for item in self._priv_func_name_list:
            self._c_file_writer.write("static void " + item + "( void );\n")

        # --------------------------------------->State Machine related features
        self._c_file_writer.write(TRANS_STATE)
        self._c_file_writer.write(SM_BASIC_CODE)
        self._c_file_writer.write(sm_handler_s)

        trans_info_list = []
        state_trans_nr = 0
        for item in st_list:
            tras_name = self.__get_trans_name_from_info_list(item.action, item.to_state, trans_info_list)
            if tras_name is None:
                item.trans_name = "st" + str(state_trans_nr)
                state_trans_nr += 1
                state_trans_str = "static const " + trans_name_s + " " + item.trans_name + " = {\n" \
                                  "    .pActFunc = " + item.action + ",\n" \
                                  "    .nextState = " + item.to_state + "\n" \
                                  "};\n\n"
                trans_info_list.append((item.trans_name, item.action, item.to_state))
                self._c_file_writer.write(state_trans_str)
            else:
                item.trans_name = tras_name

        # ---------------> Trans Table, row is condition and column is state
        self._c_file_writer.write("static const " + trans_name_s + "* "
                                  + SM_SHORT + "TransTable[" + SM_CONDI_COMMON + "END][" +
                                  SM_STATE_COMMON + "END] = {\n" +
                                  "// The row is condition and column is state\n/* |")
        # create comment line
        for state_name in self._priv_state_name_list:
            self._c_file_writer.write("    " + self.__get_str_without_com_str(state_name) + "    |")
        self._c_file_writer.write(" */\n")
        for condition_name in self._priv_condi_name_list:
            self._c_file_writer.write("    // condition :" + self.__get_str_without_com_str(condition_name) + "\n")
            # create transition code for condition with all state
            condition_stran_line = "    {"
            for state_name in self._priv_state_name_list:
                if_trans_exist, trans_name = self.__get_trans_str_name(condition_name, state_name, st_list)
                if if_trans_exist is True:
                    condition_stran_line = condition_stran_line + " &" + trans_name + "        ,"
                else:
                    condition_stran_line = condition_stran_line + " " + trans_name + "        ,"
            condition_stran_line += "},\n"
            condition_stran_line = re.sub(r",}", "}", condition_stran_line)
            self._c_file_writer.write(condition_stran_line)
        self._c_file_writer.write("};\n\n")

        # ---------------> local variable
        self._c_file_writer.write(LOCAL_VAR)
        var_str = "static StateMachineHandle_t " + sm_handler_name + " = {\n" \
                  "    .process = private_Process,\n" \
                  "    .reset = private_Reset,\n" \
                  "    .currentState = " + self._priv_state_name_list[0] + ",\n" \
                  "    .currentCondition = " + self._priv_state_name_list[0] + "\n" \
                  "};\n\n"

        self._c_file_writer.write(sm_handler_var)

        # ---------------> Public functions
        # init
        self._c_file_writer.write(PUB_FNC)
        pub_func_str = "void " + SM_SHORT + "_Init( void )\n" \
                       "{\n" \
                       "    private_Reset();\n" \
                       "}\n\n"
        self._c_file_writer.write(pub_func_str)
        # execute
        pub_func_str = "void " + SM_SHORT + "_Execute( void )\n" \
                       "{\n" \
                       "    private_Process();\n" \
                       "}\n\n"
        self._c_file_writer.write(pub_func_str)

        # ---------------> Private functions
        self._c_file_writer.write(PRIV_FUNC)
        # process
        priv_func_str = "void private_Process( void )\n" \
                        "{\n" \
                        "    const " + trans_name_s + "* currentTransition;\n\n" \
                        "    // get current transition of state machine we need to process\n" +\
                        "    currentTransition = " + SM_SHORT + "TransTable[" + sm_handler_name + ".currentCondition][" +\
                        sm_handler_name + ".currentState];\n\n" +\
                        "    " + sm_handler_name + ".currentCondition = " + SM_CONDI_COMMON + "NONE;\n\n" +\
                        "    // if it's not NULL\n" +\
                        "    if( currentTransition != NULL)\n" \
                        "    {\n" +\
                        "        // update next state to be processed\n" + \
                        "        " + sm_handler_name + ".currentState = " + "currentTransition->nextState;\n\n" + \
                        "        //execute the function for this event at state if exist\n" \
                        "        if(currentTransition->pActFunc != NULL)\n" \
                        "        {\n" \
                        "            currentTransition->pActFunc();\n" \
                        "        }\n" \
                        "    }\n" \
                        "}\n\n"
        self._c_file_writer.write(priv_func_str)
        # reset
        priv_func_str = "void private_Reset( void )\n" \
                        "{\n" +\
                        "    " + sm_handler_name + ".currentState = " + self._priv_state_name_list[0] + ";\n" + \
                        "    " + sm_handler_name + ".currentCondition = " + self._priv_condi_name_list[0] + ";\n" + \
                        "}\n\n"
        self._c_file_writer.write(priv_func_str)

        # other private functions
        for item in self._priv_func_name_list:
            priv_func_str = "static void " + item + "( void )\n" +\
                            "{\n" \
                            "\n" \
                            "}\n\n"
            self._c_file_writer.write(priv_func_str)

    @staticmethod
    def __get_trans_name_from_info_list(action, to_state, trans_info_list):
        for item in trans_info_list:
            if action == item[1] and to_state == item[2]:
                return item[0]
        return None

    @staticmethod
    def __get_str_without_nr(string):
        return re.sub(r"^[0-9]*_*", "", string)

    @staticmethod
    def __get_str_without_com_str(string):
        string = re.sub(SM_STATE_COMMON, "", string)
        string = re.sub(SM_CONDI_COMMON, "", string)
        return string

    @staticmethod
    def __get_trans_str_name(condition, state, trans_list):
        for item in trans_list:
            if condition == item.condition and state == item.from_state:
                return True, item.trans_name
        return False, "NULL"
