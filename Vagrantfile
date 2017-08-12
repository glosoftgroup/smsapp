# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.synced_folder "./devops/ansible_devops", "/vagrant/devops/ansible_devops"
  config.vm.network :private_network, ip: "10.0.0.50"
  config.vm.provision :shell, :path => "devops/ansible_devops/vagrant_bootstrap.sh"

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"

  # Share devops folder with guest VM. VirtualBox mounts shares with
  # all files as executable by default, which causes Ansible to try
  # and execute inventory files (even when they are not scripts.) The
  # mount options below prevent this.

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 2
    vb.memory = 2048
    vb.name = 'smsapp'
  end

end

