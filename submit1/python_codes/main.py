# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助

import pandas as pd
import numpy as np
import fuzzywuzzy
import re

# 进行文件的io操作
# 从指定路径读取.csv文件并加载数据到DataFrame
input_file_path = 'D:\桌面\\temp\作业2\Movies.csv'
output_file_path = 'D:\桌面\\temp\作业3\Movies.csv'
#input_people_path='D:\桌面\\temp\作业3\People.csv'

data = pd.read_csv(input_file_path, encoding='latin1', dtype={'Name': str, 'ASIN': str})#, index_col='temp_index'
data['Day']=pd.to_numeric(data['Day'], errors='coerce')
data['Month']=pd.to_numeric(data['Month'], errors='coerce')
data['Year']=pd.to_numeric(data['Year'], errors='coerce')
data['Grade']=pd.to_numeric(data['Grade'], errors='coerce')
data['Comments']=pd.to_numeric(data['Comments'], errors='coerce')
data['Time']=pd.to_numeric(data['Time'], errors='coerce')
data['Name'] = data['Name'].fillna("")

#data_people=pd.read_csv(input_people_path, encoding='latin1', dtype={'Name': str, 'match': str})
# for index,row in data.iterrows():
#     data.at[index, 'temp_index'] = index
# data.to_csv(output_file_path, index=False)

# 按Order列进行分组，获取每个组和对应的要选择的name
#max_name_per_group = data.groupby('Order')['Name'].apply(lambda x: max(x, key=len))

# count=0
# new_rows = []
# # 遍历每个组，如果组内只有1行，则直接修改 Merge 值为1；否则，新增一行并设置 Merge 值为1
# for group, max_name in max_name_per_group.items():
#     group_rows = data[data['Order'] == group]  # 获取当前组的所有行
#     count+=1
#     if count%1000==0:
#         print(count)
#     if len(group_rows) == 1:
#         data.loc[group_rows.index, 'Merge'] = 1  # 修改 Merge 值为1
#     else:
#         new_row={col: group_rows.iloc[0][col] for col in data.columns}  # 复制当前组第一行的数据
#         new_row['Name'] = str(max_name)  # 将 Name 替换为最长的 Name
#         new_row['Merge'] = 1  # 设置 Merge 值为1
#         new_rows.append(new_row)
#
# data = pd.concat([data, pd.DataFrame(new_rows)], ignore_index=True)
# print('name OK')
# data.to_csv(output_file_path, index=False)
#data=data.reset_index(drop=True)
#处理评分
# def find_right_grade_in_group(group):
#     if (group['Order'].iloc[0] % 2000 == 0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     # 在分组中找到最大的'Comments'
#     max_count = group['Comments'].max()
#     # 找到打分人数最多时打出的分数
#     right_grade = group.loc[group['Comments'] == max_count, 'Grade']
#     if right_grade.empty: #说明，虽然有很多行，但每一行都为空
#         right_grade=0
#     else:
#         right_grade=right_grade.values[0]
#     # 创建一个临时列，用于保存需要替换的 Grade 列的值
#     group['Temp_Grade'] = group['Grade']
#     # 将 Merge 值为1的行的 Grade 列替换为 right_grade
#     group.loc[group['Merge'] == 1, 'Temp_Grade'] = right_grade
#     # 将替换后的 Grade 列的值赋回到原来的 Grade 列
#     group['Grade'] = group['Temp_Grade']
#     # 删除临时列
#     group.drop('Temp_Grade', axis=1, inplace=True)
#     return group
#
# data = data.groupby('Order').apply(find_right_grade_in_group).reset_index(drop=True)
# print('grade OK')
# data.to_csv(output_file_path, index=False)
#
# #处理电影时长
# def find_right_time_in_group(group):
#     if (group['Order'].iloc[0] % 1000 == 0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     # 在分组中找到数值最大的'Time'
#     max_time = group['Time'].max()
#     # 创建一个临时列，用于保存需要替换的 Grade 列的值
#     group['Temp'] = group['Time']
#     # 将 Merge 值为1的行的 Grade 列替换为 right_grade
#     group.loc[group['Merge'] == 1, 'Temp'] = max_time
#     # 将替换后的 Grade 列的值赋回到原来的 Grade 列
#     group['Time'] = group['Temp']
#     # 删除临时列
#     group.drop('Temp', axis=1, inplace=True)
#     return group
#
# data = data.groupby('Order').apply(find_right_time_in_group).reset_index(drop=True)
# print('time OK')
# data.to_csv(output_file_path, index=False)
#
# #处理上映时间,涉及3个列：year month day
# def find_right_date_in_group(group):
#     # 在处理每个 group 前打印 group 的 Order 值
#     if(group['Order'].iloc[0]%500==0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     else:
#         # 在分组中找到数值最小且非零的'Year', 'Month', 'Day'
#         min_year = group.loc[group['Year'] > 0, 'Year'].min()
#         min_month = group.loc[
#             (group['Year'] == min_year) & (group['Month'] > 0), 'Month'].min() if not pd.isnull(min_year) else np.nan
#         min_day = group.loc[(group['Year'] == min_year) & (group['Month'] == min_month) & (
#                     group['Day'] > 0), 'Day'].min() if not pd.isnull(min_month) else np.nan
#
#         # 将 Merge 值为1的行的 Year、Month、Day 替换为最小值
#         mask = group['Merge'] == 1
#         group.loc[mask, ['Year', 'Month', 'Day']] = min_year, min_month, min_day
#
#         return group
#
# data = data.groupby('Order').apply(find_right_date_in_group).reset_index(drop=True)
# print('date OK')
# data.to_csv(output_file_path, index=False)
#
# #处理版本
# def find_formats_in_group(group):
#     # 在处理每个 group 前打印 group 的 Order 值
#     if(group['Order'].iloc[0]%500==0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     else:
#         # 将同一组的format都放进列表里面，在放的时候要注意判断这个format是否为空，以及这个format是否已经放进了列表
#         formats = []
#         for format_value in group['Format']:
#             if pd.notnull(format_value) and format_value not in formats:
#                 formats.append(format_value)
#         combined_format = ','.join(formats)
#         # 将 Merge 值为1的行的 Format替换为combined_format
#         mask = group['Merge'] == 1
#         group.loc[mask, 'Format'] = combined_format
#         return group
#
# data = data.groupby('Order').apply(find_formats_in_group)
# print('format OK')
# data.to_csv(output_file_path, index=False)

