import pandas as pd
import numpy as np
from rapidfuzz import process
import re
# 进行文件的io操作
# 从指定路径读取.csv文件并加载数据到DataFrame
input_file_path = 'D:\桌面\\temp\作业\People.csv'
output_file_path = 'D:\桌面\\temp\作业3\People.csv'

# data = pd.read_csv(input_file_path, encoding='latin1', dtype={'SingleDirector': str, 'Actor': str})
# data['SingleDirector'] = data['SingleDirector'].fillna("")
# data['Actor'] = data['Actor'].fillna("")
#
# actor_list = data['Actor'].tolist()
# director_list=data['SingleDirector'].tolist()
# invalids={'','Artist Not Provided','Not Specified'}
# people_list=[]
# count=0
# for person in actor_list:
#     count+=1
#     if(count%2000==0):
#         print(count)
#     if pd.notnull(person):
#          #把这一格的内容用逗号分隔，并去掉多余空格 最后用列表存储
#          actors_value =[actor.strip() for actor in person.split(',') ]
#          for value in actors_value:
#              if pd.notnull(value) and value not in people_list and value not in invalids:#要注意，我们在爬虫的时候用了Artist Not Provided来表示未知主演
#                   people_list.append(value)
#
# count=0
# for person in director_list:
#     count += 1
#     if (count % 3000 == 0):
#         print(count)
#     if pd.notnull(person):
#          #把这一格的内容用逗号分隔，并去掉多余空格 最后用列表存储
#          directors_value =[director.strip() for director in person.split(',') ]
#          for value in directors_value:
#              if pd.notnull(value) and value not in people_list and value not in invalids:#要注意，我们在爬虫的时候用了Artist Not Provided来表示未知主演
#                   people_list.append(value)
#
# processed_data = pd.DataFrame({'Name': people_list})

data = pd.read_csv(input_file_path, encoding='latin1',dtype={'Name': str})
#处理特殊字符
# row_to_drop=[]
# for index, row in data.iterrows():
#     if(index%5000==0):
#         print(index)
#     value = row['Name']
#     if pd.notnull(value):
#         if 'NONE' in value.upper():
#             row_to_drop.append(index)
#             continue
#         # 替换单引号为双引号
#         value = value.replace("'", '"')
#         # 去除特殊字符'&amp'和'&nbsp;'
#         value = value.replace('&nbsp;', '').replace('&amp;', '').replace('""','')
#         if(value.startswith('"')&value.count('"')%2==1):
#             value=value[1:]# 如果开头有分号，则去除开头的分号
#         value = value.strip()
#         data.at[index, 'Name'] = value  # 更新DataFrame中的值
# data.drop(row_to_drop, inplace=True)
# row_to_drop=[]
# #处理“and”
# new_rows = []
# for index, row in data.iterrows():
#     if(index%3000==0):
#         print(index)
#     value = row['Name']
#     if pd.notnull(value):
#         if re.search(r'\b[aA][nN][dD]\b', value):  # 使用正则表达式匹配包含"and"的内容
#             row_to_drop.append(index)
#             parts = re.split(r'\b[aA][nN][dD]\b', value)  # 使用split方法按照"and"分割字符串
#             for part in parts:
#                 new_rows.append({'Name': part.strip()})
# data.drop(row_to_drop,inplace=True)
# data = pd.concat([data, pd.DataFrame(new_rows)], ignore_index=True).drop_duplicates(subset='Name')

# 创建'match'列，初始值设为空字符串
data['match'] = ''
#计算相似度
for i, row in data.iterrows():
    value = row['Name']
    if i%2000==0:
        print(i)
    if i not in data.index:
        continue
    if data.at[i, 'match'] !='':#说明已经找到了匹配项
        continue
    end_index = min(i + 9, len(data))  # 防止索引超出范围
    names_to_compare = data.loc[(data['match'] == '') & (data.index > i) & (data.index <= end_index), 'Name'].values
    similar_indices = []
    #print('now'+value)
    for j, name in enumerate(names_to_compare):
        value_parts = value.split('?')[0].split()[:2]  # 取value的前两个单词（不考虑问号）
        name_parts = name.split('?')[0].split()[:2]  # 取name的前两个单词
        value_parts = ''.join(value_parts)
        name_parts=''.join(name_parts)
        if (value_parts.lower() in name_parts.lower() or name_parts.lower() in value_parts.lower()):#如果一模一样
             #print(name)
             similar_indices.append(j)
    #print(similar_indices)
    # 设置'to_remove'列为True
    if similar_indices:
        for index in similar_indices:
            data.at[i+index+1, 'match'] = value

# 保存到文件
data.to_csv(output_file_path, index=False)