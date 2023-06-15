"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles deleting friend suggestions / unfriending friends
"""
import sanic

from utils.friend_system import PlayerFriends
from utils.utils import authorized as auth

from utils.sanic_gzip import Compress

compress = Compress()
wex_profile_delete_friend = sanic.Blueprint("wex_profile_delete_friend")


# https://github.com/dippyshere/battle-breakers-documentation/blob/main/docs/wex-public-service-live-prod.ol.epicgames.com/wex/api/game/v2/profile/ec0ebb7e56f6454e86c62299a7b32e21/AddEpicFriend.md
@wex_profile_delete_friend.route("/<accountId>/DeleteFriend", methods=["POST"])
@auth(strict=True)
@compress.compress()
async def delete_friend(request: sanic.request.Request, accountId: str) -> sanic.response.JSONResponse:
    """
    This endpoint is used to unfriend or get rid of a suggestion, and is the only friend endpoint called on old versions
    :param request: The request object
    :param accountId: The account id
    :return: The modified profile
    """
    if accountId not in request.app.ctx.friends:
        request.app.ctx.friends[accountId] = PlayerFriends(accountId)
    if isinstance(request.json.get("friendInstanceIds"), list):
        for friend_id in request.json.get("friendInstanceIds"):
            friend_acc_id = (await request.ctx.profile.get_item_by_guid(friend_id,
                                                                        request.ctx.profile_id)).get("attributes").get(
                "accountId")
            await request.app.ctx.friends[accountId].remove_friend(request, friend_acc_id)
            await request.ctx.profile.remove_item(friend_id, request.ctx.profile_id)
    else:
        friend_acc_id = (await request.ctx.profile.get_item_by_guid(request.json.get("friendInstanceId"),
                                                                    request.ctx.profile_id)).get(
            "attributes").get("accountId")
        await request.app.ctx.friends[accountId].remove_friend(request, friend_acc_id)
        await request.ctx.profile.remove_item(request.json.get("friendInstanceId"), request.ctx.profile_id)
    return sanic.response.json(
        await request.ctx.profile.construct_response(request.ctx.profile_id, request.ctx.rvn,
                                                     request.ctx.profile_revisions)
    )