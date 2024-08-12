from fastapi import UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from typing import List, Dict, Tuple
import json
import logging
from .media_type import get_content_type
from fastapi.routing import APIRouter

# from config import get_bot_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# token = get_bot_token()
router = APIRouter(tags=["Telegram"])


@router.post('/send_message/{channel_name}', status_code=status.HTTP_200_OK,
             description="""
             This endpoint allows you to send media files to a specified Telegram channel or group. 
             Simply provide the channel name or chat ID after the slash (/) in the URL.
             Will add ai roast functionalities later on currently only messaging through the bot is possible
             """)
async def send_message(channel_name: str, token: str = Form(...), files: List[UploadFile] = File(None),
                       caption: str = Form(None)):
    """
    Sends a group of media files to a specified Telegram channel or group.

    This asynchronous function is designed to facilitate the sending of multiple media files to a Telegram channel or group
    using the Telegram API. It handles the processing of files, mapping their MIME types to the appropriate content types
    accepted by the Telegram API, and sends them as a media group with an optional caption.

    Args:
        channel_name (str): The name of the channel or group where the media files will be sent. This should be a string
                            representing the name of the channel or group.
        token (str): The bot token obtained from BotFather for authentication. This token is crucial for the API to
                     recognize the request as coming from an authorized bot.
        files (List[UploadFile]): A list of files to be uploaded. Each file should be an instance of UploadFile, which
                                  contains the file's content and metadata.
        caption (str, optional): An optional caption for the media files. If provided, this caption will be attached to
                                 the first media item in the group. Defaults to None.

    Returns:
        JSONResponse: A JSON response containing the result of the media upload operation. This response will include
                      details about the success or failure of the operation, as returned by the Telegram API.

    Raises:
        HTTPException:
            - 400 Bad Request: If the content type of any file is unsupported or if there is an error processing the files.
            - 500 Internal Server Error: If there is an unexpected error during the HTTP request to the Telegram API.

    Example:
        To use this endpoint, make a POST request to `/send_message/my_channel` with the following form data:
        - token: YOUR_BOT_TOKEN
        - files: [UploadFile("image.jpg", "image/jpeg"), UploadFile("video.mp4", "video/mp4")]
        - caption: "Check out these media files!"

        This will send the image and video files to the channel named "my_channel" with the provided caption.

    Note:
        This function relies on the `get_content_type` function to map MIME types to the content types accepted by the
        Telegram API. Ensure that this function is correctly implemented and available in the module.
    """


    url = f"https://api.telegram.org/bot{token}/sendMediaGroup"
    channel_id = f"@{channel_name}"
    media: list[dict[str, str]] = []
    file_data: dict[str, tuple[str | None, bytes, str | None]] = {}

    try:
        for idx, file in enumerate(files):
            content_type = file.content_type
            media_type = get_content_type(content_type)
            logger.info(f"   {media_type}")
            if not media_type:
                raise HTTPException(status_code=400, detail=f"Unsupported content type: {content_type}")

            file_content = await file.read()
            if not file_content:
                raise HTTPException(status_code=400, detail=f"File {file.filename} is empty")

            file_data[f"file{idx}"] = (file.filename, file_content, content_type)
            media.append({
                "type": media_type,
                "media": f"attach://file{idx}",
            })
    except Exception as e:
        logger.error(f"Error Processing files: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if caption and media:
        media[0]["caption"] = caption

    async with httpx.AsyncClient(timeout=None) as client:
        data = {
            'chat_id': channel_id,
            'media': json.dumps(media)
        }
        try:
            logger.info(f"Request payload: {json.dumps(data)}")
            logger.info(f"Number of files: {len(file_data)}")
            response = await client.post(url, data=data, files=file_data)
            response.raise_for_status()
            logger.info(response.text)
            return JSONResponse(content=response.json())
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTPStatusError: {e.response.status_code}")
            logger.error(f"Response headers: {e.response.headers}")
            logger.error(f"Response body: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            logger.error(f"Request error to Telegram API: {str(e)}")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
