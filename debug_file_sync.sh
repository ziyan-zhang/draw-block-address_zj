sudo mount /dev/nvme1n1 ~/nvme_ext4/
sudo rm ~/nvme_ext4/temp_file.txt
sudo dmesg -c
sudo ~/nvme_ext4/sync_example
dmesg > ~/draw-block-address/kernel_log.txt
sudo umount ~/nvme_ext4
