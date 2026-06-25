from detection.rules.bruteforce import (
    detect_bruteforce,
    detect_bruteforce_success,
)

from detection.rules.powershell import (
    powershell_execution,
    suspicious_powershell,
)

from detection.rules.users import (
    new_user_creation,
    deleting_user,
)

from detection.rules.process import (
    suspicious_process,
    
)

from detection.rules.rdp import (
    rdp_login,
    off_hours_login,
)

from detection.rules.services import (
    service_installation,
    scheduled_task_created,
)

RULE_MAP = {
    "Brute Force Detection": detect_bruteforce,
    "Brute Force Success": detect_bruteforce_success,
    "PowerShell Execution": powershell_execution,
    "Suspicious PowerShell": suspicious_powershell,
    "New User Creation": new_user_creation,
    "User Deleted": deleting_user,
    "RDP Login": rdp_login,
    "Service Installation": service_installation,
    "Scheduled Task Created": scheduled_task_created,
    "Suspicious Process": suspicious_process,
    "Off Hours Login": off_hours_login,
}