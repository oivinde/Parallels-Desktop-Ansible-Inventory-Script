# Parallels-Desktop-Ansible-Inventory-Script
If you for some reason running Ansible Tower in a Parallels Desktop vm and wants a custom inventory script for Parallels Desktop, this is the place for you!

Since Parallels Desktop not has an API that you can query from a remote node, I'm using the Ansible python API in the inventory script to execute parallels cli commands on the virtualization host(my Mac).
## Installation
You must:
1. Add parallels_desktop_inventory.py as a custom inventory script in Tower
2. Since I'm using custom credentials in Tower to  inject the authentication information to the inventory script you need to add a custom credential
3. Add authentication information to the custom credential
4. Add an inventory and set the custom inventory script as a source
### To add a new custom inventory script in Ansible Tower
1. click the **Inventory Scripts** from the left navigation bar ![Alt text](images/wheel.png?raw=true "settings").

![Alt text](images/inventory-scripts.png?raw=true "settings")
2. click the ![Add](images/add-button.png?raw=true "settings") button located in the upper right corner of the Inventory Scripts screen.   
3. Enter the name for the script, plus an optional description. Then select the Organization that this script belongs to and then paste the content from **parallels_desktop_inventory.pl** script.
![Alt text](images/add_script.png?raw=true "add script")
### To create a custom credential in Ansible Tower
1.  click the **Credential Types** ![Alt text](images/credential-types-icon.png?raw=true "Credential Types") icon from the left navigation bar.
2. Click the ![Add](images/add-button.png?raw=true "settings") button located in the upper right corner of the Credential Types screen.    
3. Enter the name for the credential, plus an optional description.
![Alt text](images/credential.png?raw=true "Credential Types")
Input Configuration:
```yaml
fields:
  - type: string
    id: username
    label: Username
  - secret: true
    type: string
    id: password
    label: Password
  - type: string
    id: hostname
    label: Hostname
required:
  - username
  - password
  - hostname
```
Injector Configuration:
```yaml
env:
  PARALLELS_HOSTNAME: '{{hostname}}'
  PARALLELS_PASSWORD: '{{password}}'
  PARALLELS_USERNAME: '{{username}}'
```
### Add a Credential for the Parallels Inventory
1. click the **Credentials** icon from the left navigation bar.   
2. click the ![Add](images/add-button.png?raw=true "settings") button located in the upper right corner of the Credentials screen.
3. Enter required information
![Add](images/credentials.png?raw=true "settings")
### Add inventory source for your inventory
![Add](images/inventory-source.png?raw=true "settings")

Happy Inventory / Peter
