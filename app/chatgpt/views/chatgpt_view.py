import logging
from flask import render_template, request
from app import app

from ..usecases.conversation_interactor import ConversationInteractor

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/chatgpt', methods=['GET', 'POST'])
def chatgpt():
    messages = {}
    form_executed = None
    if request.method == 'POST' and 'chatgpt_msg' in request.form:
        input_text = request.form.get('chatgpt_msg')

        conversation_int = ConversationInteractor.reuse_or_create_conversation()
        conversation_int.add_message('user', input_text)
        response_text = "Fake message: I don't know. Really. Please, forgive me already!"
        conversation_int.add_message('assistant', response_text)
        messages.update({
            'messages': conversation_int.get_messages(),
            'error': None,
            })
        form_executed = 'chatgpt_form_conversation'

    if request.method == 'POST' and 'chatgpt_reload_messages' in request.form:
        logger.info("Reload conversation")

        conversation_int = ConversationInteractor.reuse_or_create_conversation()
        messages.update({
            'messages': conversation_int.get_messages(),
            'error': None,
            })
        form_executed = 'chatgpt_form_reload_conversation'

    if request.method == 'POST' and 'chatgpt_new_chat' in request.form:
        logger.info("New conversation")
        conversation_int = ConversationInteractor.reuse_or_create_conversation()
        conversation_int.reset()
        form_executed = 'chatgpt_form_new_conversation'

    return render_template('chatgpt.html', messages=messages, form_executed=form_executed)
