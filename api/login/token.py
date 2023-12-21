"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the login flow
"""
import os
import re

import sanic

from utils.utils import authorized as auth, generate_authorisation_eg1, bcrypt_hash, create_account, bcrypt_check

from utils.sanic_gzip import Compress

compress = Compress()
login_token = sanic.Blueprint("login_token")


# undocumented
@login_token.route("/id/login/token", methods=["POST"])
@auth(allow_basic=True)
@compress.compress()
async def login_token_route(request: sanic.request.Request) -> sanic.response.JSONResponse:
    """
    Authenticate a mobile user logging in / signing up and return a token
    :param request: The request object
    :return: The response object
    """
    # logging in
    if request.headers.get("X-Request-Source-Form") == "login-form":
        username = request.json.get("username")[:32]
        password = request.json.get("password")
        if len(username) > 24:
            username = username.lower()
            if not re.match(r"^[a-f0-9]{32}$", username):
                raise sanic.exceptions.InvalidUsage("Invalid username",
                                                    context={"errorMessage": "This account ID is invalid"})
            else:
                account_data: dict = await request.app.ctx.database["accounts"].find_one({"_id": username}, {
                    "_id": 0,
                    "displayName": 1,
                    "extra.pwhash": 1
                })
                if account_data is None:
                    raise sanic.exceptions.InvalidUsage("Invalid username", context={
                        "errorMessage": "Your account ID doesn't exist...\nAlready have an account to import? Contact "
                                        "us on Discord.\nTrying to create an account? Sign up instead."})
                else:
                    if account_data["extra"]["pwhash"] != password:
                        raise sanic.exceptions.Unauthorized("Invalid password", context={
                            "errorMessage": "The password you entered is incorrect"})
                    else:
                        return sanic.response.json(
                            {"username": account_data["displayName"],
                             "authorisationCode": await generate_authorisation_eg1(username,
                                                                                   account_data[
                                                                                       "displayName"]),
                             "id": username, "heading": "Complete Login"
                             }
                        )
        elif len(username) < 3:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Your username is too short"})
        elif len(username) > 32:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Username/Account ID too long"})
        else:
            # TODO: support email and displayname login
            account_data: dict = await request.app.ctx.database["accounts"].find_one(
                {"_id": username.split("@")[0].strip()}, {
                    "displayName": 1,
                    "extra.pwhash": 1
                })
            if account_data is None:
                raise sanic.exceptions.InvalidUsage("Invalid username", context={
                    "errorMessage": "Your username doesn't exist...\nAlready have an account to import? Contact us on "
                                    "Discord.\nTrying to create an account? Sign up instead."})
            else:
                if not await bcrypt_check(password, account_data["extra"]["pwhash"].encode()):
                    raise sanic.exceptions.Unauthorized("Invalid password", context={
                        "errorMessage": "The password you entered is incorrect"})
                else:
                    return sanic.response.json(
                        {"username": account_data["displayName"],
                         "authorisationCode": await generate_authorisation_eg1(account_data["_id"],
                                                                               account_data["displayName"]),
                         "id": account_data["_id"], "heading": "Complete Login"
                         }
                    )
    elif request.headers.get("X-Request-Source-Form") == "signup-form":
        username = request.json.get("username")[:32]
        password = request.json.get("password")
        if len(username) < 3:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Your username is too short"})
        elif len(username) > 24:
            raise sanic.exceptions.InvalidUsage("Invalid username", context={
                "errorMessage": "Username too long"})
        elif len(str(password)) < 4:
            raise sanic.exceptions.InvalidUsage("Invalid password", context={
                "errorMessage": "Your password is too short"})
        elif len(str(password)) > 32:
            raise sanic.exceptions.InvalidUsage("Invalid password", context={
                "errorMessage": "Your password is too long"})
        else:
            # TODO: implement better signup system
            account_data: dict = await request.app.ctx.database["accounts"].find_one(
                {"_id": username.split("@")[0].strip()}, {
                    "displayName": 1,
                    "extra.pwhash": 1
                })
            if account_data is None:
                account_id = await create_account(request.app.ctx.database, username, await bcrypt_hash(password),
                                                  calendar=request.app.ctx.calendar)
                return sanic.response.json(
                    {"username": username,
                     "authorisationCode": await generate_authorisation_eg1(account_id,
                                                                           username),
                     "id": account_id, "heading": "Complete Sign Up"
                     }
                )
            else:
                if not await bcrypt_check(password, account_data["extra"]["pwhash"].encode()):
                    raise sanic.exceptions.Unauthorized("Invalid password", context={
                        "errorMessage": "Your account already exists. The password you entered is incorrect."})
                else:
                    return sanic.response.json(
                        {"username": account_data["displayName"],
                         "authorisationCode": await generate_authorisation_eg1(account_data["_id"],
                                                                               account_data["displayName"]),
                         "id": account_data["_id"], "heading": "Complete Login"
                         }
                    )
    else:
        raise sanic.exceptions.InvalidUsage("Invalid X-Request-Source-Form header")