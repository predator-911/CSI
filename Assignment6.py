# Kubernetes Concepts Implementation and Simulation in Google Colab
# This notebook demonstrates Kubernetes concepts with YAML examples and simulations

# Install required packages
!pip install kubernetes pyyaml tabulate matplotlib seaborn

import yaml
import json
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import time
import random

print("=== KUBERNETES CONCEPTS IN GOOGLE COLAB ===\n")

# =============================================================================
# 1. REPLICA SET vs REPLICATION CONTROLLER vs DEPLOYMENT
# =============================================================================

print("1. REPLICA SET vs REPLICATION CONTROLLER vs DEPLOYMENT")
print("=" * 60)

# Replication Controller YAML
replication_controller_yaml = """
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx-rc
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 80
"""

# Replica Set YAML
replica_set_yaml = """
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-rs
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 80
"""

# Deployment YAML
deployment_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 80
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
"""

print("Replication Controller YAML:")
print(replication_controller_yaml)
print("\nReplica Set YAML:")
print(replica_set_yaml)
print("\nDeployment YAML:")
print(deployment_yaml)

# Comparison table
comparison_data = [
    ["Feature", "Replication Controller", "Replica Set", "Deployment"],
    ["API Version", "v1", "apps/v1", "apps/v1"],
    ["Selector", "Equality-based", "Set-based", "Set-based"],
    ["Rolling Updates", "Manual", "Manual", "Automatic"],
    ["Rollback", "No", "No", "Yes"],
    ["History", "No", "No", "Yes"],
    ["Status", "Legacy", "Current", "Recommended"],
    ["Use Case", "Simple replication", "Advanced selection", "Production deployments"]
]

print("\n" + "=" * 80)
print("COMPARISON TABLE:")
print(tabulate(comparison_data, headers="firstrow", tablefmt="grid"))

# =============================================================================
# 2. KUBERNETES SERVICE TYPES
# =============================================================================

print("\n\n2. KUBERNETES SERVICE TYPES")
print("=" * 40)

# ClusterIP Service
clusterip_service = """
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
"""

# NodePort Service
nodeport_service = """
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
    protocol: TCP
"""

# LoadBalancer Service
loadbalancer_service = """
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
"""

print("ClusterIP Service:")
print(clusterip_service)
print("\nNodePort Service:")
print(nodeport_service)
print("\nLoadBalancer Service:")
print(loadbalancer_service)

# Service types comparison
service_comparison = [
    ["Service Type", "Accessibility", "Use Case", "External IP"],
    ["ClusterIP", "Internal only", "Internal communication", "No"],
    ["NodePort", "External via Node IP", "Development/Testing", "Node IP"],
    ["LoadBalancer", "External via Load Balancer", "Production", "Yes"]
]

print("\nSERVICE TYPES COMPARISON:")
print(tabulate(service_comparison, headers="firstrow", tablefmt="grid"))

# =============================================================================
# 3. PERSISTENT VOLUME (PV) AND PERSISTENT VOLUME CLAIM (PVC)
# =============================================================================

print("\n\n3. PERSISTENT VOLUME (PV) AND PERSISTENT VOLUME CLAIM (PVC)")
print("=" * 60)

# Persistent Volume YAML
persistent_volume_yaml = """
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  hostPath:
    path: /data/pv-storage
