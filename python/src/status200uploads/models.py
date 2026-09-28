"""The API's request and answer objects, generated from its OpenAPI file (attrs classes with
to_dict() and from_dict()). Status200.publish() takes a Post or a PostRequest as well as a dict:

    from status200uploads.models import Post, PostContent, TikTokOptions

    post = Post(account_id="@myprofile", platform="tiktok",
                content=PostContent(text="New video", media_id=[file_id]),
                tiktok=TikTokOptions(privacy_level="SELF_ONLY"))

Field names are snake_case here and the API's spelling in to_dict() (accountId, mediaID ...).
"""

from ._generated.models import *
from ._generated.models import __all__  # noqa: F401
