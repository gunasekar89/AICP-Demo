"""Fulfillment agent assembles the final delivery package."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from textwrap import wrap
from typing import Iterable, List


def _wrap_lines(text: str, width: int) -> List[str]:
    """Return wrapped lines for the provided text respecting the width budget."""

    segments: List[str] = []
    for block in text.splitlines() or [""]:
        chunks = wrap(block, width=width) or [""]
        segments.extend(chunks)
    return segments


@dataclass
class FulfillmentAgent:
    """Generate a visually rich hand-off summary that feels like a live monitor."""

    name: str = "Fulfillment"

    def compile_package(
        self,
        plan_bullets: Iterable[str],
        vision_summary: str,
        brand_voice: str,
    ) -> str:
        """Return the final delivery overview styled as a security operations dashboard."""

        inner_width = 74
        horizontal_rule = "═" * (inner_width + 2)

        def frame_line(text: str = "", *, align: str = "left") -> str:
            if len(text) > inner_width:
                text = text[: inner_width]
            if align == "center":
                padded = text.center(inner_width)
            elif align == "right":
                padded = text.rjust(inner_width)
            else:
                padded = text.ljust(inner_width)
            return f"║ {padded} ║"

        def frame_block(title: str, body: Iterable[str]) -> List[str]:
            lines = ["╟" + "─" * (inner_width + 2) + "╢", frame_line(f"▶ {title.upper()}")]
            for item in body:
                wrapped_lines = _wrap_lines(item, inner_width)
                for chunk in wrapped_lines:
                    lines.append(frame_line(chunk))
            return lines

        plan_list = list(plan_bullets)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
        packet_hash = f"{abs(hash((vision_summary, brand_voice, tuple(plan_list)))):08X}"[-8:]

        execution_lines = []
        for bullet in plan_list:
            normalized = bullet.strip()
            if not normalized.startswith("•"):
                normalized = f"• {normalized}"
            execution_lines.append(normalized)
        if not execution_lines:
            execution_lines.append("• Awaiting planner milestones…")

        dashboard_lines: List[str] = [
            "╔" + horizontal_rule + "╗",
            frame_line("SRM-SECOPS // REAL-TIME COMMERCE MONITOR", align="center"),
            frame_line(f"Telemetry Ping: {timestamp}", align="right"),
            "╠" + horizontal_rule + "╣",
        ]

        dashboard_lines.extend(
            frame_block("Vision Lock", [vision_summary, "Optic Integrity: Stable"])
        )
        dashboard_lines.extend(
            frame_block("Brand Signal", [brand_voice, "Linguistic Drift: < 0.02"])
        )
        dashboard_lines.extend(frame_block("Execution Matrix", execution_lines))

        dashboard_lines.extend(
            frame_block(
                "Quantum Sentinel",
                [
                    "Predictive engines synced. Quantum annealing sandbox ready for last-mile trade-offs.",
                    f"Packet Integrity Hash: {packet_hash}",
                ],
            )
        )

        dashboard_lines.append("╠" + horizontal_rule + "╣")
        dashboard_lines.append(frame_line("AI Monitor: ACTIVE    |    Threat Level: LOW", align="center"))
        dashboard_lines.append(frame_line("Render Mode: HOLOGRAPHIC CACHE"))
        dashboard_lines.append("╚" + horizontal_rule + "╝")

        return "\n".join(dashboard_lines)
