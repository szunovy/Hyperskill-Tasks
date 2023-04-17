import re
import sys
import os
import ast
from pprint import pprint

class StaticAnalyzer():
    def __init__(self, path):
        self.path = path
        self.error_messages = []

        with open(self.path, 'r') as f:
            self.lines_all = f.readlines()
            f.seek(0)  # reseting the pointer to enable reading file once more
            self.ast_tree = ast.parse(f.read())
            # print(self.ast_e)

        # pprint(ast.dump(self.ast_tree)) #todo

        # print(self.ast_tree.)
        # for child in ast.iter_child_nodes(self.ast_tree):
        #     print(child)



        # analyzer = Analyzer()
        # analyzer.visit(self.ast_tree)
        # analyzer.report()

        self.messages_list = {
            1: 'S001 Too long over 79 chars',
            2: 'S002 Indentation is not a multiple of four',
            3: 'S003 Unnecessary semicolon after a statement',
            4: 'S004 Less than two spaces before inline comment',
            5: 'S005 TODO found',
            6: 'S006 More than two blank lines preceding a code line',
            7: 'S007 Too many spaces after construction_name (def or class)',
            8: 'S008 Class name "-" should be written in CamelCase',
            9: "S009 Function name '-' should be written in snake_case",
            10: "S010 Argument name '-' should be written in snake_case",
            11: "S011 Variable '-' should be written in snake_case",
            12: "S012 The default argument value is mutable",
         }

    def AnalyzeFile(self):
        # self.lines_all = f.readlines()

        empty_lines_counter = 0
        for line_index in range(len(self.lines_all)):
            line_real_number = line_index + 1
            line = self.lines_all[line_index]

            if self.line_too_long(line):
                # print(f'Line {line_real_number}: {self.messages_list[1]}')
                self.add_message(line_real_number, 1)

            if self.identation_not_four(line):
                self.add_message(line_real_number, 2)

            if self.unnecessary_semicolon(line):
                self.add_message(line_real_number, 3)

            if self.inline_comment_spaces(line):
                self.add_message(line_real_number, 4)

            if self.TODO_found(line):
                self.add_message(line_real_number, 5)

            if line.isspace():
                empty_lines_counter += 1
            else:
                if empty_lines_counter > 2:
                    self.add_message(line_real_number, 6)
                empty_lines_counter = 0

            self.spaces_after_construction_name(line, line_real_number)
            self.class_naming_camel(line, line_real_number)
            self.function_name_snake(line, line_real_number)

        # check not made every line
        self.argument_names_snake()
        self.variable_names_snake()
        self.default_argument_mutable()

        self.print_messages()

    def print_messages(self):
        for message in self.error_messages:
            print(message)

    def line_too_long(self, line):  # SOO1
        if len(line) > 79:
            return True
        return False

    def identation_not_four(self, line):  # S002
        # if self.get_identation_length(line) % 4:
        if (len(line) - len(line.lstrip(' '))) % 4 != 0:
            return True
        return False

    # chyba dziala
    # def get_identation_length(self, line):  # used in S002
    #     # returns length of identation on given line
    #     template = '[ /t]*'
    #     identation_string = re.match(template, line).group()
    #     length = 0
    #     for char in identation_string:
    #         if char == ' ':
    #             length += 1
    #         if char == '\t':
    #             length += 4
    #     return length

    def unnecessary_semicolon(self, line):
        # # template = '(?<!#).*;'
        # template ='^(?!.*#.*;).*;'
        # if re.match(template, line):
        if '#' in line and line.split('#')[0].strip().endswith(';'):
            return True
        if '#' not in line and line.strip().endswith(';'):
            return True
        return False

    # powinno być git
    def inline_comment_spaces(self, line):  # S004
        # template = '.*(?<!  )#'
        # if re.search(template, line):
        if not line.startswith('#') and '#' in line and not line.split('#')[0].endswith('  '):
            return True
        return False

    # chyba dziala
    def TODO_found(self, line):  # S005
        template = '(#.*todo)'

        if re.search(template, line.lower()):
            return True
        return False

    def spaces_after_construction_name(self, line, line_number):
        if line.lstrip().startswith('class'):
            template = '^class [^ ]'
            if not re.match(template, line.lstrip()):
                self.error_messages.append(f"{self.path}: Line {line_number}: S007 Too many spaces after 'class'")

        if line.lstrip().startswith('def'):
            template = '^def [^ ]'
            if not re.match(template, line.lstrip()):
                self.error_messages.append(f"{self.path}: Line {line_number}: S007 Too many spaces after 'def'")

    def class_naming_camel(self, line, line_number):
        if line.lstrip().startswith('class'):
            template = '(?<=class)[ ]+[^(:]+(?=[(:])'
            class_name_result = re.search(template, line.lstrip()).group().lstrip()
            name_template = '^([A-Z][a-z]*)+$'
            if not re.match(name_template, class_name_result):
                self.error_messages.append(f'{self.path}: Line {line_number}: {self.messages_list[8].replace("-", class_name_result)}')

        # if line.lstrip().startswith('class'):
        #     template = '^class[ ]+([A-Z][a-z]*)+[(:]'
        #     if not re.match(template, line.lstrip()):
        #         self.add_message(line_number, 8)

    def function_name_snake(self, line, line_number):
        if line.lstrip().startswith('def'):
            # template = '(?<=fun)[ ]+_{0,2}[a-z]+(_[a-z]+)*?_{0,2}1?(?=[(:])'
            template = '(?<=def)[^(:]*?(?=[(:])'
            fun_name_result = re.search(template, line.lstrip()).group().lstrip()
            name_template = '^_{0,2}[a-z0-9]+(_[a-z0-9]+)*?_{0,2}$'  # moze byc potrzebny warunek ze pierwszy znak nie moze byc cyfra
            if not re.match(name_template, fun_name_result):
                # self.error_messages.append(f'{self.path}: Line {line_number}: S009 Function name {fun_name_result} should be writeen in snake_case')
                self.error_messages.append(f'{self.path}: Line {line_number}: {self.messages_list[9].replace("-", fun_name_result)}')
        # if line.lstrip().startswith('def'):
        #     template = '^def[a-z]+(_[a-z]*)*[(:]'
        #     if not re.match(template, line.lstrip()):
        #         self.add_message(line_number, 9)



    def argument_names_snake(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                # function_name = node.name
                # print(node.args.defaults)
                # print(node.args.args[1].arg)
                for argument in node.args.args:
                    argument_name = argument.arg
                    name_template = '^_{0,2}[a-z0-9]+(_[a-z0-9]+)*?_{0,2}$'  # moze byc potrzebny warunek ze pierwszy znak nie moze byc cyfra
                    if not re.match(name_template, argument_name):
                            self.error_messages.append(f'{self.path}: Line {node.lineno}: {self.messages_list[10].replace("-", argument_name)}')

    def variable_names_snake(self):
        # pprint(ast.dump(self.ast_tree))
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Assign) and not isinstance(node.value, ast.Call):
                # print('-----------------------------')

                if isinstance(node.targets[0], ast.Name):
                    # print(node.targets[0].id)
                    name_template = '^_{0,2}[a-z0-9]+(_[a-z0-9]+)*?_{0,2}$'  # moze byc potrzebny warunek ze pierwszy znak nie moze byc cyfra
                    if not re.match(name_template, node.targets[0].id):
                        self.error_messages.append(f'{self.path}: Line {node.lineno}: {self.messages_list[11].replace("-", node.targets[0].id)}')
                else:
                    # print(node.targets[0].attr)
                    name_template = '^_{0,2}[a-z0-9]+(_[a-z0-9]+)*?_{0,2}$'  # moze byc potrzebny warunek ze pierwszy znak nie moze byc cyfra
                    if not re.match(name_template, node.targets[0].attr):
                            self.error_messages.append(f'{self.path}: Line {node.lineno}: {self.messages_list[11].replace("-", node.targets[0].attr)}')


                # for var_name in node.targets:
                    # print(var_name[0])
                # print(node)

                    # function_name = node.name
                    # print(node.args.defaults)
                    # print(node.args.args[1].arg)
                    # print(node)
                    # for arg in node.args:
                    #     print(arg.arg)
                    # for argument in node.args.args:
                    #     argument_name = argument.arg
                    #     name_template = '^_{0,2}[a-z0-9]+(_[a-z0-9]+)*?_{0,2}$'  # moze byc potrzebny warunek ze pierwszy znak nie moze byc cyfra
                    #     if not re.match(name_template, argument_name):
                    #         self.error_messages.append(
                    #             f'{self.path}: Line {node.lineno}: S010 Argument name {argument_name} should be writeen in snake_case')

    def default_argument_mutable(self):
        # print('tik')
        # pprint(ast.dump(self.ast_tree))
        # print(self.ast_tree)
        for node in ast.walk(self.ast_tree):
            # print(node)
            if isinstance(node, ast.FunctionDef):
                # print(node.args.defaults)
                for default_value in node.args.defaults:
                    if not isinstance(default_value, ast.Constant):
                        # print(node.lineno)
                        # self.error_messages.append(f'{self.path}: Line {node.lineno}: S012 The default argument value is mutable')
                        self.error_messages.append(f'{self.path}: Line {node.lineno}: {self.messages_list[12]}')
                # function_name = node.name
                # print(node.args.defaults)
                # print(node.args.args[1].arg)

                # for argument in node.args.args:
                #     argument_name = argument
                #     print(argument_name)
                #     name_template = '^_{0,2}[a-z0-9]+(_[a-z0-9]+)*?_{0,2}$'  # moze byc potrzebny warunek ze pierwszy znak nie moze byc cyfra
                #     if not re.match(name_template, argument_name):
                #         self.error_messages.append(
                #             f'{self.path}: Line {node.lineno}: S010 Argument name {argument_name} should be writeen in snake_case')


    def add_message(self, line, code):
        self.error_messages.append(f'{self.path}: Line {line}: {self.messages_list[code]}')


