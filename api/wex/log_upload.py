"""
Handles the log uploader
"""

import sanic

wex_log = sanic.Blueprint("wex_log_upload")


# undocumented
@wex_log.route("/wex/api/feedback/log-upload/<file>", methods=["POST"])
async def logupload(request, file):
    """
    Handles the log upload request
    :param request: The request object
    :param file: The file name
    :return: The response object (204)
    """
    with open(f"res/wex/api/feedback/log-upload/{file}", "wb") as file:
        file.write(request.body)
    return sanic.response.empty()
