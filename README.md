# Catalog App
## Purpose:
----------
Mastert Flask and Oauth to relize CURD
## Description
-------
Using Flask and Oauth to develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post images and descriptions of items.   
Most important point: CRUD

* **database_setup.py** -this file is to setup database
* **project.py** -this file is the project's most logic code.
* **lotsofitems.py** -this file is set some items in the database
* **static** -this directory contains some css files and js files
* **templates** -this directory contains all the html templetes

## Introduce to install and configure
---
You need VirtualBox and Vagrant

#### VirtualBox: 
VirtualBox is the software that actually runs the VM. You can download it from [here](https://www.virtualbox.org/wiki/Downloads).Install the platform package for your operating system.  You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.  
**Windows Users** - VirtualBox Warning If you run into difficulties using VirtualBox 5 or higher then we recommend installing an earlier version (4.3.0).

**VirtualBox Error on Mac 22-AUG-15** If you encounter a problem running the command "vagrant up" on a Mac (found later in these instructions) the issue may be with the version of VirtualBox installed. Uninstall both VirtualBox and Vagrant and use the latest test build of VirtualBox for Mac found here https://www.virtualbox.org/wiki/Testbuilds and then install Vagrant as per the instructions below. Error message on VirtualBox "Failed to load VMMR0.r0 (VERR_VMM_SMAP_BUT_AC_CLEAR)." Error message on Vagrant "The guest machine entered an invalid state while waiting for it to boot. Valid states are 'starting, running'. The machine is in the 'poweroff' state. Please verify everything is configured properly and try again." Ubuntu 14.04   
**Note:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.
#### Vagrant: 
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You cand download it from [here](https://www.vagrantup.com/downloads). Install the version for your operating system.
**Windows:** Use the Git Bash program (installed with Git) to get a Unix-style terminal. Make sure to run as administrator. Other systems: Use your favorite terminal program.



## Usage
--------------
1. Clone ​this​ repo to your local machine.Example:

		git clone PASTE_PATH_TO_REPO_HERE fullstack


2. Using the terminal, change directory to **fullstack/vagrant**, the type `vagrant up` to  launch your virtual machine.
3. Files located in the **/vagrant/ItemCatalog** directory inside the virtual machine. Change directory the directory to it.
4. In the terminal, run the **database_setup.py**
	
		python database_setup.py

	then run the **lotsofitems.py** 
		
		python lotsofitems.py
	finally, run	**project.py**

5.Open your webbrowser, type the url: (localhost:8000) in the address bar, and you wil the catalog app
	