# people_invalids={'','Artist Not Provided','Not Specified'}
# def data_processing(value):
#     # 替换单引号为双引号
#     value = value.replace("'", '"')
#     # 去除特殊字符'&amp'和'&nbsp;'
#     value = value.replace('&nbsp;', '').replace('&amp;', '').replace('""','')
#     if value.startswith('"') and value.count('"') % 2 == 1:
#         value = value[1:]  # 如果开头有分号，则去除开头的分号
#     value = value.strip()
#     if re.search(r'\b[aA][nN][dD]\b', value):  # 使用正则表达式匹配包含"and"的内容
#         parts = re.split(r'\b[aA][nN][dD]\b', value)  # 使用split方法按照"and"分割字符串
#         return [part.strip() for part in parts]
#     else:
#         return [value]
#处理导演
# def find_directors_in_group(group):
#     # 在处理每个 group 前打印 group 的 Order 值
#     if(group['Order'].iloc[0]%1000==0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     else:
#         #首先要用逗号分隔开，然后要判断能否放进列表（重复项不放）
#         directors = []
#         for director_value in group['SingleDirector']:
#             if pd.notnull(director_value):
#                 #把这一格的内容用逗号分隔，并去掉多余空格 最后用列表存储
#                 directors_value =[director.strip() for director in director_value.split(',') if director.strip()]#最后面的if是为了去掉多余空格
#                 for value in directors_value:
#                     if pd.notnull(value) and value not in directors and value not in people_invalids and 'none' not in value.lower():
#                         #接下来要稍微做一下数据处理
#                         processed_values = data_processing(value)
#                         directors.extend(processed_values)
#         combined_directors = ','.join(directors)
#         # 将 Merge 值为1的行的 Format替换为combined_format
#         mask = group['Merge'] == 1
#         group.loc[mask, 'SingleDirector'] = combined_directors
#         return group
#
# data = data.groupby('Order').apply(find_directors_in_group).reset_index(drop=True)
# data.to_csv(output_file_path, index=False)

