"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2023 by Alex Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the [TBD] license.

Handles the chunkv3 manifest cdn downloads
"""
import aiofiles
import sanic

from utils.sanic_gzip import Compress

compress = Compress()
chunk_manifest = sanic.Blueprint("cdn_chunkv3_manifest")


# undocumented
@chunk_manifest.route(
    r"/<environment:(WorldExplorers\w*)>/<changelist:(CL_\d*)>/<platform>/<file:(WorldExplorers_pakchunk\d*CL_\d*\.manifest)>",
    methods=["GET"])
@compress.compress()
async def chunk_manifest_request(request: sanic.request.Request, environment: str, changelist: str, platform: str,
                                 file: str) -> sanic.response.HTTPResponse:
    """
    Handles the chunkv3 individual pak manifest request
    :param request: The request object
    :param environment: The environment (WorldExplorersLive/WorldExplorersDevTesting/etc)
    :param changelist: The changelist (CL_1234567)
    :param platform: The platform (WindowsNoEditor/Android_ETC2/Android_ASTC/etc)
    :param file: The manifest file to download (WorldExplorers_pakchunk1CL_1234567.manifest)
    :return: The response object (204)
    """
    try:
        async with aiofiles.open(f"res/wex/api/game/v2/manifests/{changelist}/{platform}/{file}", "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise sanic.exceptions.FileNotFound("Chunk manifest not found")


# undocumented
@chunk_manifest.route(
    r"/<environment:(WorldExplorers\w*)>/<changelist:(CL_\d*)>/<platform>/ChunksV3/<DataGroupList:(\d{2})>/<ChunkHashGUID:([0-9A-F]*_[0-9A-F]*\.chunk)>",
    methods=["GET"])
@compress.compress()
async def chunk_manifest_serve_chunks(request: sanic.request.Request, environment: str, changelist: str, platform: str,
                                      DataGroupList: str, ChunkHashGUID: str) -> sanic.response.HTTPResponse:
    """
    Handles the chunked cloudv3 downloads
    :param request: The request object
    :param environment: The environment (WorldExplorersLive/WorldExplorersDevTesting/etc)
    :param changelist: The changelist (CL_1234567)
    :param platform: The platform (WindowsNoEditor/Android_ETC2/Android_ASTC/etc)
    :param DataGroupList: The datagrouplist (43)
    :param ChunkHashGUID: The chunk hash guid (34254574B8C46AC9_DF511A404ABE748CE527B6A264B5389A.chunk); theres a more specific regex i could write for this but im not bothered
    :return: The response object (204)
    """
    try:
        async with aiofiles.open(
                f"D:/Battle Breakers/ChunkV3/{changelist}/{platform}/ChunksV3/{DataGroupList}/{ChunkHashGUID}",
                "rb") as file:
            return sanic.response.raw(await file.read(), content_type="application/octet-stream")
    except:
        raise sanic.exceptions.FileNotFound("chunk was not found")