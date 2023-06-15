"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the motd of old versions
"""

import sanic

from utils.sanic_gzip import Compress

compress = Compress()
wex_motd = sanic.Blueprint("wex_motd")


# undocumented
@wex_motd.route("/api/game/v2/motd", methods=['GET'])
@compress.compress()
async def motd(request: sanic.request.Request) -> sanic.response.HTTPResponse:
    """
    Handles the motd of old versions
    :param request: The request object
    :return: The response object
    """
    raise sanic.exceptions.SanicException("Not implemented", 501, quiet=True)