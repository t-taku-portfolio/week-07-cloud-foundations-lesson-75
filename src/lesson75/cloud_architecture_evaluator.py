import argparse
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
    timestamp = datetime.datetime.now(JAPAN_TOKYO).strftime('%Y_%m_%d')
    obj_dict['timestamp'] = timestamp

    if target_dir is None:
        target_dir = Path.cwd()
    file_path = Path(target_dir) / 'architecture_report.json'

    try:
        with open(file_path, 'w') as f:
            json.dump(obj= obj_dict, fp= f,indent= 4)
    except FileNotFoundError:
        print('Target directory is not found')
        raise

    return file_path


if __name__ == '__main__':

    # Create an argument parser and subparser object
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required= True)

    # Have user choose a function from the choices

    # args are str and bool
    parser_audit = subparsers.add_parser('audit')
    parser_audit.add_argument('workload_type', type= str)
    parser_audit.add_argument('custom_os_needed', type= lambda bool_str: bool_str.lower() == 'true')
    parser_audit.set_defaults(func= audit_service_tier)

    # args are float and float
    parser_calculate = subparsers.add_parser('calculate')
    parser_calculate.add_argument('primary_cost', type= float)
    parser_calculate.add_argument('replication_rate', type= float)
    parser_calculate.set_defaults(func= calulate_multiregion_budget)

    # arg is a list of int
    parser_simulate = subparsers.add_parser('simulate')
    parser_simulate.add_argument('probe_response', type= int, nargs= '+')
    parser_simulate.set_defaults(func= simulate_health_check)

    # Retrieve arguments from parser
    args = parser.parse_args()

    # Extend the args namespace as dict, and pop the func argument out from the dict
    args_dict = vars(args).copy()
    func = args_dict.pop('func')

    # Process the result
    json_dict = {f'{func.__name__}' : func(**args_dict)}

    # Save as JSON and show the file's path
    print(f'[DONE] Saved as JSON at {save_as_json(json_dict, None)}')