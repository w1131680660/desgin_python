# 4915
# i = 4096
# while i <= 4915:
#     uid = uuid.uuid4()
#     sql1 = "UPDATE customer_information SET uuid ='{}'  WHERE id= {}".format(uid,i)
#     sql2 = "UPDATE shopping_record SET uuid ='{}' WHERE id= {}".format(uid, i)
#     print(sql1,'\n')
#     print(sql2,'\n')
#     conf_fun.connect_mysql(sql1, type='dict')
#     conf_fun.connect_mysql(sql2, type='dict')
#     i +=1