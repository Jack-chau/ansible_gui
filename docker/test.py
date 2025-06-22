import docker
import os
import subprocess
import json
from typing import Dict, Any

def compare_docker_environments():
    """Compare Docker SDK and CLI configurations side-by-side"""
    # Initialize Docker clients
    sdk_client = docker.from_env()
    
    # Get SDK configuration
    sdk_config = {
        "base_url": sdk_client.api.base_url,
        "version": sdk_client.version(),
        "auth_configs": sdk_client.api._auth_configs,
        "general_configs": sdk_client.api._general_configs
    }
    
    # Get CLI configuration
    cli_info = subprocess.check_output(
        ["docker", "system", "info", "--format", "{{json .}}"],
        stderr=subprocess.PIPE
    ).decode().strip()
    
    # Print comparison
    print("\n=== Docker Configuration Comparison ===")
    print("\nSDK Configuration:")
    print(f"Base URL: {sdk_config['base_url']}")
    print(f"API Version: {sdk_config['version']['ApiVersion']}")
    print("Auth Configs:", sdk_config['auth_configs'].keys())
    
    print("\nCLI Configuration:")
    cli_data = docker.types.json.loads(cli_info)
    print(f"Docker Root: {cli_data['DockerRootDir']}")
    print(f"Server Version: {cli_data['ServerVersion']}")
    print(f"Default Runtime: {cli_data['DefaultRuntime']}")
    
    # Critical alignment checks
    print("\n=== Alignment Verification ===")
    check_alignment(
        "API Version",
        sdk_config['version']['ApiVersion'],
        cli_data['ServerVersion']
    )
    
    check_alignment(
        "Authentication",
        bool(sdk_config['auth_configs']),
        os.path.exists(os.path.expanduser("~/.docker/config.json"))
    )

def check_alignment(name: str, sdk_value: Any, cli_value: Any):
    """Helper function to compare values"""
    status = "✓" if str(sdk_value) == str(cli_value) else "✗"
    print(f"{status} {name}:")
    print(f"  SDK: {sdk_value}")
    print(f"  CLI: {cli_value}")
    print("")

if __name__ == "__main__":
    compare_docker_environments()