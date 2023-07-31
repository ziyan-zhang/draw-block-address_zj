#!/bin/bash
# 挂载交换盘和非模块文件系统盘到目录
sudo mount /dev/sdb ~/swap_dir/
sudo mount /dev/nvme0n1 ~/nvme_ext2/
sudo mount /dev/nvme1n1 ~/nvme_ext4/
sudo mount /dev/nvme2n1 ~/nvme_ext4_mj/

# 安装z-journal模块
sudo insmod ~/swap_dir/zj.ko
sudo insmod ~/swap_dir/ext4mj.ko
# 格式化z-journal盘
sudo ./e2fsprog-zj/misc/mke2fs -t ext4 -J multi_journal -F -G 1 /dev/nvme2n1
sudo ./e2fsprog-zj/misc/tune2fs -o journal_data /dev/nvme2n1
# 挂载z-journal盘
sudo mount -t ext4mj /dev/nvme2n1 ~/zj_dir/

df -T
sudo cp /home/zy/swap_dir/*.cpp ~/nvme_ext2/
sudo cp /home/zy/swap_dir/*.cpp ~/nvme_ext4/
sudo cp /home/zy/swap_dir/*.cpp ~/nvme_ext4_mj/

cd nvme_ext4/