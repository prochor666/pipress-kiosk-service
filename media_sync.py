from pipress import config, compat, core, api

conf = config.configure()

# If compat = False, break
compat.check_version()

api.sync(conf)

core.report()
