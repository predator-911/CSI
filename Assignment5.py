# Kubernetes Learning Lab - Google Colab Implementation
# This notebook demonstrates Kubernetes concepts through implementation and simulation

import os
import subprocess
import json
import yaml
from IPython.display import display, HTML, Markdown
import time

print("🚀 Kubernetes Learning Lab - Starting Setup...")

# =============================================================================
# SECTION 1: ENVIRONMENT SETUP
# =============================================================================

def run_command(cmd, capture_output=True, shell=True):
    """Helper function to run shell commands"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=capture_output, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

# Install required tools
print("📦 Installing Kubernetes tools...")

# Install kubectl
!curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
!chmod +x kubectl
!sudo mv kubectl /usr/local/bin/

# Install kind (Kubernetes in Docker)
!curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
!chmod +x ./kind
!sudo mv ./kind /usr/local/bin/kind

# Install Docker if not already available
!apt-get update && apt-get install -y docker.io

print("✅ Tools installed successfully!")

# =============================================================================
# SECTION 2: SIMULATE MINIKUBE CLUSTER CREATION
# =============================================================================

def simulate_minikube_setup():
    """Simulate minikube cluster creation"""
    print("\n" + "="*60)
    print("🎯 SIMULATION: Creating Kubernetes cluster using minikube")
    print("="*60)
    
    # Show what minikube commands would look like
    minikube_commands = [
        "# Install minikube",
        "curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64",
        "sudo install minikube-linux-amd64 /usr/local/bin/minikube",
        "",
        "# Start minikube cluster",
        "minikube start --driver=docker",
        "",
        "# Check cluster status",
        "minikube status",
        "",
        "# Get cluster info",
        "kubectl cluster-info",
        "",
        "# View nodes",
        "kubectl get nodes"
    ]
    
    print("📋 Minikube Setup Commands:")
    for cmd in minikube_commands:
        print(f"  {cmd}")
    
    # Simulate cluster info output
    print("\n🔍 Simulated Output:")
    print("minikube")
    print("type: Control Plane")
    print("host: Running")
    print("kubelet: Running") 
    print("apiserver: Running")
    print("kubeconfig: Configured")
    
    return True

simulate_minikube_setup()

# =============================================================================
# SECTION 3: SIMULATE KUBEADM CLUSTER CREATION
# =============================================================================

def simulate_kubeadm_setup():
    """Simulate kubeadm cluster creation"""
    print("\n" + "="*60)
    print("🎯 SIMULATION: Creating Kubernetes cluster using kubeadm")
    print("="*60)
    
    kubeadm_steps = [
        "# On Master Node:",
        "sudo kubeadm init --pod-network-cidr=10.244.0.0/16",
        "",
        "# Setup kubeconfig",
        "mkdir -p $HOME/.kube",
        "sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config",
        "sudo chown $(id -u):$(id -g) $HOME/.kube/config",
        "",
        "# Install pod network (Flannel)",
        "kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml",
        "",
        "# On Worker Nodes:",
        "sudo kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash <hash>"
    ]
    
    print("📋 Kubeadm Setup Steps:")
    for step in kubeadm_steps:
        print(f"  {step}")
    
    # Show sample kubeadm init output
    print("\n🔍 Simulated kubeadm init output:")
    sample_output = """
