from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.x_options_who_can_reply import XOptionsWhoCanReply, check_x_options_who_can_reply
from ..types import UNSET, Unset

T = TypeVar("T", bound="XOptions")


@_attrs_define
class XOptions:
    """
    Attributes:
        text (str | Unset): Overrides content.text for X.
        who_can_reply (XOptionsWhoCanReply | Unset):  Default: 'everyone'.
        community (str | Unset): The community's link (https://x.com/i/communities/<id>); anything else is not used
            (warnings says so).
        made_with_ai (bool | Unset): Accepted but not used (X gets no label); named in warnings.
        paid_partnership (bool | Unset): Accepted but not used (X gets no label); named in warnings.
    """

    text: str | Unset = UNSET
    who_can_reply: XOptionsWhoCanReply | Unset = "everyone"
    community: str | Unset = UNSET
    made_with_ai: bool | Unset = UNSET
    paid_partnership: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        who_can_reply: str | Unset = UNSET
        if not isinstance(self.who_can_reply, Unset):
            who_can_reply = self.who_can_reply

        community = self.community

        made_with_ai = self.made_with_ai

        paid_partnership = self.paid_partnership

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text
        if who_can_reply is not UNSET:
            field_dict["whoCanReply"] = who_can_reply
        if community is not UNSET:
            field_dict["community"] = community
        if made_with_ai is not UNSET:
            field_dict["madeWithAi"] = made_with_ai
        if paid_partnership is not UNSET:
            field_dict["paidPartnership"] = paid_partnership

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        text = d.pop("text", UNSET)

        _who_can_reply = d.pop("whoCanReply", UNSET)
        who_can_reply: XOptionsWhoCanReply | Unset
        if isinstance(_who_can_reply, Unset):
            who_can_reply = UNSET
        else:
            who_can_reply = check_x_options_who_can_reply(_who_can_reply)

        community = d.pop("community", UNSET)

        made_with_ai = d.pop("madeWithAi", UNSET)

        paid_partnership = d.pop("paidPartnership", UNSET)

        x_options = cls(
            text=text,
            who_can_reply=who_can_reply,
            community=community,
            made_with_ai=made_with_ai,
            paid_partnership=paid_partnership,
        )

        x_options.additional_properties = d
        return x_options

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
