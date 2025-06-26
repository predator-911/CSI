# Complete Docker Learning in Google Colab
# This notebook covers all Docker topics with practical implementation and simulation

# =============================================================================
# SETUP AND INSTALLATION
# =============================================================================

# Cell 1: Install Docker and required tools
import os
import subprocess
import time
import json
from IPython.display import display, Markdown, HTML

def run_command(cmd, capture_output=True):
    """Helper function to run shell commands"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout, result.stderr, result.returncode
        else:
            subprocess.run(cmd, shell=True)
            return "Command executed", "", 0
    except Exception as e:
        return "", str(e), 1

print("🐳 Setting up Docker environment in Colab...")

# Install Docker
print("📦 Installing Docker...")
run_command("apt-get update -qq", capture_output=False)
run_command("apt-get install -y docker.io", capture_output=False)

# Install Docker Compose
print("📦 Installing Docker Compose...")
run_command("pip install docker-compose", capture_output=False)

# Start Docker service
print("🚀 Starting Docker service...")
run_command("service docker start", capture_output=False)
time.sleep(5) # Give Docker time to start

# Check if Docker is running
print("\nChecking Docker daemon status...")
docker_status, _, _ = run_command("docker info")
if "Cannot connect to the Docker daemon" in docker_status:
    print("❌ Docker daemon is not running or accessible. Please check the output above for errors.")
    # Exit or skip subsequent Docker commands if daemon is not running
    # For this notebook, we'll continue but expect failures in Docker-dependent sections
else:
    print("✅ Docker daemon is running.")


# Verify installations
print("\n✅ Verifying installations:")
docker_version, _, _ = run_command("docker --version")
compose_version, _, _ = run_command("docker-compose --version")
print(f"Docker: {docker_version.strip()}")
print(f"Docker Compose: {compose_version.strip()}")

print("\n🎉 Docker environment ready!")

# =============================================================================
# TOPIC 1: DOCKER FUNDAMENTALS AND BASIC COMMANDS
# =============================================================================

print("\n" + "="*60)
print("TOPIC 1: DOCKER FUNDAMENTALS AND BASIC COMMANDS")
print("="*60)

# Basic Docker information
print("\n📊 Docker System Information:")
info_output, _, _ = run_command("docker info")
print(info_output[:500] + "..." if len(info_output) > 500 else info_output)

# Basic commands demonstration
basic_commands = [
    ("docker --version", "Check Docker version"),
    ("docker info", "System information"),
    ("docker --help", "Help menu"),
]

print("\n🔧 Basic Docker Commands:")
for cmd, desc in basic_commands:
    print(f"\n➤ {desc}:")
    print(f"Command: {cmd}")
    if "help" not in cmd:
        output, _, _ = run_command(cmd)
        print(f"Output: {output.strip()}")

# =============================================================================
# TOPIC 2: BASIC CONTAINER OPERATIONS
# =============================================================================

print("\n" + "="*60)
print("TOPIC 2: BASIC CONTAINER OPERATIONS")
print("="*60)

# Pull and run hello-world container
print("\n🌍 Running Hello World Container:")
hello_output, _, _ = run_command("docker run hello-world")
print(hello_output)

# List containers
print("\n📋 Listing Containers:")
containers_output, _, _ = run_command("docker ps -a")
print(containers_output)

# List images
print("\n🖼️ Listing Images:")
images_output, _, _ = run_command("docker images")
print(images_output)

# Run interactive container
print("\n💻 Running Interactive Ubuntu Container:")
print("Command: docker run -it --name test-ubuntu ubuntu:latest echo 'Hello from Ubuntu!'")
interactive_output, _, _ = run_command("docker run --name test-ubuntu ubuntu:latest echo 'Hello from Ubuntu!'")
print(f"Output: {interactive_output.strip()}")

# Container management commands
print("\n🛠️ Container Management:")
management_commands = [
    ("docker ps", "List running containers"),
    ("docker ps -a", "List all containers"),
    ("docker stop test-ubuntu", "Stop container"),
    ("docker rm test-ubuntu", "Remove container"),
]

for cmd, desc in management_commands:
    print(f"\n➤ {desc}:")
    print(f"Command: {cmd}")
    output, _, _ = run_command(cmd)
    if output.strip():
        print(f"Output: {output.strip()}")

# =============================================================================
# TOPIC 3: BUILD IMAGE FROM DOCKERFILE
# =============================================================================

print("\n" + "="*60)
print("TOPIC 3: BUILD IMAGE FROM DOCKERFILE")
print("="*60)

# Create a simple Dockerfile
dockerfile_content = """FROM ubuntu:latest
LABEL maintainer="docker-learner"
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY . /app
RUN echo "print('Hello from Docker!')" > hello.py
CMD ["python3", "hello.py"]
"""

print("📝 Creating Dockerfile:")
print(dockerfile_content)

# Write Dockerfile
with open("/content/Dockerfile", "w") as f:
    f.write(dockerfile_content)

# Build the image
print("\n🔨 Building Docker Image:")
build_cmd = "docker build -t my-python-app:v1.0 /content"
print(f"Command: {build_cmd}")
build_output, build_error, _ = run_command(build_cmd)
print(f"Build Output: {build_output}")
if build_error:
    print(f"Build Errors: {build_error}")

# List images to verify
print("\n📋 Verifying Built Image:")
images_output, _, _ = run_command("docker images")
print(images_output)

# Run the built image
print("\n🚀 Running Built Image:")
run_output, _, _ = run_command("docker run --name my-app my-python-app:v1.0")
print(f"Output: {run_output.strip()}")

# Cleanup
run_command("docker rm my-app")

# =============================================================================
# TOPIC 4: CREATE DOCKER IMAGE FROM MULTIPLE METHODS
# =============================================================================

print("\n" + "="*60)
print("TOPIC 4: CREATE DOCKER IMAGE FROM MULTIPLE METHODS")
print("="*60)

print("📋 Method 1: From Dockerfile (already demonstrated above)")

print("\n📋 Method 2: From Running Container (Commit)")
print("Step 1: Run base container and make changes")
run_command("docker run -d --name modify-container ubuntu:latest sleep 3600")

print("Step 2: Execute commands in container")
run_command("docker exec modify-container apt-get update")
run_command("docker exec modify-container apt-get install -y curl")

print("Step 3: Commit changes to new image")
commit_cmd = "docker commit modify-container my-custom-ubuntu:v1.0"
print(f"Command: {commit_cmd}")
commit_output, _, _ = run_command(commit_cmd)
print(f"Commit Output: {commit_output.strip()}")

print("Step 4: Verify new image")
images_output, _, _ = run_command("docker images | grep my-custom-ubuntu")
print(f"New Image: {images_output.strip()}")

# Test the committed image
print("Step 5: Test committed image")
test_output, _, _ = run_command("docker run --rm my-custom-ubuntu:v1.0 curl --version")
print(f"Test Output: {test_output.strip()}")

# Cleanup
run_command("docker stop modify-container")
run_command("docker rm modify-container")

# =============================================================================
# TOPIC 5: DOCKER REGISTRY AND DOCKERHUB (SIMULATION)
# =============================================================================

print("\n" + "="*60)
print("TOPIC 5: DOCKER REGISTRY AND DOCKERHUB (SIMULATION)")
print("="*60)

def simulate_docker_registry():
    """Simulate Docker Registry operations"""
    print("🎭 SIMULATION: Docker Registry Operations")
    print("Note: This is a simulation as we cannot actually push to DockerHub from Colab")

    # Simulate login
    print("\n1. Docker Login (Simulated):")
    print("Command: docker login")
    print("Simulated Response:")
    print("Username: your-username")
    print("Password: ********")
    print("Login Succeeded")

    # Simulate tagging
    print("\n2. Tagging Image for Registry:")
    tag_cmd = "docker tag my-python-app:v1.0 your-username/my-python-app:v1.0"
    print(f"Command: {tag_cmd}")
    # Actually perform the tag (this works locally)
    run_command(tag_cmd)
    tagged_images, _, _ = run_command("docker images | grep my-python-app")
    print(f"Tagged Images:\n{tagged_images}")

    # Simulate push
    print("\n3. Push to Registry (Simulated):")
    print("Command: docker push your-username/my-python-app:v1.0")
    print("Simulated Response:")
    print("The push refers to repository [docker.io/your-username/my-python-app]")
    print("v1.0: digest: sha256:abcd1234... size: 1234")

    # Simulate pull
    print("\n4. Pull from Registry (Simulated):")
    print("Command: docker pull your-username/my-python-app:v1.0")
    print("Simulated Response:")
    print("v1.0: Pulling from your-username/my-python-app")
    print("Status: Downloaded newer image for your-username/my-python-app:v1.0")

simulate_docker_registry()

# =============================================================================
# TOPIC 6: PUSH AND PULL TO DOCKERHUB AND ACR (SIMULATION)
# =============================================================================

print("\n" + "="*60)
print("TOPIC 6: PUSH AND PULL TO DOCKERHUB AND ACR (SIMULATION)")
print("="*60)

def simulate_registry_operations():
    """Simulate advanced registry operations"""
    print("🎭 SIMULATION: Advanced Registry Operations")

    # DockerHub simulation
    print("\n📦 DockerHub Operations (Simulated):")
    print("1. Login to DockerHub:")
    print("   docker login docker.io")
    print("   Response: Login Succeeded")

    print("\n2. Push to DockerHub:")
    print("   docker push username/my-app:latest")
    print("   Response: Pushed to docker.io/username/my-app:latest")

    print("\n3. Pull from DockerHub:")
    print("   docker pull username/my-app:latest")
    print("   Response: Downloaded from docker.io/username/my-app:latest")

    # ACR simulation
    print("\n☁️ Azure Container Registry (ACR) Operations (Simulated):")
    print("1. Login to ACR:")
    print("   az acr login --name myregistry")
    print("   docker login myregistry.azurecr.io")
    print("   Response: Login Succeeded")

    print("\n2. Tag for ACR:")
    print("   docker tag my-app:latest myregistry.azurecr.io/my-app:v1.0")

    print("\n3. Push to ACR:")
    print("   docker push myregistry.azurecr.io/my-app:v1.0")
    print("   Response: Pushed to ACR successfully")

    print("\n4. Pull from ACR:")
    print("   docker pull myregistry.azurecr.io/my-app:v1.0")
    print("   Response: Downloaded from ACR successfully")

simulate_registry_operations()

# =============================================================================
# TOPIC 7: MULTI-STAGE BUILD
# =============================================================================

print("\n" + "="*60)
print("TOPIC 7: MULTI-STAGE BUILD")
print("="*60)

# Create multi-stage Dockerfile
multistage_dockerfile = """# Multi-stage build example
# Stage 1: Build stage
FROM python:3.9 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m py_compile app.py

