import os
import errno
from SMInfoParser.StateMachineInfo import StateJumpInfo
import re
import shutil

from CodeGenerator.CGenerator.CRelatedDefines import (sm_condition_common,
                                                      sm_state_common,
                                                      state_enum_type,
                                                      condition_enum_type,
                                                      transition_name,
                                                      state_type,
                                                      transition_table_name,
                                                      init_func_name,
                                                      tick_func_name,
                                                      header_guard)

RESULT_PATH = "Result"


class CCodeGenerator:
    """
    This file help generates .c and .h code for the state machine
    """

    _sm_name = None
    _func_file_name = None
    _header_file_name = None
    _inc_file_name = None
    _h_file_writer = None
    _c_file_writer = None
    _priv_func_name_list = []
    _priv_condi_name_list = []
    _priv_state_name_list = []

    def __init__(self, state_machine_name=None):
        if state_machine_name is None:
            raise ValueError("PLease Provide state machine name\n")
        else:
            self._sm_name = "Default"

        if not os.path.exists(RESULT_PATH):
            try:
                os.makedirs(RESULT_PATH)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise RuntimeError("Cannot create the folder now")

        self._func_file_name = self._sm_name + "SMFunc.c"
        self._header_file_name = self._sm_name + "SMFunc.h"
        self._inc_file_name = self._sm_name + "SMTable.inc"
        self._prepare_dir()
        self._h_file_writer = open(RESULT_PATH + os.sep + "src" + os.sep + self._header_file_name, 'w+')
        self._c_file_writer = open(RESULT_PATH + os.sep + "src" + os.sep + self._func_file_name, 'w+')
        self._table_file_writer = open(RESULT_PATH + os.sep + "src" + os.sep + self._inc_file_name, 'w+')

    def write_file(self, st_list):
        """
        Write to the generated c file
        :param st_list:
        :return:
        """

        prepared_list = self._prepare_st_list(st_list)
        self._write_c_file()
        self._write_inc_file(prepared_list)
        self._write_header_file()
        self._copy_default_files()
        self._create_unit_test(prepared_list)

    def _prepare_dir(self):
        self.__mkdir(RESULT_PATH)
        self.__mkdir(RESULT_PATH + os.sep + "src")
        self.__mkdir(RESULT_PATH + os.sep + "src" + os.sep + "fsmMgr")

    @staticmethod
    def __mkdir(path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise RuntimeError("Cannot create the folder now")

    def _prepare_st_list(self, st_list):
        # check input
        assert isinstance(st_list, list)
        for item in st_list:
            assert isinstance(item, StateJumpInfo)
            if item.action is not None:
                if "NULL" not in item.action:
                    item.action = "private_SM_" + item.action
                    if item.action not in self._priv_func_name_list:
                        self._priv_func_name_list.append(item.action)
                item.from_state = sm_state_common(self._sm_name) + self.__get_str_without_nr(item.from_state)
                item.to_state = sm_state_common(self._sm_name) + self.__get_str_without_nr(item.to_state)
                if item.from_state not in self._priv_state_name_list:
                    self._priv_state_name_list.append(item.from_state)

                condition_prefix = sm_condition_common(self._sm_name)
                if item.condition not in self._priv_condi_name_list:
                    self._priv_condi_name_list.append(item.condition)
                item.condition = condition_prefix + self.__get_str_without_nr(item.condition)

        self._priv_condi_name_list.sort(key=lambda x: int(re.findall(r"^\d*", x)[0]))
        for i in range(0, len(self._priv_condi_name_list)):
            self._priv_condi_name_list[i] = sm_condition_common(self._sm_name) + \
                                            self.__get_str_without_nr(self._priv_condi_name_list[i])

        for item in st_list:
            item.print()

        return st_list

    def _write_c_file(self):
        self.__create_include()
        self.__create_local_variable()
        self.__create_private_func_define()
        self.__create_link_to_table()
        self.__create_private_func_body()

    def __create_link_to_table(self):
        self._c_file_writer.write("#include \"" + self._inc_file_name + "\"\n")
        self._c_file_writer.write("\n")

    def __create_include(self):
        self._c_file_writer.write("#include \"MealyFSM.h\"\n")
        self._c_file_writer.write("#include \"" + self._header_file_name + "\"\n")
        self._c_file_writer.write("\n")

    def __create_local_variable(self):
        self._c_file_writer.write("\n")
        self._c_file_writer.write("STATIC FSM_t* smHandler;\n")
        self._c_file_writer.write("\n")

    def __create_private_func_define(self):
        for item in self._priv_func_name_list:
            self._c_file_writer.write("STATIC void " + item + "( void );\n")

        self._c_file_writer.write("\n")

    def __create_private_func_body(self):
        for item in self._priv_func_name_list:
            priv_func_str = "STATIC void " + item + "( void ){\n" \
                            "\n" \
                            "}\n\n"
            self._c_file_writer.write(priv_func_str)

    def _write_header_file(self):
        self._h_file_writer.write("#ifndef " + header_guard(self._sm_name) + "\n")
        self._h_file_writer.write("#define " + header_guard(self._sm_name) + "\n")
        self._h_file_writer.write("\n")
        self._h_file_writer.write("#include <stdbool.h>\n")
        self._h_file_writer.write("\n")
        self._h_file_writer.write("bool " + init_func_name(self._sm_name) + "( void );\n")
        self._h_file_writer.write("void " + tick_func_name(self._sm_name) + "( void );\n")
        self._h_file_writer.write("\n")
        self._h_file_writer.write("#endif\n")

    def _write_inc_file(self, prepared_list):
        self.__create_enumeration(self._table_file_writer)
        self.__create_transition_table_line_type(self._table_file_writer)
        self.__create_table(prepared_list)
        self.__create_init_func()
        self.__create_tick_func()

    def __create_enumeration(self, file_descriptor):
        list_nr = len(self._priv_state_name_list)
        file_descriptor.write("typedef enum{\n")
        for i in range(0, list_nr):
            file_descriptor.write("    " + self._priv_state_name_list[i] + ",\n")
        file_descriptor.write("    " + sm_state_common(self._sm_name) + "END,\n")
        file_descriptor.write("}" + state_enum_type(self._sm_name) + ";\n\n")

        list_nr = len(self._priv_condi_name_list)
        file_descriptor.write("typedef enum{\n")
        for i in range(0, list_nr):
            file_descriptor.write("    " + self._priv_condi_name_list[i] + ",\n")
        file_descriptor.write("    " + sm_condition_common(self._sm_name) + "END,\n")
        file_descriptor.write("}" + condition_enum_type(self._sm_name) + ";\n\n")

    def __create_transition_table_line_type(self, file_descriptor):
        file_descriptor.write("typedef struct{\n")
        file_descriptor.write("    Transition_t transition[" +
                              sm_condition_common(self._sm_name) + "END" + "];\n")
        file_descriptor.write("}" + state_type(self._sm_name) + ";\n")
        file_descriptor.write("\n")

    def __create_table(self, prepared_list):
        self._table_file_writer.write("STATIC const " + state_type(self._sm_name) + " " +
                                      transition_table_name(self._sm_name) + "[" +
                                      sm_state_common(self._sm_name) + "END" + "] = {\n")

        non_empty_state_list = []
        for state in self._priv_state_name_list:
            for item in prepared_list:
                if item.from_state in state:
                    # we have something to write for this state
                    non_empty_state_list.append(item)

            if len(non_empty_state_list) != 0:  # if list is not empty
                self._table_file_writer.write("    [" + state + "] = {\n")
                self._table_file_writer.write("        .transition = {\n")

                for item in non_empty_state_list:
                    self._table_file_writer.write("            [" + item.condition + "] = {\n")
                    self._table_file_writer.write("                .pTransFunc = " + item.action + ",\n")
                    self._table_file_writer.write("                .nextState = " + item.to_state + ",\n")
                    self._table_file_writer.write("                .isTransitionValid = true,\n")
                    self._table_file_writer.write("            },\n")

                self._table_file_writer.write("        },\n")
                self._table_file_writer.write("    },\n")

            non_empty_state_list = []

        self._table_file_writer.write("};\n")
        self._table_file_writer.write("\n")

    def __create_init_func(self):
        self._table_file_writer.write("bool " + init_func_name(self._sm_name) + "(void){\n")
        self._table_file_writer.write("    smHandler = FSM_New((void*) " + transition_table_name(self._sm_name) + ",\n")
        self._table_file_writer.write("                        sizeof(" + state_type(self._sm_name) + "),\n")
        self._table_file_writer.write("                        " + self._priv_state_name_list[0] + ",\n")
        self._table_file_writer.write("                        " + self._priv_condi_name_list[0] + ",\n")
        self._table_file_writer.write("                        " + self._priv_state_name_list[0] + ",\n")
        self._table_file_writer.write("                        " + self._priv_condi_name_list[0] + ");\n")
        self._table_file_writer.write("    return (smHandler == NULL ) ? false : true;\n}\n")
        self._table_file_writer.write("\n")

    def __create_tick_func(self):
        self._table_file_writer.write("void " + tick_func_name(self._sm_name) + "(void){\n")
        self._table_file_writer.write("    FSM_Tick(smHandler);\n")
        self._table_file_writer.write("}\n")

    def _copy_default_files(self):
        c_generator_dir = os.path.dirname(os.path.abspath(__file__))
        self.__copytree(c_generator_dir + os.sep + "fsmMgr", RESULT_PATH + os.sep + "src" + os.sep + "fsmMgr")

    def _create_unit_test(self, prepared_list):
        self.__copy_ceedling()
        utest_file_writer = open(RESULT_PATH + os.sep + "unit_test" + os.sep + "test" +
                                 os.sep + "test_" + self._sm_name + "SMFunc.c", 'w+')
        self.__write_include(utest_file_writer)
        self.__create_enumeration(utest_file_writer)
        self.__create_transition_table_line_type(utest_file_writer)
        self.__write_extern(utest_file_writer)
        self.__write_ceedling_func(utest_file_writer)
        self.__write_test_enum_change(utest_file_writer)
        self.__write_test_table_size(utest_file_writer)
        self.__write_test_defined_transition(utest_file_writer, prepared_list)
        self.__write_test_no_new_transition(utest_file_writer, prepared_list)

        utest_file_writer.close()

    def __write_include(self, utest_file_descriptor):
        utest_file_descriptor.write("#include \"unity.h\"\n#include \"" +
                                    self._header_file_name + "\"\n#include \"mock_MealyFSM.h\"\n\n")

    def __write_extern(self, utest_file_descriptor):
        for item in self._priv_func_name_list:
            utest_file_descriptor.write("extern void " + item + "( void );\n")
        utest_file_descriptor.write("extern FSM_t* smHandler;\n")
        utest_file_descriptor.write("extern const " + state_type(self._sm_name) + " " +
                                    transition_table_name(self._sm_name) + "[" +
                                    sm_state_common(self._sm_name) + "END" + "];\n")
        utest_file_descriptor.write("\n")

    def __write_ceedling_func(self, utest_file_descriptor):
        utest_file_descriptor.write("void setUp(void)\n"
                                    "{\n"
                                    "}\n"
                                    "\n"
                                    "void tearDown(void)\n"
                                    "{\n"
                                    "}\n"
                                    "\n")
        utest_file_descriptor.write("void test_InitFailed(void)\n"
                                    "{\n"
                                    "    FSM_New_ExpectAnyArgsAndReturn(NULL);\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(false, " + self._sm_name + "_Init());\n"
                                    "}\n"
                                    "\n"
                                    "void test_InitSuccess(void)\n"
                                    "{\n"
                                    "    FSM_t fsm;\n"
                                    "    FSM_New_ExpectAnyArgsAndReturn(&fsm);\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(true, " + self._sm_name + "_Init());\n"
                                    "}\n"
                                    "\n"
                                    "void test_TickIsCalled(void)\n"
                                    "{\n"
                                    "    FSM_Tick_ExpectAnyArgs();\n"
                                    "\n"
                                    "    " + self._sm_name + "_Tick();\n"
                                    "}\n"
                                    "\n")

    def __write_test_enum_change(self, utest_file_descriptor):
        utest_file_descriptor.write("void test_EnumNotChange(void)\n{\n")

        list_nr = len(self._priv_state_name_list)
        for i in range(0, list_nr):
            utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(i) + ", " +
                                        self._priv_state_name_list[i] + ");\n")
        utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(list_nr) + ", " +
                                    sm_state_common(self._sm_name) + "END);\n\n")
        list_nr = len(self._priv_condi_name_list)
        for i in range(0, list_nr):
            utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(i) + ", " +
                                        self._priv_condi_name_list[i] + ");\n")
        utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(list_nr) + ", " +
                                    sm_condition_common(self._sm_name) + "END);\n")

        utest_file_descriptor.write("}\n\n")

    def __write_test_table_size(self, utest_file_descriptor):
        condition_end_name = sm_condition_common(self._sm_name) + "END"
        state_end_name = sm_state_common(self._sm_name) + "END"

        utest_file_descriptor.write("void test_LineSizeNotChange(void)\n"
                                    "{\n"
                                    "    uint32_t expectedSize = " + condition_end_name + " * sizeof(Transition_t);\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(expectedSize, sizeof(" + state_type(self._sm_name) + "));\n"
                                    "}\n"
                                    "\n"
                                    "void test_TableSizeNotChange(void)\n"
                                    "{\n"
                                    "    uint32_t expectedSize = " + condition_end_name +
                                    " * sizeof(Transition_t) *" + state_end_name + ";\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(expectedSize, sizeof(" + transition_table_name(self._sm_name) + "));\n"
                                    "}\n\n")

    def __write_test_defined_transition(self, utest_file_descriptor, prepared_list):
        for item in prepared_list:
            func_name = "test_Transition_s_" + item.from_state + "_c_" + item.condition
            utest_file_descriptor.write("void " + func_name + "(void)\n")
            utest_file_descriptor.write("{\n"
                                        "    TransitionFunction expectedFunc = " + item.action + ";\n"
                                        "    " + state_enum_type(self._sm_name) + "  expectedNextState = " + item.to_state + ";\n\n")
            utest_file_descriptor.write("    " + state_type(self._sm_name) + " tableLine = " +
                                        transition_table_name(self._sm_name) + "[" + item.from_state + "];\n")
            utest_file_descriptor.write("    Transition_t actualTransition = " +
                                        "tableLine.transition[" + item.condition + "];\n\n")
            utest_file_descriptor.write("    TEST_ASSERT_EQUAL(expectedFunc, actualTransition.pTransFunc);\n"
                                        "    TEST_ASSERT_EQUAL(expectedNextState, actualTransition.nextState);\n"
                                        "    TEST_ASSERT_EQUAL(true, actualTransition.isTransitionValid);\n"
                                        "}\n\n")

    def __write_test_no_new_transition(self, utest_file_descriptor, prepared_list):

        utest_file_descriptor.write("void test_NoTransistionAdded(void)\n"
                                    "{\n"
                                    "    uint8_t expectedValidTransitionNumber = " + str(len(prepared_list)) + ", actualNumber = 0;\n"
                                    "    " + state_type(self._sm_name) + " tableLine;\n"
                                    "    Transition_t actualTransition;\n\n")

        utest_file_descriptor.write("    for (" + state_enum_type(self._sm_name) + " i = " + self._priv_state_name_list[0] +
                                    "; i < " + sm_state_common(self._sm_name) + "END; i++)\n")

        utest_file_descriptor.write("    {\n"
                                    "        for ( " + condition_enum_type(self._sm_name) + " j = " +
                                    self._priv_condi_name_list[0] + "; j < " +
                                    sm_condition_common(self._sm_name) + "END; j++)\n")
        utest_file_descriptor.write("        {\n"
                                    "            tableLine = " + transition_table_name(self._sm_name) + "[i];\n"
                                    "            actualTransition = tableLine.transition[j];\n"
                                    "            if ( true == actualTransition.isTransitionValid )\n"
                                    "            {\n"
                                    "                actualNumber++;\n"
                                    "            }\n"
                                    "        }\n"
                                    "    }\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(expectedValidTransitionNumber, actualNumber);\n"
                                    "}\n\n")

    def __copy_ceedling(self):
        c_generator_dir = os.path.dirname(os.path.abspath(__file__))
        self.__copytree(c_generator_dir + os.sep + "unit_test", RESULT_PATH + os.sep + "unit_test")

    @staticmethod
    def __copytree(src, dst):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    @staticmethod
    def __get_trans_name_from_info_list(action, to_state, trans_info_list):
        for item in trans_info_list:
            if action == item[1] and to_state == item[2]:
                return item[0]
        return None

    @staticmethod
    def __get_str_without_nr(string):
        return re.sub(r"^[0-9]*_*", "", string)

    def __get_str_without_com_str(self, string):
        string = re.sub(sm_state_common(self._sm_name), "", string)
        string = re.sub(sm_condition_common(self._sm_name), "", string)
        return string

    @staticmethod
    def __get_trans_str_name(condition, state, trans_list):
        for item in trans_list:
            if condition == item.condition and state == item.from_state:
                return True, item.trans_name
        return False, "NULL"
