




Cadasta Platform :: an Open Source Land Registration System
===========================================================

About
-----
Cadasta Foundation harnesses innovative technology to simplify, modernize, and expedite the documentation of land and resource rights around the world.

Why?
One third of the people on the planet, from urban shanty town residents to rural smallholder farmers, have no documented right to the land they rely on. Their undocumented rights to land and resources leave them vulnerable to displacement, marginalizes them, and traps them in poverty. 
Learn more about how helping these communities document their own land and resource rights can reduce poverty and conflict, support conservation efforts, and spark more inclusive economic growth.

How?
Cadasta is a free platform designed to help you collect, organize, and store information about the land and resource rights of your community. 
Cadasta is a suite of tools for providing partners with a way to get boundary lines, ownership/tenant information and much more information stored up in the cloud in a safe and secure way. All data collected in Cadasta is owned by the person who collected and imported it. 

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="//www.youtube.com/embed/KIdW7sPY9y0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


You are welcome to use the demo platform at https://demo.cadasta.org for playing around and testing.  Happy Mapping!

|build-status-image|

Install for development
-----------------------

Install:

* `VirtualBox <https://www.virtualbox.org/>`_
    * Version 5.0.x
* `Vagrant <https://www.vagrantup.com/>`_
    * Version 1.8.1
    * If you are behind a proxy, you may need to install and configure the `vagrant-proxyconf <https://rubygems.org/gems/vagrant-proxyconf/versions/1.5.2>`_ plugin
* `Ansible <http://www.ansible.com/>`_
    * Version 2.1.3.0
    * For Linux and Mac, install Ansible 2 via pip
    * For Windows (unsupported), go through `Ansible Documentation <http://docs.ansible.com/ansible/intro_windows.html>`_ or this `blog <https://www.jeffgeerling.com/blog/running-ansible-within-windows>`_

Clone the `repository <https://github.com/cadasta/cadasta-platform>`_ to your local machine and enter the cadasta-platform directory.
Run the following commands to access the virtual machine.

Provision the VM::

  vagrant up --provision

SSH into the VM (automatically activates the Python virtual environment)::

  vagrant ssh
  
Enter the cadasta directory and start the server:: 
 
  cd cadasta
  ./runserver

Open ``http://localhost:8000/`` in your local machine's browser. This will forward you to the web server port on the VM and you should see the front page of the platform site.

See the wiki (`here <https://devwiki.corp.cadasta.org/Installation>`_ and `here <https://devwiki.corp.cadasta.org/Run%20for%20development>`_) for detailed instructions on installation and running the platform for development.

Run tests
---------

Within the development VM, from the ``/vagrant`` directory run::

  py.test cadasta

To get coverage reports run::

  py.test cadasta --cov=cadasta  --cov-report=html

This creates a HTML report under ``htmlcov``. See `pytest-cov docs <http://pytest-cov.readthedocs.org/en/latest/readme.html#reporting>`_ for other report formats.

AWS Deployment
--------------

Do this::

  vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box
  vagrant plugin install vagrant-aws
  ...

  vagrant up --provider=aws ...
  
  
.. |build-status-image| image:: https://secure.travis-ci.org/Cadasta/cadasta-platform.svg?branch=master
   :target: http://travis-ci.org/Cadasta/cadasta-platform?branch=master

Acknowledgements
================

Cadasta is grateful for the technical considerations and support provided by:

- `BrowserStack <https://www.browserstack.com/>`_

- `Opbeat <https://opbeat.com>`_

- `Travis CI <https://travis-ci.com/>`_
