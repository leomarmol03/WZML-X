from asyncio import sleep

from json import dumps
from random import randint
from re import match
from shutil import which

from aiofiles import open as aiopen
from aiofiles.os import listdir, makedirs, path, rename
from aioshutil import rmtree

from myjd import MyJdApi

from .. import JDOWNLOADER_DIR, LOGGER
from .cpu import service_cores
from ..helper.ext_utils.bot_utils import cmd_exec, new_task
from .config_manager import BinConfig, Config
from .tg_client import TgClient

_MAX_BOOT_RETRIES = 5
_BOOT_RETRY_DELAY = 10


class JDownloader(MyJdApi):
    def __init__(self):
        super().__init__()
        self._username = ""
        self._password = ""
        self._device_name = ""
        self.is_connected = False
        self.error = "JDownloader Credentials not provided!"

    async def _write_config(self, path, data):
        async with aiopen(path, "w") as f:
            await f.write(dumps(data))

    @new_task
    async def boot(self, _retries=0):
        await cmd_exec(["pkill", "-9", "-f", "java"])
        if not Config.JD_EMAIL or not Config.JD_PASS:
            self.is_connected = False
            self.error = "JDownloader Credentials not provided!"
            return
        self.error = "Connecting... Try again after couple of seconds"
        self._device_name = f"{randint(0, 1000)}@{TgClient.BNAME}"
        if await path.exists(f"{JDOWNLOADER_DIR}/logs"):
            LOGGER.info(
                "Starting JDownloader... This might take up to 10 sec and might restart once if update available!"
            )
        else:
            LOGGER.info(
                "Starting JDownloader... This might take up to 8 sec and might restart once after build!"
            )
        jdata = {
            "autoconnectenabledv2": True,
            "password": Config.JD_PASS,
            "devicename": f"{self._device_name}",
            "email": Config.JD_EMAIL,
        }
        remote_data = {
            "localapiserverheaderaccesscontrollalloworigin": "",
            "deprecatedapiport": 3128,
            "localapiserverheaderxcontenttypeoptions": "nosniff",
            "localapiserverheaderxframeoptions": "DENY",
            "externinterfaceenabled": False,
            "deprecatedapilocalhostonly": True,
            "localapiserverheaderreferrerpolicy": "no-referrer",
            "deprecatedapienabled": True,
            "localapiserverheadercontentsecuritypolicy": "default-src 'self'",
            "jdanywhereapienabled": False,
            "externinterfacelocalhostonly": True,
            "localapiserverheaderxxssprotection": "1; mode=block",
        }
        config_dir = f"{JDOWNLOADER_DIR}/cfg"
        await makedirs(config_dir, exist_ok=True)
        await self._write_config(
            f"{config_dir}/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            jdata,
        )
        await self._write_config(
            f"{config_dir}/org.jdownloader.api.RemoteAPIConfig.json",
            remote_data,
        )
        ffmpeg_data = {
            "binarypath": which(BinConfig.FFMPEG_NAME) or BinConfig.FFMPEG_NAME,
        }
        await self._write_config(
            f"{config_dir}/org.jdownloader.controlling.ffmpeg.FFmpegSetup.json",
            ffmpeg_data,
        )
        jar_path = f"{JDOWNLOADER_DIR}/JDownloader.jar"
        if not await path.exists(jar_path):
            pattern = r"JDownloader\.jar\.backup.\d$"
            for filename in await listdir(JDOWNLOADER_DIR):
                if match(pattern, filename):
                    await rename(f"{JDOWNLOADER_DIR}/{filename}", jar_path)
                    break
            await rmtree(f"{JDOWNLOADER_DIR}/update", ignore_errors=True)
            await rmtree(f"{JDOWNLOADER_DIR}/tmp", ignore_errors=True)
        svc_cores = service_cores()
        cmd = [
            "cpulimit",
            "-l",
            str(Config.CPU_LIMIT),
            "--",
            "java",
            "-Xms256m",
            "-Xmx500m",
            "-Dsun.jnu.encoding=UTF-8",
            "-Dfile.encoding=UTF-8",
            "-Djava.awt.headless=true",
            "-jar",
            jar_path,
        ]
        if svc_cores:
            cmd = ["taskset", "-c", svc_cores, *cmd]
        self.is_connected = True
        _, __, code = await cmd_exec(cmd)
        self.is_connected = False
        if code != -9 and _retries < _MAX_BOOT_RETRIES:
            LOGGER.warning(
                f"JDownloader exited with code {code}, retrying in {_BOOT_RETRY_DELAY}s ({_retries + 1}/{_MAX_BOOT_RETRIES})"
            )
            await sleep(_BOOT_RETRY_DELAY)
            await self.boot(_retries + 1)


jdownloader = JDownloader()
