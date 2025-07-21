# Azure DevOps Complete Tutorial - Google Colab Implementation
# This notebook simulates and demonstrates Azure DevOps concepts

import os
import json
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
from tabulate import tabulate
import base64
import hashlib
import random
from typing import Dict, List, Any

print("🚀 Azure DevOps Tutorial Environment Setup Complete!")
print("=" * 60)

# ============================================================================
# 1. CONFIGURE DASHBOARD AND QUERIES FOR WORK ITEMS
# ============================================================================

print("\n📊 1. WORK ITEMS DASHBOARD AND QUERIES")
print("=" * 50)

class WorkItemManager:
    def __init__(self):
        self.work_items = []
        self.queries = {}

    def create_sample_work_items(self):
        """Create sample work items for demonstration"""
        work_item_types = ['Bug', 'User Story', 'Task', 'Epic', 'Feature']
        states = ['New', 'Active', 'Resolved', 'Closed']
        priorities = ['Critical', 'High', 'Medium', 'Low']

        for i in range(50):
            work_item = {
                'id': f"WI-{1000 + i}",
                'title': f"Sample {work_item_types[i % len(work_item_types)]} {i+1}",
                'type': work_item_types[i % len(work_item_types)],
                'state': random.choice(states),
                'priority': random.choice(priorities),
                'assigned_to': f"user{(i % 5) + 1}@company.com",
                'created_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'story_points': random.randint(1, 13) if work_item_types[i % len(work_item_types)] == 'User Story' else None
            }
            self.work_items.append(work_item)

    def create_query(self, name: str, criteria: Dict[str, Any]):
        """Create a work item query"""
        self.queries[name] = criteria
        print(f"✅ Query '{name}' created successfully")

    def execute_query(self, query_name: str):
        """Execute a work item query"""
        if query_name not in self.queries:
            print(f"❌ Query '{query_name}' not found")
            return []

        criteria = self.queries[query_name]
        filtered_items = self.work_items.copy()

        for field, value in criteria.items():
            if isinstance(value, list):
                filtered_items = [item for item in filtered_items if item.get(field) in value]
            else:
                filtered_items = [item for item in filtered_items if item.get(field) == value]

        return filtered_items

    def display_dashboard(self):
        """Display work items dashboard"""
        df = pd.DataFrame(self.work_items)

        # Summary statistics
        print("\n📈 Work Items Summary Dashboard")
        print("-" * 40)

        summary_stats = {
            'Total Work Items': len(self.work_items),
            'Active Items': len([item for item in self.work_items if item['state'] == 'Active']),
            'Resolved Items': len([item for item in self.work_items if item['state'] == 'Resolved']),
            'Critical Priority': len([item for item in self.work_items if item['priority'] == 'Critical'])
        }

        for key, value in summary_stats.items():
            print(f"{key}: {value}")

        # Visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Work items by type
        type_counts = df['type'].value_counts()
        axes[0, 0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Work Items by Type')

        # Work items by state
        state_counts = df['state'].value_counts()
        axes[0, 1].bar(state_counts.index, state_counts.values, color='skyblue')
        axes[0, 1].set_title('Work Items by State')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Work items by priority
        priority_counts = df['priority'].value_counts()
        axes[1, 0].bar(priority_counts.index, priority_counts.values, color='orange')
        axes[1, 0].set_title('Work Items by Priority')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # Work items by assigned user
        user_counts = df['assigned_to'].value_counts()
        axes[1, 1].bar(range(len(user_counts)), user_counts.values, color='green')
        axes[1, 1].set_title('Work Items by Assigned User')
        axes[1, 1].set_xticks(range(len(user_counts)))
        axes[1, 1].set_xticklabels([f"User {i+1}" for i in range(len(user_counts))], rotation=45)

        plt.tight_layout()
        plt.show()

# Initialize Work Item Manager
wim = WorkItemManager()
wim.create_sample_work_items()

# Create sample queries
wim.create_query("Active Bugs", {"type": "Bug", "state": "Active"})
wim.create_query("High Priority Items", {"priority": ["Critical", "High"]})
wim.create_query("My Work Items", {"assigned_to": "user1@company.com"})

# Execute queries
print("\n🔍 Executing Sample Queries:")
active_bugs = wim.execute_query("Active Bugs")
print(f"Active Bugs: {len(active_bugs)} items found")

high_priority = wim.execute_query("High Priority Items")
print(f"High Priority Items: {len(high_priority)} items found")

# Display dashboard
wim.display_dashboard()

# ============================================================================
# 2. PIPELINE VARIABLES CONFIGURATION
# ============================================================================

print("\n\n🔧 2. PIPELINE VARIABLES CONFIGURATION")
print("=" * 50)

class PipelineVariableManager:
    def __init__(self):
        self.variables = {
            'build': {},
            'release': {},
            'environment': {}
        }

    def add_variable(self, scope: str, name: str, value: str, is_secret: bool = False):
        """Add a pipeline variable"""
        if scope not in self.variables:
            self.variables[scope] = {}

        self.variables[scope][name] = {
            'value': value if not is_secret else '*' * len(value),
            'is_secret': is_secret,
            'actual_value': value
        }

        print(f"✅ Variable '{name}' added to '{scope}' scope")

    def get_variable(self, scope: str, name: str):
        """Get a pipeline variable"""
        if scope in self.variables and name in self.variables[scope]:
            return self.variables[scope][name]['actual_value']
        return None

    def list_variables(self, scope: str = None):
        """List pipeline variables"""
        if scope:
            scopes = [scope]
        else:
            scopes = self.variables.keys()

        for s in scopes:
            print(f"\n📋 Variables in '{s}' scope:")
            if s in self.variables:
                for name, details in self.variables[s].items():
                    secret_indicator = " (Secret)" if details['is_secret'] else ""
                    print(f"  {name}: {details['value']}{secret_indicator}")

    def generate_yaml_config(self):
        """Generate YAML configuration for pipeline variables"""
        yaml_config = {
            'variables': []
        }

        for scope, vars_dict in self.variables.items():
            for name, details in vars_dict.items():
                yaml_config['variables'].append({
                    'name': name,
                    'value': details['actual_value']
                })

        return yaml.dump(yaml_config, default_flow_style=False)

# Initialize Pipeline Variable Manager
pvm = PipelineVariableManager()

# Add sample variables
pvm.add_variable('build', 'BuildConfiguration', 'Release')
pvm.add_variable('build', 'BuildPlatform', 'Any CPU')
pvm.add_variable('build', 'Version', '1.0.$(Build.BuildId)')

pvm.add_variable('release', 'Environment', 'Production')
pvm.add_variable('release', 'ConnectionString', 'Server=prod-db;Database=app', is_secret=True)
pvm.add_variable('release', 'ApiKey', 'sk-1234567890abcdef', is_secret=True)

pvm.add_variable('environment', 'AZURE_SUBSCRIPTION', 'prod-subscription-id')
pvm.add_variable('environment', 'RESOURCE_GROUP', 'rg-production')

# List variables
pvm.list_variables()

# Generate YAML configuration
print(f"\n📄 Generated YAML Configuration:")
print(pvm.generate_yaml_config())

# ============================================================================
# 3. VARIABLE AND TASK GROUPS
# ============================================================================

print("\n\n👥 3. VARIABLE AND TASK GROUPS")
print("=" * 50)

class VariableGroupManager:
    def __init__(self):
        self.variable_groups = {}
        self.task_groups = {}

    def create_variable_group(self, name: str, description: str, variables: Dict[str, str]):
        """Create a variable group"""
        self.variable_groups[name] = {
            'description': description,
            'variables': variables,
            'created_date': datetime.now(),
            'scopes': []
        }
        print(f"✅ Variable group '{name}' created")

    def add_scope_to_variable_group(self, group_name: str, scope: str):
        """Add scope to variable group"""
        if group_name in self.variable_groups:
            self.variable_groups[group_name]['scopes'].append(scope)
            print(f"✅ Scope '{scope}' added to variable group '{group_name}'")

    def create_task_group(self, name: str, tasks: List[Dict[str, Any]]):
        """Create a task group"""
        self.task_groups[name] = {
            'tasks': tasks,
            'created_date': datetime.now()
        }
        print(f"✅ Task group '{name}' created with {len(tasks)} tasks")

    def list_groups(self):
        """List all variable and task groups"""
        print("\n📋 Variable Groups:")
        for name, details in self.variable_groups.items():
            print(f"  {name}: {details['description']}")
            print(f"    Variables: {len(details['variables'])}")
            print(f"    Scopes: {', '.join(details['scopes'])}")

        print(f"\n📋 Task Groups:")
        for name, details in self.task_groups.items():
            print(f"  {name}: {len(details['tasks'])} tasks")

# Initialize Variable Group Manager
vgm = VariableGroupManager()

# Create variable groups
vgm.create_variable_group(
    "Database-Config",
    "Database configuration variables",
    {
        "DB_HOST": "prod-db-server.database.windows.net",
        "DB_NAME": "ProductionDB",
        "DB_PORT": "1433"
    }
)

vgm.create_variable_group(
    "Azure-Resources",
    "Azure resource configuration",
    {
        "SUBSCRIPTION_ID": "12345678-1234-1234-1234-123456789012",
        "RESOURCE_GROUP": "rg-production",
        "LOCATION": "East US"
    }
)

# Add scopes
vgm.add_scope_to_variable_group("Database-Config", "Production")
vgm.add_scope_to_variable_group("Database-Config", "Staging")
vgm.add_scope_to_variable_group("Azure-Resources", "Production")

# Create task groups
build_tasks = [
    {"task": "NuGetRestore", "inputs": {"solution": "**/*.sln"}},
    {"task": "VSBuild", "inputs": {"solution": "**/*.sln", "configuration": "Release"}},
    {"task": "VSTest", "inputs": {"testAssemblyVer2": "**/*Tests.dll"}}
]

deploy_tasks = [
    {"task": "AzureWebApp", "inputs": {"appName": "my-web-app", "package": "$(Build.ArtifactStagingDirectory)/**/*.zip"}},
    {"task": "AzureSQLDatabaseDeployment", "inputs": {"ServerName": "$(DB_HOST)", "DatabaseName": "$(DB_NAME)"}}
]

vgm.create_task_group("Build-DotNet", build_tasks)
vgm.create_task_group("Deploy-WebApp", deploy_tasks)

# List all groups
vgm.list_groups()

# ============================================================================
# 4. SERVICE CONNECTIONS
# ============================================================================

print("\n\n🔗 4. SERVICE CONNECTIONS")
print("=" * 50)

class ServiceConnectionManager:
    def __init__(self):
        self.connections = {}

    def create_service_connection(self, name: str, connection_type: str, config: Dict[str, Any]):
        """Create a service connection"""
        connection_id = f"sc-{hashlib.md5(name.encode()).hexdigest()[:8]}"

        self.connections[name] = {
            'id': connection_id,
            'type': connection_type,
            'config': config,
            'created_date': datetime.now(),
            'status': 'Active'
        }

        print(f"✅ Service connection '{name}' created (ID: {connection_id})")
        return connection_id

    def test_connection(self, name: str):
        """Test a service connection"""
        if name in self.connections:
            # Simulate connection test
            import time
            print(f"🔄 Testing connection '{name}'...")
            time.sleep(1)
            print(f"✅ Connection '{name}' test successful")
            return True
        else:
            print(f"❌ Connection '{name}' not found")
            return False

    def list_connections(self):
        """List all service connections"""
        print("\n📋 Service Connections:")
        for name, details in self.connections.items():
            print(f"  {name} ({details['type']})")
            print(f"    ID: {details['id']}")
            print(f"    Status: {details['status']}")
            print(f"    Created: {details['created_date'].strftime('%Y-%m-%d %H:%M:%S')}")

# Initialize Service Connection Manager
scm = ServiceConnectionManager()

# Create sample service connections
scm.create_service_connection(
    "Azure-Production",
    "Azure Resource Manager",
    {
        "subscription_id": "12345678-1234-1234-1234-123456789012",
        "tenant_id": "87654321-4321-4321-4321-210987654321",
        "service_principal_id": "sp-12345",
        "authentication_method": "Service Principal"
    }
)

scm.create_service_connection(
    "Docker-Registry",
    "Docker Registry",
    {
        "registry_url": "myregistry.azurecr.io",
        "username": "myregistry",
        "authentication_method": "Username and Password"
    }
)

scm.create_service_connection(
    "GitHub-Repo",
    "GitHub",
    {
        "repository_url": "https://github.com/myorg/myproject.git",
        "authentication_method": "Personal Access Token"
    }
)

# Test connections
scm.test_connection("Azure-Production")
scm.test_connection("Docker-Registry")

# List all connections
scm.list_connections()

# ============================================================================
# 5. SELF-HOSTED AGENTS (SIMULATION)
# ============================================================================

print("\n\n💻 5. SELF-HOSTED AGENTS")
print("=" * 50)

class SelfHostedAgentManager:
    def __init__(self):
        self.agents = {}
        self.agent_pools = {}

    def create_agent_pool(self, name: str, description: str):
        """Create an agent pool"""
        self.agent_pools[name] = {
            'description': description,
            'agents': [],
            'created_date': datetime.now()
        }
        print(f"✅ Agent pool '{name}' created")

    def register_agent(self, name: str, os_type: str, pool_name: str, capabilities: List[str]):
        """Register a self-hosted agent"""
        agent_id = f"agent-{hashlib.md5(name.encode()).hexdigest()[:8]}"

        agent = {
            'id': agent_id,
            'name': name,
            'os_type': os_type,
            'pool': pool_name,
            'capabilities': capabilities,
            'status': 'Online',
            'registered_date': datetime.now(),
            'last_activity': datetime.now()
        }

        self.agents[name] = agent

        if pool_name in self.agent_pools:
            self.agent_pools[pool_name]['agents'].append(agent_id)

        print(f"✅ Agent '{name}' registered in pool '{pool_name}' (ID: {agent_id})")

    def generate_agent_setup_script(self, os_type: str, pool_name: str, agent_name: str):
        """Generate agent setup script"""
        if os_type.lower() == 'linux':
            script = f'''#!/bin/bash
# Azure DevOps Self-Hosted Agent Setup Script (Linux)

# Download and extract agent
mkdir -p ~/azagent && cd ~/azagent
wget https://vstsagentpackage.azureedge.net/agent/2.206.1/vsts-agent-linux-x64-2.206.1.tar.gz
tar zxvf vsts-agent-linux-x64-2.206.1.tar.gz

# Configure agent
./config.sh --unattended \\
    --agent "{agent_name}" \\
    --url "https://dev.azure.com/yourorg" \\
    --auth PAT \\
    --token "YOUR_PAT_TOKEN" \\
    --pool "{pool_name}" \\
    --work "_work" \\
    --acceptTeeEula

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start

echo "✅ Agent {agent_name} configured and started"
'''
        else:  # Windows
            script = f'''@echo off
REM Azure DevOps Self-Hosted Agent Setup Script (Windows)

REM Create directory and download agent
mkdir C:\\azagent
cd C:\\azagent
powershell -Command "Invoke-WebRequest -Uri 'https://vstsagentpackage.azureedge.net/agent/2.206.1/vsts-agent-win-x64-2.206.1.zip' -OutFile 'agent.zip'"
powershell -Command "Expand-Archive -Path 'agent.zip' -DestinationPath '.'"

REM Configure agent
.\\config.cmd --unattended ^
    --agent "{agent_name}" ^
    --url "https://dev.azure.com/yourorg" ^
    --auth PAT ^
    --token "YOUR_PAT_TOKEN" ^
    --pool "{pool_name}" ^
    --work "_work" ^
    --acceptTeeEula

REM Install as service
.\\config.cmd --service
net start vstsagent.yourorg.{agent_name}

echo ✅ Agent {agent_name} configured and started
'''

        return script

    def list_agents(self):
        """List all agents"""
        print("\n📋 Self-Hosted Agents:")
        for name, agent in self.agents.items():
            print(f"  {name} ({agent['os_type']})")
            print(f"    ID: {agent['id']}")
            print(f"    Pool: {agent['pool']}")
            print(f"    Status: {agent['status']}")
            print(f"    Capabilities: {', '.join(agent['capabilities'])}")

# Initialize Self-Hosted Agent Manager
sham = SelfHostedAgentManager()

# Create agent pools
sham.create_agent_pool("Linux-Agents", "Pool for Linux-based agents")
sham.create_agent_pool("Windows-Agents", "Pool for Windows-based agents")

# Register sample agents
sham.register_agent(
    "ubuntu-agent-01",
    "Linux",
    "Linux-Agents",
    ["docker", "nodejs", "python", "dotnet"]
)

sham.register_agent(
    "windows-agent-01",
    "Windows",
    "Windows-Agents",
    ["msbuild", "visualstudio", "dotnet", "powershell"]
)

# Generate setup scripts
print(f"\n🐧 Linux Agent Setup Script:")
linux_script = sham.generate_agent_setup_script("linux", "Linux-Agents", "ubuntu-agent-02")
print(linux_script[:300] + "...")

print(f"\n🪟 Windows Agent Setup Script:")
windows_script = sham.generate_agent_setup_script("windows", "Windows-Agents", "windows-agent-02")
print(windows_script[:300] + "...")

# List agents
sham.list_agents()

# ============================================================================
# 6. RELEASE PIPELINE APPROVALS
# ============================================================================

print("\n\n✋ 6. RELEASE PIPELINE APPROVALS")
print("=" * 50)

class ReleaseApprovalManager:
    def __init__(self):
        self.environments = {}
        self.approvals = {}
        self.approval_requests = []

    def create_environment(self, name: str, description: str):
        """Create an environment"""
        self.environments[name] = {
            'description': description,
            'pre_deployment_approvers': [],
            'post_deployment_approvers': [],
            'created_date': datetime.now()
        }
        print(f"✅ Environment '{name}' created")

    def add_approver(self, environment: str, approver_email: str, approval_type: str):
        """Add an approver to an environment"""
        if environment in self.environments:
            if approval_type == "pre":
                self.environments[environment]['pre_deployment_approvers'].append(approver_email)
            elif approval_type == "post":
                self.environments[environment]['post_deployment_approvers'].append(approver_email)

            print(f"✅ Added {approval_type}-deployment approver {approver_email} to {environment}")

    def request_approval(self, environment: str, deployment_id: str, approval_type: str):
        """Request approval for deployment"""
        request_id = f"approval-{hashlib.md5(f'{deployment_id}-{approval_type}'.encode()).hexdigest()[:8]}"

        approvers = []
        if approval_type == "pre":
            approvers = self.environments[environment]['pre_deployment_approvers']
        elif approval_type == "post":
            approvers = self.environments[environment]['post_deployment_approvers']

        approval_request = {
            'id': request_id,
            'deployment_id': deployment_id,
            'environment': environment,
            'type': approval_type,
            'approvers': approvers,
            'status': 'Pending',
            'requested_date': datetime.now(),
            'responses': {}
        }

        self.approval_requests.append(approval_request)
        print(f"📨 Approval request {request_id} sent to {len(approvers)} approvers for {environment}")
        return request_id

    def process_approval(self, request_id: str, approver: str, decision: str, comment: str = ""):
        """Process an approval response"""
        for request in self.approval_requests:
            if request['id'] == request_id:
                if approver in request['approvers']:
                    request['responses'][approver] = {
                        'decision': decision,
                        'comment': comment,
                        'response_date': datetime.now()
                    }

                    # Check if all approvers have responded
                    if len(request['responses']) == len(request['approvers']):
                        all_approved = all(resp['decision'] == 'Approved' for resp in request['responses'].values())
                        request['status'] = 'Approved' if all_approved else 'Rejected'

                    print(f"✅ Approval processed: {approver} {decision} request {request_id}")
                    return True

        print(f"❌ Approval request {request_id} not found or approver not authorized")
        return False

    def list_approval_requests(self, status: str = None):
        """List approval requests"""
        print(f"\n📋 Approval Requests {f'({status})' if status else ''}:")

        filtered_requests = self.approval_requests
        if status:
            filtered_requests = [req for req in self.approval_requests if req['status'] == status]

        for request in filtered_requests:
            print(f"  {request['id']} - {request['environment']} ({request['type']}-deployment)")
            print(f"    Status: {request['status']}")
            print(f"    Approvers: {len(request['approvers'])}")
            print(f"    Responses: {len(request['responses'])}/{len(request['approvers'])}")

# Initialize Release Approval Manager
ram = ReleaseApprovalManager()

# Create environments
ram.create_environment("Staging", "Staging environment for testing")
ram.create_environment("Production", "Production environment")

# Add approvers
ram.add_approver("Staging", "lead@company.com", "pre")
ram.add_approver("Production", "manager@company.com", "pre")
ram.add_approver("Production", "lead@company.com", "pre")
ram.add_approver("Production", "devops@company.com", "post")

# Simulate approval workflow
deployment_id = "deploy-12345"
print(f"\n🚀 Simulating deployment {deployment_id} to Production...")

# Request pre-deployment approval
pre_approval_id = ram.request_approval("Production", deployment_id, "pre")

# Process approvals
ram.process_approval(pre_approval_id, "manager@company.com", "Approved", "LGTM")
ram.process_approval(pre_approval_id, "lead@company.com", "Approved", "Approved after code review")

# Request post-deployment approval
post_approval_id = ram.request_approval("Production", deployment_id, "post")
ram.process_approval(post_approval_id, "devops@company.com", "Approved", "Deployment successful, monitoring looks good")

# List approval requests
ram.list_approval_requests()

# ============================================================================
# 7. CI/CD PIPELINE FOR DOCKER TO ACR AND AKS
# ============================================================================

print("\n\n🐳 7. CI/CD PIPELINE: DOCKER TO ACR AND AKS")
print("=" * 50)

class DockerACRAKSPipeline:
    def __init__(self):
        self.pipeline_runs = []
        self.acr_images = []
        self.aks_deployments = []

    def generate_pipeline_yaml(self):
        """Generate Azure DevOps pipeline YAML for Docker to ACR and AKS"""
        pipeline_yaml = '''
trigger:
- main

variables:
  dockerRegistryServiceConnection: 'docker-registry-connection'
  imageRepository: 'myapp'
  containerRegistry: 'myregistry.azurecr.io'
  dockerfilePath: '**/Dockerfile'
  tag: '$(Build.BuildId)'
  imagePullSecret: 'myregistry-auth'
  aksServiceConnection: 'aks-service-connection'
  aksCluster: 'my-aks-cluster'
  aksNamespace: 'default'

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  displayName: Build and Push Docker Image
  jobs:
  - job: Build
    displayName: Build Docker Image
    steps:
    - task: Docker@2
      displayName: Build and push Docker image to ACR
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          latest

- stage: Deploy
  displayName: Deploy to AKS
  dependsOn: Build
  jobs:
  - deployment: Deploy
    displayName: Deploy to AKS
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            displayName: Deploy to Kubernetes cluster
            inputs:
              action: deploy
              kubernetesServiceConnection: $(aksServiceConnection)
              namespace: $(aksNamespace)
              manifests: |
                k8s/deployment.yaml
                k8s/service.yaml
              containers: |
                $(containerRegistry)/$(imageRepository):$(tag)
'''
        return pipeline_yaml

    def generate_kubernetes_manifests(self):
        """Generate Kubernetes deployment and service manifests"""
        deployment_yaml = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry.azurecr.io/myapp:latest
        ports:
        - containerPort: 80
        env:
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        imagePullSecrets:
        - name: myregistry-auth
'''

        service_yaml = '''
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
'''

        return deployment_yaml, service_yaml

    def simulate_pipeline_run(self, build_id: str):
        """Simulate a pipeline run"""
        run_id = f"run-{build_id}"

        # Simulate build stage
        print(f"🔨 Building Docker image for build {build_id}...")
        image_tag = f"myregistry.azurecr.io/myapp:{build_id}"

        # Add to ACR images
        acr_image = {
            'repository': 'myapp',
            'tag': build_id,
            'full_name': image_tag,
            'size': f"{random.randint(100, 500)}MB",
            'created_date': datetime.now()
        }
        self.acr_images.append(acr_image)
        print(f"✅ Image pushed to ACR: {image_tag}")

        # Simulate deployment to AKS
        print(f"🚀 Deploying to AKS cluster...")
        aks_deployment = {
            'deployment_id': f"deploy-{build_id}",
            'image': image_tag,
            'replicas': 3,
            'namespace': 'default',
            'status': 'Running',
            'deployed_date': datetime.now()
        }
        self.aks_deployments.append(aks_deployment)
        print(f"✅ Deployed to AKS: {aks_deployment['deployment_id']}")

        # Record pipeline run
        pipeline_run = {
            'run_id': run_id,
            'build_id': build_id,
            'status': 'Succeeded',
            'start_time': datetime.now() - timedelta(minutes=5),
            'end_time': datetime.now(),
            'stages': ['Build', 'Deploy'],
            'image_pushed': image_tag,
            'deployment_id': aks_deployment['deployment_id']
        }
        self.pipeline_runs.append(pipeline_run)

        return pipeline_run

    def list_acr_images(self):
        """List ACR images"""
        print("\n📦 Azure Container Registry Images:")
        for image in self.acr_images[-5:]:  # Show last 5
            print(f"  {image['full_name']}")
            print(f"    Size: {image['size']}")
            print(f"    Created: {image['created_date'].strftime('%Y-%m-%d %H:%M:%S')}")

    def list_aks_deployments(self):
        """List AKS deployments"""
        print("\n☸️ AKS Deployments:")
        for deployment in self.aks_deployments[-3:]:  # Show last 3
            print(f"  {deployment['deployment_id']}")
            print(f"    Image: {deployment['image']}")
            print(f"    Replicas: {deployment['replicas']}")
            print(f"    Status: {deployment['status']}")

# Initialize Docker ACR AKS Pipeline
dak_pipeline = DockerACRAKSPipeline()

# Generate pipeline configuration
print("📄 Azure DevOps Pipeline YAML:")
yaml_config = dak_pipeline.generate_pipeline_yaml()
print(yaml_config[:500] + "...")

print("\n📄 Kubernetes Manifests:")
deployment_manifest, service_manifest = dak_pipeline.generate_kubernetes_manifests()
print("Deployment manifest generated ✅")
print("Service manifest generated ✅")

# Simulate pipeline runs
for i in range(3):
    build_id = f"2024{random.randint(100, 999)}"
    print(f"\n🚀 Pipeline Run #{i+1} (Build ID: {build_id})")
    dak_pipeline.simulate_pipeline_run(build_id)

# List results
dak_pipeline.list_acr_images()
dak_pipeline.list_aks_deployments()

# ============================================================================
# 8. CI/CD PIPELINE FOR DOCKER TO ACR AND ACI
# ============================================================================

print("\n\n🐳 8. CI/CD PIPELINE: DOCKER TO ACR AND ACI")
print("=" * 50)

class DockerACRACIPipeline:
    def __init__(self):
        self.pipeline_runs = []
        self.aci_containers = []

    def generate_pipeline_yaml(self):
        """Generate Azure DevOps pipeline YAML for Docker to ACR and ACI"""
        pipeline_yaml = '''
trigger:
- main

variables:
  dockerRegistryServiceConnection: 'docker-registry-connection'
  imageRepository: 'myapp'
  containerRegistry: 'myregistry.azurecr.io'
  dockerfilePath: '**/Dockerfile'
  tag: '$(Build.BuildId)'
  azureSubscription: 'azure-service-connection'
  resourceGroupName: 'rg-containers'
  location: 'East US'
  containerInstanceName: 'myapp-$(Build.BuildId)'

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  displayName: Build and Push Docker Image
  jobs:
  - job: Build
    displayName: Build Docker Image
    steps:
    - task: Docker@2
      displayName: Build and push Docker image to ACR
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          latest

- stage: Deploy
  displayName: Deploy to ACI
  dependsOn: Build
  jobs:
  - job: Deploy
    displayName: Deploy to Azure Container Instances
    steps:
    - task: AzureCLI@2
      displayName: Deploy to ACI
      inputs:
        azureSubscription: $(azureSubscription)
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          az container create \\
            --resource-group $(resourceGroupName) \\
            --name $(containerInstanceName) \\
            --image $(containerRegistry)/$(imageRepository):$(tag) \\
            --dns-name-label $(containerInstanceName) \\
            --ports 80 \\
            --cpu 1 \\
            --memory 1.5 \\
            --environment-variables ENVIRONMENT=production
'''
        return pipeline_yaml

    def simulate_pipeline_run(self, build_id: str):
        """Simulate ACI pipeline run"""
        run_id = f"aci-run-{build_id}"

        print(f"🔨 Building Docker image for ACI deployment (Build {build_id})...")
        image_tag = f"myregistry.azurecr.io/myapp:{build_id}"

        # Simulate ACI deployment
        print(f"🚀 Deploying to Azure Container Instances...")
        aci_container = {
            'name': f"myapp-{build_id}",
            'image': image_tag,
            'status': 'Running',
            'fqdn': f"myapp-{build_id}.eastus.azurecontainer.io",
            'cpu': 1.0,
            'memory': 1.5,
            'ports': [80],
            'created_date': datetime.now()
        }
        self.aci_containers.append(aci_container)
        print(f"✅ ACI container created: {aci_container['name']}")
        print(f"🌐 Available at: http://{aci_container['fqdn']}")

        # Record pipeline run
        pipeline_run = {
            'run_id': run_id,
            'build_id': build_id,
            'status': 'Succeeded',
            'container_name': aci_container['name'],
            'fqdn': aci_container['fqdn'],
            'completed_date': datetime.now()
        }
        self.pipeline_runs.append(pipeline_run)

        return pipeline_run

    def list_aci_containers(self):
        """List ACI containers"""
        print("\n🏗️ Azure Container Instances:")
        for container in self.aci_containers:
            print(f"  {container['name']}")
            print(f"    Image: {container['image']}")
            print(f"    Status: {container['status']}")
            print(f"    FQDN: {container['fqdn']}")
            print(f"    Resources: {container['cpu']} CPU, {container['memory']}GB Memory")

# Initialize Docker ACR ACI Pipeline
daci_pipeline = DockerACRACIPipeline()

# Generate pipeline configuration
print("📄 Azure DevOps Pipeline YAML for ACI:")
aci_yaml = daci_pipeline.generate_pipeline_yaml()
print(aci_yaml[:400] + "...")

# Simulate pipeline runs
for i in range(2):
    build_id = f"aci{random.randint(100, 999)}"
    print(f"\n🚀 ACI Pipeline Run #{i+1} (Build ID: {build_id})")
    daci_pipeline.simulate_pipeline_run(build_id)

# List ACI containers
daci_pipeline.list_aci_containers()

# ============================================================================
# 9. CI/CD PIPELINE FOR .NET APPLICATION TO AZURE APP SERVICE
# ============================================================================

print("\n\n🔷 9. CI/CD PIPELINE: .NET APP TO AZURE APP SERVICE")
print("=" * 50)

class DotNetAppServicePipeline:
    def __init__(self):
        self.pipeline_runs = []
        self.deployments = []

    def generate_pipeline_yaml(self):
        """Generate Azure DevOps pipeline YAML for .NET to App Service"""
        pipeline_yaml = '''
trigger:
- main

variables:
  buildConfiguration: 'Release'
  azureSubscription: 'azure-service-connection'
  webAppName: 'my-dotnet-webapp'
  environmentName: 'Production'

pool:
  vmImage: 'windows-latest'

stages:
- stage: Build
  displayName: Build .NET Application
  jobs:
  - job: Build
    displayName: Build
    steps:
    - task: UseDotNet@2
      displayName: 'Use .NET 8.0'
      inputs:
        packageType: 'sdk'
        version: '8.0.x'

    - task: DotNetCoreCLI@2
      displayName: 'Restore packages'
      inputs:
        command: 'restore'
        projects: '**/*.csproj'

    - task: DotNetCoreCLI@2
      displayName: 'Build application'
      inputs:
        command: 'build'
        projects: '**/*.csproj'
        arguments: '--configuration $(buildConfiguration) --no-restore'

    - task: DotNetCoreCLI@2
      displayName: 'Run unit tests'
      inputs:
        command: 'test'
        projects: '**/*Tests/*.csproj'
        arguments: '--configuration $(buildConfiguration) --no-build --logger trx --collect:"XPlat Code Coverage"'

    - task: DotNetCoreCLI@2
      displayName: 'Publish application'
      inputs:
        command: 'publish'
        projects: '**/*.csproj'
        arguments: '--configuration $(buildConfiguration) --output $(Build.ArtifactStagingDirectory)'
        publishWebProjects: true
        zipAfterPublish: true

    - task: PublishBuildArtifacts@1
      displayName: 'Publish artifact'
      inputs:
        pathToPublish: '$(Build.ArtifactStagingDirectory)'
        artifactName: 'drop'

- stage: Deploy
  displayName: Deploy to Azure App Service
  dependsOn: Build
  jobs:
  - deployment: Deploy
    displayName: Deploy to App Service
    environment: $(environmentName)
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            displayName: 'Deploy to Azure Web App'
            inputs:
              azureSubscription: $(azureSubscription)
              appType: 'webApp'
              appName: $(webAppName)
              package: '$(Pipeline.Workspace)/drop/**/*.zip'
              deploymentMethod: 'auto'
'''
        return pipeline_yaml

    def generate_app_settings(self):
        """Generate App Service configuration"""
        app_settings = {
            "ASPNETCORE_ENVIRONMENT": "Production",
            "ConnectionStrings__DefaultConnection": "Server=tcp:prod-db.database.windows.net;Database=MyApp;Authentication=Active Directory Default;",
            "ApplicationInsights__ConnectionString": "InstrumentationKey=12345678-1234-1234-1234-123456789012",
            "Logging__LogLevel__Default": "Information",
            "Logging__LogLevel__Microsoft.AspNetCore": "Warning"
        }
        return app_settings

    def simulate_pipeline_run(self, build_id: str):
        """Simulate .NET App Service pipeline run"""
        run_id = f"dotnet-run-{build_id}"

        print(f"🔨 Building .NET application (Build {build_id})...")
        print(f"  - Restoring NuGet packages...")
        print(f"  - Building solution...")
        print(f"  - Running unit tests... ✅ 15 tests passed")
        print(f"  - Publishing application...")

        # Simulate deployment
        print(f"🚀 Deploying to Azure App Service...")
        deployment = {
            'deployment_id': f"deploy-{build_id}",
            'app_name': f"my-dotnet-webapp-{build_id}",
            'build_id': build_id,
            'url': f"https://my-dotnet-webapp-{build_id}.azurewebsites.net",
            'status': 'Running',
            'deployment_date': datetime.now(),
            'app_settings': self.generate_app_settings()
        }
        self.deployments.append(deployment)
        print(f"✅ Deployed successfully to: {deployment['url']}")

        # Record pipeline run
        pipeline_run = {
            'run_id': run_id,
            'build_id': build_id,
            'status': 'Succeeded',
            'build_duration': f"{random.randint(2, 8)} minutes",
            'deploy_duration': f"{random.randint(1, 3)} minutes",
            'tests_passed': random.randint(10, 20),
            'app_url': deployment['url']
        }
        self.pipeline_runs.append(pipeline_run)

        return pipeline_run

    def list_deployments(self):
        """List App Service deployments"""
        print("\n🌐 Azure App Service Deployments:")
        for deployment in self.deployments:
            print(f"  {deployment['app_name']}")
            print(f"    URL: {deployment['url']}")
            print(f"    Status: {deployment['status']}")
            print(f"    Deployed: {deployment['deployment_date'].strftime('%Y-%m-%d %H:%M:%S')}")

# Initialize .NET App Service Pipeline
dotnet_pipeline = DotNetAppServicePipeline()

# Generate pipeline configuration
print("📄 Azure DevOps Pipeline YAML for .NET App Service:")
dotnet_yaml = dotnet_pipeline.generate_pipeline_yaml()
print(dotnet_yaml[:500] + "...")

# Generate app settings
print("\n⚙️ App Service Configuration:")
app_settings = dotnet_pipeline.generate_app_settings()
for key, value in list(app_settings.items())[:3]:
    print(f"  {key}: {value}")
print("  ... and more")

# Simulate pipeline runs
for i in range(2):
    build_id = f"net{random.randint(1000, 9999)}"
    print(f"\n🚀 .NET Pipeline Run #{i+1} (Build ID: {build_id})")
    dotnet_pipeline.simulate_pipeline_run(build_id)

# List deployments
dotnet_pipeline.list_deployments()

# ============================================================================
# 10. CI/CD PIPELINE FOR REACT APPLICATION TO AZURE VM
# ============================================================================

print("\n\n⚛️ 10. CI/CD PIPELINE: REACT APP TO AZURE VM")
print("=" * 50)

class ReactVMPipeline:
    def __init__(self):
        self.pipeline_runs = []
        self.vm_deployments = []

    def generate_pipeline_yaml(self):
        """Generate Azure DevOps pipeline YAML for React to VM"""
        pipeline_yaml = '''
trigger:
- main

variables:
  nodeVersion: '18.x'
  vmServiceConnection: 'vm-service-connection'
  vmResourceGroup: 'rg-vms'
  vmName: 'react-app-vm'
  deploymentPath: '/var/www/myapp'

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  displayName: Build React Application
  jobs:
  - job: Build
    displayName: Build
    steps:
    - task: NodeTool@0
      displayName: 'Use Node.js $(nodeVersion)'
      inputs:
        versionSpec: $(nodeVersion)

    - script: |
        npm ci
        npm run lint
        npm run test -- --coverage --watchAll=false
        npm run build
      displayName: 'Install, Lint, Test, and Build'
      workingDirectory: '$(Build.SourcesDirectory)'

    - task: PublishTestResults@2
      displayName: 'Publish test results'
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: 'coverage/junit.xml'
        mergeTestResults: true

    - task: PublishCodeCoverageResults@1
      displayName: 'Publish code coverage'
      inputs:
        codeCoverageTool: 'Cobertura'
        summaryFileLocation: 'coverage/cobertura-coverage.xml'

    - task: ArchiveFiles@2
      displayName: 'Archive build files'
      inputs:
        rootFolderOrFile: '$(Build.SourcesDirectory)/build'
        includeRootFolder: false
        archiveType: 'tar'
        tarCompression: 'gz'
        archiveFile: '$(Build.ArtifactStagingDirectory)/react-app.tar.gz'

    - task: PublishBuildArtifacts@1
      displayName: 'Publish artifact'
      inputs:
        pathToPublish: '$(Build.ArtifactStagingDirectory)'
        artifactName: 'react-build'

- stage: Deploy
  displayName: Deploy to Azure VM
  dependsOn: Build
  jobs:
  - deployment: Deploy
    displayName: Deploy to VM
    environment: 'Production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: DownloadBuildArtifacts@0
            displayName: 'Download artifacts'
            inputs:
              buildType: 'current'
              downloadType: 'single'
              artifactName: 'react-build'

          - task: CopyFilesOverSSH@0
            displayName: 'Copy files to VM'
            inputs:
              sshEndpoint: $(vmServiceConnection)
              sourceFolder: '$(System.ArtifactsDirectory)/react-build'
              contents: 'react-app.tar.gz'
              targetFolder: '/tmp'

          - task: SSH@0
            displayName: 'Deploy on VM'
            inputs:
              sshEndpoint: $(vmServiceConnection)
              runOptions: 'inline'
              inline: |
                sudo systemctl stop nginx
                sudo rm -rf $(deploymentPath)/*
                sudo mkdir -p $(deploymentPath)
                sudo tar -xzf /tmp/react-app.tar.gz -C $(deploymentPath)
                sudo chown -R www-data:www-data $(deploymentPath)
                sudo systemctl start nginx
                sudo systemctl reload nginx
                echo "Deployment completed successfully"
'''
        return pipeline_yaml

    def generate_nginx_config(self):
        """Generate Nginx configuration for React app"""
        nginx_config = '''
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/myapp;
    index index.html;

    # Handle React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static assets caching
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;
}
'''
        return nginx_config

    def generate_package_json(self):
        """Generate sample package.json for React app"""
        package_json = {
            "name": "my-react-app",
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0",
                "axios": "^1.3.0"
            },
            "devDependencies": {
                "@testing-library/jest-dom": "^5.16.5",
                "@testing-library/react": "^13.4.0",
                "@testing-library/user-event": "^14.4.3",
                "react-scripts": "5.0.1",
                "eslint": "^8.0.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "lint": "eslint src/",
                "eject": "react-scripts eject"
            }
        }
        return package_json

    def simulate_pipeline_run(self, build_id: str):
        """Simulate React VM pipeline run"""
        run_id = f"react-run-{build_id}"

        print(f"🔨 Building React application (Build {build_id})...")
        print(f"  - Installing npm packages...")
        print(f"  - Running ESLint... ✅ No issues found")
        print(f"  - Running tests... ✅ {random.randint(15, 25)} tests passed")
        print(f"  - Building for production... ✅ Build optimized")

        # Calculate build metrics
        bundle_size = f"{random.randint(500, 1500)}KB"
        test_coverage = f"{random.randint(75, 95)}%"

        # Simulate VM deployment
        print(f"🚀 Deploying to Azure VM...")
        print(f"  - Copying files to VM...")
        print(f"  - Stopping Nginx...")
        print(f"  - Extracting build files...")
        print(f"  - Starting Nginx...")

        vm_deployment = {
            'deployment_id': f"vm-deploy-{build_id}",
            'build_id': build_id,
            'vm_name': f"react-vm-{build_id}",
            'url': f"http://react-vm-{build_id}.eastus.cloudapp.azure.com",
            'bundle_size': bundle_size,
            'test_coverage': test_coverage,
            'status': 'Running',
            'deployment_date': datetime.now()
        }
        self.vm_deployments.append(vm_deployment)
        print(f"✅ Deployed successfully to: {vm_deployment['url']}")

        # Record pipeline run
        pipeline_run = {
            'run_id': run_id,
            'build_id': build_id,
            'status': 'Succeeded',
            'bundle_size': bundle_size,
            'test_coverage': test_coverage,
            'build_duration': f"{random.randint(3, 8)} minutes",
            'deploy_duration': f"{random.randint(1, 4)} minutes",
            'vm_url': vm_deployment['url']
        }
        self.pipeline_runs.append(pipeline_run)

        return pipeline_run

    def list_vm_deployments(self):
        """List VM deployments"""
        print("\n💻 Azure VM Deployments:")
        for deployment in self.vm_deployments:
            print(f"  {deployment['vm_name']}")
            print(f"    URL: {deployment['url']}")
            print(f"    Bundle Size: {deployment['bundle_size']}")
            print(f"    Test Coverage: {deployment['test_coverage']}")
            print(f"    Status: {deployment['status']}")

# Initialize React VM Pipeline
react_pipeline = ReactVMPipeline()

# Generate pipeline configuration
print("📄 Azure DevOps Pipeline YAML for React to VM:")
react_yaml = react_pipeline.generate_pipeline_yaml()
print(react_yaml[:400] + "...")

# Generate supporting files
print("\n⚙️ Nginx Configuration:")
nginx_config = react_pipeline.generate_nginx_config()
print(nginx_config[:200] + "...")

print("\n📦 Package.json:")
package_json = react_pipeline.generate_package_json()
print(json.dumps(package_json, indent=2)[:300] + "...")

# Simulate pipeline runs
for i in range(2):
    build_id = f"react{random.randint(100, 999)}"
    print(f"\n🚀 React Pipeline Run #{i+1} (Build ID: {build_id})")
    react_pipeline.simulate_pipeline_run(build_id)

# List VM deployments
react_pipeline.list_vm_deployments()

# ============================================================================
# COMPREHENSIVE DASHBOARD AND SUMMARY
# ============================================================================

print("\n\n📊 COMPREHENSIVE AZURE DEVOPS DASHBOARD")
print("=" * 60)

def create_comprehensive_dashboard():
    """Create a comprehensive dashboard showing all pipeline metrics"""

    # Collect all pipeline data
    all_runs = []

    # Add Docker ACR/AKS runs
    for run in dak_pipeline.pipeline_runs:
        all_runs.append({
            'type': 'Docker→ACR→AKS',
            'build_id': run['build_id'],
            'status': run['status'],
            'duration': (run['end_time'] - run['start_time']).total_seconds() / 60,
            'date': run['start_time']
        })

    # Add Docker ACR/ACI runs
    for run in daci_pipeline.pipeline_runs:
        all_runs.append({
            'type': 'Docker→ACR→ACI',
            'build_id': run['build_id'],
            'status': run['status'],
            'duration': random.randint(3, 8),  # Simulated duration
            'date': run['completed_date']
        })

    # Add .NET App Service runs
    for run in dotnet_pipeline.pipeline_runs:
        build_duration = int(run['build_duration'].split()[0])
        deploy_duration = int(run['deploy_duration'].split()[0])
        all_runs.append({
            'type': '.NET→App Service',
            'build_id': run['build_id'],
            'status': run['status'],
            'duration': build_duration + deploy_duration,
            'date': datetime.now()
        })

    # Add React VM runs
    for run in react_pipeline.pipeline_runs:
        build_duration = int(run['build_duration'].split()[0])
        deploy_duration = int(run['deploy_duration'].split()[0])
        all_runs.append({
            'type': 'React→Azure VM',
            'build_id': run['build_id'],
            'status': run['status'],
            'duration': build_duration + deploy_duration,
            'date': datetime.now()
        })

    # Create DataFrame
    df = pd.DataFrame(all_runs)

    if len(df) > 0:
        # Summary statistics
        print(f"📈 Pipeline Summary Statistics")
        print(f"Total Pipelines: {len(df)}")
        print(f"Successful Runs: {len(df[df['status'] == 'Succeeded'])}")
        print(f"Average Duration: {df['duration'].mean():.1f} minutes")
        print(f"Pipeline Types: {df['type'].nunique()}")

        # Visualizations
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Pipeline runs by type
        type_counts = df['type'].value_counts()
        axes[0, 0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Pipeline Runs by Type')

        # Pipeline duration by type
        df.boxplot(column='duration', by='type', ax=axes[0, 1])
        axes[0, 1].set_title('Pipeline Duration by Type')
        axes[0, 1].set_xlabel('Pipeline Type')
        axes[0, 1].set_ylabel('Duration (minutes)')

        # Success rate by type
        success_rate = df.groupby('type')['status'].apply(lambda x: (x == 'Succeeded').mean() * 100)
        axes[1, 0].bar(range(len(success_rate)), success_rate.values, color='green', alpha=0.7)
        axes[1, 0].set_title('Success Rate by Pipeline Type')
        axes[1, 0].set_xticks(range(len(success_rate)))
        axes[1, 0].set_xticklabels(success_rate.index, rotation=45)
        axes[1, 0].set_ylabel('Success Rate (%)')

        # Pipeline runs over time (simulated)
        timeline_data = df.groupby('type').size()
        axes[1, 1].bar(timeline_data.index, timeline_data.values, color='skyblue')
        axes[1, 1].set_title('Total Runs by Pipeline Type')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].set_ylabel('Number of Runs')

        plt.suptitle('Azure DevOps Comprehensive Dashboard', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.show()

        # Display detailed table
        print(f"\n📋 Detailed Pipeline Runs:")
        print(tabulate(df, headers='keys', tablefmt='psql'))

    else:
        print("No pipeline run data available to display dashboard.")


create_comprehensive_dashboard()


print("\n\n🎉 AZURE DEVOPS TUTORIAL COMPLETE!")
print("=" * 50)
print("""
This notebook simulated and demonstrated key Azure DevOps features:
1. Work Items Dashboard and Queries
2. Pipeline Variables Configuration
3. Variable and Task Groups
4. Service Connections
5. Self-Hosted Agents (Simulation)
6. Release Pipeline Approvals
7. CI/CD Pipeline: Docker to ACR and AKS
8. CI/CD Pipeline: Docker to ACR and ACI
9. CI/CD Pipeline: .NET App to Azure App Service
10. CI/CD Pipeline: React App to Azure VM

You can adapt these simulations and YAML configurations for your own projects and learning!
""")
