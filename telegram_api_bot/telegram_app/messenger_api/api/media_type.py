"""
explanation of what MIME is for future:
MIME stands for "Multipurpose Internet Mail Extensions." It is a standard that was originally developed to enable
 the exchange of different kinds of data files, such as text, audio, video, images, and application programs,
 through Internet email. Over time, MIME has also become widely used in other contexts such as HTTP for the web.
"""


def get_content_type(content_type: str) -> str | None:
    """
    Maps a given MIME type to its corresponding content type accepted by the Telegram API.

    Args:
        content_type (str): The MIME type to be mapped.

    Returns:
        str: The corresponding content type accepted by the Telegram API, such as 'audio', 'document',
             'photo', 'video', 'animation', 'voice', or 'web_page'. Returns None if the MIME type
             does not match any known content type.

    The function checks the provided MIME type against predefined categories:
    - 'audio': Accepts 'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac'.
    - 'document': Accepts 'application/pdf', 'application/msword',
                  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                  'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                  'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'.
    - 'photo': Accepts 'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'.
    - 'video': Accepts 'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo', 'video/x-ms-wmv'.
    - 'animation': Accepts 'image/gif'.
    - 'voice': Accepts 'audio/ogg', 'audio/mpeg', 'audio/wav'.
    - 'web_page': Currently accepts no MIME types.

    Example:
        content_type = "audio/mpeg"
        result = get_content_type(content_type)
        # result will be 'audio'
    """
    content_type_to_mime_type = {
        "audio": ["audio/mpeg", "audio/wav", "audio/ogg", "audio/aac", "audio/mp3"],
        "document": ["application/pdf", "application/msword",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                     "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     "application/vnd.ms-powerpoint",
                     "application/vnd.openxmlformats-officedocument.presentationml.presentation"],
        "photo": ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/webp"],
        "video": ["video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo", "video/x-ms-wmv"],
        "animation": ["image/gif"],
        "web_page": []
    }

    for media_type, mime_types in content_type_to_mime_type.items():
        if content_type in mime_types:
            return media_type
    return None
