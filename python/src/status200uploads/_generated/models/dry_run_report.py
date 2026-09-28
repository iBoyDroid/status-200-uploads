from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dry_run_report_checks_item import DryRunReportChecksItem
    from ..models.dry_run_report_media import DryRunReportMedia
    from ..models.dry_run_report_plan_type_0 import DryRunReportPlanType0
    from ..models.dry_run_report_reason_type_0 import DryRunReportReasonType0
    from ..models.dry_run_report_target import DryRunReportTarget
    from ..models.dry_run_report_warnings_item import DryRunReportWarningsItem
    from ..models.dry_run_report_will_send import DryRunReportWillSend


T = TypeVar("T", bound="DryRunReport")


@_attrs_define
class DryRunReport:
    """
    Attributes:
        dry_run (bool):
        checked_at (datetime.datetime):
        target (DryRunReportTarget):
        outcome (str):
        would_publish (bool):
        reason (DryRunReportReasonType0 | None): Why it would not go out now, with the code, message and HTTP status
            this address would answer (and that refusal's extras). null when outcome is publish.
        warnings (list[DryRunReportWarningsItem]):
        plan (DryRunReportPlanType0 | None):
        media (DryRunReportMedia):
        checks (list[DryRunReportChecksItem]):
        will_send (DryRunReportWillSend | Unset): YouTube and TikTok only; the title and description a publish would
            send.
    """

    dry_run: bool
    checked_at: datetime.datetime
    target: DryRunReportTarget
    outcome: str
    would_publish: bool
    reason: DryRunReportReasonType0 | None
    warnings: list[DryRunReportWarningsItem]
    plan: DryRunReportPlanType0 | None
    media: DryRunReportMedia
    checks: list[DryRunReportChecksItem]
    will_send: DryRunReportWillSend | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dry_run_report_plan_type_0 import DryRunReportPlanType0
        from ..models.dry_run_report_reason_type_0 import DryRunReportReasonType0

        dry_run = self.dry_run

        checked_at = self.checked_at.isoformat()

        target = self.target.to_dict()

        outcome = self.outcome

        would_publish = self.would_publish

        reason: dict[str, Any] | None
        if isinstance(self.reason, DryRunReportReasonType0):
            reason = self.reason.to_dict()
        else:
            reason = self.reason

        warnings = []
        for warnings_item_data in self.warnings:
            warnings_item = warnings_item_data.to_dict()
            warnings.append(warnings_item)

        plan: dict[str, Any] | None
        if isinstance(self.plan, DryRunReportPlanType0):
            plan = self.plan.to_dict()
        else:
            plan = self.plan

        media = self.media.to_dict()

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        will_send: dict[str, Any] | Unset = UNSET
        if not isinstance(self.will_send, Unset):
            will_send = self.will_send.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dry_run": dry_run,
                "checked_at": checked_at,
                "target": target,
                "outcome": outcome,
                "would_publish": would_publish,
                "reason": reason,
                "warnings": warnings,
                "plan": plan,
                "media": media,
                "checks": checks,
            }
        )
        if will_send is not UNSET:
            field_dict["will_send"] = will_send

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.dry_run_report_checks_item import DryRunReportChecksItem
        from ..models.dry_run_report_media import DryRunReportMedia
        from ..models.dry_run_report_plan_type_0 import DryRunReportPlanType0
        from ..models.dry_run_report_reason_type_0 import DryRunReportReasonType0
        from ..models.dry_run_report_target import DryRunReportTarget
        from ..models.dry_run_report_warnings_item import DryRunReportWarningsItem
        from ..models.dry_run_report_will_send import DryRunReportWillSend

        d = dict(src_dict)
        dry_run = d.pop("dry_run")

        checked_at = datetime.datetime.fromisoformat(d.pop("checked_at"))

        target = DryRunReportTarget.from_dict(d.pop("target"))

        outcome = d.pop("outcome")

        would_publish = d.pop("would_publish")

        def _parse_reason(data: object) -> DryRunReportReasonType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reason_type_0 = DryRunReportReasonType0.from_dict(data)

                return reason_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DryRunReportReasonType0 | None, data)

        reason = _parse_reason(d.pop("reason"))

        warnings = []
        _warnings = d.pop("warnings")
        for warnings_item_data in _warnings:
            warnings_item = DryRunReportWarningsItem.from_dict(warnings_item_data)

            warnings.append(warnings_item)

        def _parse_plan(data: object) -> DryRunReportPlanType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plan_type_0 = DryRunReportPlanType0.from_dict(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DryRunReportPlanType0 | None, data)

        plan = _parse_plan(d.pop("plan"))

        media = DryRunReportMedia.from_dict(d.pop("media"))

        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = DryRunReportChecksItem.from_dict(checks_item_data)

            checks.append(checks_item)

        _will_send = d.pop("will_send", UNSET)
        will_send: DryRunReportWillSend | Unset
        if isinstance(_will_send, Unset):
            will_send = UNSET
        else:
            will_send = DryRunReportWillSend.from_dict(_will_send)

        dry_run_report = cls(
            dry_run=dry_run,
            checked_at=checked_at,
            target=target,
            outcome=outcome,
            would_publish=would_publish,
            reason=reason,
            warnings=warnings,
            plan=plan,
            media=media,
            checks=checks,
            will_send=will_send,
        )

        dry_run_report.additional_properties = d
        return dry_run_report

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