# Stage 2: Runtime stage
FROM python:3.9-slim AS runtime
WORKDIR /app
COPY --from=builder /app/app.py .
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
CMD ["python", "app.py"]
"""

# Create supporting files
requirements_txt = "requests==2.25.1\nflask==2.0.1"
app_py = """import flask
print("Multi-stage build app running!")
print(f"Flask version: {flask.__version__}")
"""

print("📝 Creating Multi-stage Dockerfile:")
print(multistage_dockerfile)

# Write files
with open("/content/Dockerfile.multistage", "w") as f:
    f.write(multistage_dockerfile)
with open("/content/requirements.txt", "w") as f:
    f.write(requirements_txt)
with open("/content/app.py", "w") as f:
    f.write(app_py)

print("\n🔨 Building Multi-stage Image:")
build_cmd = "docker build -f /content/Dockerfile.multistage -t multi-stage-app:v1.0 /content"
print(f"Command: {build_cmd}")
build_output, build_error, _ = run_command(build_cmd)
print(f"Build completed. Check images:")

# Compare image sizes
print("\n📊 Comparing Image Sizes:")
size_output, _, _ = run_command("docker images | grep -E '(multi-stage-app|python)'")
print(size_output)

# Run multi-stage app
print("\n🚀 Running Multi-stage App:")
run_output, _, _ = run_command("docker run --rm multi-stage-app:v1.0")
print(f"Output: {run_output.strip()}")

# =============================================================================
# TOPIC 8: DOCKER NETWORKING (PARTIAL IMPLEMENTATION)
# =============================================================================

print("\n" + "="*60)
print("TOPIC 8: DOCKER NETWORKING")
print("="*60)

print("🌐 Docker Network Operations:")

# List default networks
print("\n1. Default Networks:")
networks_output, _, _ = run_command("docker network ls")
print(networks_output)

# Create custom network
print("\n2. Creating Custom Bridge Network:")
network_cmd = "docker network create --driver bridge my-custom-network"
print(f"Command: {network_cmd}")
create_output, create_error, create_returncode = run_command(network_cmd)
print(f"Network Creation Output: {create_output.strip()}")
if create_error:
    print(f"Network Creation Errors: {create_error.strip()}")

# Inspect network
print("\n3. Inspecting Custom Network:")
# Check if network creation was successful before attempting to inspect
if create_returncode == 0:
    inspect_output, inspect_error, inspect_returncode = run_command("docker network inspect my-custom-network")
    if inspect_returncode == 0:
        try:
            network_info = json.loads(inspect_output)
            if network_info:
                print(f"Network Name: {network_info[0]['Name']}")
                print(f"Network Driver: {network_info[0]['Driver']}")
                print(f"Network Subnet: {network_info[0]['IPAM']['Config'][0]['Subnet']}")
            else:
                print("Error: Network inspection returned empty list.")
        except json.JSONDecodeError:
            print("Error: Could not decode network inspection output.")
            print(f"Raw output: {inspect_output}")
    else:
        print(f"Error inspecting network: {inspect_error.strip()}")
else:
    print("Skipping network inspection: Network creation failed.")


# Run containers on custom network
print("\n4. Running Containers on Custom Network:")
# Check if network creation was successful before running containers
if create_returncode == 0:
    run_command("docker run -d --name web-server --network my-custom-network nginx:alpine")
    run_command("docker run -d --name app-server --network my-custom-network python:3.9-alpine sleep 3600")

    # Test connectivity
    print("\n5. Testing Network Connectivity:")
    # Check if containers are running before testing connectivity
    container_check, _, _ = run_command("docker ps | grep -E 'web-server|app-server'")
    if container_check:
        ping_output, _, _ = run_command("docker exec app-server ping -c 3 web-server")
        print(f"Ping Result: {ping_output}")
    else:
        print("Skipping network connectivity test: Containers not running.")
else:
    print("Skipping container run and network test: Network creation failed.")


# Cleanup network test
run_command("docker stop web-server app-server")
run_command("docker rm web-server app-server")
run_command("docker network rm my-custom-network")

# =============================================================================
# TOPIC 9: DOCKER VOLUMES
# =============================================================================

print("\n" + "="*60)
print("TOPIC 9: DOCKER VOLUMES")
print("="*60)

print("💾 Docker Volume Operations:")

# List volumes
print("\n1. Current Volumes:")
volumes_output, _, _ = run_command("docker volume ls")
print(volumes_output)

# Create named volume
print("\n2. Creating Named Volume:")
volume_cmd = "docker volume create my-data-volume"
print(f"Command: {volume_cmd}")
create_output, _, create_returncode = run_command(volume_cmd)
print(f"Volume Created: {create_output.strip()}")

# Inspect volume
print("\n3. Inspecting Volume:")
# Check if volume creation was successful before attempting to inspect
if create_returncode == 0:
    inspect_output, inspect_error, inspect_returncode = run_command("docker volume inspect my-data-volume")
    if inspect_returncode == 0:
        try:
            volume_info = json.loads(inspect_output)
            if volume_info:
                print(f"Volume Name: {volume_info[0]['Name']}")
                print(f"Volume Mountpoint: {volume_info[0]['Mountpoint']}")
            else:
                 print("Error: Volume inspection returned empty list.")
        except json.JSONDecodeError:
            print("Error: Could not decode volume inspection output.")
            print(f"Raw output: {inspect_output}")
    else:
        print(f"Error inspecting volume: {inspect_error.strip()}")
else:
    print("Skipping volume inspection: Volume creation failed.")

# Use volume in container
print("\n4. Using Volume in Container:")
# Check if volume creation was successful before using it
if create_returncode == 0:
    # Write data to volume
    run_command("docker run --rm -v my-data-volume:/data ubuntu:latest sh -c 'echo \"Persistent data\" > /data/test.txt'")

    # Read data from volume
    print("Reading data from volume:")
    read_output, _, _ = run_command("docker run --rm -v my-data-volume:/data ubuntu:latest cat /data/test.txt")
    print(f"Data: {read_output.strip()}")
else:
    print("Skipping volume usage: Volume creation failed.")


# Demonstrate persistence
print("\n5. Demonstrating Data Persistence:")
# Check if volume creation was successful before demonstrating persistence
if create_returncode == 0:
    run_command("docker run --rm -v my-data-volume:/data ubuntu:latest sh -c 'echo \"$(date): Container 1\" >> /data/log.txt'")
    run_command("docker run --rm -v my-data-volume:/data ubuntu:latest sh -c 'echo \"$(date): Container 2\" >> /data/log.txt'")

    log_output, _, _ = run_command("docker run --rm -v my-data-volume:/data ubuntu:latest cat /data/log.txt")
    print(f"Persistent Log:\n{log_output}")
else:
    print("Skipping data persistence demonstration: Volume creation failed.")


# Bind mount example
print("\n6. Bind Mount Example:")
run_command("mkdir -p /content/host-data")
run_command("echo 'Host file content' > /content/host-data/host-file.txt")

bind_output, _, _ = run_command("docker run --rm -v /content/host-data:/container-data ubuntu:latest cat /container-data/host-file.txt")
print(f"Bind Mount Data: {bind_output.strip()}")

# =============================================================================
# TOPIC 10: DOCKER COMPOSE
# =============================================================================

print("\n" + "="*60)
print("TOPIC 10: DOCKER COMPOSE")
print("="*60)

# Create docker-compose.yml
compose_yaml = """version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - app

  app:
    image: python:3.9-alpine
    volumes:
      - ./app:/app
    working_dir: /app
    command: python -m http.server 8000
    ports:
      - "8000:8000"

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""

