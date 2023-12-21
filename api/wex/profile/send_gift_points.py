"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles sending gifts.
"""

import sanic

from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_send_gift = sanic.Blueprint("wex_profile_send_gift")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/World%20Explorers%20Service/wex/api/game/v2/profile/accountId/QueryProfile(profile0).md
@wex_profile_send_gift.route("/<accountId>/SendGiftPoints", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def send_gift_points(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    Handles the send gift point request
    :param request: The request object
    :param accountId: The account id
    :return: The response object
    """
    return sanic.response.json({
        "profileRevision": 39840,
        "profileId": "profile0",
        "profileChangesBaseRevision": 39838,
        "profileChanges": [{
            "changeType": "statModified",
            "name": "activity",
            "value": {
                "a": {
                    "date": "2022-12-28T00:00:00.000Z",
                    "claimed": False,
                    "props": {
                        "BaseBonus": 10
                    }
                },
                "b": {
                    "date": "2022-12-27T00:00:00.000Z",
                    "claimed": True,
                    "props": {
                        "BaseBonus": 10,
                        "EnergySpent": 3
                    }
                },
                "standardGift": 10
            }
        }],
        "profileCommandRevision": 23699,
        "serverTime": "2022-12-28T11:37:06.741Z",
        "multiUpdate": [{
            "profileRevision": 9864,
            "profileId": "friends",
            "profileChangesBaseRevision": 9862,
            "profileChanges": [],
            "profileCommandRevision": 8247
        }],
        "responseVersion": 1
    })