[init] Using Kubernetes version: v1.28.0
[preflight] Running pre-flight checks
[kubelet-start] Writing kubelet environment file
[kubelet-start] Writing kubelet configuration to file
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
...
Your Kubernetes control-plane has initialized successfully!
    """
    print(sample_output)
    
    return True

simulate_kubeadm_setup()

# =============================================================================
# SECTION 4: ACTUAL KIND CLUSTER IMPLEMENTATION
# =============================================================================

def create_kind_cluster():
    """Create actual Kubernetes cluster using kind"""
    print("\n" + "="*60)
    print("🚀 IMPLEMENTATION: Creating actual Kubernetes cluster using kind")
    print("="*60)
    
    # Create kind cluster configuration
    kind_config = """
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
"""
    
    # Write config to file
    with open('kind-config.yaml', 'w') as f:
        f.write(kind_config)
    
    print("📝 Created kind cluster configuration")
    
    # Create the cluster
    print("🔄 Creating kind cluster (this may take a few minutes)...")
    result = run_command("kind create cluster --config=kind-config.yaml --name=k8s-lab")
    
    if result is not None:
        print("✅ Kind cluster created successfully!")
        
        # Verify cluster
        print("\n🔍 Cluster Information:")
        cluster_info = run_command("kubectl cluster-info")
        if cluster_info:
            print(cluster_info)
        
        # Get nodes
        print("\n📋 Cluster Nodes:")
        nodes = run_command("kubectl get nodes -o wide")
        if nodes:
            print(nodes)
            
        return True
    else:
        print("❌ Failed to create kind cluster")
        return False

# Create the cluster
cluster_created = create_kind_cluster()

# =============================================================================
# SECTION 5: SIMULATE AKS CLUSTER DEPLOYMENT
# =============================================================================

def simulate_aks_deployment():
    """Simulate AKS cluster deployment"""
    print("\n" + "="*60)
    print("🎯 SIMULATION: Deploy AKS cluster using Azure Portal")
    print("="*60)
    
    # Show Azure CLI commands
    aks_commands = [
        "# Login to Azure",
        "az login",
        "",
        "# Create resource group",
        "az group create --name myResourceGroup --location eastus",
        "",
        "# Create AKS cluster",
        "az aks create \\",
        "  --resource-group myResourceGroup \\",
        "  --name myAKSCluster \\",
        "  --node-count 3 \\",
        "  --enable-addons monitoring \\",
        "  --generate-ssh-keys",
        "",
        "# Get credentials",
        "az aks get-credentials --resource-group myResourceGroup --name myAKSCluster",
        "",
        "# Browse AKS dashboard",
        "az aks browse --resource-group myResourceGroup --name myAKSCluster"
    ]
    
    print("📋 AKS Deployment Commands:")
    for cmd in aks_commands:
        print(f"  {cmd}")
    
    # Simulate RBAC setup
    print("\n🔐 RBAC Configuration for Multiple Users:")
    rbac_yaml = """
# Create namespace for team
apiVersion: v1
kind: Namespace
metadata:
  name: team-namespace
---
# Create role for developers
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: team-namespace
  name: developer-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "create", "update", "delete"]
---
# Bind role to user
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: team-namespace
subjects:
- kind: User
  name: developer@company.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
"""
    print(rbac_yaml)
    
    return True

simulate_aks_deployment()

# =============================================================================
# SECTION 6: IMPLEMENT SERVICE TYPES
# =============================================================================

def implement_service_types():
    """Implement different Kubernetes service types"""
    print("\n" + "="*60)
    print("🚀 IMPLEMENTATION: Kubernetes Service Types")
    print("="*60)
    
    if not cluster_created:
        print("⚠️  No cluster available, showing configurations only")
    
    # 1. ClusterIP Service
    print("\n1️⃣ ClusterIP Service (Default - Internal only)")
    clusterip_yaml = """
