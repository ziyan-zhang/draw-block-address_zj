###
 # @Author: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
 # @Date: 2023-07-29 19:45:10
 # @LastEditors: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
 # @LastEditTime: 2023-07-31 08:16:25
 # @FilePath: /draw-block-address/debug_file_sync.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

sudo mount /dev/nvme1n1 ~/nvme_ext4/
sudo rm ~/nvme_ext4/temp_file.txt
sudo dmesg -c
sudo ~/nvme_ext4/sync_example
sudo dmesg > ~/swap_dir/kernel_log.txt
sudo umount ~/nvme_ext4
cd
sudo umount ~/swap_dir