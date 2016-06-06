# Item Catalog - Project

Item Catalog Project for Udacity's full-stack [Nanodegree Program]. This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Installation

Here are the tools you'll need to install to get it running:
* `Git`: If you don't already have Git installed, [download Git from git-scm.com]. Install the version for your operating system.
* `VirtualBox`: Is the software that actually runs the VM. [You can download it from virtualbox.org, here.] Install the version for your operating system.
* `Vagrant`: Is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  [You can download it from vagrantup.com.] Install the version for your operating system.


### Use Git/GitHub to fetch the VM configuration
This GitHub repository contains all of the code you will need to run the Item Catalog application.

1. Fork this repository (Click **Fork** in the top-right corner)
2. Copy the HTTPS method of your newly forked repository.
3. Then from the terminal run: `git clone PASTE_PATH_TO_REPO_HERE catalog`.

This will give you a directory named **catalog`**. Note: you will want to paste the path you copied from step 2 into `PASTE_PATH_TO_REPO_HERE`.

### Run the virtual machine
To Run the virtual machine follow the next steps:
* Using the terminal, change directory to catalog/vagrant (`cd catalog/vagrant`), then type `vagrant up` to launch your virtual machine.
* Once it is up and running, type `vagrant ssh` to log into it.
* One you log into, then explore the starter code for this project provided type `cd /vargrant/catalog` where you will see the followings directory/files you have to work with on this project.
  ```
  catalog/
  ├── static/  - this directory is used to store static resources of the application (css,img)
  ├── templates/  - this directory is used to store the html templates of the application
  ├── database_setup.py - this file is used to set up the database schema
  ├── populate_db.py - this file is used to populate the database schema
  ├── client_secrets.json - google credentials to authentication
  ├── fb_client_secrets.json - fb credentials to authentication
  └── application.py - this file is used to run the application

  ```
### Create Database and Run application

* To build and access the database we run `python database_setup.py`.
* Then we populate the database running `python populate_db.py`.
* Once database schema is created and it's populated. We run the program from the command line with `$ python application.py`.
* Finally, Access and test your application by visiting [http://localhost:8000] locally on your browser.

[Nanodegree Program]: <https://www.udacity.com/nanodegree>
[download Git from git-scm.com]: <https://git-scm.com/downloads>
[You can download it from virtualbox.org, here.]: <https://www.virtualbox.org/wiki/Downloads>
[You can download it from vagrantup.com.]: <https://www.vagrantup.com/downloads.html>
[Python website]: <https://www.python.org/download/releases/2.7/>
[http://localhost:8000]: <http://localhost:8000>