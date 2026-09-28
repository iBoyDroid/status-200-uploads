from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.figures_metrics import FiguresMetrics


T = TypeVar("T", bound="Figures")


@_attrs_define
class Figures:
    """
    Attributes:
        metrics (FiguresMetrics): A figure the network reported, or null. Null never means zero.
        not_reported (list[str]):
        engagement (float | None):
        polled_at (datetime.datetime | None):
        note (None | str):
    """

    metrics: FiguresMetrics
    not_reported: list[str]
    engagement: float | None
    polled_at: datetime.datetime | None
    note: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metrics = self.metrics.to_dict()

        not_reported = self.not_reported

        engagement: float | None
        engagement = self.engagement

        polled_at: None | str
        if isinstance(self.polled_at, datetime.datetime):
            polled_at = self.polled_at.isoformat()
        else:
            polled_at = self.polled_at

        note: None | str
        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metrics": metrics,
                "not_reported": not_reported,
                "engagement": engagement,
                "polled_at": polled_at,
                "note": note,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.figures_metrics import FiguresMetrics

        d = dict(src_dict)
        metrics = FiguresMetrics.from_dict(d.pop("metrics"))

        not_reported = cast(list[str], d.pop("not_reported"))

        def _parse_engagement(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        engagement = _parse_engagement(d.pop("engagement"))

        def _parse_polled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                polled_at_type_0 = datetime.datetime.fromisoformat(data)

                return polled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        polled_at = _parse_polled_at(d.pop("polled_at"))

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        figures = cls(
            metrics=metrics,
            not_reported=not_reported,
            engagement=engagement,
            polled_at=polled_at,
            note=note,
        )

        figures.additional_properties = d
        return figures

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
