import os
import time
import csv
import pandas as pd

# def main():
#     current_dir = os.path.abspath('.')
#     file_name = os.path.join(current_dir, "csss.csv")
#     csvfile = open(file_name, 'wt', newline='')  # encoding='utf-8'
#     data = []
#     header = []
#     data = {'1': [[1, 2, 3, 4, 5], [11, 12, 34, 55, 66]]}
#
#     for key in data.keys():
#         header.append(key)
#         temp = []
#         for i in range(len(data[key][0])):
#             temp.append((data[key][0][i], data[key][1][i]))
#
#     writer = csv.writer(csvfile, delimiter=",")
#
#     writer.writerow(header)
#     writer.writerows(zip(temp))
#
#     csvfile.close()
#
# def main():
#     file_name = 'csss.csv'
#     data = {'1': [[1, 2, 3, 4, 5], [11, 12, 34, 55, 66]]}
#     zz = []
#     for key in data.keys():
#         temp = []
#         for i in range(len(data[key][0])):
#             temp.append((data[key][0][i], data[key][1][i]))
#         temp = zip(temp)
#         zz.append(temp)
#     result = pd.DataFrame({''.format(key): temp})
#
#     result.to_csv(file_name, encoding='gbk')
#
#
# if __name__ == '__main__':
#     main()


import csv
import pandas as pd

# 文件头，一般就是数据名

ss ={}
data = {'1': [[1, 2, 3, 4, 5], [11, 12, 34, 55, 66]],
        '2': [[12, 22, 32, 42, 52,99], [11, 12, 34, 55, 66,222]]
        }
fileHeader = []
maxlen = 0
for key in data.keys():
    fileHeader.append(key)
    maxlen= max(maxlen,len(data[key][0]))
print(maxlen)
df =pd.DataFrame(columns=fileHeader)
for key in data.keys():
    temp = []
    for i in range(len(data[key][0])):
        temp.append((data[key][0][i], data[key][1][i]))
    print(temp)
    # temp = zip(temp)
    fill = maxlen - len(temp)
    print(fill)
    temp.extend(fill*[''])
    df[key] = temp
df.to_csv('Experiments.csv', mode='a', encoding='gbk')

    # test = pd.DataFrame(columns=fileHeader, data=temp)
    # test.to_csv('Experiments.csv',mode = 'a', encoding='gbk')

