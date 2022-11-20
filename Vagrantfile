# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # https://docs.vagrantup.com.

  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "centos/7"

  config.vm.box_check_update = false
  config.vm.network "public_network"

  config.vm.provision "shell", inline: <<-SHELL
    # 默认开启 root 远程登录
    # https://teamsmiley.github.io/2018/03/17/vagrant-ssh-root/
    # root password set
    sudo -s
    echo -e "123456\n123456" | passwd
    # root login allow
    sed  -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config;
    sed  -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config;

    systemctl restart sshd;
    # reboot;
  SHELL

  config.vm.allow_hosts_modification = true
  config.vm.hostname = "hadoop"

end
