# Parallels-Desktop-Ansible-Inventory-Script
If you for some reason running Ansible Tower in a Parallels Desktop vm and wants a custom inventory script for Parallels Desktop, this is the place for you!

Since Parallels Desktop not has an API you can query from a remote node, I'm using the Ansible python API in the inventory script to execute parallels cli commands on the virtualization host(my Mac).
## Installation
You must:
1. Add parallels_desktop_inventory.py as a custom inventory script in Tower
2. Since I'm using custom credentials in Tower to  inject the authentication information to the inventory script you need to add a custom credential
3. Add authentication information to the custom credential
4. Add an inventory and set the custom inventory script as a source
### To add a new custom inventory script in Ansible Tower
1. click the **Inventory Scripts** from the left navigation bar ![Alt text](images/wheel.png?raw=true "settings").

![Alt text](images/inventory-scripts.png?raw=true "settings")
2. click the ![Add](images/add-button.png?raw=true "settings") button.   
3. Enter the name for the script, plus an optional description. Then select the Organization that this script belongs to and then paste the content from **parallels_desktop_inventory.pl** script.
![Alt text](images/add_script.png?raw=true "add script")
### To create a custom credential in Ansible Tower
1.  click the **Credential Types** ![Alt text](images/credential-types-icon.png?raw=true "Credential Types") icon from the left navigation bar.
2.
3.