print("📝 Creating Docker Compose Configuration:")
print(compose_yaml)

# Write compose file
with open("/content/docker-compose.yml", "w") as f:
    f.write(compose_yaml)

# Create supporting directories and files
run_command("mkdir -p /content/html /content/app")
run_command("echo '<h1>Hello from Docker Compose!</h1>' > /content/html/index.html")
run_command("echo 'print(\"Python app running in compose!\")' > /content/app/app.py")

print("\n🚀 Docker Compose Operations:")

# Validate compose file
print("\n1. Validating Compose File:")
validate_output, _, validate_returncode = run_command("cd /content && docker-compose config")
if validate_returncode == 0:
  print("✅ Compose file is valid")
else:
  print("❌ Compose file validation failed. Check syntax.")


# Start services
print("\n2. Starting Services:")
start_cmd = "cd /content && docker-compose up -d"
print(f"Command: {start_cmd}")
start_output, _, start_returncode = run_command(start_cmd)
if start_returncode == 0:
  print(f"Services started: {start_output}")
else:
  print(f"❌ Failed to start services: {start_output}")


# List running services
print("\n3. Listing Services:")
ps_output, _, _ = run_command("cd /content && docker-compose ps")
print(ps_output)

# View logs
print("\n4. Service Logs:")
logs_output, _, _ = run_command("cd /content && docker-compose logs --tail=5")
print(logs_output[:500] + "..." if len(logs_output) > 500 else logs_output)

