#!/bin/python

import re

def extract_numbers(lines):
    number_pattern = r'\b(\d+)\b$'
    num_array_1 = []
    num_array_2 = []
    
    for line in lines:
        if line.startswith("我的打印jbd2_journal_commit_transaction") or line.startswith("我的打印jbd2_journal_get_descriptor_buffer"):
            match = re.search(number_pattern, line)
            if match:
                number = int(match.group(1))
                if line.startswith("我的打印jbd2_journal_commit_transaction"):
                    num_array_1.append(number)
                else:
                    num_array_2.append(number)
    
    return num_array_1, num_array_2

# 示例输入
lines = [
    "我的打印jbd2_journal_commit_transaction, jbd2_journal_next_log_block - blocknr: 1083125",
    "其他行没有数字",
    "我的打印jbd2_journal_get_descriptor_buffer, jbd2_journal_next_log_block - blocknr: 1083128",
    "我的打印jbd2_journal_commit_transaction, jbd2_journal_next_log_block - blocknr: 987654321",
    "其他行没有数字"
]

# 提取数字并打印结果
numbers_1, numbers_2 = extract_numbers(lines)
print("Numbers from '我的打印jbd2_journal_commit_transaction' lines:", numbers_1)
print("Numbers from '我的打印jbd2_journal_get_descriptor_buffer' lines:", numbers_2)