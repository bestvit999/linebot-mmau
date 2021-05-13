from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, CarouselTemplate, CarouselColumn, URIAction, PostbackAction, MessageAction, TemplateSendMessage, ImageSendMessage
)

import dbmgr
import Imgur
import Dot
import time

app = Flask(__name__)

line_bot_api = LineBotApi('LineBotApi')
handler = WebhookHandler('WebhookHandler')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # replyToken of User/Chatroom
    to = event.reply_token

    if 'fbb ' in str(event.message.text).lower(): 
        # hench is a string type
        hench = str(event.message.text).lower().replace('fbb ','')

        if is_number(hench):
            fList = dbmgr.selectHenchByLevel(hench)

            # show the monster information by carousel_template
            if len(fList) > 0:
                carousel_columns = []
                template_message = [TextSendMessage(text='the hench probably you are looking for')]
                for _hench in fList:
                    carousel_columns.append(
                        CarouselColumn(
                            thumbnail_image_url='https://mixmasteronline.com.au/resources/uploads/common/formular/' + Dot.swapDeadImg(dbmgr.selectPic(_hench)),
                            title = 'Hench: ' + _hench + '\n' + dbmgr.selectLevel(_hench),
                            text = 'press the buttons below',
                            actions = [
                                PostbackAction(label='find monster info', data='find',text='fbb '+ _hench),
                                PostbackAction(label='hench in formular', data='monsterinformular',text='showmonsterinformular '+ _hench),
                                PostbackAction(label='associated hench', data='associatedinfo',text='associatedinfo ' + _hench)
                            ]
                        )
                    )
                if len(carousel_columns) <= 10:
                    carousel_template = CarouselTemplate(
                        columns=carousel_columns
                    )
                    template_message.append(TemplateSendMessage(
                        alt_text= hench + ' associated information', template=carousel_template))
                        
                elif len(carousel_columns) > 10:
                    carousel_columns = splitList(carousel_columns,10)

                    # message reply size only can be 1~5
                    if len(carousel_columns) <= 5:
                        for columns in carousel_columns:
                            # use CarouselTemplate to view each hench (max:10 columns)
                            carousel_template_chunk = CarouselTemplate(
                                columns=columns
                            )
                            template_message.append(TemplateSendMessage(
                                alt_text=hench + ' associated information',template=carousel_template_chunk))
                    else:
                        template_message = TextSendMessage(text = 'searching text is out of scale, please re-type more detail.')

            else:
                template_message = TextSendMessage(text = 'No exist any hench, please re-type the text')

            line_bot_api.reply_message(to, template_message)

        # if can exactly find monster
        elif dbmgr.selectMonster(hench) != '':
            buttons_template = ButtonsTemplate(
                title='Hench: ' + hench + '\n' + dbmgr.selectLevel(hench), text='press the buttons below' , thumbnail_image_url = 'https://mixmasteronline.com.au/resources/uploads/common/formular/' + Dot.swapDeadImg(dbmgr.selectPic(hench)),
                actions=[
                    PostbackAction(label='show info', data='info',text='showmonsterinfo '+ hench),
                    PostbackAction(label='hench in formular', data='monsterinformular',text='showmonsterinformular '+ hench),
                    PostbackAction(label='associated hench', data='associatedinfo',text='associatedinfo ' + hench),
                    PostbackAction(label='mix graph', data='mixgraph',text='mix ' + hench)
                ])
            template_message = TemplateSendMessage(
                alt_text=hench + ' details', template=buttons_template)
            line_bot_api.reply_message(to, template_message)

        # if cannot exactly find monster, then find possible monster by insensitive search
        elif dbmgr.selectMonster(hench) == '':
            possiblehenchs = dbmgr.selectMonsterInsensitive(hench)

            # show the monster information by carousel_template
            if len(possiblehenchs) > 0:
                carousel_columns = []
                template_message = [TextSendMessage(text='the hench probably you are looking for')]
                for _hench in possiblehenchs:
                    carousel_columns.append(
                        CarouselColumn(
                            thumbnail_image_url='https://mixmasteronline.com.au/resources/uploads/common/formular/' + Dot.swapDeadImg(dbmgr.selectPic(_hench)),
                            title = 'Hench: ' + _hench + '\n' + dbmgr.selectLevel(_hench),
                            text = 'press the buttons below',
                            actions = [
                                PostbackAction(label='find monster info', data='find',text='fbb '+ _hench),
                                PostbackAction(label='hench in formular', data='monsterinformular',text='showmonsterinformular '+ _hench),
                                PostbackAction(label='associated hench', data='associatedinfo',text='associatedinfo ' + _hench)
                            ]
                        )
                    )
                if len(carousel_columns) <= 10:
                    carousel_template = CarouselTemplate(
                        columns=carousel_columns
                    )
                    template_message.append(TemplateSendMessage(
                        alt_text= hench + ' associated information', template=carousel_template))
                        
                elif len(carousel_columns) > 10:
                    carousel_columns = splitList(carousel_columns,10)

                    # message reply size only can be 1~5
                    if len(carousel_columns) <= 5:
                        for columns in carousel_columns:
                            # use CarouselTemplate to view each hench (max:10 columns)
                            carousel_template_chunk = CarouselTemplate(
                                columns=columns
                            )
                            template_message.append(TemplateSendMessage(
                                alt_text=hench + ' associated information',template=carousel_template_chunk))
                    else:
                        template_message = TextSendMessage(text = 'searching text is out of scale, please re-type more detail.')

            else:
                template_message = TextSendMessage(text = 'No exist any hench, please re-type the text')

            line_bot_api.reply_message(to, template_message)

    elif 'showmonsterinformular ' in str(event.message.text).lower():
        hench = str(event.message.text).lower().replace('showmonsterinformular ','')
        fList = dbmgr.selectMonsterinFormular(hench)
        
        # if there is None associate monster then return a information message
        if len(fList) > 0 :
            # defind CarouselColumn according associated info of hench
            carousel_columns = []
            for _hench in fList:
                carousel_columns.append(
                    CarouselColumn(
                        thumbnail_image_url='https://mixmasteronline.com.au/resources/uploads/common/formular/' + Dot.swapDeadImg(dbmgr.selectPic(_hench)),
                        title = 'Hench: ' + _hench + '\n' + dbmgr.selectLevel(_hench),
                        text = 'press the buttons below',
                        actions = [
                            PostbackAction(label='find monster info', data='find',text='fbb '+ _hench),
                            PostbackAction(label='hench in formular', data='monsterinformular',text='showmonsterinformular '+ _hench),
                            PostbackAction(label='associated hench', data='associatedinfo',text='associatedinfo ' + _hench)
                        ]
                    )
                )

            if len(carousel_columns) <= 10:
                # use CarouselTemplate to view each hench (max:10 columns)
                carousel_template = CarouselTemplate(
                    columns=carousel_columns
                )
                template_message = TemplateSendMessage(
                    alt_text= hench + ' associated information', template=carousel_template)

            elif len(carousel_columns) > 10:
                carousel_columns = splitList(carousel_columns,10)
                template_message = []
                for columns in carousel_columns:
                    # use CarouselTemplate to view each hench (max:10 columns)
                    carousel_template_chunk = CarouselTemplate(
                        columns=columns
                    )
                    template_message.append(TemplateSendMessage(
                        alt_text=hench + ' associated information',template=carousel_template_chunk))

        else:
            template_message = TextSendMessage(text = 'no formular exist')

        line_bot_api.reply_message(to, template_message)

    elif 'showmonsterinfo ' in str(event.message.text).lower():
        hench = str(event.message.text).lower().replace('showmonsterinfo ','')
        # text is detail about the hench information
        txt = dbmgr.selectMonster(hench)
        line_bot_api.reply_message(to, TextSendMessage(text=txt))    

    # find asscoiated monster info (maximum:10) 
    # if exceed 10, can use two carousels or more to present
    elif 'associatedinfo ' in str(event.message.text).lower():
        hench = str(event.message.text).lower().replace('associatedinfo ','')
        fList = dbmgr.selectCanBeMixed(hench)

        # if there is None associate monster then return a information message
        if len(fList) > 0 :
            # defind CarouselColumn according associated info of hench
            carousel_columns = []
            for _hench in fList:
                carousel_columns.append(
                    CarouselColumn(
                        thumbnail_image_url='https://mixmasteronline.com.au/resources/uploads/common/formular/' + Dot.swapDeadImg(dbmgr.selectPic(_hench)),
                        title = 'Hench: ' + _hench + '\n' + dbmgr.selectLevel(_hench),
                        text = 'press the buttons below',
                        actions = [
                            PostbackAction(label='find monster info', data='find',text='fbb '+ _hench),
                            PostbackAction(label='hench in formular', data='monsterinformular',text='showmonsterinformular '+ _hench),
                            PostbackAction(label='associated hench', data='associatedinfo',text='associatedinfo ' + _hench)
                        ]
                    )
                )

            if len(carousel_columns) <= 10:
                # use CarouselTemplate to view each hench (max:10 columns)
                carousel_template = CarouselTemplate(
                    columns=carousel_columns
                )
                template_message = TemplateSendMessage(
                    alt_text= hench + ' associated information', template=carousel_template)

            elif len(carousel_columns) > 10:
                carousel_columns = splitList(carousel_columns,10)
                template_message = []
                for columns in carousel_columns:
                    # use CarouselTemplate to view each hench (max:10 columns)
                    carousel_template_chunk = CarouselTemplate(
                        columns=columns
                    )
                    template_message.append(TemplateSendMessage(
                        alt_text=hench + ' associated information',template=carousel_template_chunk))

        else:
            template_message = TextSendMessage(text = 'highest core, cannot be further mixed.')

        line_bot_api.reply_message(to, template_message)

    elif 'mix ' in str(event.message.text).lower():
        hench = str(event.message.text).lower().replace('mix ','')        
        path = Dot.createGraph(hench)
        url = Imgur.upload_photo(path)

        line_bot_api.reply_message(to,
        ImageSendMessage(original_content_url=url,preview_image_url=url))

        # imgId = url.replace('https://i.imgur.com/','').replace('.png','')
        # Imgur.deleteImage(imgId)

# split the list, n unit in each chunk
def splitList(L,n):
    chunks = int(len(L) / n)
    restStart = 0
    output = []
    for i in range(chunks):
        output.append(L[i*n:i*n+n])
        restStart = i
    restStart += 1
    output.append(L[restStart*n:len(L)])
    return output

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