"""

# Persistent Volume Claim YAML
persistent_volume_claim_yaml = """
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
"""

# Pod with PVC
pod_with_pvc_yaml = """
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-storage
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - mountPath: /data
      name: storage
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: pvc-storage
"""

print("Persistent Volume YAML:")
print(persistent_volume_yaml)
print("\nPersistent Volume Claim YAML:")
print(persistent_volume_claim_yaml)
print("\nPod with PVC YAML:")
print(pod_with_pvc_yaml)

# =============================================================================
# 4. AZURE KUBERNETES SERVICE (AKS) - SIMULATION
# =============================================================================

print("\n\n4. AZURE KUBERNETES SERVICE (AKS) - SIMULATION")
print("=" * 50)

class AKSClusterSimulator:
    def __init__(self, name, node_count=3, vm_size="Standard_D2_v3"):
        self.name = name
        self.node_count = node_count
        self.vm_size = vm_size
        self.status = "Creating"
        self.created_time = datetime.now()
        self.version = "1.25.6"
        
    def create_cluster(self):
        print(f"Creating AKS cluster '{self.name}'...")
        print(f"Node count: {self.node_count}")
        print(f"VM size: {self.vm_size}")
        print(f"Kubernetes version: {self.version}")
        time.sleep(2)  # Simulate creation time
        self.status = "Running"
        print(f"✓ Cluster '{self.name}' created successfully!")
        
    def scale_cluster(self, new_node_count):
        print(f"Scaling cluster '{self.name}' from {self.node_count} to {new_node_count} nodes...")
        time.sleep(1)
        self.node_count = new_node_count
        print(f"✓ Cluster scaled successfully!")
        
    def upgrade_cluster(self, new_version):
        print(f"Upgrading cluster '{self.name}' from {self.version} to {new_version}...")
        time.sleep(2)
        self.version = new_version
        print(f"✓ Cluster upgraded successfully!")
        
    def get_status(self):
        return {
            "name": self.name,
            "status": self.status,
            "node_count": self.node_count,
            "vm_size": self.vm_size,
            "version": self.version,
            "created": self.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }

# Simulate AKS operations
aks_cluster = AKSClusterSimulator("my-aks-cluster")
aks_cluster.create_cluster()
print("\nCluster Status:")
print(json.dumps(aks_cluster.get_status(), indent=2))

# Simulate scaling
aks_cluster.scale_cluster(5)

# Simulate upgrade
aks_cluster.upgrade_cluster("1.26.2")

# =============================================================================
# 5. HEALTH PROBES (LIVENESS AND READINESS)
# =============================================================================

print("\n\n5. HEALTH PROBES (LIVENESS AND READINESS)")
print("=" * 45)

# Deployment with health probes
deployment_with_probes = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-probes
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: nginx:1.16
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
"""

print("Deployment with Health Probes:")
print(deployment_with_probes)

# Probe types comparison
probe_comparison = [
    ["Probe Type", "Purpose", "Action on Failure", "When to Use"],
    ["Liveness", "Check if container is alive", "Restart container", "Detect deadlocks"],
    ["Readiness", "Check if container is ready", "Remove from service", "Startup checks"],
    ["Startup", "Check if container has started", "Kill container", "Slow starting apps"]
]

print("\nHEALTH PROBES COMPARISON:")
print(tabulate(probe_comparison, headers="firstrow", tablefmt="grid"))

# =============================================================================
# 6. TAINTS AND TOLERATIONS
# =============================================================================

print("\n\n6. TAINTS AND TOLERATIONS")
print("=" * 30)

# Taint command simulation
print("Applying taint to node:")
print("kubectl taint nodes node1 key=value:NoSchedule")

# Toleration YAML
toleration_yaml = """
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-toleration
spec:
  containers:
  - name: app
    image: nginx
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
"""

print("\nPod with Toleration:")
print(toleration_yaml)

# Taint effects comparison
taint_effects = [
    ["Effect", "Description", "Behavior"],
    ["NoSchedule", "Pods without toleration won't be scheduled", "Existing pods remain"],
    ["PreferNoSchedule", "Scheduler tries to avoid scheduling", "Soft constraint"],
    ["NoExecute", "Pods without toleration are evicted", "Existing pods affected"]
]

print("\nTAINT EFFECTS:")
print(tabulate(taint_effects, headers="firstrow", tablefmt="grid"))

# =============================================================================
# 7. HORIZONTAL POD AUTOSCALER (HPA)
# =============================================================================

print("\n\n7. HORIZONTAL POD AUTOSCALER (HPA)")
print("=" * 40)

# HPA YAML
hpa_yaml = """
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
"""

print("Horizontal Pod Autoscaler YAML:")
print(hpa_yaml)

