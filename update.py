import os
import skytap
import sys
from update_scripts import update_write


def start(args):
    """Redirect to update function based on args."""

    envs = skytap.Environments()

    try:
        import yaml
    except ImportError:
        sys.stderr.write("You do not have the 'yaml' module installed. "
                         "Please see http://pyyaml.org/wiki/PyYAMLDocumentation"
                         " for more information.")
        exit(1)

    try:
        f = open("config.yml")
        config_data = yaml.safe_load(f)
        f.close()
    except IOError:
        sys.stderr.write("There is no config.yml in the directory. Create one "
                         "and then try again.\nFor reference, check config_"
                         "template.yml and follow the listed guidelines.\n")
        exit(1)

    # Go to specific functions based on passed arguments
    # Ex. "python update.py write" or "python update.py services"
    if (args[1] == "write"):
        os.system("clear")
        if len(args) < 3:
            print ("Writing wiki pages.")
            update_write.start(envs, config_data)
        else:
            print ("Writing wiki pages for all environments with \""
                   "" + args[2] + "\" in the name.")
            update_write.start(envs, config_data, args[2].strip())
    else:
        print ("Command not recognized.")

    print ("\n\nJob\'s done.\n")


if __name__ == '__main__':
    start(sys.argv)
