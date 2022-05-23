import json

def app_config():

    with open(f"json/config.json") as config:
        data = json.load(config)

        return data


def configure():
    return app_config()

