import itchat
from itchat.content import *
import re
import os

# 消息字典
msg_dict = {}
face_bug = None


@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=True)
def handle_withdrawn_message(msg):
    """
    发送对方撤回的消息
    :return:
    """
    global face_bug
    # 消息id
    msg_id = msg['MsgId']
    # 消息时间
    msg_time = msg['CreateTime']
    # 发送人
    msg_from = (itchat.search_friends(userName=msg['FromUserName']))["NickName"]
    msg_content = None

    # 文本消息
    if msg['Type'] == 'Text':
        msg_content = msg['Content']
    # 表情 附件 语音消息
    elif msg['Type'] == 'Picture' or msg['Type'] == 'Attachment' or msg['Type'] == 'Recording':
        msg_content = r"" + msg['FileName']
        # 下载保存文件
        msg['Text'](msg['FileName'])
    face_bug = msg_content
    msg_dict.update(
        {
            msg_id: {"msg_from": msg_from, "msg_time": msg_time, "msg_type": msg['Type'], "msg_content": msg_content}
        }
    )


@itchat.msg_register([NOTE])
def send_withdrawn_message(msg):
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_dict.get(old_msg_id, {})
        if len(old_msg_id) < 11:
            itchat.send_file(face_bug, toUserName='filehelper')
            os.remove(face_bug)
        else:
            msg_body = old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "内容:" + "\n" \
                       + r"" + old_msg.get('msg_content')
            itchat.send(msg_body, toUserName='filehelper')
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
            msg_dict.pop(old_msg_id)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
