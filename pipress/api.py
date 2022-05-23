import requests
import os
import json
from pipress import core


def sync(conf):
    data = api(conf, f"/device?mac={core.mac()}")

    local_temp_dir = core.check_dir(
        f"{core.root_dir}/{conf['storage']['local_temp_dir']}")

    if core.device == 'pi':
        web_media_dir = f"{conf['storage']['web_media_dir']}"
    else:
        web_media_dir = local_temp_dir

    if isinstance(data, dict) and 'status' in data and data['status'] == True and 'layout' in data and isinstance(data['layout'], dict):

        if 'data' in data['layout'] and isinstance(data['layout'], dict) and 'lang' in data:

            core.file_save(
                f"{core.root_dir}/json/device.json", json.dumps(data))

            if 'media' in data['layout']['data'] and isinstance(data['layout']['data']['media'], dict):

                filter_media(
                    web_media_dir, data['layout']['data']['media'])

                # core.refresh_browser()


def filter_media(web_media_dir, remote):

    for item in os.listdir(f"{web_media_dir}"):

        file_basename = os.path.basename(item)
        if os.path.isfile(f"{web_media_dir}/{file_basename}"):

            local_size = os.path.getsize(f"{web_media_dir}/{item}")

            if file_basename not in remote['files']:
                print(f"Remove {item} from local, not used anymore")
                os.remove(f"{web_media_dir}/{item}")
            else:

                if file_basename in remote['files'] and local_size != remote['files'][item]['size']:
                    print(
                        f"Remove {item} from local {remote['files'][item]['size']} == {local_size}, bad size")
                    os.remove(f"{web_media_dir}/{item}")

                if file_basename in remote['files'] and local_size == remote['files'][item]['size']:
                    print(
                        f"Remove {item} from remote, same file {remote['files'][item]['size']} == {local_size}, same size")
                    remote['files'].pop(item)

    download_new_media(web_media_dir, remote)


def download_new_media(web_media_dir, remote):

    for remote_file, data in remote['files'].items():

        print(f"Download {remote['url']}/{data['basename']} from API")
        core.download_file(
            f"{remote['url']}/{data['basename']}", f"{web_media_dir}/{data['basename']}")


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