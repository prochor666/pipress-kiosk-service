from pipress import config, compat, core, api, commands

conf = config.configure()

# If compat = False, break
compat.check_version()

# Sync data from API
remote_command = api.sync(conf)

# Run remote commands
commands.watch(remote_command)

# Report to API
core.report()
