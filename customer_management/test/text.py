import docx,os
from customer_management.settings import conf_fun


def email_demo():
    path = os.getcwd()
    path = os.path.join(path,'美国-邮件回复.docx')

    file = docx.Document(path).paragraphs
    fle_len = len(file)

    print(file[1].text,'\n')
    i =1
    q= 1
    while i < fle_len:

        translate_client = conf_fun.translate_func(file[i].text)
        # template_client = conf_fun.translate_func(file[i+2].text)
        print('客户', q, file[i].text, '\n',   translate_client ,'\n')
        email_keyword(translate_client)
        print('不知道',file[i+1].text ,'\n')
        print('模板',q , file[i+2].text, '\n','\n' )
        print('这是',file[i+3].text, '\n')
        i += 5
        q +=1


# txte= ' 你好。我想把这张桌子还回去。我有卓越亚马逊，它说这将是免费退货，但在退货说明中，它说我需要附上适当的邮资。我对付那么多邮资不感兴趣，尤其是当我应该得到免费的亚马逊prime退货时。我希望你能帮忙。谢谢你 '
def email_keyword(txte):
    content = conf_fun.keyword_func(txte)
    for dict_1 in content:
        key = dict_1.get('pos')
        if key in ['n', 'nz','v'] and dict_1.get('item') not in ['你好','想', '有','是','希望', '帮忙', '能','帮忙' ,'谢谢']:
            print(dict_1.get('item'))
            sql = "INSERT  ignore into problem_keyword_1 ( problem_keyword) VALUES ('%s')"%(dict_1.get('item'))
            conf_fun.connect_mysql(sql, type='dict')
email_demo()