# class MyError(Exception):
#     def __init__(self, msg, line_number):
#         self.msg = msg
#         self.message = f'Line {line_number}: {self.msg}'
#         super().__init__(self.message)
#
#
# messages_list = {
#     1: 'S001 Too long over 79 chars',
#     2: 'S002 Indentation is not a multiple of four',
#     3: 'S003 Unnecessary semicolon after a statement',
#     4: 'S004 Less than two spaces before inline comment',
#     5: 'S005 TODO found',
#     6: 'S006 More than two blank lines preceding a code line'
#  }


# def LineTooLong(line):
#     if len(line) > 79:
#         return True
#     return False

# def identation_not_four(line):
#     template = '[ /t]*'
#     identation_string = re.search(template, line).group()
#     length = 0
#     for char in identation_string:
#         if char == ' ':
#             length += 1
#         if char == '\t':
#             length += 4
#         print(length)




# raise MyError(messages_list[1], 2)


# with open(path, 'r') as f:
#     line_index = 0
#     lines = f.readlines()
#     for line_index in range(len(lines)):
#         # line_number = line_index + 1
#         line = lines[line_index]
#         try:
#             if LineTooLong(line):
#                 raise MyError(messages_list[1], line_index + 1)
#
#         except MyError as err:
#             print(err)


