"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the presence api
"""
import sanic
from .slug import sac_code
from .version import affiliate_version

affiliate = sanic.Blueprint.group(sac_code, affiliate_version, url_prefix="/affiliate")