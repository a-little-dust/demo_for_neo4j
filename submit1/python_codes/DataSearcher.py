import pandas as pd
import requests
import json

input_file_path = 'D:\桌面\\temp\作业2\\01.csv'
output_file_path = 'D:\桌面\\temp\作业2\GetData.csv'
data = pd.read_csv(input_file_path, encoding='latin1', dtype={'Name': str})
data['Day']=pd.to_numeric(data['Day'], errors='coerce')
data['Month']=pd.to_numeric(data['Month'], errors='coerce')
data['Year']=pd.to_numeric(data['Year'], errors='coerce')
data['Runtime']=pd.to_numeric(data['Runtime'], errors='coerce')
data['Name'] = data['Name'].fillna("")

# 假设row是你处理的某一行数据
for index,row in data.iterrows():
    if index%100==0:
        print(index)
    if pd.notna(row['Name']) and row['Name']!='':
        if pd.isna(row['Day']) or row['Day']==0 or row['Runtime']==0:
            title = row['Name']
            url1 = 'https://imdb-api.com/API/SearchMovie/k_5j8b8k9e/' + title
            response1 = requests.get(url1)  # 第一个请求
            res_json = json.loads(response1.text)
            if res_json.get('results'):
                movie_id = res_json.get('results')[0].get('id')
                url2 = 'https://imdb-api.com/en/API/Title/k_5j8b8k9e/' + movie_id
                response2 = requests.get(url2)  # 第二个请求
                movie_json = json.loads(response2.text)
                run_time=movie_json.get('runtimeMins')
                release_date = movie_json.get('releaseDate')
                # 更新数据
                if(row['Runtime']==0):
                   data.at[index,'Runtime']=run_time
                if pd.isna(row['Day']) or row['Day'] == 0:
                    data.at[index,'release_date']=release_date
                else:
                    data.at[index, 'release_date'] =f"{row['Year']}/{row['Month']}/{row['Day']}"

data.to_csv(output_file_path, index=False)
