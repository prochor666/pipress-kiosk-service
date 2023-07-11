from pipress import config, compat, core, api, commands
import json

conf = config.configure()

# If compat = False, break
compat.check_version()

# Sync data from API
remote_command = api.sync(conf)

# Run remote commands
commands.watch(remote_command)

# Report to API
report = core.report(conf)

dataPost = {
    'mac': core.mac(),
    'meta': {
        'os_stats': report,
    },
}

result = api.api_post(conf, '/api/v1/auth/pair', dataPost)
print(json.dumps(result, indent = 4))