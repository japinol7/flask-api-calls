import logging
from flask import render_template, request
from app import app

from ..usecases.conversation_interactor import ConversationInteractor
from ..models.message import Message

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/chatgpt', methods=['GET', 'POST'])
def chatgpt():
    messages = {}
    form_executed = None
    if request.method == 'POST' and 'chatgpt_msg' in request.form:
        input_text = request.form.get('chatgpt_msg')
        msg = Message('user', input_text)
        response_text = "Fake message: I don't know. Really. Please, forgive me already!"
        response = Message('assistant', response_text)
        logger.info(msg)
        logger.info(response)
        messages.update({
            'messages': _get_all_msgs(),
            'error': None,
            })
        form_executed = 'chatgpt_form_conversation'

    if request.method == 'POST' and 'chatgpt_reload_messages' in request.form:
        logger.info("Reload conversation")
        messages.update({
            'messages': _get_all_msgs(),
            'error': None,
            })
        form_executed = 'chatgpt_form_reload_conversation'

    if request.method == 'POST' and 'chatgpt_new_chat' in request.form:
        logger.info("New conversation")
        Message.reset()
        form_executed = 'chatgpt_form_new_conversation'

    return render_template('chatgpt.html', messages=messages, form_executed=form_executed)


def _get_all_msgs():
    return Message.messages
