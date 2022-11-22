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
  mv -f vagrant vagrant.bak
fi

git clone https://github.com/geekyouth/vagrant.git
cd ./vagrant
ls -alh

cd ./cluster
ls -alh

echo #################################################
cat Vagrantfile
echo #################################################

vagrant up
vagrant status

#################################################
# curl -sSL https://raw.githubusercontent.com/geekyouth/vagrant/main/start.sh | sh -x
