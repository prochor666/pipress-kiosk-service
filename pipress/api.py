import requests
import os
import json
from pipress import core


def sync(conf):
    data = api(conf, f"/device?mac={core.mac()}")

    local_temp_dir = core.check_dir(
        f"{core.root_dir}/{conf['storage']['local_temp_dir']}")

    if core.device == 'pi':
        web_data_dir = f"{conf['storage']['web_data_dir']}"
    else:
        web_data_dir = local_temp_dir

    local_json_dir = core.check_dir(
        f"{web_data_dir}/json")

    if isinstance(data, dict) and 'status' in data and data['status'] == True and 'layout' in data and isinstance(data['layout'], dict):

        if 'data' in data['layout'] and isinstance(data['layout'], dict) and 'lang' in data:

            core.file_save(
                f"{local_json_dir}/device.json", json.dumps(data))

            if 'media' in data['layout']['data'] and isinstance(data['layout']['data']['media'], dict):

                filter_media(
                    web_data_dir, data['layout']['data']['media'])

                # core.refresh_browser()


def filter_media(web_data_dir, remote):

    for item in os.listdir(f"{web_data_dir}"):

        file_basename = os.path.basename(item)
        if os.path.isfile(f"{web_data_dir}/{file_basename}"):

            local_size = os.path.getsize(f"{web_data_dir}/{item}")

            if file_basename not in remote['files']:
                print(f"Remove {item}, not used anymore")
                os.remove(f"{web_data_dir}/{item}")
            else:

                if file_basename in remote['files'] and local_size != remote['files'][item]['size']:
                    print(
                        f"Remove {item}, size remote: {remote['files'][item]['size']}/local: {local_size} and download again, size changed")
                    os.remove(f"{web_data_dir}/{item}")

                if file_basename in remote['files'] and local_size == remote['files'][item]['size']:
                    print(
                        f"No change on {item}, size remote: {remote['files'][item]['size']}/local: {local_size}, same file/size")
                    remote['files'].pop(item)

    download_new_media(web_data_dir, remote)


def download_new_media(web_data_dir, remote):

    for remote_file, data in remote['files'].items():

        print(f"Download new {data['basename']} from API")
        core.download_file(
            f"{remote['url']}/{data['basename']}", f"{web_data_dir}/{data['basename']}")


def api(conf, path):
    try:
        r = requests.get(
            f"{conf['api']['url']}{path}", {
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
        })
        j = r.json()
    except:
        j = {
            'status': False
        }
    finally:
        pass
    return j