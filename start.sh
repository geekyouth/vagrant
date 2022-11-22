#!/bin/bash

sudo -s;
cd;

# https://ius.io/setup
yum install -y \
vim net-tools wget epel-release yum-utils htop tcping \
https://repo.ius.io/ius-release-el7.rpm \
https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
git236;

if [[ -d "vagrant" ]];then
  echo "vagrant directory already exists, backuping...";
  mv -f vagrant vagrant.bak;
fi

git clone https://github.com/geekyouth/vagrant.git;
cd ./vagrant; ls -alh;

cd ./cluster; ls -alh;
#cat Vagrantfile;
vargant up; vargant status;

#################################################
# curl -sSL https://raw.githubusercontent.com/geekyouth/vagrant/main/start.sh | sh -x
