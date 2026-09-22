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

    failure_rate_percent = 30
    failure_count = 0

    for status_code in probe_response:
        if (type(status_code) is int) and (status_code > 400):
            failure_count += 1

    return (failure_count * 100 / len(probe_response)) > failure_rate_percent


def save_json() -> str:
# Save the evaluation results as a formatted JSON report
    return 'path'