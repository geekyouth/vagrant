#!/bin/bash

sudo -s
cd

yum install -y \
  vim net-tools wget htop tcping \
  https://repo.ius.io/ius-release-el7.rpm \
  https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

git --version
if [[ $? == 0 ]]; then
  echo "Git is already installed"
else
  echo "Installing Git"
  # https://ius.io/setup
  yum install -y https://repo.ius.io/ius-release-el7.rpm git236
fi

if [[ -d "vagrant" ]]; then
  echo "vagrant directory already exists, backuping..."
  mv -f vagrant vagrant.$(date +%s).bak
fi

git clone https://github.com/geekyouth/vagrant.git
cd ./vagrant
ls -alh

vagrant -v
if [[ $? == 0 ]]; then
  echo "Vagrant is already installed"
else
  echo "Installing Vagrant"
  yum install -y yum-utils
  yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
  yum -y install vagrant
fi

cd ./cluster
ls -alh

echo "#################################################"
cat Vagrantfile
echo "#################################################"

size=$(vagrant plugin list|grep -c vagrant-disksize)
if [[ $size == 0 ]]; then
  echo "Installing vagrant-disksize plugin"
  vagrant plugin install vagrant-disksize
fi

systemctl status vboxdrv
if [[ $? == 0 ]]; then
  echo "VirtualBox is already installed"
else
  echo "Installing VirtualBox"
  yum install -y kernel-devel kernel-headers make patch gcc perl
  wget https://download.virtualbox.org/virtualbox/rpm/el/virtualbox.repo -P /etc/yum.repos.d
  yum install -y VirtualBox-7.0
  sudo /sbin/vboxconfig
  systemctl status vboxdrv
fi

vagrant up
vagrant status

#################################################
# curl -sSL https://raw.githubusercontent.com/geekyouth/vagrant/main/start.sh | sh -x

#################################################
#Current machine states:
#
#hadoop81                  running (virtualbox)
#hadoop82                  running (virtualbox)
#hadoop83                  running (virtualbox)
#hadoop84                  running (virtualbox)

# 销毁：
# vagrant destroy -f
