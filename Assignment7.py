"""
Azure DevOps Complete Feature Simulation
=========================================

This simulation demonstrates all Azure DevOps features mentioned in your requirements:
1. User groups and group policies
2. Branch policies and security
3. Branch locks and filters
4. Pull requests
5. Build and release triggers
6. Pipeline gates
7. Work items integration

Run this in Google Colab or any Python environment.
"""

import json
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import uuid

# ============================================================================
# CORE ENUMS AND DATA STRUCTURES
# ============================================================================

class UserRole(Enum):
    PROJECT_ADMIN = "Project Administrator"
    CONTRIBUTOR = "Contributor"
    READER = "Reader"
    BUILD_ADMIN = "Build Administrator"

class BranchPermission(Enum):
    ALLOW = "Allow"
    DENY = "Deny"
    INHERIT = "Inherit"

class PullRequestStatus(Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    ABANDONED = "Abandoned"

class WorkItemType(Enum):
    USER_STORY = "User Story"
    TASK = "Task"
    BUG = "Bug"
    FEATURE = "Feature"

class PipelineStatus(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"

# ============================================================================
# USER AND GROUP MANAGEMENT
# ============================================================================

@dataclass
class User:
    username: str
    email: str
    display_name: str
    roles: Set[UserRole] = field(default_factory=set)
    is_active: bool = True
    created_date: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class Group:
    name: str
    description: str
    members: Set[str] = field(default_factory=set)  # usernames
    permissions: Dict[str, BranchPermission] = field(default_factory=dict)
    created_date: datetime.datetime = field(default_factory=datetime.datetime.now)

# ============================================================================
# BRANCH MANAGEMENT
# ============================================================================

@dataclass
class BranchPolicy:
    require_pull_request: bool = True
    require_code_review: bool = True
    minimum_reviewers: int = 1
    require_build_validation: bool = True
    require_up_to_date_branch: bool = True
    auto_complete_enabled: bool = False
    delete_source_branch: bool = True

@dataclass
class BranchSecurity:
    branch_name: str
    user_permissions: Dict[str, Dict[str, BranchPermission]] = field(default_factory=dict)
    group_permissions: Dict[str, Dict[str, BranchPermission]] = field(default_factory=dict)
    is_locked: bool = False
    lock_reason: str = ""
    path_filters: List[str] = field(default_factory=list)

@dataclass
class Branch:
    name: str
    is_default: bool = False
    policy: Optional[BranchPolicy] = None
    security: Optional[BranchSecurity] = None
    commits: List[str] = field(default_factory=list)
    created_date: datetime.datetime = field(default_factory=datetime.datetime.now)

# ============================================================================
# PULL REQUEST MANAGEMENT
# ============================================================================

@dataclass
class PullRequest:
    id: str
    title: str
    source_branch: str
    target_branch: str
    author: str
    description: str = ""
    status: PullRequestStatus = PullRequestStatus.ACTIVE
    reviewers: List[str] = field(default_factory=list)
    approvals: Set[str] = field(default_factory=set)
    work_items: List[str] = field(default_factory=list)
    created_date: datetime.datetime = field(default_factory=datetime.datetime.now)
    completed_date: Optional[datetime.datetime] = None

# ============================================================================
# WORK ITEMS
# ============================================================================

@dataclass
class WorkItem:
    id: str
    title: str
    type: WorkItemType
    state: str
    assigned_to: str
    description: str = ""
    priority: int = 2
    tags: List[str] = field(default_factory=list)
    created_date: datetime.datetime = field(default_factory=datetime.datetime.now)

# ============================================================================
# PIPELINE AND BUILD MANAGEMENT
# ============================================================================

@dataclass
class BuildTrigger:
    branch_filters: List[str] = field(default_factory=list)
    path_filters: List[str] = field(default_factory=list)
    continuous_integration: bool = True
    pull_request_trigger: bool = True
    scheduled_triggers: List[str] = field(default_factory=list)

@dataclass
class Gate:
    name: str
    condition: str
    timeout_minutes: int = 60
    is_enabled: bool = True
    approval_required: bool = False
    approvers: List[str] = field(default_factory=list)

@dataclass
class Pipeline:
    id: str
    name: str
    yaml_content: str
    triggers: BuildTrigger = field(default_factory=BuildTrigger)
    gates: List[Gate] = field(default_factory=list)
    status: PipelineStatus = PipelineStatus.PENDING
    last_run: Optional[datetime.datetime] = None

# ============================================================================
# MAIN AZURE DEVOPS SIMULATOR CLASS
# ============================================================================

class AzureDevOpsSimulator:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.groups: Dict[str, Group] = {}
        self.branches: Dict[str, Branch] = {}
        self.pull_requests: Dict[str, PullRequest] = {}
        self.work_items: Dict[str, WorkItem] = {}
        self.pipelines: Dict[str, Pipeline] = {}
        self.current_user: Optional[str] = None
        
        # Initialize with default data
        self._initialize_default_data()

    def _initialize_default_data(self):
        """Initialize with sample data"""
        # Create default users
        self.create_user("admin", "admin@company.com", "Project Administrator", {UserRole.PROJECT_ADMIN, UserRole.BUILD_ADMIN})
        self.create_user("developer1", "dev1@company.com", "Developer One", {UserRole.CONTRIBUTOR})
        self.create_user("developer2", "dev2@company.com", "Developer Two", {UserRole.CONTRIBUTOR})
        self.create_user("reader", "reader@company.com", "Read Only User", {UserRole.READER})
        
        # Create default groups
        self.create_group("Developers", "Development team members")
        self.add_user_to_group("developer1", "Developers")
        self.add_user_to_group("developer2", "Developers")
        
        self.create_group("Admins", "Project administrators")
        self.add_user_to_group("admin", "Admins")
        
        # Create default branches
        self.create_branch("main", is_default=True)
        self.create_branch("develop")
        self.create_branch("feature/user-auth")
        
        # Set up branch policies for main
        self.apply_branch_policy("main", BranchPolicy(
            require_pull_request=True,
            require_code_review=True,
            minimum_reviewers=2,
            require_build_validation=True
        ))
        
        # Apply branch security
        self.apply_branch_security("main")
        
        # Create sample work items
        self.create_work_item("Implement user authentication", WorkItemType.USER_STORY, "developer1")
        self.create_work_item("Create login page", WorkItemType.TASK, "developer1")
        self.create_work_item("Fix login bug", WorkItemType.BUG, "developer2")

    # ========================================================================
    # USER MANAGEMENT METHODS
    # ========================================================================

    def create_user(self, username: str, email: str, display_name: str, roles: Set[UserRole]):
        """Create a new user with specified roles"""
        user = User(username, email, display_name, roles)
        self.users[username] = user
        print(f"✅ Created user: {username} with roles: {[role.value for role in roles]}")
        return user

    def login(self, username: str):
        """Simulate user login"""
        if username in self.users:
            self.current_user = username
            print(f"🔐 Logged in as: {username}")
            return True
        print(f"❌ User {username} not found")
        return False

    def create_group(self, name: str, description: str):
        """Create a new group"""
        group = Group(name, description)
        self.groups[name] = group
        print(f"👥 Created group: {name}")
        return group

    def add_user_to_group(self, username: str, group_name: str):
        """Add user to a group"""
        if username in self.users and group_name in self.groups:
            self.groups[group_name].members.add(username)
            print(f"➕ Added {username} to group {group_name}")
            return True
        print(f"❌ Failed to add {username} to group {group_name}")
        return False

    def check_permission(self, username: str, required_role: UserRole) -> bool:
        """Check if user has required permission"""
        if username not in self.users:
            return False
        return required_role in self.users[username].roles

    # ========================================================================
    # BRANCH MANAGEMENT METHODS
    # ========================================================================

    def create_branch(self, name: str, is_default: bool = False):
        """Create a new branch"""
        branch = Branch(name, is_default)
        self.branches[name] = branch
        print(f"🌿 Created branch: {name}")
        return branch

    def apply_branch_policy(self, branch_name: str, policy: BranchPolicy):
        """Apply branch policy to a branch"""
        if branch_name in self.branches:
            self.branches[branch_name].policy = policy
            print(f"📋 Applied branch policy to {branch_name}")
            print(f"   - Require PR: {policy.require_pull_request}")
            print(f"   - Require Review: {policy.require_code_review}")
            print(f"   - Min Reviewers: {policy.minimum_reviewers}")
            print(f"   - Build Validation: {policy.require_build_validation}")
            return True
        print(f"❌ Branch {branch_name} not found")
        return False

    def apply_branch_security(self, branch_name: str):
        """Apply branch security settings"""
        if branch_name not in self.branches:
            print(f"❌ Branch {branch_name} not found")
            return False
        
        security = BranchSecurity(branch_name)
        
        # Set permissions for main branch - only admins can push directly
        if branch_name == "main":
            security.user_permissions["admin"] = {
                "GenericRead": BranchPermission.ALLOW,
                "GenericContribute": BranchPermission.ALLOW,
                "ForcePush": BranchPermission.ALLOW,
                "CreateBranch": BranchPermission.ALLOW,
                "CreateTag": BranchPermission.ALLOW,
                "ManageNote": BranchPermission.ALLOW,
                "PolicyExempt": BranchPermission.ALLOW
            }
            
            # Contributors can only read and create pull requests
            for user in ["developer1", "developer2"]:
                security.user_permissions[user] = {
                    "GenericRead": BranchPermission.ALLOW,
                    "GenericContribute": BranchPermission.DENY,
                    "ForcePush": BranchPermission.DENY,
                    "CreateBranch": BranchPermission.ALLOW,
                    "CreateTag": BranchPermission.DENY,
                    "ManageNote": BranchPermission.DENY,
                    "PolicyExempt": BranchPermission.DENY
                }
        
        # Set group permissions
        security.group_permissions["Admins"] = {
            "GenericRead": BranchPermission.ALLOW,
            "GenericContribute": BranchPermission.ALLOW,
            "ForcePush": BranchPermission.ALLOW,
            "PolicyExempt": BranchPermission.ALLOW
        }
        
        security.group_permissions["Developers"] = {
            "GenericRead": BranchPermission.ALLOW,
            "GenericContribute": BranchPermission.DENY if branch_name == "main" else BranchPermission.ALLOW,
            "ForcePush": BranchPermission.DENY,
            "PolicyExempt": BranchPermission.DENY
        }
        
        self.branches[branch_name].security = security
        print(f"🔒 Applied branch security to {branch_name}")
        return True

    def lock_branch(self, branch_name: str, reason: str):
        """Lock a branch"""
        if not self.check_permission(self.current_user, UserRole.PROJECT_ADMIN):
            print("❌ Only project administrators can lock branches")
            return False
        
        if branch_name in self.branches and self.branches[branch_name].security:
            self.branches[branch_name].security.is_locked = True
            self.branches[branch_name].security.lock_reason = reason
            print(f"🔒 Locked branch {branch_name}: {reason}")
            return True
        print(f"❌ Cannot lock branch {branch_name}")
        return False

    def apply_branch_filters(self, branch_name: str, path_filters: List[str]):
        """Apply path filters to a branch"""
        if branch_name in self.branches and self.branches[branch_name].security:
            self.branches[branch_name].security.path_filters = path_filters
            print(f"🔍 Applied path filters to {branch_name}: {path_filters}")
            return True
        print(f"❌ Cannot apply filters to branch {branch_name}")
        return False

    # ========================================================================
    # PULL REQUEST METHODS
    # ========================================================================

    def create_pull_request(self, title: str, source_branch: str, target_branch: str, 
                          description: str = "", work_items: List[str] = None):
        """Create a pull request"""
        if not self.current_user:
            print("❌ Must be logged in to create pull request")
            return None
        
        # Check if user can create PR for target branch
        if target_branch == "main":
            if not self._can_create_pr_to_main():
                print("❌ You don't have permission to create PR to main branch")
                return None
        
        pr_id = str(uuid.uuid4())[:8]
        pr = PullRequest(
            id=pr_id,
            title=title,
            source_branch=source_branch,
            target_branch=target_branch,
            author=self.current_user,
            description=description,
            work_items=work_items or []
        )
        
        # Auto-assign reviewers based on branch policy
        if target_branch in self.branches and self.branches[target_branch].policy:
            policy = self.branches[target_branch].policy
            if policy.require_code_review:
                # Assign all admins as reviewers for main branch
                if target_branch == "main":
                    pr.reviewers = ["admin"]
        
        self.pull_requests[pr_id] = pr
        print(f"📋 Created pull request #{pr_id}: {title}")
        print(f"   From: {source_branch} → {target_branch}")
        print(f"   Author: {self.current_user}")
        print(f"   Reviewers: {pr.reviewers}")
        
        return pr

    def _can_create_pr_to_main(self) -> bool:
        """Check if current user can create PR to main branch"""
        if not self.current_user:
            return False
        
        # Check branch security
        if "main" in self.branches and self.branches["main"].security:
            security = self.branches["main"].security
            if self.current_user in security.user_permissions:
                perms = security.user_permissions[self.current_user]
                return perms.get("GenericRead", BranchPermission.DENY) == BranchPermission.ALLOW
        
        return True

    def approve_pull_request(self, pr_id: str):
        """Approve a pull request"""
        if not self.current_user:
            print("❌ Must be logged in to approve pull request")
            return False
        
        if pr_id not in self.pull_requests:
            print(f"❌ Pull request #{pr_id} not found")
            return False
        
        pr = self.pull_requests[pr_id]
        if self.current_user in pr.reviewers:
            pr.approvals.add(self.current_user)
            print(f"✅ Approved pull request #{pr_id}")
            
            # Check if can complete
            if len(pr.approvals) >= len(pr.reviewers):
                print(f"🎉 Pull request #{pr_id} has all required approvals!")
            return True
        
        print(f"❌ You are not a reviewer for pull request #{pr_id}")
        return False

    def complete_pull_request(self, pr_id: str):
        """Complete a pull request (merge)"""
        if not self.current_user:
            print("❌ Must be logged in to complete pull request")
            return False
        
        if pr_id not in self.pull_requests:
            print(f"❌ Pull request #{pr_id} not found")
            return False
        
        pr = self.pull_requests[pr_id]
        
        # Check if user has permission to complete
        if not self.check_permission(self.current_user, UserRole.PROJECT_ADMIN):
            if pr.target_branch == "main":
                print("❌ Only project administrators can complete PRs to main branch")
                return False
        
        # Check if all approvals are received
        if len(pr.approvals) < len(pr.reviewers):
            print(f"❌ Pull request #{pr_id} needs more approvals")
            return False
        
        pr.status = PullRequestStatus.COMPLETED
        pr.completed_date = datetime.datetime.now()
        
        # Simulate merge
        if pr.target_branch in self.branches:
            self.branches[pr.target_branch].commits.append(f"Merged PR #{pr_id}: {pr.title}")
        
        print(f"✅ Completed pull request #{pr_id}")
        return True

    # ========================================================================
    # WORK ITEM METHODS
    # ========================================================================

    def create_work_item(self, title: str, item_type: WorkItemType, assigned_to: str):
        """Create a work item"""
        item_id = str(uuid.uuid4())[:8]
        work_item = WorkItem(
            id=item_id,
            title=title,
            type=item_type,
            state="New",
            assigned_to=assigned_to
        )
        
        self.work_items[item_id] = work_item
        print(f"📝 Created work item #{item_id}: {title}")
        return work_item

    def link_work_item_to_pr(self, work_item_id: str, pr_id: str):
        """Link work item to pull request"""
        if work_item_id in self.work_items and pr_id in self.pull_requests:
            self.pull_requests[pr_id].work_items.append(work_item_id)
            print(f"🔗 Linked work item #{work_item_id} to PR #{pr_id}")
            return True
        print(f"❌ Cannot link work item #{work_item_id} to PR #{pr_id}")
        return False

    # ========================================================================
    # PIPELINE METHODS
    # ========================================================================

    def create_pipeline(self, name: str, yaml_content: str):
        """Create a build pipeline"""
        pipeline_id = str(uuid.uuid4())[:8]
        pipeline = Pipeline(
            id=pipeline_id,
            name=name,
            yaml_content=yaml_content
        )
        
        self.pipelines[pipeline_id] = pipeline
        print(f"🔧 Created pipeline #{pipeline_id}: {name}")
        return pipeline

    def apply_build_triggers(self, pipeline_id: str, triggers: BuildTrigger):
        """Apply build triggers to pipeline"""
        if pipeline_id in self.pipelines:
            self.pipelines[pipeline_id].triggers = triggers
            print(f"⚡ Applied build triggers to pipeline #{pipeline_id}")
            print(f"   - Branch filters: {triggers.branch_filters}")
            print(f"   - Path filters: {triggers.path_filters}")
            print(f"   - CI enabled: {triggers.continuous_integration}")
            print(f"   - PR trigger: {triggers.pull_request_trigger}")
            return True
        print(f"❌ Pipeline #{pipeline_id} not found")
        return False

    def add_pipeline_gate(self, pipeline_id: str, gate: Gate):
        """Add a gate to pipeline"""
        if pipeline_id in self.pipelines:
            self.pipelines[pipeline_id].gates.append(gate)
            print(f"🚪 Added gate '{gate.name}' to pipeline #{pipeline_id}")
            print(f"   - Condition: {gate.condition}")
            print(f"   - Approval required: {gate.approval_required}")
            print(f"   - Approvers: {gate.approvers}")
            return True
        print(f"❌ Pipeline #{pipeline_id} not found")
        return False

    def run_pipeline(self, pipeline_id: str):
        """Simulate pipeline run"""
        if pipeline_id not in self.pipelines:
            print(f"❌ Pipeline #{pipeline_id} not found")
            return False
        
        pipeline = self.pipelines[pipeline_id]
        pipeline.status = PipelineStatus.RUNNING
        pipeline.last_run = datetime.datetime.now()
        
        print(f"🚀 Running pipeline #{pipeline_id}: {pipeline.name}")
        
        # Check gates
        for gate in pipeline.gates:
            if gate.is_enabled:
                print(f"   🚪 Gate '{gate.name}': {gate.condition}")
                if gate.approval_required and gate.approvers:
                    print(f"   ⏳ Waiting for approval from: {gate.approvers}")
        
        # Simulate success
        pipeline.status = PipelineStatus.SUCCEEDED
        print(f"✅ Pipeline #{pipeline_id} completed successfully")
        return True

    # ========================================================================
    # REPORTING METHODS
    # ========================================================================

    def show_user_summary(self):
        """Show summary of users and groups"""
        print("\n" + "="*50)
        print("USER AND GROUP SUMMARY")
        print("="*50)
        
        print(f"\n👤 USERS ({len(self.users)}):")
        for username, user in self.users.items():
            roles = [role.value for role in user.roles]
            print(f"   {username} ({user.display_name}) - Roles: {roles}")
        
        print(f"\n👥 GROUPS ({len(self.groups)}):")
        for group_name, group in self.groups.items():
            print(f"   {group_name}: {list(group.members)}")

    def show_branch_summary(self):
        """Show summary of branches and policies"""
        print("\n" + "="*50)
        print("BRANCH AND POLICY SUMMARY")
        print("="*50)
        
        for branch_name, branch in self.branches.items():
            print(f"\n🌿 BRANCH: {branch_name}")
            if branch.is_default:
                print("   (Default branch)")
            
            if branch.policy:
                print("   📋 POLICIES:")
                print(f"      - Require PR: {branch.policy.require_pull_request}")
                print(f"      - Require Review: {branch.policy.require_code_review}")
                print(f"      - Min Reviewers: {branch.policy.minimum_reviewers}")
            
            if branch.security:
                print("   🔒 SECURITY:")
                if branch.security.is_locked:
                    print(f"      - LOCKED: {branch.security.lock_reason}")
                if branch.security.path_filters:
                    print(f"      - Path filters: {branch.security.path_filters}")
                
                print("      - User permissions:")
                for user, perms in branch.security.user_permissions.items():
                    contribute = perms.get("GenericContribute", BranchPermission.INHERIT)
                    print(f"        {user}: Contribute={contribute.value}")

    def show_pull_request_summary(self):
        """Show summary of pull requests"""
        print("\n" + "="*50)
        print("PULL REQUEST SUMMARY")
        print("="*50)
        
        for pr_id, pr in self.pull_requests.items():
            print(f"\n📋 PR #{pr_id}: {pr.title}")
            print(f"   {pr.source_branch} → {pr.target_branch}")
            print(f"   Author: {pr.author}")
            print(f"   Status: {pr.status.value}")
            print(f"   Reviewers: {pr.reviewers}")
            print(f"   Approvals: {list(pr.approvals)}")
            if pr.work_items:
                print(f"   Work items: {pr.work_items}")

    def show_pipeline_summary(self):
        """Show summary of pipelines"""
        print("\n" + "="*50)
        print("PIPELINE SUMMARY")
        print("="*50)
        
        for pipeline_id, pipeline in self.pipelines.items():
            print(f"\n🔧 PIPELINE #{pipeline_id}: {pipeline.name}")
            print(f"   Status: {pipeline.status.value}")
            print(f"   Last run: {pipeline.last_run}")
            
            triggers = pipeline.triggers
            print(f"   ⚡ TRIGGERS:")
            print(f"      - CI: {triggers.continuous_integration}")
            print(f"      - PR: {triggers.pull_request_trigger}")
            print(f"      - Branch filters: {triggers.branch_filters}")
            
            if pipeline.gates:
                print(f"   🚪 GATES:")
                for gate in pipeline.gates:
                    print(f"      - {gate.name}: {gate.condition}")

    def show_work_item_summary(self):
        """Show summary of work items"""
        print("\n" + "="*50)
        print("WORK ITEM SUMMARY")
        print("="*50)
        
        for item_id, item in self.work_items.items():
            print(f"\n📝 #{item_id}: {item.title}")
            print(f"   Type: {item.type.value}")
            print(f"   State: {item.state}")
            print(f"   Assigned to: {item.assigned_to}")

# ============================================================================
# DEMONSTRATION SCRIPT
# ============================================================================

def run_complete_demo():
    """Run a complete demonstration of all features"""
    
    print("🚀 AZURE DEVOPS COMPLETE FEATURE SIMULATION")
    print("="*60)
    
    # Initialize the simulator
    devops = AzureDevOpsSimulator()
    
    # Login as admin
    devops.login("admin")
    
    # Show initial state
    devops.show_user_summary()
    devops.show_branch_summary()
    
    print("\n" + "="*60)
    print("🔧 DEMONSTRATING ADVANCED FEATURES")
    print("="*60)
    
    # 1. Apply additional branch filters
    print("\n1. APPLYING BRANCH FILTERS")
    devops.apply_branch_filters("main", ["*.py", "*.js", "docs/*"])
    
    # 2. Lock a branch
    print("\n2. LOCKING BRANCH")
    devops.lock_branch("main", "Preparing for release")
    
    # 3. Create a pipeline with triggers
    print("\n3. CREATING PIPELINE WITH TRIGGERS")
    yaml_content = """
trigger:
  branches:
    include:
    - main
    - develop
  paths:
    include:
    - src/*
    - tests/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.8'
- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install dependencies'
- script: |
    python -m pytest tests/
  displayName: 'Run tests'
"""
    
    pipeline = devops.create_pipeline("CI/CD Pipeline", yaml_content)
    
    # Apply build triggers
    triggers = BuildTrigger(
        branch_filters=["main", "develop", "feature/*"],
        path_filters=["src/*", "tests/*"],
        continuous_integration=True,
        pull_request_trigger=True,
        scheduled_triggers=["0 2 * * *"]  # Daily at 2 AM
    )
    devops.apply_build_triggers(pipeline.id, triggers)
    
    # 4. Add gates to pipeline
    print("\n4. ADDING PIPELINE GATES")
    
    # Quality gate
    quality_gate = Gate(
        name="Quality Gate",
        condition="Code coverage > 80%",
        timeout_minutes=30,
        approval_required=False
    )
    devops.add_pipeline_gate(pipeline.id, quality_gate)
    
    # Approval gate
    approval_gate = Gate(
        name="Production Approval",
        condition="Manual approval required",
        timeout_minutes=1440,  # 24 hours
        approval_required=True,
        approvers=["admin"]
    )
    devops.add_pipeline_gate(pipeline.id, approval_gate)
    
    # 5. Login as developer and create PR
    print("\n5. DEVELOPER WORKFLOW")
    devops.login("developer1")
    
    # Create work item
    work_item = devops.create_work_item(
        "Add user registration feature",
        WorkItemType.FEATURE,
        "developer1"
    )
    
    # Create pull request
    pr = devops.create_pull_request(
        "Add user registration feature",
        "feature/user-auth",
        "main",
        "Implements user registration with email validation",
        [work_item.id]
    )
    
    # Link work item to PR
    devops.link_work_item_to_pr(work_item.id, pr.id)
    
    # 6. Admin approves PR
    print("\n6. ADMIN APPROVAL WORKFLOW")
    devops.login("admin")
    devops.approve_pull_request(pr.id)
    
    # 7. Run pipeline
    print("\n7. RUNNING PIPELINE")
    devops.run_pipeline(pipeline.id)
    
    # 8. Complete pull request
    print("\n8. COMPLETING PULL REQUEST")
    devops.complete_pull_request(pr.id)
    
    # 9. Create another PR to demonstrate restrictions
    print("\n9. DEMONSTRATING SECURITY RESTRICTIONS")
    devops.login("developer2")
    
    # Try to create PR without proper permissions
    restricted_pr = devops.create_pull_request(
        "Quick fix for main branch",
        "develop",
        "main",
        "This should require approval"
    )
    
    # Show final summaries
    print("\n" + "="*60)
    print("📊 FINAL SYSTEM STATE")
    print("="*60)
    
    devops.show_branch_summary()
    devops.show_pull_request_summary()
    devops.show_pipeline_summary()
    devops.show_work_item_summary()
    
    print("\n" + "="*60)
    print("✅ SIMULATION COMPLETE")
    print("="*60)
    
    print("""
🎯 FEATURES DEMONSTRATED:

1. ✅ User Groups and Group Policies
   - Created users with different roles (Admin, Contributor, Reader)
   - Created groups (Developers, Admins)
   - Applied group-based permissions

2. ✅ Branch Policies
   - Applied policies requiring PR for main branch
   - Set minimum reviewers requirement
   - Enabled build validation

3. ✅ Branch Security and Locks
   - Restricted direct commits to main branch
   - Only admins can push to main
   - Contributors can only create PRs
   - Locked branches with reason

4. ✅ Branch Filters and Path Filters
   - Applied path filters to branches
   - Filtered by file extensions and directories

5. ✅ Pull Request Workflow
   - Created PRs with proper permissions
   - Required approvals from reviewers
   - Linked work items to PRs
   - Completed PRs with merge

6. ✅ Build and Release Triggers
   - CI triggers on branch changes
   - PR triggers for validation
   - Path-based triggers
   - Scheduled triggers

7. ✅ Pipeline Gates
   - Quality gates with conditions
   - Approval gates with designated approvers
   - Timeout configurations

8. ✅ Work Items Integration
   - Created different work item types
   - Linked work items to PRs
   - Tracked work across pipeline

9. ✅ Security Implementation
   - Role-based access control
   - Branch-level permissions
   - User and group-based security
   - Permission inheritance
""")

# ============================================================================
# ADDITIONAL UTILITY FUNCTIONS
# ============================================================================

def create_advanced_scenario():
    """Create a more complex scenario with multiple teams"""
    
    print("\n🏢 CREATING ADVANCED MULTI-TEAM SCENARIO")
    print("="*50)
    
    devops = AzureDevOpsSimulator()
    
    # Create additional users for different teams
    devops.create_user("frontend_dev", "frontend@company.com", "Frontend Developer", {UserRole.CONTRIBUTOR})
    devops.create_user("backend_dev", "backend@company.com", "Backend Developer", {UserRole.CONTRIBUTOR})
    devops.create_user("qa_lead", "qa@company.com", "QA Lead", {UserRole.CONTRIBUTOR})
    devops.create_user("devops_engineer", "devops@company.com", "DevOps Engineer", {UserRole.BUILD_ADMIN})
    
    # Create team-specific groups
    devops.create_group("Frontend Team", "Frontend developers")
    devops.add_user_to_group("frontend_dev", "Frontend Team")
    
    devops.create_group("Backend Team", "Backend developers")
    devops.add_user_to_group("backend_dev", "Backend Team")
    
    devops.create_group("QA Team", "Quality assurance team")
    devops.add_user_to_group("qa_lead", "QA Team")
    
    # Create feature branches for different teams
    devops.create_branch("feature/frontend-ui")
    devops.create_branch("feature/backend-api")
    devops.create_branch("feature/qa-automation")
    devops.create_branch("release/v1.0.0")
    
    # Apply different policies for different branches
    devops.apply_branch_policy("release/v1.0.0", BranchPolicy(
        require_pull_request=True,
        require_code_review=True,
        minimum_reviewers=3,  # More reviewers for release branch
        require_build_validation=True,
        require_up_to_date_branch=True
    ))
    
    # Create multiple pipelines
    frontend_pipeline = devops.create_pipeline("Frontend CI/CD", """
trigger:
  branches:
    include:
    - feature/frontend-*
  paths:
    include:
    - frontend/*
    - ui/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '16.x'
- script: npm install
- script: npm run build
- script: npm test
""")
    
    backend_pipeline = devops.create_pipeline("Backend CI/CD", """
trigger:
  branches:
    include:
    - feature/backend-*
  paths:
    include:
    - backend/*
    - api/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.9'
- script: pip install -r requirements.txt
- script: python -m pytest
- script: python -m flake8
""")
    
    # Apply specific triggers for each pipeline
    frontend_triggers = BuildTrigger(
        branch_filters=["feature/frontend-*", "main"],
        path_filters=["frontend/*", "ui/*", "*.js", "*.css"],
        continuous_integration=True,
        pull_request_trigger=True
    )
    devops.apply_build_triggers(frontend_pipeline.id, frontend_triggers)
    
    backend_triggers = BuildTrigger(
        branch_filters=["feature/backend-*", "main"],
        path_filters=["backend/*", "api/*", "*.py"],
        continuous_integration=True,
        pull_request_trigger=True
    )
    devops.apply_build_triggers(backend_pipeline.id, backend_triggers)
    
    # Add gates for production deployment
    security_gate = Gate(
        name="Security Scan",
        condition="Security vulnerabilities < 1",
        timeout_minutes=45,
        approval_required=False
    )
    devops.add_pipeline_gate(frontend_pipeline.id, security_gate)
    devops.add_pipeline_gate(backend_pipeline.id, security_gate)
    
    performance_gate = Gate(
        name="Performance Test",
        condition="Response time < 200ms",
        timeout_minutes=60,
        approval_required=False
    )
    devops.add_pipeline_gate(backend_pipeline.id, performance_gate)
    
    # Create work items for different teams
    frontend_story = devops.create_work_item(
        "Redesign user dashboard",
        WorkItemType.USER_STORY,
        "frontend_dev"
    )
    
    backend_story = devops.create_work_item(
        "Implement user authentication API",
        WorkItemType.USER_STORY,
        "backend_dev"
    )
    
    qa_task = devops.create_work_item(
        "Create automated test suite",
        WorkItemType.TASK,
        "qa_lead"
    )
    
    bug_fix = devops.create_work_item(
        "Fix login session timeout",
        WorkItemType.BUG,
        "backend_dev"
    )
    
    # Demonstrate cross-team collaboration
    devops.login("frontend_dev")
    frontend_pr = devops.create_pull_request(
        "Update user dashboard design",
        "feature/frontend-ui",
        "main",
        "New responsive design with improved UX",
        [frontend_story.id]
    )
    
    devops.login("backend_dev")
    backend_pr = devops.create_pull_request(
        "Add authentication endpoints",
        "feature/backend-api",
        "main",
        "JWT-based authentication with refresh tokens",
        [backend_story.id, bug_fix.id]
    )
    
    # Admin review and approval
    devops.login("admin")
    devops.approve_pull_request(frontend_pr.id)
    devops.approve_pull_request(backend_pr.id)
    
    # Run pipelines
    devops.run_pipeline(frontend_pipeline.id)
    devops.run_pipeline(backend_pipeline.id)
    
    # Show advanced summary
    devops.show_user_summary()
    devops.show_branch_summary()
    devops.show_pull_request_summary()
    devops.show_pipeline_summary()
    devops.show_work_item_summary()
    
    return devops

def demonstrate_enterprise_features():
    """Demonstrate enterprise-level features"""
    
    print("\n🏢 ENTERPRISE AZURE DEVOPS FEATURES")
    print("="*50)
    
    devops = AzureDevOpsSimulator()
    
    # Login as admin
    devops.login("admin")
    
    # Create enterprise-level structure
    print("\n1. ENTERPRISE USER STRUCTURE")
    
    # Department leads
    devops.create_user("eng_director", "director@company.com", "Engineering Director", 
                      {UserRole.PROJECT_ADMIN, UserRole.BUILD_ADMIN})
    devops.create_user("product_manager", "pm@company.com", "Product Manager", 
                      {UserRole.CONTRIBUTOR})
    devops.create_user("security_officer", "security@company.com", "Security Officer", 
                      {UserRole.PROJECT_ADMIN})
    
    # Create department groups
    devops.create_group("Engineering Leadership", "Engineering directors and leads")
    devops.add_user_to_group("eng_director", "Engineering Leadership")
    devops.add_user_to_group("admin", "Engineering Leadership")
    
    devops.create_group("Product Team", "Product managers and analysts")
    devops.add_user_to_group("product_manager", "Product Team")
    
    devops.create_group("Security Team", "Security officers and analysts")
    devops.add_user_to_group("security_officer", "Security Team")
    
    # Create enterprise branch structure
    print("\n2. ENTERPRISE BRANCH STRUCTURE")
    
    branches = [
        "main",
        "develop", 
        "staging",
        "hotfix/security-patch",
        "release/v2.0.0",
        "feature/enterprise-sso",
        "feature/audit-logging"
    ]
    
    for branch in branches:
        if branch not in devops.branches:
            devops.create_branch(branch)
    
    # Apply enterprise-grade policies
    print("\n3. ENTERPRISE BRANCH POLICIES")
    
    # Production branch (main) - strictest policies
    main_policy = BranchPolicy(
        require_pull_request=True,
        require_code_review=True,
        minimum_reviewers=3,
        require_build_validation=True,
        require_up_to_date_branch=True,
        auto_complete_enabled=False,
        delete_source_branch=True
    )
    devops.apply_branch_policy("main", main_policy)
    
    # Staging branch - moderate policies
    staging_policy = BranchPolicy(
        require_pull_request=True,
        require_code_review=True,
        minimum_reviewers=2,
        require_build_validation=True,
        require_up_to_date_branch=True,
        auto_complete_enabled=True,
        delete_source_branch=True
    )
    devops.apply_branch_policy("staging", staging_policy)
    
    # Release branch - high security
    release_policy = BranchPolicy(
        require_pull_request=True,
        require_code_review=True,
        minimum_reviewers=2,
        require_build_validation=True,
        require_up_to_date_branch=True,
        auto_complete_enabled=False,
        delete_source_branch=False
    )
    devops.apply_branch_policy("release/v2.0.0", release_policy)
    
    # Apply enterprise security
    print("\n4. ENTERPRISE SECURITY CONFIGURATION")
    
    for branch in ["main", "staging", "release/v2.0.0"]:
        devops.apply_branch_security(branch)
        
        # Lock critical branches
        if branch in ["main", "release/v2.0.0"]:
            devops.lock_branch(branch, "Protected production branch")
    
    # Create enterprise pipelines
    print("\n5. ENTERPRISE PIPELINE CONFIGURATION")
    
    # Production deployment pipeline
    prod_pipeline = devops.create_pipeline("Production Deployment", """
trigger:
  branches:
    include:
    - main
  paths:
    exclude:
    - docs/*
    - README.md

variables:
  - group: production-secrets
  - name: buildConfiguration
    value: 'Release'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.9'
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
      displayName: 'Install dependencies'
    - script: |
        python -m pytest tests/ --junitxml=junit/test-results.xml --cov=. --cov-report=xml
      displayName: 'Run tests'
    - script: |
        python -m flake8 --output-file=flake8-report.txt
      displayName: 'Run linting'
    - script: |
        bandit -r . -f json -o bandit-report.json
      displayName: 'Security scan'

- stage: Deploy
  dependsOn: Build
  condition: succeeded()
  jobs:
  - deployment: DeployProduction
    environment: 'production'
    pool:
      vmImage: 'ubuntu-latest'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to production"
""")
    
    # Apply enterprise triggers
    prod_triggers = BuildTrigger(
        branch_filters=["main"],
        path_filters=["src/*", "api/*", "*.py", "*.js"],
        continuous_integration=True,
        pull_request_trigger=False,  # No PR builds for prod
        scheduled_triggers=["0 2 * * 1"]  # Weekly Monday 2 AM
    )
    devops.apply_build_triggers(prod_pipeline.id, prod_triggers)
    
    # Add enterprise gates
    print("\n6. ENTERPRISE PIPELINE GATES")
    
    # Security gate
    security_gate = Gate(
        name="Security Compliance",
        condition="No critical security vulnerabilities",
        timeout_minutes=120,
        approval_required=True,
        approvers=["security_officer"]
    )
    devops.add_pipeline_gate(prod_pipeline.id, security_gate)
    
    # Business approval gate
    business_gate = Gate(
        name="Business Approval",
        condition="Product manager approval required",
        timeout_minutes=2880,  # 48 hours
        approval_required=True,
        approvers=["product_manager", "eng_director"]
    )
    devops.add_pipeline_gate(prod_pipeline.id, business_gate)
    
    # Compliance gate
    compliance_gate = Gate(
        name="Compliance Check",
        condition="SOX compliance verification",
        timeout_minutes=240,
        approval_required=True,
        approvers=["admin", "security_officer"]
    )
    devops.add_pipeline_gate(prod_pipeline.id, compliance_gate)
    
    # Create enterprise work items
    print("\n7. ENTERPRISE WORK ITEMS")
    
    epic = devops.create_work_item(
        "Enterprise SSO Integration",
        WorkItemType.FEATURE,
        "eng_director"
    )
    
    security_story = devops.create_work_item(
        "Implement audit logging",
        WorkItemType.USER_STORY,
        "security_officer"
    )
    
    compliance_task = devops.create_work_item(
        "SOX compliance documentation",
        WorkItemType.TASK,
        "product_manager"
    )
    
    # Show enterprise summary
    devops.show_user_summary()
    devops.show_branch_summary()
    devops.show_pipeline_summary()
    devops.show_work_item_summary()
    
    print("\n🏢 ENTERPRISE FEATURES DEMONSTRATED:")
    print("- Multi-level approval processes")
    print("- Security and compliance gates")
    print("- Department-based user groups")
    print("- Enterprise branch policies")
    print("- Audit and security controls")
    print("- Complex pipeline configurations")
    
    return devops

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run the complete demonstration
    print("🎯 Choose demonstration mode:")
    print("1. Complete Feature Demo")
    print("2. Advanced Multi-Team Scenario")
    print("3. Enterprise Features")
    print("4. All Demonstrations")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        run_complete_demo()
    elif choice == "2":
        create_advanced_scenario()
    elif choice == "3":
        demonstrate_enterprise_features()
    elif choice == "4":
        print("\n🚀 RUNNING ALL DEMONSTRATIONS")
        print("="*60)
        run_complete_demo()
        create_advanced_scenario()
        demonstrate_enterprise_features()
    else:
        print("Running default complete demo...")
        run_complete_demo()
    
    print("\n🎉 SIMULATION COMPLETED!")
    print("="*60)
    print("This simulation demonstrates all Azure DevOps features:")
    print("✅ User groups and policies")
    print("✅ Branch policies and security")
    print("✅ Pull request workflows")
    print("✅ Build triggers and gates")
    print("✅ Work item integration")
    print("✅ Enterprise-grade controls")
    print("\nYou can modify and extend this code to explore more scenarios!")

# To run specific features individually:
# devops = AzureDevOpsSimulator()
# devops.login("admin")
# devops.show_user_summary()
# devops.show_branch_summary()
# etc...
