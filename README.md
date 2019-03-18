# Parallels-Desktop-Ansible-Inventory-Script
If you for some reason running Ansible Tower in a Parallels Desktop vm and wants a custom inventory script for Parallels Desktop, this is the place for you!

Since Parallels Desktop not has an API you can query from a remote node, I'm using the Ansible python API in the inventory script to execute parallels cli commands on the virtualization host(my Mac).
## Installation
You must:
1.) Add parallels_desktop_inventory.py as a custom inventory script in Tower
2.) Since I'm using custom credentials in Tower to  inject the authentication information to the inventory script you need to add a custom credential
3.) Add authentication information to the custom credential
4.) Add an inventory and set the custom inventory script as a source
### To add a new custom inventory script in Ansible Tower
1.) choose **Inventory Scripts** from the Setup ![Alt text](images/wheel.png?raw=true "settings") menu.