# HPA Simulation
class HPASimulator:
    def __init__(self, min_replicas=2, max_replicas=10, target_cpu=70):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu
        self.current_replicas = min_replicas
        self.cpu_usage = []
        self.replica_history = []
        
    def simulate_load(self, duration_minutes=30):
        print(f"Simulating HPA behavior for {duration_minutes} minutes...")
        
        for minute in range(duration_minutes):
            # Simulate CPU usage pattern
            if minute < 10:
                cpu = random.uniform(30, 50)  # Low load
            elif minute < 20:
                cpu = random.uniform(80, 95)  # High load
            else:
                cpu = random.uniform(40, 60)  # Normal load
                
            self.cpu_usage.append(cpu)
            
            # HPA decision logic
            if cpu > self.target_cpu and self.current_replicas < self.max_replicas:
                self.current_replicas = min(self.current_replicas + 1, self.max_replicas)
            elif cpu < self.target_cpu - 10 and self.current_replicas > self.min_replicas:
                self.current_replicas = max(self.current_replicas - 1, self.min_replicas)
                
            self.replica_history.append(self.current_replicas)
            
        self.plot_hpa_behavior()
        
    def plot_hpa_behavior(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # CPU Usage plot
        ax1.plot(range(len(self.cpu_usage)), self.cpu_usage, 'b-', linewidth=2)
        ax1.axhline(y=self.target_cpu, color='r', linestyle='--', label=f'Target CPU ({self.target_cpu}%)')
        ax1.set_ylabel('CPU Usage (%)')
        ax1.set_title('HPA Simulation - CPU Usage vs Pod Replicas')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Replica count plot
        ax2.plot(range(len(self.replica_history)), self.replica_history, 'g-', linewidth=2, marker='o')
        ax2.axhline(y=self.min_replicas, color='orange', linestyle='--', label=f'Min Replicas ({self.min_replicas})')
        ax2.axhline(y=self.max_replicas, color='red', linestyle='--', label=f'Max Replicas ({self.max_replicas})')
        ax2.set_ylabel('Pod Replicas')
        ax2.set_xlabel('Time (minutes)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Run HPA simulation
hpa_sim = HPASimulator()
hpa_sim.simulate_load(30)

# =============================================================================
# 8. IMPLEMENTATION FEASIBILITY IN COLAB
# =============================================================================

print("\n\n8. IMPLEMENTATION FEASIBILITY IN GOOGLE COLAB")
print("=" * 50)

implementation_feasibility = [
    ["Concept", "Colab Implementation", "Status", "Alternative"],
    ["Replica Sets/Controllers", "YAML examples only", "❌ Limited", "minikube locally"],
    ["Deployments", "YAML examples only", "❌ Limited", "minikube locally"],
    ["Services", "YAML examples only", "❌ Limited", "minikube locally"],
    ["PV/PVC", "YAML examples only", "❌ Limited", "minikube locally"],
    ["AKS Management", "Simulation possible", "✅ Partial", "Azure CLI"],
    ["Health Probes", "YAML examples only", "❌ Limited", "minikube locally"],
    ["Taints/Tolerations", "YAML examples only", "❌ Limited", "minikube locally"],
    ["HPA", "Simulation possible", "✅ Partial", "Full cluster"],
    ["Monitoring", "Simulation possible", "✅ Partial", "Prometheus/Grafana"]
]

print(tabulate(implementation_feasibility, headers="firstrow", tablefmt="grid"))

# =============================================================================
# 9. RECOMMENDED LEARNING PATH
# =============================================================================

print("\n\n9. RECOMMENDED LEARNING PATH")
print("=" * 35)

learning_steps = [
    "1. Study YAML configurations (this notebook)",
    "2. Install minikube locally for hands-on practice",
    "3. Practice with kubectl commands",
    "4. Set up Azure AKS cluster for production scenarios",
    "5. Implement monitoring with Prometheus/Grafana",
    "6. Practice CI/CD with Kubernetes deployments",
    "7. Learn advanced topics: Helm, Operators, Service Mesh"
]

for step in learning_steps:
    print(step)

print("\n" + "=" * 80)
print("SUMMARY:")
print("- Most Kubernetes concepts require an actual cluster")
print("- Google Colab is excellent for learning YAML configurations")
print("- Use simulations to understand HPA and cluster management")
print("- For hands-on practice, use minikube locally or cloud providers")
print("- This notebook provides a comprehensive foundation for Kubernetes learning")
print("=" * 80)

# Save YAML files for reference
yaml_files = {
    'replication-controller.yaml': replication_controller_yaml,
    'replica-set.yaml': replica_set_yaml,
    'deployment.yaml': deployment_yaml,
    'services.yaml': clusterip_service + '---\n' + nodeport_service + '---\n' + loadbalancer_service,
    'storage.yaml': persistent_volume_yaml + '---\n' + persistent_volume_claim_yaml,
    'health-probes.yaml': deployment_with_probes,
    'tolerations.yaml': toleration_yaml,
    'hpa.yaml': hpa_yaml
}

print("\nYAML files created for download:")
for filename, content in yaml_files.items():
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✓ {filename}")

print("\nTo download these files, use the Files panel in Colab or run:")
print("from google.colab import files")
print("files.download('deployment.yaml')  # Replace with desired filename")
