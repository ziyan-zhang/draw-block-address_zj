#! /bin/python3
'''
Author: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
Date: 2023-07-29 19:45:10
LastEditors: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
LastEditTime: 2023-08-01 08:37:27
FilePath: /draw-block-address/extract_blocknr_of_next_blk.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import matplotlib.pyplot as plt
import time
import os

line_nrs = []  # 存储行号

# 一共维护了10个数组
jbd2_journal_next_log_blocks = []  # 存储第一种格式的块号
jbd2_journal_write_metadata_buffers = []  # 存储第一种格式的块号
zj_journal_next_log_blocks = []  # 存储第一种格式的块号
zj_journal_write_metadata_buffers = []  # 存储第一种格式的块号

jbd_jh_b_blocknrs = []  # 存储第二种格式的块号
zj_jh_b_blocknrs = []

jbd2_commit_trans_submits = [] # 调用submitbh提交的块号
zj_commit_trans_submits = [] # 调用submitbh提交的块号
jbd2_submit_commit_record_submits = []
zj_submit_commit_record_submits = []

log_file = '/home/zy/lab/swap_dir/kernel_log.txt'
# 提取log_file的创建时间, 并转化成字符串形式
log_file_create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(log_file)))
# 打印log_file的创建时间
print(f"log_file: {log_file} 的创建时间: {log_file_create_time}")

with open(log_file, 'r') as file:
    for line_number, line in enumerate(file, start=1):
        line = line.rstrip()  # 去除行尾的换行符和空格
        if '我的块号' in line and ': blocknr: ' in line:
            block_number = int(line.split('blocknr: ')[1])
            if 'jbd2_journal_next_log_block' in line:
                jbd2_journal_next_log_blocks.append((line_number, block_number))
            elif 'jbd2_journal_write_metadata_buffer' in line:
                jbd2_journal_write_metadata_buffers.append((line_number, block_number))

            if 'zj_journal_next_log_block' in line:
                zj_journal_next_log_blocks.append((line_number, block_number))
            elif 'zj_journal_write_metadata_buffer' in line:
                zj_journal_write_metadata_buffers.append((line_number, block_number))


        elif '我的块号' in line and ': jh2bh(jh)->b_blocknr: ' in line:
            assert '_journal_write_metadata_buffer' in line
            block_number = int(line.split('b_blocknr: ')[1])

            if 'jbd2_journal_write_metadata_buffer' in line:
                jbd_jh_b_blocknrs.append((line_number, block_number))

            elif 'zj_journal_write_metadata_buffer' in line:
                zj_jh_b_blocknrs.append((line_number, block_number))

        line_nrs.append(line_number)
        
        if "我的提交" in line:
            assert " submit_bh: " in line
            if "jbd2_journal_commit_transaction, " in line:
                block_number = int(line.split('submit_bh: ')[1])
                jbd2_commit_trans_submits.append((line_number, block_number))

            if "zj_journal_commit_transaction, " in line:
                block_number = int(line.split('submit_bh: ')[1])
                zj_commit_trans_submits.append((line_number, block_number))

            if "jbd2/commit.c/ journal_submit_commit_record" in line:
                block_number = int(line.split('submit_bh: ')[1])
                jbd2_submit_commit_record_submits.append((line_number, block_number))

            if "zj/commit.c/ journal_submit_commit_record" in line:
                block_number = int(line.split('submit_bh: ')[1])
                zj_submit_commit_record_submits.append((line_number, block_number))


# 上面的10个数组合成一个数组, 按照数组每一项的第一个维度大小排序
block_numbers = sorted(jbd2_journal_next_log_blocks + jbd2_journal_write_metadata_buffers \
    + zj_journal_next_log_blocks + zj_journal_write_metadata_buffers \
    + jbd_jh_b_blocknrs + zj_jh_b_blocknrs \
    + jbd2_commit_trans_submits + zj_commit_trans_submits \
    + jbd2_submit_commit_record_submits + zj_submit_commit_record_submits, key=lambda x: x[0])

# 将下面的几句话包装到一个函数里面
def plot_10lines():
    # 将三个数组画散点图到一张图像上, 数组的每一项分别作为横纵坐标. 并把每个点的横纵坐标打印到图中
    plt.scatter(*zip(*jbd2_journal_next_log_blocks), c='r', marker='o', label='jbd2_next_log_block')
    for line_number, block_number in jbd2_journal_next_log_blocks:
        plt.text(line_number, block_number, block_number, ha='center', va='bottom', fontsize=10)

    plt.scatter(*zip(*zj_journal_next_log_blocks), c='k', marker='d', label='zj_next_log_block')
    for line_number, block_number in zj_journal_next_log_blocks:
        plt.text(line_number, block_number, block_number, ha='center', va='bottom', fontsize=10)


    plt.scatter(*zip(*jbd2_journal_write_metadata_buffers), c='b', marker='x', label='jbd2_write_metadata_buffer')
    plt.scatter(*zip(*zj_journal_write_metadata_buffers), c='c', marker='s', label='zj_write_metadata_buffer')

    plt.scatter(*zip(*jbd_jh_b_blocknrs), c='g', marker='^', label='jbd_jh_b_blocknrs')
    plt.scatter(*zip(*zj_jh_b_blocknrs), c='m', marker='v', label='zj_jh_b_blocknrs')

    # 下面打印*_submits结尾的数组
    
    plt.scatter(*zip(*jbd2_commit_trans_submits), c='y', marker='*', label='jbd2_commit_trans_submits')
    for line_number, block_number in jbd2_commit_trans_submits:
        plt.text(line_number, block_number, block_number, ha='center', va='bottom', fontsize=10)

    plt.scatter(*zip(*zj_commit_trans_submits), c='orange', marker='*', label='zj_commit_trans_submits')
    for line_number, block_number in zj_commit_trans_submits:
        plt.text(line_number, block_number, block_number, ha='center', va='bottom', fontsize=10)

    plt.scatter(*zip(*jbd2_submit_commit_record_submits), c='brown', marker='*', label='jbd2_submit_commit_record_submits')
    for line_number, block_number in jbd2_submit_commit_record_submits:
        plt.text(line_number, block_number, block_number, ha='center', va='bottom', fontsize=10)

    plt.scatter(*zip(*zj_submit_commit_record_submits), c='black', marker='*', label='zj_submit_commit_record_submits')
    for line_number, block_number in zj_submit_commit_record_submits:
        plt.text(line_number, block_number, block_number, ha='center', va='bottom', fontsize=10)
    

# # 分别设定y轴范围为[520000, 530000], [1082300, 1082350], [2097000, 2098000]. 仿照上面的代码段

plt.subplot(222)
plt.ylim(1081560, 1081590)
plot_10lines()

# plt.subplot(424)
# plt.ylim(520000, 570000)
# plot_10lines()

plt.subplot(224)
plt.ylim(90000, 140000)
plot_10lines()

# plt.subplot(428)
# plt.ylim(-5000, 35000)
# plot_10lines()

plt.subplot(121)
# plt.plot(*zip(*block_numbers), c='gray', marker='', label='block_numbers')
plot_10lines()
plt.legend()
plt.title(log_file_create_time)


plt.savefig('blocknr.png')
plt.show()

print("Done!")