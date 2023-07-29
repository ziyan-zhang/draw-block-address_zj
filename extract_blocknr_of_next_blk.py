#! /bin/python3
'''
Author: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
Date: 2023-07-29 19:45:10
LastEditors: Ziyan ZHANG zhangzy273@mail2.sysu.edu.cn
LastEditTime: 2023-07-29 19:48:35
FilePath: /draw-block-address/extract_blocknr_of_next_blk.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
lines = []  # 存储行号
block_numbers_1 = []  # 存储第一种格式的块号
block_numbers_2 = []  # 存储第二种格式的块号

with open('kernel_log.txt', 'r') as file:
    for line_number, line in enumerate(file, start=1):
        line = line.rstrip()  # 去除行尾的换行符和空格
        if '我的块号' in line:
            if 'blocknr:' in line:
                block_number = line.split('blocknr: ')[1]
                block_numbers_1.append((line_number, block_number))
            elif 'b_blocknr:' in line:
                block_number = line.split('b_blocknr: ')[1]
                block_numbers_2.append((line_number, block_number))
            lines.append(line_number)

# 打印结果
print("第一种格式的块号:")
for line_number, block_number in block_numbers_1:
    print(f"行号: {line_number}, 块号: {block_number}")

print("\n第二种格式的块号:")
for line_number, block_number in block_numbers_2:
    print(f"行号: {line_number}, 块号: {block_number}")