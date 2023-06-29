# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import mysql.connector
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, Activity, Attachment, MediaUrl

from config import DefaultConfig
from database_connector import *
import openai
import threading
import pandas as pd
from PIL import Image
import time
import os
from langchain.agents import *
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
import random


class EchoBot(ActivityHandler):
    def __init__(self) -> None:
        self.messages = [
        {"role": "system", "content": "You are a helpful and kind AI Assistant."},
        ]
        self.db= database()
        self.cus_stt=0
        self.lastmess=' '
        self.rm_id='000000'
        self.flagnote=False
        self.flagfeedback=False
        self.flagGetRmID=False
        self.icon=['☁☁☁','😎']
        self.flagEm=False
        self.data=pd.read_csv('data_demo.csv',encoding='UTF-8').head(3)
        self.categories=pd.read_csv('categories.csv',encoding='UTF-8')
        self.summery = pd.read_csv('summery.csv',encoding='UTF-8')
        self.chatbot(f'Tôi sẽ cung cấp nhóm cột, nghĩa nghĩa cột, tên cột và khoảng dữ liệu của bảng main_cus như sau: {self.categories}')
        self.chatbot(f'''Bảng "id_cus" bao gồm định danh của khách hàng như số thứ tự, số điện thoại, email, số CIF với tên cột lần lượt là STT, CUS_CIF_NBR, CUS_PHONE, CUS_MAIL''')
        self.chatbot(f'Thông tin nhóm nhân khẩu học gồm các cột CUS_CIF_NBR,CUS_NM, DTE_OPN_CIF,BRN_OPN_CIF,CUS_GEN,AGE,TINHTRANGHONNHAN,CUS_PHONE,CUS_MAIL,CUS_ADRR,TINHCHATCVHT,TRINHDOHOCVAN,AVG_AMT_3M; nhóm thông tin dữ liệu bảo hiểm gồm cột CALL_DATE,STATUS_ADV,CUST_BANCASED,SANPHAMBHNTDAMUA,NGAYMUABH; nhóm thông tin quan hệ với ngân hàng vcb bao gồm những cột: SPDV,PRIORITYFLAG,BRN_MNGT_PRIO,PAYROLLFLAG,DSCTTHEGHINO,DSCTTHETINDUNG,DSCTNOTIENGUI,DSCTCOTIENGUI,DSCTDIGIBANK,AVG_BAL_TA_E12M,AVG_BAL_TM_E12M,AVG_BAL_LN_E12M,SODUTIENGUI,SODUTIETKIEM,DUNOVAY,NHOMNOVCB,MATDT,CHITIEUCHOYTE,CHITIEUCHOGD,CHITIEUCHODULICH,CHITIEUDAUTUCK')
        self.chatbot('Đối với câu hỏi tính toán, hãy trả lời bằng câu lệnh SQL; nếu là câu hỏi về dữ liệu; tên bảng là main_cus; định danh trong bảng bằng "Số thứ tự" của khách hàng')
    
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
                model="gpt-3.5-turbo-16k", messages=self.messages, temperature=0
            )
            
            reply = chat.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reply})
            return reply
    
    
    async def on_message_activity(self, turn_context: TurnContext):
        message=str(turn_context.activity.text).lower()
        icon = self.icon[random.randint(0, len(self.icon)-1)]

        if 'lý do' in message:
            response=self.chatbot(message + ''' với tên cột là LYDOMUABAOHIEM trong bảng "main_cus", trả lời chỉ bằng câu lệnh SQL, không trả lời kèm tên bảng, tên cột, trả lời thành đoạn văn''')
            print(response)
            try:
                sql = get_sql_from_msg(response)
                re = self.db.execute_sql(f'''{sql}''')
                response=self.chatbot(f'''Chuyển đoạn kết quả sau thành ngôn ngữ tự nhiên bao gồm ý nghĩa của trường và giá trị {re},kết quả trả về dưới dạng gạch đầu dòng , thêm vào cuối đoạn tin nhắn icon {icon}, câu trả lời bắt đầu bằng "Kết quả thu được như sau:" ''') 
                print(response)
                return await turn_context.send_activity(
                MessageFactory.text(response)
            )
            except:
                print('error sql')
                return await turn_context.send_activity(
                MessageFactory.text('Vui lòng nhập rõ hơn câu hỏi'))

        if message.startswith('hãy cung cấp cho tôi định danh'):
            response=self.chatbot(message + ''' về số thứ tự, số điện thoại, email, CIF trong bảng "id_cus", trả lời chỉ bằng câu lệnh SQL, không trả lời kèm tên bảng, kết quả trả về dưới dạng gạch đầu dòng ''')
            print(response)
            try:
                sql = get_sql_from_msg(response)
                re = self.db.execute_sql(f'''{sql}''')
                print(sql)
                response=self.chatbot(f'''Chuyển đoạn kết quả sau thành ngôn ngữ tự nhiên kèm theo ý nghĩa của cột không phải tên cột trong bảng {re}, câu trả lời bắt đầu bằng "Kết quả định danh thu được như sau:", thêm vào cuối đoạn tin nhắn icon {icon} ''') 
                # print(response)
                self.cus_stt=re[0][0]
                self.waitRMIDRes=response
                self.flagGetRmID=True
                return await turn_context.send_activity(MessageFactory.text('Xin nhập mã cán bộ'))     
            except:
                print('error sql')
                self.flagEm=False
                return await turn_context.send_activity(MessageFactory.text('Xin nhập lại câu hỏi'))

        if self.flagGetRmID==True:
            sql=f'''UPDATE main_cus SET RMTIEPCAN = "{message}" WHERE STT = "{self.cus_stt}"'''
            self.db.execute_sql(f'''{sql}''')
            self.db.mydb.commit()
            self.flagGetRmID=False
            self.flagfeedback=True
            await turn_context.send_activity(MessageFactory.text(self.waitRMIDRes))
            return await turn_context.send_activity(MessageFactory.text(
                    '''Xin nhập số thứ tự tương ứng với feedback của khách hàng trên:\n 1. Khách hàng từ chối \n 2. Khách hàng quan tâm nhưng chưa hẹn gặp \n 3. Khách hàng hẹn gặp lại sau \n 4. Không liên hệ được khách hàng \n 5. Khách hàng đồng ý gặp mặt \n 6. Khác'''))
        
        if self.flagfeedback==True:
            feedback='Khác'
            if message=='1':
                feedback='Từ chối'
            elif message=='2':
                feedback='Quan tâm nhưng chưa hẹn gặp'
            elif message=='3':
                feedback='Hẹn gặp lại sau'
            elif message=='4':
                feedback='Không liên hệ được'
            elif message=='5':
                feedback='Đồng ý gặp mặt'
            else:
                feedback='Khác'

            sql=f'''UPDATE main_cus SET FEEDBACK = "{feedback}" WHERE STT = "{self.cus_stt}"'''
            print(sql)

            self.db.execute_sql(f'''{sql}''')
            self.db.mydb.commit()
            del self.messages[-4:]
            self.flagnote=True
            self.flagfeedback=False
            await turn_context.send_activity(MessageFactory.text(f'đã ghi nhận feedback của khách hàng có STT {self.cus_stt}'))
            return await turn_context.send_activity(MessageFactory.text('Hãy ghi chú về khách hàng này (Khách hàng đã có bảo hiểm, sai số điện thoại khách hàng, cần tiếp tục theo dõi thêm,...'))



        if self.flagnote==True:
            sql=f'''UPDATE main_cus SET NOTE = "{message}" WHERE STT = "{self.cus_stt}"'''
            self.db.execute_sql(f'''{sql}''')
            self.db.mydb.commit()
            self.flagnote=False
            return await turn_context.send_activity(MessageFactory.text('đã ghi nhận ghi chú của khách hàng này'))
        
        
        
        if message=='start':
            self.messages=self.messages[:10]    
            return await turn_context.send_activity(MessageFactory.text('Bắt đầu lại đoạn hội thoại'))
                                           
        self.chatbot('trong câu trả lời tiếp bằng câu lệnh SQL không có truy vấn con dùng dữ liệu trong bảng main_cus, không trả lời kèm tên bảng , kết quả trả về dưới dạng gạch đầu dòng') 
        response=self.chatbot(message) 
        try:
            sql = get_sql_from_msg(response)
            re = self.db.execute_sql(f'''{sql}''')
            response=self.chatbot(f'''Chuyển đoạn kết quả sau thành ngôn ngữ tự nhiên bao gồm ý nghĩa của trường và giá trị {re},kết quả trả về dưới dạng gạch đầu dòng , thêm vào cuối đoạn tin nhắn icon {icon}, câu trả lời bắt đầu bằng "Kết quả thu được như sau:" ''') 
            print(response)
            return await turn_context.send_activity(
            MessageFactory.text(response)
        )
        except:
            print('error sql')
        if len(self.messages)>18:
                self.messages = self.messages[:10]
                print('clear cache')
        return await turn_context.send_activity(MessageFactory.text(response))