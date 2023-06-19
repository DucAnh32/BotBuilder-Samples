# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, Activity, Attachment, MediaUrl

# from config import DefaultConfig
# from database_connector import *
import openai
import threading
import pandas as pd
from PIL import Image



class EchoBot(ActivityHandler):
    def __init__(self) -> None:
        self.messages = [
        {"role": "system", "content": "You are a helpful and kind AI Assistant."},
        ]
        # self.db= database()
        # self.schema=self.db.get_sample()
        self.data=pd.read_csv('data_demo.csv',encoding='UTF-8').head(3)
        self.categories=pd.read_csv('categories.csv',encoding='UTF-8')
        # self.chatbot(f'Tôi sẽ cung cấp bảng dữ liệu gồm nhóm, ý nghĩa và tên cột như sau: {self.categories}')
        self.chatbot(f'Tôi sẽ cung cấp bảng dữ liệu mẫu như sau: {self.data}')
        self.chatbot('những câu trả lời tính toán hãy đưa ra câu lệnh sql')
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("DAC xin chào")
    
    def chatbot(self, input):
        if input:
            self.messages.append({"role": "user", "content": input})
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages
            )
            reply = chat.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reply})
            return reply
    
    def execute_sql(self,msg):
        sql = get_sql_from_msg(msg)
        print(sql)
        sql_response = self.db.execute_sql(sql)
        self.chatbot(str(sql_response))
    
    async def on_message_activity(self, turn_context: TurnContext):
        message=str(turn_context.activity.text).lower()
        prompt=''
        response=self.chatbot(message) 
        print(response)
        try:
            sql = get_sql_from_msg(response)
            re = self.db.execute_sql(sql)
            print(re)
        except:
            print('error sql')
        return await turn_context.send_activity(
            MessageFactory.text(response)
        )
        # attachment = Attachment(
        #     content_type='image/jpeg',
        #     content_url="image",
        #     name='350365420_1031850424449301_8816508884114267913_n.jpg'
        # )
        # return await turn_context.send_activity(MessageFactory.attachment(attachment))
        # return await turn_context.send_activity(MessageFactory.text(response))