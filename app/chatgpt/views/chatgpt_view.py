import logging
from flask import render_template, request
from app import app

from ..usecases.conversation_interactor import ConversationInteractor
from ..models.message import Message
from ...tools.utils import utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/chatgpt', methods=['GET', 'POST'])
def chatgpt():
    messages = {}
    form_executed = None
    if request.method == 'POST' and 'chatgpt_msg' in request.form:
        input_text = request.form.get('chatgpt_msg')
        msg = Message(1, 'user', input_text)
        response_text = "I don't know. Really. Please, forgive me already!"
        response = Message(2, 'assistant', response_text)
        messages.update({
            'messages': [msg, response],
            'error': None,
            })
        form_executed = 'chatgpt_form_conversation'
        logger.info(messages)
    return render_template('chatgpt.html', messages=messages, form_executed=form_executed)
