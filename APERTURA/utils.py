import os

__author__ = 'dgraham'


def create_plink_script(cmd_dict, script_dir, script_name, jobid):
    """Create a .txt file formatted for use as a PLINK script, writing the file to disk.

    :param cmd_dict: Dictionary containing PLINK command line arguments.
    :param script_dir: Target directory for script file output.
    :param script_name: Script file name without file extension. (.txt will be appended)
    :param jobid: UUID4 job id as a string.
    :return: String containing path of script file created.
    """
    script_fname = jobid  + '_' + script_name + '.txt'
    script_path = os.path.join(script_dir, script_fname)
    script_file = open(script_path, 'wb')
    lines = []

    for key, value in cmd_dict:
        line = "-- %s %s \n" % (key, value)
        lines.append(line)
        script_file.write(line)

    # print("Script Text: %s" % lines)

    script_file.close()

    # print("Script Path: %s" % script_path)
    return script_path


def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
