# vagrant
vagrant 批量部署集群  
快速体验：
```shell
# 在 linux 机器执行以下命令，目前只兼容 centos7
# 强烈要求使用科学上网环境！！！
# 强烈要求使用科学上网环境！！！
# 强烈要求使用科学上网环境！！！
# 科学上网环境部署：https://github.com/juewuy/ShellClash

curl -sSL https://raw.githubusercontent.com/geekyouth/vagrant/main/start.sh | sh -x
```

## 参考：  
- Vagrant—多节点虚拟机集群搭建_个人文章 - SegmentFault 思否 <https://segmentfault.com/a/1190000019897182>
- Vagrat、SaltStack、Ansible、Docker、Chef、Puppet、Packer.. <https://www.reddit.com/r/sysadmin/comments/2fmkvq/vagrat_saltstack_ansible_docker_chef_puppet/>

# ansible

## ansible 学习：
- <https://getansible.com/>
- <https://github.com/shijingjing1221/ansible-first-book-examples>

## ansible-tower 激活：
- docker方式快速安装ansible-tower+破解host限制_高可用/自动化_梦绘设计  
  <https://mhsj.net/213.html>
- Ansible-Tower安装及破解 - Weclome to TTP  
  <https://ttpc.asia/archives/82/>
- Ansible-Tower--安装配置及破解 - 运维人在路上 - 博客园  
  <https://www.cnblogs.com/hujinzhong/p/12172903.html>  

# hadoop 集群
- hadoop-ansible: 利用ansible 自动 安装Hadoop 集群  
  <https://gitee.com/pippozq/hadoop-ansible>  
  <https://github.com/pippozq/hadoop-ansible>
- Ansible搭建hadoop-3.1.3高可用 - 腾讯云开发者社区-腾讯云  
  <https://cloud.tencent.com/developer/article/1676789>
- 大数据集群环境搭建 - 赵广陆 - 博客园  
  <https://www.cnblogs.com/zhaoguanglu/p/15653049.html>
- 这样搭建Spark学习环境效率似乎更高  
  <https://showme.codes/2017-01-31/setup-spark-dev-env/>  
  <https://github.com/bigdata-labs/spark2-hadoop2.6-hbase-labs>
  
# DONE:
- [x] vagrant + virtualbox 一键初始化 hadoop 集群基础环境

# TODO：
- 集成 hadoop（HDFS+Yarn）
- 集成 hive（关联 HBase）
- 集成 HBase
- 集成 phoenix
- 集成 spark
- 集成 dolphinscheduler
- 集成 HUE
- 集成 kafka（监控：KnowStreaming）
- 集成 zookeeper
- 集成 flink
- 集成 elasticsearch
- 集成 kibana
- 集成 ansible-tower
- 集成 cloudcanal
- 集成 flume
- 集成 sqoop
- 集成 MongoDB
- 集成 redis
- 集成 Kylin
- 集成 ClickHouse
- 集成 StarRocks
- 集成 Drios
- 集成 DataEase
- 集成 Atlas
- 集成 SuperSet
- 集成 Hudi
