from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FiguresMetrics")


@_attrs_define
class FiguresMetrics:
    """A figure the network reported, or null. Null never means zero.

    Attributes:
        views (float | None):
        likes (float | None):
        comments (float | None):
        shares (float | None):
        impressions (float | None):
        reach (float | None):
        saves (float | None):
        clicks (float | None):
        watch_time_seconds (float | None):
    """

    views: float | None
    likes: float | None
    comments: float | None
    shares: float | None
    impressions: float | None
    reach: float | None
    saves: float | None
    clicks: float | None
    watch_time_seconds: float | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        views: float | None
        views = self.views

        likes: float | None
        likes = self.likes

        comments: float | None
        comments = self.comments

        shares: float | None
        shares = self.shares

        impressions: float | None
        impressions = self.impressions

        reach: float | None
        reach = self.reach

        saves: float | None
        saves = self.saves

        clicks: float | None
        clicks = self.clicks

        watch_time_seconds: float | None
        watch_time_seconds = self.watch_time_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "views": views,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "impressions": impressions,
                "reach": reach,
                "saves": saves,
                "clicks": clicks,
                "watch_time_seconds": watch_time_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_views(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        views = _parse_views(d.pop("views"))

        def _parse_likes(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        likes = _parse_likes(d.pop("likes"))

        def _parse_comments(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        comments = _parse_comments(d.pop("comments"))

        def _parse_shares(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        shares = _parse_shares(d.pop("shares"))

        def _parse_impressions(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        impressions = _parse_impressions(d.pop("impressions"))

        def _parse_reach(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        reach = _parse_reach(d.pop("reach"))

        def _parse_saves(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        saves = _parse_saves(d.pop("saves"))

        def _parse_clicks(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        clicks = _parse_clicks(d.pop("clicks"))

        def _parse_watch_time_seconds(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        watch_time_seconds = _parse_watch_time_seconds(d.pop("watch_time_seconds"))

        figures_metrics = cls(
            views=views,
            likes=likes,
            comments=comments,
            shares=shares,
            impressions=impressions,
            reach=reach,
            saves=saves,
            clicks=clicks,
            watch_time_seconds=watch_time_seconds,
        )

        figures_metrics.additional_properties = d
        return figures_metrics

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
