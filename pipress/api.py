import requests
import os
import json
from pipress import core


def sync(conf):
    data = api(conf, f"/device?mac={core.mac()}")

    local_temp_dir = core.check_dir(
        f"{core.root_dir}/{conf['storage']['local_temp_dir']}")

    if core.device == 'pi':
        web_data_dir = f"{conf['storage']['web_data_dir_prod']}"
    else:
        web_data_dir = f"{conf['storage']['web_data_dir_dev']}"

    local_json_dir = core.check_dir(
        f"{web_data_dir}/json")

    core.check_dir(
        f"{web_data_dir}/media")

    if isinstance(data, dict) and 'status' in data and data['status'] == True and 'layout' in data and isinstance(data['layout'], dict):

        if 'data' in data['layout'] and isinstance(data['layout'], dict) and 'lang' in data:

            if 'media' in data['layout']['data'] and isinstance(data['layout']['data']['media'], dict):

                data['layout']['data']['media']['files'] = filter_media(
                    f"{web_data_dir}/media", data['layout']['data']['media'])

            core.file_save(
                f"{local_json_dir}/device.json", json.dumps(data))
            # core.refresh_browser()

    else:

        if os.path.isfile(f"{local_json_dir}/device.json"):

            os.remove(f"{local_json_dir}/device.json")


def filter_media(web_data_dir, remote):

    new_files = []

    for item in os.listdir(f"{web_data_dir}"):

        file_basename = os.path.basename(item)
        if os.path.isfile(f"{web_data_dir}/{file_basename}"):

            local_size = os.path.getsize(f"{web_data_dir}/{item}")

            #if file_basename not in remote['files']:
            search = search_file(file_basename, remote['files'])

            if search == -1:

                print(f"Remove {item}, not used anymore")
                os.remove(f"{web_data_dir}/{item}")
            else:

                if search > -1 and local_size != remote['files'][search]['size']:
                    print(
                        f"Remove {item}, size remote: {remote['files'][search]['size']}/local: {local_size} and download again, size changed")

                    os.remove(f"{web_data_dir}/{item}")
                    new_files.append(remote['files'][search])

                if search > -1 and local_size == remote['files'][search]['size']:
                    print(
                        f"No change on {item}, size remote: {remote['files'][search]['size']}/local: {local_size}, same file/size")
                    new_files.append(remote['files'][search])
                    remote['files'].pop(search)

    download_new_media(web_data_dir, remote)
    return new_files


def search_file(file, files):
    index = 0
    for item in files:

        if item["basename"] == file:
            return index
        index += 1

    return -1


def download_new_media(web_data_dir, remote):

    for data in remote['files']:

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