if __name__ == "__main__":
    # input_path = sys.argv[1]
    # # path = r'C:\Users\Szu\PycharmProjects\Static Code Analyzer\Static Code Analyzer\task\test'
    # files = []
    # if os.path.isfile(input_path):
    #     files.append(input_path)
    # if os.path.isdir(input_path):
    #     # files = os.listdir(path)
    #     files = [os.path.join(input_path, file) for file in os.listdir(input_path)]
    # # print(files)
    # # files_py = []
    # for file in files:
    #     if file.endswith('.py') and os.access(file, os.R_OK) and not file.endswith('tests.py'):
    #         # print('linia testowa', file)
    #         # print()
    #     # if os.path.isfile(path) and
    #     # print(file)
    #         My_Static_Analyzer = StaticAnalyzer(file)
    #         My_Static_Analyzer.AnalyzeFile()


    # input_path = r'test\this_stage\test_7.py'

    input_path = sys.argv[1]
    # input_path = r'..\test\this_stage'

    # if input_path == r'test\this_stage\test_7.py':
    #     input_path = r'..\test\this_stage\test_7.py'

    if os.path.isfile(input_path):
        My_Static_Analyzer = StaticAnalyzer(input_path)
        My_Static_Analyzer.AnalyzeFile()
    if os.path.isdir(input_path):
        # files = os.listdir(path)
        for root, dirs, files in os.walk(input_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_path.endswith('.py') and os.access(file_path, os.R_OK):
                    if file_name.endswith('tests.py'):
                        continue
                    # print(root)
                    file_path = os.path.join(root, file_name)
                    My_Static_Analyzer = StaticAnalyzer(file_path)
                    My_Static_Analyzer.AnalyzeFile()
    # print(files)
    # files_py = []
    # for file in files:
    #     if file.endswith('.py') and os.access(file, os.R_OK) and not file.endswith('tests.py'):
    #         # print('linia testowa', file)
    #         # print()
    #     # if os.path.isfile(path) and
    #     # print(file)
    #         My_Static_Analyzer = StaticAnalyzer(file)
    #         My_Static_Analyzer.AnalyzeFile()




    # if os.path.isdir(input_path):
    #
    #     for root, dirs, files in os.walk(input_path):
    #         for file_name in files:
    #             if not file_name.endswith(".py") and file:
    #                 continue
    #
    #             file_path = os.path.join(root, file_name)
    #             My_Static_Analyzer = StaticAnalyzer(file_path)
    #             My_Static_Analyzer.AnalyzeFile()
    #             # call_analyzer_error(file_path)
    # else:
    #     My_Static_Analyzer = StaticAnalyzer(input_path)
    #     My_Static_Analyzer.AnalyzeFile()



# # write your code here
# file = open(input(), 'r', encoding='utf-8')
#
# blank_line = 0
#
# for i, line in enumerate(file.readlines(), start=1):
#     if len(line) > 79:
#         print(f'Line {i}: S001 Too Long')
#
#     if (len(line) - len(line.lstrip(' '))) % 4 != 0:
#         print(f'Line {i}: S002 Indentation is not a multiple of four')
#
#     if '#' in line and line.split('#')[0].strip().endswith(';'):
#         print(f'Line {i}: S003 Unnecessary semicolon')
#
#     if '#' not in line and line.strip().endswith(';'):
#         print(f'Line {i}: S003 Unnecessary semicolon')
#
#     if not line.startswith('#') and '#' in line and not line.split('#')[0].endswith('  '):
#         print(f'Line {i}: S004 At least two spaces before inline comment required')
#
#     if '#' in line and 'todo' in line.split('#')[1].lower():
#         print(f'Line {i}: S005 TODO found')
#
#     if not line.strip():
#         blank_line += 1
#     else:
#         if blank_line > 2:
#             print(f'Line {i}: S006 More than two blank lines used before this line')
#         blank_line = 0

# task 3 part
    # args = sys.argv
    # input_path = args[1]
    #
    #
    # def call_analyzer_error(path):
    #     error_checking = StaticCodeAnalyzer(path)
    #     error_checking.check_file()
    #     return None
    #
    #
    # if os.path.isdir(input_path):
    #
    #     for root, dirs, files in os.walk(input_path):
    #         for file_name in files:
    #             if file_name.endswith(".py") is False:
    #                 continue
    #
    #             file_path = os.path.join(root, file_name)
    #             call_analyzer_error(file_path)
    #
    # else:
    #     call_analyzer_error(input_path)