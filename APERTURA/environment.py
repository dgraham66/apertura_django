import os
import utils
from abc import ABCMeta, abstractmethod
import uuid
import utils

__author__ = 'dgraham'


class Job(object):

    def __init__(self, name=None, job_id=str(uuid.uuid4())):
        self.job_id = job_id
        self.name = name if name is not None else self.job_id
        self.path_map = PathMap(job_id=self.job_id)
        self.status = 0
        self.__status_dict = {
            0: 'Zero status.',
            1: 'One status.',
            2: 'Two status.',
            3: 'Three status.'
        }

    def status_desc(self):
        return self.__status_dict[self.status]


class PathMap(object):
    def __init__(
            self,
            job_id,
            jobs_root_dir=None,
            path_data=None
    ):
        self.job_id = job_id
        self.jobs_root_dir = jobs_root_dir if jobs_root_dir is not None else os.path.abspath('data/jobs/')

        # Properties
        self._job_dir = None
        self._input_dir = None
        self._output_dir = None
        self._tmp_dir = None
        self._logs_dir = None
        self._dir_dict = {}
        self._file_dict = {}

        # Init values to defaults
        self.__init_default_dirs()

        # Check dir dict for default
        if path_data is not None:
            self.__copy_path_dict__(path_data)

    def __init_default_dirs(self):
        self._job_dir = self.__get_abs_path(
            self.jobs_root_dir,
            self.job_id
        )
        self._input_dir = self.__get_abs_path(
            self._job_dir,
            'input'
        )
        self._output_dir = self.__get_abs_path(
            self._job_dir,
            'output'
        )
        self._tmp_dir = self.__get_abs_path(
            self._job_dir,
            'tmp'
        )
        self._logs_dir = self.__get_abs_path(
            self._job_dir,
            'logs'
        )
        # Init directory dictionary
        self.dir_dict['job_dir'] = self._job_dir
        self.dir_dict['input_dir'] = self._input_dir
        self.dir_dict['output_dir'] = self._output_dir
        self.dir_dict['tmp_dir'] = self._tmp_dir
        self.dir_dict['logs_dir'] = self._logs_dir

    def __copy_path_dict__(self, data):
        self._job_dir = self.dir_dict['job_dir'] = data['job_dir']
        self._input_dir = self.dir_dict['input_dir'] = data['input_dir']
        self._output_dir = self.dir_dict['output_dir'] = data['output_dir']
        self._tmp_dir = self.dir_dict['tmp_dir'] = data['tmp_dir']
        self._logs_dir = self.dir_dict['logs_dir'] = data['logs_dir']

    def __get_abs_path(self, dir, sub_dir):
        return os.path.abspath(os.path.join(dir, sub_dir))

    @property
    def job_dir(self):
        return self._job_dir

    @job_dir.setter
    def job_dir(self, value):
        self._job_dir = value

    @property
    def input_dir(self):
        return self._input_dir

    @input_dir.setter
    def input_dir(self, value):
        self._input_dir = value

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value):
        self._output_dir = value

    @property
    def tmp_dir(self):
        return self._tmp_dir

    @tmp_dir.setter
    def tmp_dir(self, value):
        self._tmp_dir = value

    @property
    def logs_dir(self):
        return self._logs_dir

    @logs_dir.setter
    def logs_dir(self, value):
        self._logs_dir = value

    @property
    def dir_dict(self):
        return self._dir_dict

    @dir_dict.setter
    def dir_dict(self, value):
        self._dir_dict = value

    @property
    def file_dict(self):
        return self._file_dict

    @file_dict.setter
    def file_dict(self, value):
        self._file_dict = value
