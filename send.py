import itchat
from time import time
from itchat.content import *

# 登录
itchat.auto_login(hotReload=True)

msg_dict = {}


@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=True)
def send_withdrawn_message(msg):
    """
    发送对方撤回的消息
    :return:
    """
    # 消息id
    msg_id = msg['MsgId']
    # 消息时间
    msg_time = msg['CreateTime']
    # 发送人
    msg_from = (itchat.search_friends(userName=msg['FromUserName']))["NickName"]
    msg_content = None
    msg_url = None

    # 文本消息
    if msg['Type'] == 'Text':
        msg_content = msg['Content']
    # 表情 附件 语音消息
    elif msg['Type'] == 'Picture' or msg['Type'] == 'Attachment' or msg['Type'] == 'Recording':
        msg_content = r"" + msg['FileName']