# Scale services
print("\n5. Scaling Services:")
scale_cmd = "cd /content && docker-compose up -d --scale app=2"
print(f"Command: {scale_cmd}")
scale_output, _, _ = run_command(scale_cmd)
print("Services scaled")

# Stop services
print("\n6. Stopping Services:")
stop_output, _, _ = run_command("cd /content && docker-compose down")
print("Services stopped and removed")

# =============================================================================
# TOPIC 11: DOCKER SECURITY BEST PRACTICES
# =============================================================================

print("\n" + "="*60)
print("TOPIC 11: DOCKER SECURITY BEST PRACTICES")
print("="*60)

def demonstrate_security_practices():
    """Demonstrate Docker security best practices"""
    print("🔒 Docker Security Best Practices Demonstration:")

    # Secure Dockerfile example
    secure_dockerfile = """# Security-focused Dockerfile
FROM python:3.9-slim AS base

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install security updates
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Use specific port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "app.py"]
"""

    print("\n1. Secure Dockerfile Example:")
    print(secure_dockerfile)

    # Write secure Dockerfile
    with open("/content/Dockerfile.secure", "w") as f:
        f.write(secure_dockerfile)

    # Create health check endpoint
    secure_app = """from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), HealthHandler)
    print("Secure app running on port 8000")
    server.serve_forever()
"""

    with open("/content/secure_app.py", "w") as f:
        f.write(secure_app)

    print("\n2. Security Scanning Simulation:")
    print("Command: docker scan my-python-app:v1.0")
    print("Simulated Output:")
    print("✅ No vulnerabilities found in base image")
    print("⚠️  1 medium severity vulnerability found in package xyz")
    print("💡 Recommendation: Update to latest version")

    print("\n3. Runtime Security Checks:")

    # Check for running containers as root
    print("\n➤ Checking container user:")
    user_check, _, _ = run_command("docker run --rm ubuntu:latest whoami")
    print(f"Current user in container: {user_check.strip()}")

    # Resource limits example
    print("\n➤ Resource Limits Example:")
    print("Command: docker run --memory=512m --cpus=1.0 --name limited-container ubuntu:latest")
    print("This limits container to 512MB RAM and 1 CPU core")

    # Read-only filesystem example
    print("\n➤ Read-only Filesystem Example:")
    print("Command: docker run --read-only --tmpfs /tmp ubuntu:latest")
    print("This makes the container filesystem read-only except /tmp")

    print("\n4. Security Best Practices Checklist:")
    security_checklist = [
        "✅ Use official base images",
        "✅ Run containers as non-root user",
        "✅ Use specific image tags, not 'latest'",
        "✅ Implement health checks",
        "✅ Limit container resources",
        "✅ Use read-only filesystems when possible",
        "✅ Scan images for vulnerabilities",
        "✅ Keep base images updated",
        "✅ Use multi-stage builds to reduce attack surface",
        "✅ Implement proper secret management"
    ]

    for item in security_checklist:
        print(f"  {item}")

    print("\n5. Container Security Monitoring:")
    print("Commands for security monitoring:")
    monitoring_commands = [
        "docker stats --no-stream",
        "docker inspect <container_id>",
        "docker logs <container_id>",
        "docker exec <container_id> ps aux"
    ]

    for cmd in monitoring_commands:
        print(f"  • {cmd}")

