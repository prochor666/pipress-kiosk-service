from pipress import core
import os


def watch(remote_command):

    script_to_run = f"/tmp/{os.path.basename(remote_command['command_script'])}"

    if isinstance(remote_command['command_script'], str) and len(remote_command['command_script']) > 0:

        if core.device == 'pi':

            core.file_download(
                remote_command['command_script'], script_to_run)

            print(f"Script {script_to_run} will run")

            core.os_command(f"dos2unix {script_to_run}")
            core.os_command(f"chmod +x {script_to_run}")
            core.os_command(script_to_run)

        if core.device == 'fake-pi':

            print(f"Script {script_to_run} will run (Linux only)")

