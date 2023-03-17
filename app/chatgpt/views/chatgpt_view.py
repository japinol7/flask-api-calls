import logging

from flask import render_template, request
from app import app

from ..usecases.conversation_interactor import ConversationInteractor

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

REQUEST_FORM_ID_MAPPINGS = {
    'chatgpt_msg': 'chatgpt_form_conversation',
    'chatgpt_reload_messages': 'chatgpt_form_reload_conversation',
    'chatgpt_new_chat': 'chatgpt_form_new_conversation',
    }


@app.route('/chatgpt', methods=['GET', 'POST'])
def chatgpt():
    form_names = list(REQUEST_FORM_FUNCT_MAPPINGS.keys() & request.form.keys())
    if request.method != 'POST' or not form_names:
        return render_template('chatgpt.html', messages={}, form_executed=None)

    form_name = form_names[0]
    conversation_int = ConversationInteractor.reuse_or_create_conversation()
    messages = REQUEST_FORM_FUNCT_MAPPINGS[form_name](conversation_int)
    form_executed = REQUEST_FORM_ID_MAPPINGS[form_name]
    return render_template('chatgpt.html', messages=messages, form_executed=form_executed)


def process_form_chatgpt_msg(conversation_int):
    logger.info("Process user input")
    input_text = request.form.get('chatgpt_msg')
    is_fake_msg = 'Fake ChatGPT Answer' in request.form.getlist('flags')

    if is_fake_msg:
        logger.info("Generate fake answer")
        conversation_int.get_chatgpt_answer_fake(input_text)
    else:
        conversation_int.get_chatgpt_answer(input_text)

    return {
        'messages': conversation_int.get_messages(),
        'error': None,
        }


def process_form_chatgpt_reload_messages(conversation_int):
    logger.info("Reload conversation")
    return {
        'messages': conversation_int.get_messages(),
        'error': None,
        }


def process_form_chatgpt_new_chat(conversation_int):
    logger.info("New conversation")
    conversation_int.reset()
    return {}


REQUEST_FORM_FUNCT_MAPPINGS = {
    'chatgpt_msg': process_form_chatgpt_msg,
    'chatgpt_reload_messages': process_form_chatgpt_reload_messages,
    'chatgpt_new_chat': process_form_chatgpt_new_chat,
    }
