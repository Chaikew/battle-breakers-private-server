"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the eula tracking
"""
import sanic
from .agreements import agreements
from .version import eulatracking_version

agreements = sanic.Blueprint.group(agreements, eulatracking_version, url_prefix="/eulatracking")