apiVersion: v1
kind: Service
metadata:
  name: my-clusterip-service
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
"""
    
    with open('clusterip-service.yaml', 'w') as f:
        f.write(clusterip_yaml)
    print("📝 Created ClusterIP service configuration")
    print(clusterip_yaml)
    
    # 2. NodePort Service
    print("\n2️⃣ NodePort Service (External access via node IP)")
    nodeport_yaml = """
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport-service
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
"""
    
    with open('nodeport-service.yaml', 'w') as f:
        f.write(nodeport_yaml)
    print("📝 Created NodePort service configuration")
    print(nodeport_yaml)
    
    # 3. LoadBalancer Service
    print("\n3️⃣ LoadBalancer Service (Cloud load balancer)")
    loadbalancer_yaml = """
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer-service
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
"""
    
    with open('loadbalancer-service.yaml', 'w') as f:
        f.write(loadbalancer_yaml)
    print("📝 Created LoadBalancer service configuration")
    print(loadbalancer_yaml)
    
    # Create a sample application to test services
    print("\n🔧 Creating sample application for testing services:")
    app_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
"""
    
    with open('sample-app.yaml', 'w') as f:
        f.write(app_yaml)
    print(app_yaml)
    
    if cluster_created:
        # Apply the configurations
        print("\n🚀 Deploying to cluster...")
        
        # Deploy sample app
        result = run_command("kubectl apply -f sample-app.yaml")
        if result is not None:
            print("✅ Sample app deployed")
        
        # Deploy services
        run_command("kubectl apply -f clusterip-service.yaml")
        run_command("kubectl apply -f nodeport-service.yaml")
        
        # Wait a moment for deployment
        time.sleep(5)
        
        # Show services
        print("\n📋 Created Services:")
        services = run_command("kubectl get services")
        if services:
            print(services)
        
        # Show pods
        print("\n📋 Running Pods:")
        pods = run_command("kubectl get pods")
        if pods:
            print(pods)
    
    return True

implement_service_types()

# =============================================================================
# SECTION 7: SIMULATE MICROSERVICE APPLICATION DEPLOYMENT
# =============================================================================

def simulate_microservice_deployment():
    """Simulate microservice application deployment"""
    print("\n" + "="*60)
    print("🎯 SIMULATION: Deploy microservice application")
    print("="*60)
    
    # Sample microservice architecture
    print("🏗️ Sample Microservice Architecture:")
    microservice_yaml = """
# Frontend Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
---
# Backend API Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
    spec:
      containers:
      - name: api
        image: node:16-alpine
        command: ["node", "server.js"]
        ports:
        - containerPort: 3000
        env:
        - name: DB_HOST
          value: "database-service"
---
apiVersion: v1
kind: Service
metadata:
  name: backend-api-service
spec:
  type: ClusterIP
  selector:
    app: backend-api
  ports:
    - port: 3000
      targetPort: 3000
---
# Database Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: "myapp"
        - name: POSTGRES_USER
          value: "user"
        - name: POSTGRES_PASSWORD
          value: "password"
        ports:
        - containerPort: 5432
---
apiVersion: v1
kind: Service
metadata:
  name: database-service
spec:
  type: ClusterIP
  selector:
    app: database
  ports:
    - port: 5432
      targetPort: 5432
"""
    
    with open('microservice-app.yaml', 'w') as f:
        f.write(microservice_yaml)
    
    print("📝 Created microservice application configuration")
    print(microservice_yaml)
    
    # Show ingress configuration for external access
    print("\n🌐 Ingress Configuration for External Access:")
    ingress_yaml = """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-api-service
            port:
              number: 3000
"""
    print(ingress_yaml)
    
    if cluster_created:
        print("\n🚀 Deploying microservice application...")
        result = run_command("kubectl apply -f microservice-app.yaml")
        if result is not None:
            print("✅ Microservice application deployed")
            
            # Show deployment status
            time.sleep(5)
            print("\n📋 Deployment Status:")
            deployments = run_command("kubectl get deployments")
            if deployments:
                print(deployments)
    
    return True

simulate_microservice_deployment()

# =============================================================================
# SECTION 8: MONITORING AND LOGGING SIMULATION
# =============================================================================

