# ===============================
# Simulated Azure Tasks in Colab
# ===============================
from IPython.display import Markdown, display

def md(text):
    display(Markdown(text))

md("# ☁️ Azure CLI Tasks – Simulation in Colab")
md("Simulating common Azure admin/devops tasks without a real Azure account.")

# 1. Observe Assigned Subscriptions
md("## 🔍 1. Observe Assigned Subscriptions")
print("Command: az account show")
print("Simulated Output:\n{\n  'id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',\n  'name': 'Free Trial',\n  'user': {'name': 'you@example.com'},\n  'tenantId': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'\n}")

# 2. Observe Azure Entra ID
md("## 🔍 2. Observe Azure Entra ID (Azure AD)")
print("Command: az ad signed-in-user show")
print("Simulated Output:\n{\n  'displayName': 'Test User',\n  'mail': 'you@example.com',\n  'userPrincipalName': 'you@example.com'\n}")

# 3. Create Test Users and Groups
md("## 👥 3. Create Test Users and Groups")
print("Command: az ad user create --display-name 'User1' --password 'Password123!' --user-principal-name user1@example.com")
print("Command: az ad group create --display-name 'TestGroup' --mail-nickname 'testgroup'")
print("Simulated Output:\nUser and group created successfully.")

# 4. Assign a RBAC Role
md("## 🔐 4. Assign a Role to a User")
print("Command: az role assignment create --assignee user1@example.com --role Contributor --scope /subscriptions/<sub-id>")
print("Simulated Output:\nRole Contributor assigned to user1@example.com")

# 5. Create and Assign a Custom Role
md("## 🛠 5. Create and Assign a Custom Role")
print("Custom Role JSON Example:")
print('''
{
  "Name": "Custom Reader",
  "IsCustom": true,
  "Description": "Can read resources.",
  "Actions": [ "Microsoft.Resources/subscriptions/resourceGroups/read" ],
  "NotActions": [],
  "AssignableScopes": [ "/subscriptions/<sub-id>" ]
}
''')
print("Command: az role definition create --role-definition ./custom-role.json")
print("Command: az role assignment create --assignee user1@example.com --role 'Custom Reader'")
print("Simulated Output:\nCustom role assigned.")

# 6. Create VM and VNet
md("## 🖥 6. Create a Virtual Machine and VNet")
print("Command: az network vnet create --name MyVnet --resource-group MyRG --subnet-name MySubnet")
print("Command: az vm create --name MyVM --resource-group MyRG --image UbuntuLTS --admin-username azureuser")
print("Simulated Output:\nVM and VNet created successfully.")

# 7. Assign Policy at Subscription Level
md("## 📜 7. Create and Assign a Policy")
print("Command: az policy definition create --name 'AllowedLocations' --rules 'rules.json' --params 'params.json' --mode All")
print("Command: az policy assignment create --policy 'AllowedLocations' --scope /subscriptions/<sub-id>")
print("Simulated Output:\nPolicy assigned to subscription.")

# 8. Azure Key Vault: Store & Retrieve Secret
md("## 🔑 8. Create Key Vault, Store & Retrieve Secrets")
print("Command: az keyvault create --name MyKeyVault --resource-group MyRG")
print("Command: az keyvault secret set --vault-name MyKeyVault --name MySecret --value 'SuperSecret'")
print("Command: az keyvault secret show --vault-name MyKeyVault --name MySecret")
print("Simulated Output:\nSecret stored and retrieved.")

# 9. Create VM from PowerShell
md("## ⚙️ 9. Create VM using PowerShell (simulated)")
print("PowerShell Script:")
print('''
New-AzVM `
  -ResourceGroupName "MyRG" `
  -Name "MyVM" `
  -Location "East US" `
  -VirtualNetworkName "MyVnet" `
  -SubnetName "MySubnet" `
  -SecurityGroupName "MyNSG" `
  -PublicIpAddressName "MyPublicIP"
''')
print("Simulated Output:\nVM created via PowerShell.")

# 10. Daily Backup Schedule
md("## 📦 10. Schedule Daily Backup at 3 AM")
print("Command: az backup protection enable-for-vm --resource-group MyRG --vault-name MyVault --vm MyVM --policy-name DailyPolicy")
print("Simulated Output:\nDaily backup scheduled at 3 AM.")

# 11. Alert Rule for CPU > 80%
md("## 🚨 11. Create Alert Rule for High CPU Usage")
print("Command: az monitor metrics alert create --name HighCPUAlert --resource-group MyRG --scopes /subscriptions/<sub-id>/resourceGroups/MyRG/providers/Microsoft.Compute/virtualMachines/MyVM --condition \"avg Percentage CPU > 80\" --description \"CPU usage alert\" --action emailActionGroup")
print("Simulated Output:\nAlert rule created and email will be sent if CPU > 80%.")

md("---")
md("✅ **All tasks simulated!** Even though you're not using a real Azure account, you now understand the CLI/PowerShell steps involved.")
