import luigi
import subprocess
import os
import errno
import yaml
from environment import PathMap
from environment import Job
import utils
import yaml


__author__ = 'dgraham'


class EntryPoint(object):
    def __init__(self, job_id, template_path, auto_run=True, run_local=False):
        self.job_id = job_id
        self.template_path = os.path.abspath(template_path)
        self.was_called = False
        self.has_completed = False
        self.result_string = ''
        self.cmd = []
        self.run_local = run_local

        self.param_dict = {
            'luigi_call': 'luigi',
            'module_name_1': 'APERTURA.pipeline',
            'module_name_2': 'PlinkWrapper',
            'job_id': str(self.job_id),
            'template_path': str(self.template_path)
        }
        if run_local:
            self.param_dict['scheduler'] = '--local-scheduler'
        if auto_run:
            self.was_called = True
            self.has_completed = self.__execute_cmd__()

    def __execute_cmd__(self):
        try:
            self.cmd = self.__build_command__()
            # self.result_string += "call_cmd: %s \n" % str(self.cmd)
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE)
            output = process.communicate()[0]
            process.wait()
            # self.result_string += "Plink Call Output: %s \n" % output
            # print(self.result_string)
        except:
            return False

        return True

    def __build_command__(self):
        tmp_cmd = []
        tmp_cmd.append(self.param_dict['luigi_call'])
        tmp_cmd.append('--module')
        tmp_cmd.append(self.param_dict['module_name_1'])
        tmp_cmd.append(self.param_dict['module_name_2'])
        if self.run_local:
            tmp_cmd.append(self.param_dict['scheduler'])
        tmp_cmd.append('--jobid')
        tmp_cmd.append(self.param_dict['job_id'])
        tmp_cmd.append('--templatepath')
        tmp_cmd.append(self.param_dict['template_path'])
        return tmp_cmd


class PlinkWrapper(luigi.WrapperTask):
    jobid = luigi.Parameter()
    templatepath = luigi.Parameter(default=os.path.abspath('static/script_templates/demo_basic_qa.yaml'))
    cmdtype = luigi.Parameter(default='demo_basic_qa')

    def requires(self):
        path_map = PathMap(job_id=self.jobid)
        yield SetupJob(jobid=self.jobid)
        # yield PlinkScriptBuilder(jobid=self.jobid, inpath=self.template_path)
        yield PlinkCommand(
            jobid=self.jobid,
            cmdtype=self.cmdtype,
            templatepath=self.templatepath,
            resultdir=path_map.output_dir
        )


class PlinkScriptBuilder(luigi.ExternalTask):
    """Builds a script file executable by a PLINK command line call."""
    priority = 800
    jobid = luigi.Parameter()
    inpath = luigi.Parameter()

    script_path = None
    script_name = None

    def requires(self):
        return SetupJob(jobid=self.jobid)

    def output(self):
        path_map = PathMap(job_id=self.jobid)
        self.script_name = os.path.splitext(self.inpath)[0] + '.txt'
        # print(self.script_name)
        self.outpath = os.path.join(
            path_map.input_dir,
            self.script_name
        )
        data = yaml.load(open(self.inpath, 'r'))
        options = data['plink_options']
        script_file = open(self.outpath, 'wb')
        lines = []
        # print(options)

        for opt_dict in options:
            if opt_dict['opt_type'] == 'OPT_BOOL' and str(opt_dict['opt_value']).lower() == "true":
                line = "--%s %s \n" % (opt_dict['opt_key'], '')
                lines.append(line)
            else:
                line = "--%s %s \n" % (opt_dict['opt_key'], opt_dict['opt_value'])
                lines.append(line)
            script_file.write(line)

        # print("Script Text: %s \n" % lines)

        script_file.close()

        # print("Script Path: %s \n" % self.outpath)

        return luigi.LocalTarget(self.outpath)


class PlinkCommand(luigi.Task):
    """Executes a PLINK command line job using a preconfigured script."""
    priority = 600
    jobid = luigi.Parameter()
    cmdtype = luigi.Parameter(default='demo_basic_qa')
    plink_exe = luigi.Parameter(default='plink1.9')
    cmd = []
    resultdir = luigi.Parameter(default=os.path.abspath('data/tmp'))
    templatepath = luigi.Parameter(default=os.path.abspath('static/script_templates/demo_basic_qa.yaml'))
    script_name = ''
    script_path = ''

    def requires(self):
        # script_name = "%s_%s.txt" % (str(self.jobid), str(self.cmd_type))
        # self.script_path = os.path.join(os.path.abspath('data/tmp/'), script_name)
        return SetupJob(jobid=self.jobid), PlinkScriptBuilder(jobid=self.jobid, inpath=str(self.templatepath))

    def run(self):
        # print("(run) script_path: %s \n" % str(self.script_path))
        # script_name = "%s_%s.txt" % (str(self.jobid), str(self.cmd_type))
        # self.script_path = os.path.join(os.path.abspath('data/tmp/'), script_name)
        self.__plink_call__(script_path=str(self.input()[1].fn))

    def output(self):
        output_path = os.path.join(self.resultdir, self.jobid)

        if not os.path.exists(os.path.dirname(output_path)):
            try:
                os.makedirs(os.path.dirname(output_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        return luigi.LocalTarget(path=output_path)

    def __plink_call__(self, script_path):
        """Executes the configured PLINK call as a subprocess."""
        # working_dir = os.path.abspath(os.getcwd())
        call_cmd = [str(self.plink_exe), '--script', str(script_path)]
        # print("call_cmd: %s \n" % call_cmd)
        process = subprocess.Popen(call_cmd, stdout=subprocess.PIPE)
        output = process.communicate()[0]
        process.wait()
        print("\n\nPlink Call Output:\n%s\n\n" % output)


class SetupJob(luigi.ExternalTask):
    priority = 1000
    jobid = luigi.Parameter()

    output_file = None

    def output(self):
        job = Job(job_id=self.jobid)
        # print(job.path_map.dir_dict)
        self.output_file = os.path.join(job.path_map.tmp_dir, 'dir_dict.yaml')
        for path in job.path_map.dir_dict.itervalues():
            utils.check_dir(path=path)
            # print(path)

        yaml.dump(data=job.path_map.dir_dict, stream=open(self.output_file, 'w'))

        return luigi.LocalTarget(path=self.output_file)