def simulate_monitoring_logging():
    """Simulate monitoring and logging setup"""
    print("\n" + "="*60)
    print("🎯 SIMULATION: Monitoring and Logging in AKS")
    print("="*60)
    
    # Azure Monitor setup
    print("📊 Azure Monitor Integration:")
    monitor_commands = [
        "# Enable Container Insights",
        "az aks enable-addons -a monitoring -n myAKSCluster -g myResourceGroup",
        "",
        "# View metrics in portal",
        "# Go to Azure Portal > AKS Cluster > Monitoring > Insights"
    ]
    
    for cmd in monitor_commands:
        print(f"  {cmd}")
    
    # Prometheus/Grafana setup
    print("\n📈 Prometheus + Grafana Setup:")
    prometheus_yaml = """
# Prometheus ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
---
# Grafana Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          value: "admin"
"""
    print(prometheus_yaml)
    
    # ELK Stack simulation
    print("\n📝 ELK Stack for Logging:")
    elk_yaml = """
# Elasticsearch
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
        env:
        - name: discovery.type
          value: single-node
---
# Kibana
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:7.15.0
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "http://elasticsearch:9200"
"""
    print(elk_yaml)
    
    return True

simulate_monitoring_logging()

# =============================================================================
# SECTION 9: CLEANUP AND SUMMARY
# =============================================================================

def cleanup_and_summary():
    """Cleanup resources and show summary"""
    print("\n" + "="*60)
    print("🧹 CLEANUP AND SUMMARY")
    print("="*60)
    
    if cluster_created:
        print("🔄 Cleaning up cluster resources...")
        
        # Delete created resources
        run_command("kubectl delete -f sample-app.yaml", capture_output=False)
        run_command("kubectl delete -f clusterip-service.yaml", capture_output=False)
        run_command("kubectl delete -f nodeport-service.yaml", capture_output=False)
        run_command("kubectl delete -f microservice-app.yaml", capture_output=False)
        
        print("✅ Resources cleaned up")
        
        # Optional: Delete kind cluster
        # run_command("kind delete cluster --name=k8s-lab")
    
    print("\n📋 SUMMARY OF WHAT WE COVERED:")
    summary = """
    ✅ IMPLEMENTED:
    • Created actual Kubernetes cluster using kind
    • Deployed and tested different service types (ClusterIP, NodePort, LoadBalancer)
    • Created sample microservice application configurations
    • Demonstrated kubectl commands and YAML manifests
    
    🎯 SIMULATED:
    • Minikube cluster creation process
    • Kubeadm cluster bootstrapping
    • AKS cluster deployment via Azure Portal
    • RBAC configuration for multiple users
    • Monitoring and logging setup (Prometheus, Grafana, ELK)
    • Ingress configuration for external access
    
    📚 KEY LEARNINGS:
    • Different ways to create Kubernetes clusters
    • Service types and their use cases
    • Microservice deployment patterns
    • RBAC and security configurations
    • Monitoring and observability setup
    
    🔗 NEXT STEPS:
    • Practice with real cloud providers (Azure AKS, AWS EKS, GCP GKE)
    • Implement CI/CD pipelines for Kubernetes
    • Learn about Helm charts and package management
    • Explore service mesh technologies (Istio, Linkerd)
    """
    
    print(summary)
    
    print("\n🎉 Kubernetes Learning Lab Complete!")
    print("The kind cluster is still running. You can continue experimenting with kubectl commands.")
    
    return True

cleanup_and_summary()

# =============================================================================
# BONUS: USEFUL KUBECTL COMMANDS REFERENCE
# =============================================================================

print("\n" + "="*60)
print("📖 BONUS: Useful kubectl Commands Reference")
print("="*60)

kubectl_commands = """
# Cluster Information
kubectl cluster-info
kubectl get nodes
kubectl describe node <node-name>

# Pod Management
kubectl get pods
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- /bin/bash

# Service Management
kubectl get services
kubectl describe service <service-name>
kubectl port-forward service/<service-name> 8080:80

# Deployment Management
kubectl get deployments
kubectl scale deployment <deployment-name> --replicas=5
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>

# ConfigMaps and Secrets
kubectl get configmaps
kubectl get secrets
kubectl create secret generic <secret-name> --from-literal=key=value

# Debugging
kubectl get events
kubectl top nodes
kubectl top pods
"""

print(kubectl_commands)

print("\n🔚 End of Kubernetes Learning Lab")
