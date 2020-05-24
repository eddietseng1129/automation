"""

資料來源：PTT中文語料庫(418202筆資料)  →   https://goo.gl/LZPEbY 

目的：可以自行調整語庫數，愈高能回的愈多，但花的時間成本愈高

輸入：Gossiping-QA-Dataset.txt  ←  PTT中文語料庫 ； limit_num 預設 100筆 ； 預設名稱：conversations.yml

輸出：conversations.yml ← 給訓練模型用的yml格式資料

檔案位置：輸入輸出都可在當下目錄進行

※yml檔案產出後要先手動放進Lib裡面chinese的資料夾才行，如果非 window 或無 Anaconda3，請路徑再自行調設

例子；C:\\Users\\{使用者}\\Anaconda3\\Lib\\site-packages\\chatterbot_corpus\\data\\chinese



參考文獻： 

1.https://goo.gl/uRXkbW 【擁有自動學習的 Python 機器人 - ChatterBot】
2.https://goo.gl/FxANqv 【基于Python-ChatterBot搭建不同adapter的聊天机器人】

"""

def transform_yml_data(data_to_train_yml,limit_num,yml_name):

    import json
    import io
    import yaml

    with io.open(data_to_train_yml, 'r', encoding='utf-8') as dataset:

        # 為了滿足yml檔案裡面的資料格式，我們必須以這樣的形勢儲存 
        #  {'conversations': [total_list]} 等於下方   \↓
        #  {'conversations': [[問話 1,回答 1],[問話 2,回答 2],[問話 3,回答 3]]}
        
        total_list = [] # 輸入 
        dict_data = {} # 輸入
        i = 0 # 控制計算變數，依需求看要用到幾筆，經驗是1000較好，1萬很慢，但細部參數調整或許可改效能

        for line in dataset:

            i = i + 1 # 
            mv = [] # 每段對話的儲存list 規則： ['問','答']
            line = line.strip('\n') # 儲存的資料形式是一次問與答一行，故這寫\n
            question, answer = line.split('\t') # 儲存的資料形式，問與答相隔 tab，故這是\t

            if question == '': #語音庫有空白字 - 贓資料，空白的則跳出迴圈，繼續。這裡與法有改良的空間
                continue
            if answer == '':
                continue
            if i == limit_num: # 超過限制金額則跳出
                break

            mv = [question,answer] # 每次的問與答都存成一個 list
            total_list.append(mv) # 存完在放進總list裡面，迴圈開始時會清空


        dict_data = {'conversations':total_list} # 存成 dict，key名稱是conversations

    # 存成 yml，才能讓機器人讀取語庫，存完會在當下目錄出現
    with io.open(yml_name, 'w', encoding='utf8') as outfile:
        yaml.dump(dict_data, outfile, default_flow_style=False, allow_unicode=True)
    print('存 yml 檔案成功!')
    




"""
建立機器人，並匯入資料進行訓練

匯入 yml 格式資料(匯入名稱只要檔案名稱，不用類型名稱)

※yml檔案產出後要先手動放進Lib裡面chinese的資料夾才行，如果非 window 或無 Anaconda3，請路徑再自行調設

※很重要，要說三次！

例子；C:\\Users\\{使用者}\\Anaconda3\\Lib\\site-packages\\chatterbot_corpus\\data\\chinese

ex : create_chatbot('conversations')

"""

def create_chatbot(data_yml_name):
    
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer

    chatbot = ChatBot('Ron Obvious')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.chinese.{}".format(data_yml_name)) 
    
    return chatbot