#处理演员，和处理导演的方式类似
# def find_actors_in_group(group):
#     # 在处理每个 group 前打印 group 的 Order 值
#     if(group['Order'].iloc[0]%2000==0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     else:
#         #首先要用逗号分隔开，然后要判断能否放进列表（重复项不放）
#         actors = []
#         for actor_value in group['Actor']:
#             if pd.notnull(actor_value):
#                 #把这一格的内容用逗号分隔，并去掉多余空格 最后用列表存储
#                 actors_value =[actor.strip() for actor in actor_value.split(',') if actor.strip()]#最后面的if是为了去掉多余空格
#                 for value in actors_value:
#                     if pd.notnull(value) and value not in actors and value not in people_invalids and 'none' not in value.lower():
#                         #接下来要稍微做一下数据处理
#                         processed_values = data_processing(value)
#                         actors.extend(processed_values)
#         combined_actors = ','.join(actors)
#         # 将 Merge 值为1的行的 Format替换为combined_format
#         mask = group['Merge'] == 1
#         group.loc[mask, 'Actor'] = combined_actors
#         return group
#
# data = data.groupby('Order').apply(find_actors_in_group).reset_index(drop=True)
# print('actor OK')
# data.to_csv(output_file_path, index=False)
#
# #处理电影风格
# def find_genres_in_group(group):
#     # 在处理每个 group 前打印 group 的 Order 值
#     if(group['Order'].iloc[0]%3000==0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     else:
#         #首先要用逗号分隔开，然后要判断能否放进列表（重复项不放）
#         genres = []
#         invalids={'Blu-ray','Studio Specials','Widescreen','Movies','MOD CreateSpace Video','Digital VHS','Fully Loaded DVDs'}#这些是不正确的genre。定义为集合类型以便检查
#         for genre_value in group['Type']:
#             if pd.notnull(genre_value):
#                 #把这一格的内容用逗号分隔，并去掉多余空格 最后用列表存储
#                 genres_value =[genre.strip() for genre in genre_value.split(',') if genre.strip()]#最后面的if是为了去掉多余空格
#                 for value in genres_value:
#                     if pd.notnull(value) and value not in genres and value not in invalids:#要注意，我们在爬虫的时候用了Artist Not Provided来表示未知主演
#                         genres.append(value)
#         combined_genres = ','.join(genres)
#         # 将 Merge 值为1的行的 Format替换为combined_format
#         mask = group['Merge'] == 1
#         group.loc[mask, 'Type'] = combined_genres
#         return group
#
# data = data.groupby('Order').apply(find_genres_in_group).reset_index(drop=True)
# print('genre OK')
# data.to_csv(output_file_path, index=False)
#
# #处理URL,它用于表示数据血缘
# def find_URLs_in_group(group):
#     # 在处理每个 group 前打印 group 的 Order 值
#     if(group['Order'].iloc[0]%1000==0):
#         print(f"Processing group {group['Order'].iloc[0]}")
#     if(len(group)==1):
#         return group
#     else:
#         #首先要用逗号分隔开，然后要判断能否放进列表（重复项不放）
#         URLs = []
#         for URL_value in group['URL']:
#             if pd.notnull(URL_value) and URL_value not in URLs:
#                URLs.append(URL_value)
#         combined_URLs = ','.join(URLs)
#         # 将 Merge 值为1的行的 Format替换为combined_format
#         mask = group['Merge'] == 1
#         group.loc[mask, 'URL'] = combined_URLs
#         return group
#
# data = data.groupby('Order').apply(find_URLs_in_group).reset_index(drop=True)
# print('URL OK')
# data.to_csv(output_file_path, index=False)

#处理表格，去除不需要的行，修改列的名字
# 删除 Merge 列值为空的行
data.dropna(subset=['Merge'], inplace=True)
# 重命名各个列
data.rename(columns={'URL': 'URLs','Time': 'Runtime','Actor': 'Actors','Type': 'Genres','Format': 'Formats','SingleDirector': 'Directors'}, inplace=True)
# 删除多个列
data.drop(['ASIN', 'Comments','temp_index'], axis=1, inplace=True)

#接下来，处理人名信息，它存在于导演、演员字段


# 将处理后的数据保存到新的.csv文件
data.to_csv(output_file_path, index=False)
