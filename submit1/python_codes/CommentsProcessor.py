import pandas as pd

i = 0

productId = []
userId = []
profileName = []
helpfulness = []
score = []
time = []
summary = []
text = []

output_file_path = 'D:\桌面\\temp\作业\Comments.csv'
for line in open("D:\MC浏览器\movies_txt\movies.txt", 'r', encoding='UTF-8', errors='ignore'):
    split = line.split(' ', 1)
    #     print(split)
    if split == []:
        continue

    if split[0] == "product/productId:":
        productId.append(split[1].strip())
    elif split[0] == "review/userId:":
        userId.append(split[1].strip())
    elif split[0] == "review/profileName:":
        profileName.append(split[1].strip())
    elif split[0] == "review/helpfulness:":
        helpfulness.append(split[1].strip())
    elif split[0] == "review/score:":
        score.append(split[1].strip())
    elif split[0] == "review/time:":
        time.append(split[1].strip())
    elif split[0] == "review/summary:":
        summary.append(split[1].strip())
    elif split[0] == "review/text:":
        text.append(split[1].strip())
        i += 1

    if i % 1000000 == 0:
        print(i)

print(i)
# 字典中的key值即为csv中列名
dataframe = pd.DataFrame(
    {'productId': productId, 'userId': userId, 'profileName': profileName, 'helpfulness': helpfulness, 'score': score,
     'time': time, 'summary': summary, 'text': text})

# 将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv(output_file_path, index=False, sep=',')