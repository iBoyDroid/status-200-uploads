from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_read_data_type_0 import PostReadDataType0
    from ..models.post_read_data_type_1 import PostReadDataType1
    from ..models.warning import Warning_


T = TypeVar("T", bound="PostRead")


@_attrs_define
class PostRead:
    """
    Attributes:
        data (PostReadDataType0 | PostReadDataType1):
        warnings (list[Warning_] | Unset):
    """

    data: PostReadDataType0 | PostReadDataType1
    warnings: list[Warning_] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.post_read_data_type_0 import PostReadDataType0

        data: dict[str, Any]
        if isinstance(self.data, PostReadDataType0):
            data = self.data.to_dict()
        else:
            data = self.data.to_dict()

        warnings: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = []
            for warnings_item_data in self.warnings:
                warnings_item = warnings_item_data.to_dict()
                warnings.append(warnings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.post_read_data_type_0 import PostReadDataType0
        from ..models.post_read_data_type_1 import PostReadDataType1
        from ..models.warning import Warning_

        d = dict(src_dict)

        def _parse_data(data: object) -> PostReadDataType0 | PostReadDataType1:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = PostReadDataType0.from_dict(data)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            data_type_1 = PostReadDataType1.from_dict(data)

            return data_type_1

        data = _parse_data(d.pop("data"))

        _warnings = d.pop("warnings", UNSET)
        warnings: list[Warning_] | Unset = UNSET
        if _warnings is not UNSET:
            warnings = []
            for warnings_item_data in _warnings:
                warnings_item = Warning_.from_dict(warnings_item_data)

                warnings.append(warnings_item)

        post_read = cls(
            data=data,
            warnings=warnings,
        )

        post_read.additional_properties = d
        return post_read

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
