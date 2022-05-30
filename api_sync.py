from pipress import config, compat, core, api

conf = config.configure()

# If compat = False, break
compat.check_version()

commands = api.sync(conf)

core.report()

if len(commands) > 0:

    for command in commands:

        core.os_command(command)


