from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.import_budget_error import ImportBudgetError


T = TypeVar("T", bound="MediaError")


@_attrs_define
class MediaError:
    """
    Attributes:
        error (ImportBudgetError | str):
        code (str | Unset): On the 429 (rate_limited), the Idempotency-Key answers, and a refused share link (its 400
            code, 403 plan_limit_reached, 503 uploads_busy).
        provider (str | Unset): A refused share link's source. Next to it, next_step says what fixes it.
        upgrade_url (str | Unset): 403 plan_limit_reached of a share link - where the paid plans are.
        file_name (str | Unset): 415 of a share link - the shared file's name, when the provider sent it.
        retry_after_seconds (int | Unset):
        size (int | None | Unset): 413 - the declared size.
        file_id (str | Unset): 413 when the storage refused the file after the import started.
        status (str | Unset):
        started_at (str | Unset):
        first_used_at (str | Unset):
    """

    error: ImportBudgetError | str
    code: str | Unset = UNSET
    provider: str | Unset = UNSET
    upgrade_url: str | Unset = UNSET
    file_name: str | Unset = UNSET
    retry_after_seconds: int | Unset = UNSET
    size: int | None | Unset = UNSET
    file_id: str | Unset = UNSET
    status: str | Unset = UNSET
    started_at: str | Unset = UNSET
    first_used_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.import_budget_error import ImportBudgetError

        error: dict[str, Any] | str
        if isinstance(self.error, ImportBudgetError):
            error = self.error.to_dict()
        else:
            error = self.error

        code = self.code

        provider = self.provider

        upgrade_url = self.upgrade_url

        file_name = self.file_name

        retry_after_seconds = self.retry_after_seconds

        size: int | None | Unset
        if isinstance(self.size, Unset):
            size = UNSET
        else:
            size = self.size

        file_id = self.file_id

        status = self.status

        started_at = self.started_at

        first_used_at = self.first_used_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code
        if provider is not UNSET:
            field_dict["provider"] = provider
        if upgrade_url is not UNSET:
            field_dict["upgrade_url"] = upgrade_url
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
        if retry_after_seconds is not UNSET:
            field_dict["retry_after_seconds"] = retry_after_seconds
        if size is not UNSET:
            field_dict["size"] = size
        if file_id is not UNSET:
            field_dict["file_id"] = file_id
        if status is not UNSET:
            field_dict["status"] = status
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if first_used_at is not UNSET:
            field_dict["first_used_at"] = first_used_at

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.import_budget_error import ImportBudgetError

        d = dict(src_dict)

        def _parse_error(data: object) -> ImportBudgetError | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_1 = ImportBudgetError.from_dict(data)

                return error_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ImportBudgetError | str, data)

        error = _parse_error(d.pop("error"))

        code = d.pop("code", UNSET)

        provider = d.pop("provider", UNSET)

        upgrade_url = d.pop("upgrade_url", UNSET)

        file_name = d.pop("file_name", UNSET)

        retry_after_seconds = d.pop("retry_after_seconds", UNSET)

        def _parse_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size = _parse_size(d.pop("size", UNSET))

        file_id = d.pop("file_id", UNSET)

        status = d.pop("status", UNSET)

        started_at = d.pop("started_at", UNSET)

        first_used_at = d.pop("first_used_at", UNSET)

        media_error = cls(
            error=error,
            code=code,
            provider=provider,
            upgrade_url=upgrade_url,
            file_name=file_name,
            retry_after_seconds=retry_after_seconds,
            size=size,
            file_id=file_id,
            status=status,
            started_at=started_at,
            first_used_at=first_used_at,
        )

        media_error.additional_properties = d
        return media_error

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
