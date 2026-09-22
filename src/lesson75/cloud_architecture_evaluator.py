import datetime
import json
import zoneinfo
from pathlib import Path


def audit_service_tier(workload_type: str, custom_os_needed: bool) -> str:
# Recommends "IaaS", "PaaS", or "SaaS" based on customization and administrative needs.

    paaS_workloads = ['api', 'web_app', 'managed_database', 'container']
    saas_workloads = ['email', 'crm', 'office_suite', 'monitoring_tool']

    if custom_os_needed:
        return 'IaaS'
    elif workload_type.lower() in paaS_workloads:
        return 'PaaS'
    elif workload_type.lower() in saas_workloads:
        return 'SaaS'
    else:
        return f'[ERROR] unknown workload type {workload_type}'
    

def calulate_multiregion_budget(primary_cost: float, replication_rate: float= 0.8) -> float:
# Calculates total multi-region disaster recovery budget including primary infrastructure and secondary warm-standby infrastructure.

    estimated_budget = primary_cost * (1 + replication_rate)
    return estimated_budget


def simulate_health_check(probe_response: list) -> bool:
# Evaluates a list of HTTP status codes (e.g., [200, 200, 503]) and returns False if failure rate exceeds 30%.

    failure_threshold_percent = 30
    failure_count = 0

    for status_code in probe_response:
        if (type(status_code) is int) and (status_code > 400):
            failure_count += 1

    return (failure_count * 100 / len(probe_response)) < failure_threshold_percent


def save_as_json(obj_dict: dict, target_dir: str) -> str:
# Save the evaluation results as a formatted JSON report
# Add timestamp automatically

    JAPAN_TOKYO = zoneinfo.ZoneInfo('Asia/Tokyo')
    timestamp = datetime.datetime.now(JAPAN_TOKYO).strftime('Y%_m%_d%')
    obj_dict['timestamp'] = timestamp

    file_path = Path(target_dir) / 'architecture_report.json'

    try:
        with open(file_path, 'w') as f:
            json.dump(obj= obj_dict, fp= f,indent= 4)
    except FileNotFoundError:
        print('Target directory is not found')
        raise

    return file_path


if __name__ == '__main__':
    obj_dict = {}

    obj_dict['service_tier'] = audit_service_tier()
    obj_dict['multiregion_budget'] = calulate_multiregion_budget()
    obj_dict['isHealthy'] = simulate_health_check()

    print(f'[DONE] Saved as JSON at {save_as_json()}')