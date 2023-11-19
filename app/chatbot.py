import openai
from config import Config
openai.api_key = Config.OPENAI_API

def get_completion(message, chat_id, new_chat, sysp ,csm):
    context = make_context(message, chat_id, new_chat, sysp ,csm)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=context,
        temperature=0, # this is the degree of randomness of the model's output
    )
    context.append({"role": "assistant", "content": response.choices[0].message["content"]})
    csm.update_context(chat_id, "context", context)
    return response.choices[0].message["content"]

def make_context(message, chat_id, new_chat, system_prompt,csm):
    if new_chat:
        context = [{"role": "system", "content": system_prompt}]
        context.append({"role": "user", "content": message})
        csm.create_session(chat_id)
        csm.update_context(chat_id, "context", context)
    else:
        context = csm.get_context(chat_id, 'context')
        if context ==  None:
            context = [{"role": "system", "content": system_prompt}]
            csm.create_session(chat_id)
            csm.update_context(chat_id, 'context', context)
        context.append({"role": "user", "content": message})
        csm.update_context(chat_id, "context", context)
        

    return context



if __name__ == '__main__':
    from session_manager import ChatSessionManager
    csm = ChatSessionManager()
    message = "Hello"
    reply = get_completion(message, "6sa4d6a4sf64sa64fas4f6", True, csm)
    print(reply)
    message = "help me with your privacy policy"
    reply = get_completion(message, "6sa4d6a4sf64sa64fas4f6", False, csm)
    print(reply)