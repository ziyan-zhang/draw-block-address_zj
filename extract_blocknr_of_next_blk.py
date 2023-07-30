#! /bin/python3
'''
Author: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
Date: 2023-07-29 19:45:10
LastEditors: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
LastEditTime: 2023-07-30 10:52:45
FilePath: /draw-block-address/extract_blocknr_of_next_blk.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import matplotlib.pyplot as plt


lines = []  # 存储行号
block_numbers_next_log_block = []  # 存储第一种格式的块号
block_numbers_metadata_buffer = []  # 存储第一种格式的块号
jh_b_blocknr = []  # 存储第二种格式的块号

with open('/home/zy/lab/swap_dir/kernel_log.txt', 'r') as file:
    for line_number, line in enumerate(file, start=1):
        line = line.rstrip()  # 去除行尾的换行符和空格
        if '我的块号' in line:
            if ': blocknr: ' in line:
                block_number = int(line.split('blocknr: ')[1])
                if 'jbd2_journal_next_log_block' in line:
                    block_numbers_next_log_block.append((line_number, block_number))
                elif 'jbd2_journal_write_metadata_buffer' in line:
                    block_numbers_metadata_buffer.append((line_number, block_number))
            elif ': jh2bh(jh)->b_blocknr: ' in line:
                block_number = int(line.split('b_blocknr: ')[1])
                jh_b_blocknr.append((line_number, block_number))
            lines.append(line_number)

# 打印结果
print("第一种blocknr格式的块号, block_numbers_next_log_block:")
for line_number, block_number in block_numbers_next_log_block:
    print(f"行号: {line_number}, 块号: {block_number}")

print("第一种blocknr格式的块号, block_numbers_metadata_buffer:")
for line_number, block_number in block_numbers_metadata_buffer:
    print(f"行号: {line_number}, 块号: {block_number}")

print("\n第二种b_blocknr格式的块号:")
for line_number, block_number in jh_b_blocknr:
    print(f"行号: {line_number}, 块号: {block_number}")


# 将三个数组画散点图到一张图像上, 数组的每一项分别作为横纵坐标
plt.scatter(*zip(*block_numbers_next_log_block), c='r', marker='o', label='next_log_block')
plt.scatter(*zip(*block_numbers_metadata_buffer), c='b', marker='x', label='metadata_buffer')
plt.scatter(*zip(*jh_b_blocknr), c='g', marker='^', label='jh_b_blocknr')
plt.legend()

plt.savefig('blocknr.png')


print("Done!")