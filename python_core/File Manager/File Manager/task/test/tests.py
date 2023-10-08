from hstest.stage_test import StageTest
from hstest.check_result import CheckResult
from hstest import dynamic_test, TestedProgram, WrongAnswer
import os
import shutil

# adapted from the first DuplicateFileHandler test

# dict for creating files
files = {
    'info.txt': {'path': ['root_folder'],
                 'content': 'eed110d0dbd1d89d1ffea807d1d88679'},
    'lost.json': {'path': ['root_folder'],
                  'content': '3a70ac2ebacf4174aa11dfbd1af835bd'},
    'phones.csv': {'path': ['root_folder'],
                   'content': '671ab9fbf94dc377568fb7b2928960c9'},
    'python.txt': {'path': ['root_folder'],
                   'content': 'd2c2ee4cbb368731f1a5399015160d7d'},
    'bikeshare.csv': {'path': ['root_folder', 'calc'],
                      'content': 'c03285172453d7278a85a5db4d06423c'},
    'server.php': {'path': ['root_folder', 'calc'],
                   'content': 'a5c662fe853b7ab48d68532791a86367'},
    'db_cities.js': {'path': ['root_folder', 'files'],
                     'content': 'f2e5cf58ae9b2d2fd0ae9bf8fa1774da'},
    'some_text.txt': {'path': ['root_folder', 'files'],
                      'content': 'd2c2ee4cbb368731f1a5399015160d7d'},
    'cars.json': {'path': ['root_folder', 'files', 'stage'],
                  'content': '3a70ac2ebacf4174aa11dfbd1af835bd'},
    'package-lock.json': {'path': ['root_folder', 'files', 'stage'],
                          'content': 'eebf1c62a13284ea1bcfe53820e83f11'},
    'index.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                 'content': '797ac79aa6a3c2ef733fecbaff5a655f'},
    'libs.txt': {'path': ['root_folder', 'files', 'stage', 'src'],
                 'content': '4909fd0404ac7ebe1fb0c50447975a2a'},
    'reviewslider.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                        'content': 'abc96a9b62c4701f27cf7c8dbd484fdc'},
    'spoiler.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                   'content': 'b614ccac263d3d78b60b37bf35e860f3'},
    'src.txt': {'path': ['root_folder', 'files', 'stage', 'src'],
                'content': 'eed110d0dbd1d89d1ffea807d1d88679'},
    'toggleminimenu.js': {'path': ['root_folder', 'files', 'stage', 'src'],
                          'content': '7eceb7dd5a0daaccc32739e1dcc6c3b0'},
    'extraversion.csv': {'path': ['root_folder', 'project'],
                         'content': 'fc88cf4d79437fa06e6cfdd80bd0eed2'},
    'index.html': {'path': ['root_folder', 'project'],
                   'content': '3f0f7b61205b863d2051845037541835'},
    'python_copy.txt': {'path': ['root_folder', 'project'],
                        'content': 'd2c2ee4cbb368731f1a5399015160d7d'}
}


root_dir_path = os.path.join('module', 'root_folder')


def create_files(path):
    # delete root_folder
    if os.path.isdir(path):
        shutil.rmtree(path)

    # create files
    for key, dict_val in files.items():
        path = os.path.join('module', *dict_val['path'])
        if not os.path.isdir(path):
            os.makedirs(path)
        file_path = os.path.join(path, key)
        with open(file_path, 'a+') as f:
            f.write(dict_val['content'])


class FileManagerTest(StageTest):

    @dynamic_test()
    def test1(self):
        x = '4'
        expected_result = 'Invalid command'
        pr = TestedProgram()
        pr.start()
        output = pr.execute(stdin=x)
        if not output:
            raise WrongAnswer('Your program did not print anything.')
        expected_result_cleaned = expected_result.lower().strip().replace(' ', '')
        output_cleaned = output.lower().strip().replace(' ', '')
        check = expected_result_cleaned in output_cleaned
        return CheckResult(check, f'Wrong message returned. \nInput message: {x} \nYou printed: {output} \nWe printed {expected_result}')

    @dynamic_test()
    def test2(self):
        x = 'cd files'
        expected_result = 'files'
        pr = TestedProgram()
        pr.start()
        output = pr.execute(stdin=x)
        if not output:
            raise WrongAnswer('Your program did not print anything.')
        expected_result_cleaned = expected_result.lower().strip().replace(' ', '')
        output_cleaned = output.lower().strip().replace(' ', '')
        check = expected_result_cleaned in output_cleaned
        return CheckResult(check, f'Wrong message returned. \nInput message: {x} \nYou printed: {output} \nWe printed {expected_result}')

    @dynamic_test()
    def test3(self):
        x = 'cd project\npwd'
        expected_result_a = 'root_folder\project'
        expected_result_b = 'root_folder/project'
        pr = TestedProgram()
        pr.start()
        output = pr.execute(stdin=x)
        if not output:
            raise WrongAnswer('Your program did not print anything.')
        expected_result_a_cleaned = expected_result_a.lower().strip().replace(' ', '')
        expected_result_b_cleaned = expected_result_b.lower().strip().replace(' ', '')
        output_cleaned = output.lower().strip().replace(' ', '')
        check = (expected_result_a_cleaned in output_cleaned) or (expected_result_b_cleaned in output_cleaned)
        return CheckResult(check, f'Wrong message returned. \nInput message: {x} \nYou printed: {output} \nWe expected the absolute path to the correct folder.')

    @dynamic_test()
    def test4(self):
        x = 'cd module\ncd root_folder\ncd ..'
        expected_result = 'module'
        pr = TestedProgram()
        pr.start()
        output = pr.execute(stdin=x)
        if not output:
            raise WrongAnswer('Your program did not print anything.')
        expected_result_cleaned = expected_result.lower().strip().replace(' ', '')
        output_cleaned = output.lower().strip().replace(' ', '')
        check = (expected_result_cleaned in output_cleaned)
        return CheckResult(check, f'Wrong message returned. \nInput message: {x} \nYou printed: {output} \nWe expected {expected_result}')

    def after_all_tests(self):
        try:
            create_files(root_dir_path)
        except Exception as ignored:
            pass

    def generate(self):
        try:
            create_files(root_dir_path)
        except Exception as ignored:
            pass
        return []


if __name__ == '__main__':
    FileManagerTest().run_tests()
