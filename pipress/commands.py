from pipress import core
import os


def watch(remote_command):

    script_to_run = f"/tmp/pipress-remote-command.sh"

    if isinstance(remote_command['command_script'], str) and len(remote_command['command_script']) > 0:

        if core.device == 'pi':

            core.file_download(
                remote_command['command_script'], script_to_run)

            print(f"Script {script_to_run} will run")

        if core.device == 'fake-pi':

            print(f"Script {script_to_run} will run Linux only")

