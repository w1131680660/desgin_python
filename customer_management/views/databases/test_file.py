import os 


file_path = os.getcwd() + "/胤佑日本_订单报告_2020_12_31.txt"
print("文件路径: ", file_path)

with open(file_path, "rb") as fr:
    mark = 0
    for line in fr:
        if line != " " and line != "" and line != "\n":
            print("一行开始")
            if mark == 0:
                data_header = line.split(b"\t")
                data_header[-1] = data_header[-1][:-2]
                print("表头: ", data_header)
                print("表头长度: ", len(data_header))
            else:
                data_content = line.split(b"\t")
                print("内容: ", data_content)
                print("内容长度: ", len(data_content))
            mark += 1
            print("一行结束")
            print("============================")
