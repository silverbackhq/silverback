"""
Upgrade Module
"""

# third-party
import requests

# local Django
from app.settings.info import RELEASES
from app.settings.info import VERSION
from app.settings.info import DOWNLOAD_URL


class Upgrade():

    def need_upgrade(self):
        latest = self.get_latest_version()
        current = self.get_current_version()

        latest_version = int(latest["version"].replace(".", ""))
        current_version = int(current["version"].replace(".", ""))

        return latest_version > current_version

    def get_latest_version(self):
        r = requests.get(RELEASES)

        if r.status_code == 200 and r.headers['content-type'].find("json"):
            result = r.json()
            if len(result) > 0 and "tag_name" in result[0] and "html_url" in result[0]:
                return {
                    "version": result[0]["tag_name"],
                    "download_url": result[0]["html_url"]
                }
            else:
                return {
                    "version": VERSION,
                    "download_url": DOWNLOAD_URL
                }

    def get_current_version(self):
        return {
            "version": VERSION,
            "download_url": DOWNLOAD_URL
        }
