# @Time    : 2023/8/15 09:51
# @Author  : Lan
# @File    : settings.py
# @Software: PyCharm
from pathlib import Path
import json, os

BASE_DIR = Path(__file__).resolve().parent.parent
data_root = BASE_DIR / "data"
mysql_url = os.getenv('MYSQL_URL')

if not data_root.exists():
    data_root.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG = {
    "file_storage": "webdav",
    "storage_path": "",
    "name": "FileCodeBox",
    "description": "Sending files like delivering packages",
    "notify_title": "Note",
    "notify_content": "Welcome to DPFileBox，open-sourced on <a href=\"https://github.com/DiamondPie/FileCodeBox\" target=\"_blank\">Github</a>",
    "page_explain": "",
    "keywords": "FileCodeBox, file cabinet, password delivery box, anonymous password sharing text, text",
    "s3_access_key_id": "",
    "s3_secret_access_key": "",
    "s3_bucket_name": "",
    "s3_endpoint_url": "",
    "s3_region_name": "auto",
    "s3_signature_version": "s3v2",
    "s3_hostname": "",
    "s3_proxy": 0,
    "max_save_seconds": 0,
    "aws_session_token": "",
    "onedrive_domain": "",
    "onedrive_client_id": "",
    "onedrive_username": "",
    "onedrive_password": "",
    "onedrive_root_path": "filebox_storage",
    "onedrive_proxy": 0,
    "webdav_hostname": "",
    "webdav_root_path": "filebox_storage",
    "webdav_proxy": 0,
    "admin_token": os.getenv('ADMIN_TOKEN'),
    "openUpload": 1,
    "uploadSize": 20971520,
    "expireStyle": ["day", "hour", "minute", "count"],
    "uploadMinute": 1,
    "enableChunk": 0,
    "webdav_url": "https://zeze.teracloud.jp/dav/",
    "webdav_password": os.getenv('WEBDAV_PASSWORD', ''),
    "webdav_username": "DiamondPie",
    "opacity": 0.9,
    "background": "",
    "uploadCount": 10,
    "themesChoices": [
        {
            "name": "2023",
            "key": "themes/2023",
            "author": "Lan",
            "version": "1.0"
        },
        {
            "name": "2024",
            "key": "themes/2024",
            "author": "Lan",
            "version": "1.0"
        }
    ],
    "themesSelect": "themes/2024",
    "errorMinute": 1,
    "errorCount": 1,
    "port": 12345,
    "showAdminAddr": 0,
    "robotsText": "User-agent: *\nDisallow: /"
}

def load_secrets(file_name):
    print("尝试读取配置文件...")
    try:
        with open(f'/etc/secrets/{file_name}', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print('未找到配置文件，使用默认设置')
        return {}

class Settings:
    def __init__(self, defaults=None):
        self.default_config = load_secrets('settings.json') or defaults or {}
        self.user_config = {}

    def __getattr__(self, attr):
        if attr in self.user_config:
            return self.user_config[attr]
        if attr in self.default_config:
            return self.default_config[attr]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{attr}'"
        )

    def __setattr__(self, key, value):
        if key in ["default_config", "user_config"]:
            super().__setattr__(key, value)
        else:
            self.user_config[key] = value

    def items(self):
        return {**self.default_config, **self.user_config}.items()


settings = Settings(DEFAULT_CONFIG)
