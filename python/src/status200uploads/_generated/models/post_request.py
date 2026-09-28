from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post import Post


T = TypeVar("T", bound="PostRequest")


@_attrs_define
class PostRequest:
    """A field this API does not read never refuses a post: the answer names it in warnings.

    Attributes:
        post (Post): One flat post. Only the option block of post.platform is read (another network's block is named in
            warnings). Per network: Pinterest needs pinterest.boardId (400 pinterest_board_required); Skool needs
            skool.group and skool.title; media is required except for text posts on X, LinkedIn, Threads, Skool and Facebook
            (400 otherwise). dryRun may also be sent inside post (and as dry_run).
        dry_run (bool | Unset): true: check this post and send nothing (every check a publish makes; the answer is 200
            with dry_run true, and it is not counted in the key's request count). false or absent: publish. Also read as
            dry_run, and inside post; a dry run may send the post as validate instead of post. Any value but true or false
            (or true in one place and false in another) is 400 and nothing is published.
    """

    post: Post
    dry_run: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post = self.post.to_dict()

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "post": post,
            }
        )
        if dry_run is not UNSET:
            field_dict["dryRun"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.post import Post

        d = dict(src_dict)
        post = Post.from_dict(d.pop("post"))

        dry_run = d.pop("dryRun", UNSET)

        post_request = cls(
            post=post,
            dry_run=dry_run,
        )

        post_request.additional_properties = d
        return post_request

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
