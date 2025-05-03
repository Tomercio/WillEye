def remediation_guide(history: dict) -> str:
    lines = ["Remediation Recommendations:\n"]
    for phase, output in history.items():
        lines.append(
            f"- {phase}: review findings and apply patches/configuration fixes.\n")
    return "".join(lines)
