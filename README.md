Azure.azure_modules
=========

This role includes the latest changes and bug fixes for Azure modules from the `devel` branch of [Ansible repository](https://github.com/ansible/ansible). If you cannot wait for Ansible's next release, installing this role is a good choice. 

Prerequisite
------------

The usage of this role assumes that you've already setup an Ansible environment for Azure. For details, please refer to Ansible tutorial [Getting Started with Azure](http://docs.ansible.com/ansible/latest/guide_azure.html)


Installation
------------

``` bash
$ ansible-galaxy install Azure.azure_modules
```

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
        - { role: Azure.azure_modules }
      tasks:
      - name: create storage account
        azure_rm_storageaccount:
          resource_group: resourcegroupname
          name: storagename
          account_type: Standard_LRS

License
-------
MIT
