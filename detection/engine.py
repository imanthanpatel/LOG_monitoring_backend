from detection.models import RuleConfig
from detection.rule_registry import RULE_MAP


def run_all_rules():
    """
    Execute all enabled detection rules.
    Rules are loaded dynamically from RuleConfig.
    """

    enabled_rules = RuleConfig.objects.filter(
        enabled=True
    )

    if not enabled_rules.exists():
        print("[SIEM] No enabled rules found.")
        return

    for config in enabled_rules:

        rule_func = RULE_MAP.get(config.name)

        if not rule_func:
            print(
                f"[SIEM] Rule '{config.name}' "
                f"not found in RULE_MAP."
            )
            continue

        try:
            rule_func()

        except Exception as e:
            print(
                f"[SIEM] Error running "
                f"'{config.name}': {e}"
            )