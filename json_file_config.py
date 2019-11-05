import re
import os
import json

'''
class that collecting json config files from the dir provided, and the keys contained in json files would be transferred to the properties of the instance when instantiation.
after instantiation, you can get the value by instance.key.key conveniently.
you can pass a regex express(default be r'.*\.json') to match the json files that will be registed with the instance.

there also be another choice that passing a dict obj to regist_attr to transfer the dict keys to the properties of the instance with out traverse the dirs. 
'''

class Config:

    def __init__(self, include_dir='./', exclude_dir=None, regex=r'.*\.json$', regist_attr=None):
        '''

        :param include_dir: str or list obj, path that will be traversed to find the json files.
        :param exclude_dir: str or list obj, path that will ignored when traversing.
        :param regex: str obj, the pattern that used to match the json files you want to include.
        :param regist_attr: dict obj, directlly transfer the keys to the properties of the instance with out traverse the dirs.
        '''
        self.include_dir = self.list_dirs(include_dir)
        self.exclude_dir = self.list_dirs(exclude_dir)
        self.pattern = re.compile(regex)
        self.file_list = []
        if not regist_attr:
            self.search()
        else:
            self.regist(regist_attr)

    def __getattr__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            return None

    def list_dirs(self, dirs):
        if isinstance(dirs, str):
            dir_list = [dirs]
        elif isinstance(dirs, list):
            dir_list = [i for i in dirs]
        else:
            dir_list = []
        return dir_list

    def regist(self, config_dict: dict):
        '''
        transfer the dict keys to the instance attributes
        :param config_dict: dict obj that keys will be transferred to the instance properties
        :return:
        '''
        for key, value in config_dict.items():

            if isinstance(value, dict):
                setattr(self, key, Config(regist_attr=value))
            else:
                setattr(self, key, value)

    def search(self):
        '''
        search dirs that may include valid json files and transfer the keys contained in the json files to instance properties
        :return:
        '''
        dir_list = [i for i in self.include_dir]
        while dir_list:

            iter_path = dir_list.pop()
            # ignore the dir in exclude_dir
            if iter_path in self.exclude_dir:
                continue
            # ignore the dir that doesn't exist
            if not os.path.exists(iter_path):
                continue
            # iter the files or dirs under the iter_path
            for path in os.listdir(iter_path):
                deep_path = os.path.join(iter_path, path)
                # if the path is a file and the file name match the pattern, then add the file path into the file_list
                if os.path.isfile(deep_path):
                    if re.match(self.pattern, deep_path):
                        self.file_list.append(deep_path)
                # if the path is an dir, then add the dir to dir_list
                elif os.path.isdir(deep_path):
                    dir_list.append(deep_path)
        # iter the valid json file and call the regist func to transfer the key-value json content to instance properties
        for json_file in self.file_list:
            with open(json_file, 'r', encoding='utf8') as f:
                content = f.read()
                content_json = json.loads(content)
                self.regist(content_json)


if __name__ == '__main__':

    c = Config()

    print(c)
    print(c.file_list)


