import requests
import xmltodict


class NextCloud:
    def __init__(self, nextcloud_url, user, password):
        self.base_url = nextcloud_url + "/remote.php/webdav/"
        self.user = user
        self.password = password
        self.webdav_options = """<?xml version="1.0" encoding="UTF-8"?>
            <d:propfind xmlns:d="DAV:">
                <d:prop xmlns:oc="http://owncloud.org/ns">
                    <d:getlastmodified/>
                    <d:getcontenttype/>
                    <oc:fileid/>
                </d:prop>
            </d:propfind>"""

    def list_dir(self, dir_path):
        dir_content = []
        get_contents = requests.request(
            "PROPFIND",
            self.base_url + dir_path,
            auth=(self.user, self.password),
            data=self.webdav_options,
        )

        xml_dict = xmltodict.parse(get_contents.text, dict_constructor=dict)

        for response in xml_dict["d:multistatus"]["d:response"]:
            filename = response["d:href"].replace("/remote.php/webdav/", "")
            dir_content.append(self.base_url + filename)
        return dir_content

    def get_file(self, file_path):
        get_file = requests.request(
            "GET", file_path, auth=(self.user, self.password), data=self.webdav_options
        )

        if get_file.status_code == 200:
            return get_file.content
        else:
            raise Exception("response status code: {}".format(get_file.status_code))
