from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.platform import Platform, check_platform
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facebook_options import FacebookOptions
    from ..models.instagram_options import InstagramOptions
    from ..models.linked_in_options import LinkedInOptions
    from ..models.pinterest_options import PinterestOptions
    from ..models.post_content import PostContent
    from ..models.skool_options import SkoolOptions
    from ..models.threads_options import ThreadsOptions
    from ..models.tik_tok_options import TikTokOptions
    from ..models.x_options import XOptions
    from ..models.you_tube_options import YouTubeOptions


T = TypeVar("T", bound="Post")


@_attrs_define
class Post:
    """One flat post. Only the option block of post.platform is read (another network's block is named in warnings). Per
    network: Pinterest needs pinterest.boardId (400 pinterest_board_required); Skool needs skool.group and skool.title;
    media is required except for text posts on X, LinkedIn, Threads, Skool and Facebook (400 otherwise). dryRun may also
    be sent inside post (and as dry_run).

        Attributes:
            account_id (str): The profile: its UUID, "@name" or the bare name, as on the Connections page (GET /accounts
                lists them). Capital letters do not matter; two profiles whose names differ only by capital letters are 400
                profile_name_ambiguous (send the exact name or the id). A profile that is not yours is 403 account_not_found
                (404 api_error on the older address).
            platform (Platform):
            scheduled_for (float | None | str | Unset): When to publish. An ISO 8601 time WITH a time zone
                ("2026-09-30T10:00:00Z", "2026-09-30T12:00:00+02:00"), a date with the month as a word and a zone ("Wed, 30 Sep
                2026 10:00:00 GMT"), or a Unix time in seconds or milliseconds (from 1e11). Absent, null, "" or "now", a past
                time, or one within 60 seconds: published now. More than 60 seconds and up to 365 days ahead: scheduled (202
                scheduled; at most 500 posts waiting per account). Otherwise 400 scheduled_for_invalid with error.reason
                no_time_zone (even a past time without a zone), unreadable (not a date and time, a date written with numbers
                only such as 01/10/2026 included) or too_far_ahead.
            content (PostContent | Unset):
            tiktok (TikTokOptions | Unset):
            instagram (InstagramOptions | Unset):
            facebook (FacebookOptions | Unset):
            youtube (YouTubeOptions | Unset):
            x (XOptions | Unset):
            linkedin (LinkedInOptions | Unset):
            pinterest (PinterestOptions | Unset):
            threads (ThreadsOptions | Unset):
            skool (SkoolOptions | Unset):
    """

    account_id: str
    platform: Platform
    scheduled_for: float | None | str | Unset = UNSET
    content: PostContent | Unset = UNSET
    tiktok: TikTokOptions | Unset = UNSET
    instagram: InstagramOptions | Unset = UNSET
    facebook: FacebookOptions | Unset = UNSET
    youtube: YouTubeOptions | Unset = UNSET
    x: XOptions | Unset = UNSET
    linkedin: LinkedInOptions | Unset = UNSET
    pinterest: PinterestOptions | Unset = UNSET
    threads: ThreadsOptions | Unset = UNSET
    skool: SkoolOptions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = self.account_id

        platform: str = self.platform

        scheduled_for: float | None | str | Unset
        if isinstance(self.scheduled_for, Unset):
            scheduled_for = UNSET
        else:
            scheduled_for = self.scheduled_for

        content: dict[str, Any] | Unset = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_dict()

        tiktok: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tiktok, Unset):
            tiktok = self.tiktok.to_dict()

        instagram: dict[str, Any] | Unset = UNSET
        if not isinstance(self.instagram, Unset):
            instagram = self.instagram.to_dict()

        facebook: dict[str, Any] | Unset = UNSET
        if not isinstance(self.facebook, Unset):
            facebook = self.facebook.to_dict()

        youtube: dict[str, Any] | Unset = UNSET
        if not isinstance(self.youtube, Unset):
            youtube = self.youtube.to_dict()

        x: dict[str, Any] | Unset = UNSET
        if not isinstance(self.x, Unset):
            x = self.x.to_dict()

        linkedin: dict[str, Any] | Unset = UNSET
        if not isinstance(self.linkedin, Unset):
            linkedin = self.linkedin.to_dict()

        pinterest: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pinterest, Unset):
            pinterest = self.pinterest.to_dict()

        threads: dict[str, Any] | Unset = UNSET
        if not isinstance(self.threads, Unset):
            threads = self.threads.to_dict()

        skool: dict[str, Any] | Unset = UNSET
        if not isinstance(self.skool, Unset):
            skool = self.skool.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "platform": platform,
            }
        )
        if scheduled_for is not UNSET:
            field_dict["scheduledFor"] = scheduled_for
        if content is not UNSET:
            field_dict["content"] = content
        if tiktok is not UNSET:
            field_dict["tiktok"] = tiktok
        if instagram is not UNSET:
            field_dict["instagram"] = instagram
        if facebook is not UNSET:
            field_dict["facebook"] = facebook
        if youtube is not UNSET:
            field_dict["youtube"] = youtube
        if x is not UNSET:
            field_dict["x"] = x
        if linkedin is not UNSET:
            field_dict["linkedin"] = linkedin
        if pinterest is not UNSET:
            field_dict["pinterest"] = pinterest
        if threads is not UNSET:
            field_dict["threads"] = threads
        if skool is not UNSET:
            field_dict["skool"] = skool

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.facebook_options import FacebookOptions
        from ..models.instagram_options import InstagramOptions
        from ..models.linked_in_options import LinkedInOptions
        from ..models.pinterest_options import PinterestOptions
        from ..models.post_content import PostContent
        from ..models.skool_options import SkoolOptions
        from ..models.threads_options import ThreadsOptions
        from ..models.tik_tok_options import TikTokOptions
        from ..models.x_options import XOptions
        from ..models.you_tube_options import YouTubeOptions

        d = dict(src_dict)
        account_id = d.pop("accountId")

        platform = check_platform(d.pop("platform"))

        def _parse_scheduled_for(data: object) -> float | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | str | Unset, data)

        scheduled_for = _parse_scheduled_for(d.pop("scheduledFor", UNSET))

        _content = d.pop("content", UNSET)
        content: PostContent | Unset
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = PostContent.from_dict(_content)

        _tiktok = d.pop("tiktok", UNSET)
        tiktok: TikTokOptions | Unset
        if isinstance(_tiktok, Unset):
            tiktok = UNSET
        else:
            tiktok = TikTokOptions.from_dict(_tiktok)

        _instagram = d.pop("instagram", UNSET)
        instagram: InstagramOptions | Unset
        if isinstance(_instagram, Unset):
            instagram = UNSET
        else:
            instagram = InstagramOptions.from_dict(_instagram)

        _facebook = d.pop("facebook", UNSET)
        facebook: FacebookOptions | Unset
        if isinstance(_facebook, Unset):
            facebook = UNSET
        else:
            facebook = FacebookOptions.from_dict(_facebook)

        _youtube = d.pop("youtube", UNSET)
        youtube: YouTubeOptions | Unset
        if isinstance(_youtube, Unset):
            youtube = UNSET
        else:
            youtube = YouTubeOptions.from_dict(_youtube)

        _x = d.pop("x", UNSET)
        x: XOptions | Unset
        if isinstance(_x, Unset):
            x = UNSET
        else:
            x = XOptions.from_dict(_x)

        _linkedin = d.pop("linkedin", UNSET)
        linkedin: LinkedInOptions | Unset
        if isinstance(_linkedin, Unset):
            linkedin = UNSET
        else:
            linkedin = LinkedInOptions.from_dict(_linkedin)

        _pinterest = d.pop("pinterest", UNSET)
        pinterest: PinterestOptions | Unset
        if isinstance(_pinterest, Unset):
            pinterest = UNSET
        else:
            pinterest = PinterestOptions.from_dict(_pinterest)

        _threads = d.pop("threads", UNSET)
        threads: ThreadsOptions | Unset
        if isinstance(_threads, Unset):
            threads = UNSET
        else:
            threads = ThreadsOptions.from_dict(_threads)

        _skool = d.pop("skool", UNSET)
        skool: SkoolOptions | Unset
        if isinstance(_skool, Unset):
            skool = UNSET
        else:
            skool = SkoolOptions.from_dict(_skool)

        post = cls(
            account_id=account_id,
            platform=platform,
            scheduled_for=scheduled_for,
            content=content,
            tiktok=tiktok,
            instagram=instagram,
            facebook=facebook,
            youtube=youtube,
            x=x,
            linkedin=linkedin,
            pinterest=pinterest,
            threads=threads,
            skool=skool,
        )

        post.additional_properties = d
        return post

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