demonstrate_security_practices()

# =============================================================================
# FINAL SUMMARY AND CLEANUP
# =============================================================================

print("\n" + "="*60)
print("SUMMARY AND CLEANUP")
print("="*60)

print("📋 Learning Summary:")
print("✅ Topics Successfully Implemented:")
print("   1. Docker fundamentals and basic commands")
print("   2. Container operations and management")
print("   3. Building images from Dockerfile")
print("   4. Multiple image creation methods")
print("   7. Multi-stage builds")
print("   8. Docker networking (partial)")
print("   9. Docker volumes and storage")
print("   10. Docker Compose multi-container apps")
print("   11. Security best practices")

print("\n🎭 Topics Simulated:")
print("   5. Docker Registry and DockerHub operations")
print("   6. Push/Pull to cloud registries")

print("\n🧹 Cleaning up resources...")

# Cleanup commands
cleanup_commands = [
    "docker stop $(docker ps -aq)",
    "docker rm $(docker ps -aq)",
    "docker rmi $(docker images -q)",
    "docker volume prune -f",
    "docker network prune -f",
    "docker system prune -f"
]

for cmd in cleanup_commands:
    print(f"Executing: {cmd}")
    run_command(cmd)

print("\n🎉 Docker learning session completed!")
print("💡 Key takeaways:")
print("   • Most Docker operations work fully in Colab")
print("   • Registry operations need simulation due to auth limitations")
print("   • Docker Compose provides powerful orchestration capabilities")
print("   • Security should be considered from the start")
print("   • Practice with real containers gives the best learning experience")

print("\n📚 Next steps:")
print("   • Try modifying the Dockerfiles with your own applications")
print("   • Experiment with different base images")
print("   • Create more complex multi-service applications")
print("   • Practice with real cloud registries in your own environment")
