azure.azure_modules
=========

This role includes the latest changes and bug fixes for Azure modules from the `devel` branch of [Ansible repository](https://github.com/ansible/ansible). If you cannot wait for Ansible's next release, installing this role is a good choice. 

Prerequisite
------------

The usage of this playbook role assumes that you've already setup an Ansible environment for Azure. For details, please refer to Ansible tutorial [Getting Started with Azure](http://docs.ansible.com/ansible/latest/guide_azure.html) or [Install and configure Ansible](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/ansible-install-configure). 


Installation
------------

1. Install the role.

  ``` bash
  $ ansible-galaxy install azure.azure_modules
  ```

2. Upgrade Azure Python SDKs required by new Azure modules.

  ``` bash
  $ pip install -r ~/.ansible/roles/azure.azure_modules/files/requirements-azure.txt
  ```
    
  &nbsp;&nbsp;&nbsp;&nbsp;or
      
  ``` bash
  $ sudo pip install -r ~/.ansible/roles/azure.azure_modules/files/requirements-azure.txt
  ```

   Several reasons for installing Python SDKs are listed here.

   - A new module is added to the role and this module is for one new Azure resource, which is not included in existing Ansible releases yet. The corresponding SDK for this new resource needs to be installed.

   - Newer versions of SDKs may introduce breaking API change. One specific working version should be installed here.

   The required SDKs are listed in the *[~/files/requirements-azure.txt](files/requirements-azure.txt)* file. The `requirements-azure.txt` file can be found in the installed role folder, which is usually at `~/.ansible/roles/files` folder.
    
   The tricky part is the installation location, which has to be the same as where existing Azure Python SDKs are installed. If you meet any error when executing the above command, please read below part carefully to double check the installation location. 

   Taking Ubuntu for example, the existing SDKs may be located in folders like `/home/<your-user-name>/.local/lib/python2.7/site-packages` or `/usr/local/lib/python2.7/dist-packages`. The former is a user folder and the latter is a system folder, which requires sudo access. This depends on how you have installed `ansible`. In short, you should install the SDKs the same way as you installed `ansible` so that the SDKs are in the same `site-packages` folder.

   On macOS, the existing SDKs may be located in folders like `/Users/<your-user-name>/Library/Python/2.7/lib/python/site-packages` or `/Library/Python/2.7/site-packages`. Like Ubuntu, the former is a user folder and the latter is a system folder.

   One way to figure out the correct `site-packages` path is to check the details of existing packages, say `azure-mgmt-storage` by running the command below:

  ``` bash
  $ pip show azure-mgmt-storage
  ```

   You can get the output like below. 

  ``` bash
  your-user-name@ansible:~$ pip show azure-mgmt-storage
  Name: azure-mgmt-storage
  Version: 1.5.0
  Summary: Microsoft Azure Storage Management Client Library for Python
  Home-page: https://github.com/Azure/azure-sdk-for-python
  Author: Microsoft Corporation
  Author-email: azpysdkhelp@microsoft.com
  License: MIT License
  Location: /home/<your-user-name>/.local/lib/python2.7/site-packages
  Requires: azure-common, azure-mgmt-nspkg, msrestazure
  ```

From above information you can learn that the SDKs are installed in *user* `site-packages` folder and use `pip install` to install the listed packages. If the SDKs are installed in *system* path, use `sudo pip install` to install the listed packages.

Role Variables
--------------

No.

Dependencies
------------

No dependencies on other roles.

Example Playbook
----------------

    - hosts: localhost
      roles:
        - { role: azure.azure_modules }
      tasks:
      - name: create storage account
        azure_rm_storageaccount:
          resource_group: resourcegroupname
          name: storagename
          account_type: Standard_LRS

License
-------
MIT
