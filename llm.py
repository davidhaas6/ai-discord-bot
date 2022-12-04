import os
import openai
import re
import random
import pandas as pd

# https://beta.openai.com/examples

def get_resp_text(response: str) -> list:
    return [c['text'] for c in response["choices"]]


def chatbot_query(prompt):
    # marv chatbot settings
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )


def sassy_chatbot(question: str):
    prompt = "Marv is a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google."
    prompt += "You: " + question + "\nMarv:"
    return get_resp_text(chatbot_query(prompt))


def color_pallet(description: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"The best CSS color pallete for {description}:\n\nPrimary color: #",
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[";"]
    )
    str_reponse = '#'+get_resp_text(response)[0]
    find_hex=r"(#([A-Z0-9])+)"
    colors = [c for c,_ in re.findall(find_hex,str_reponse)]
    return colors


def discord_user(message:str, author:str, mimic_uname:str=None):
    data = pd.read_csv('pinbot_msg.csv')

    if mimic_uname is None:
        source_material = data
    else:
        source_material = data[data.name == mimic_uname]
    
    if len(source_material) == 0: 
        return

    source_material = [f'{row["name"]}:{row["message"]}' for i, row in source_material.iterrows()]
    random.shuffle(source_material)
    usr_prepend = '\n'.join(source_material[:60])

    setting_prepend = ""#f"{mimic_uname} is a poetic fan of Shakespear who responds to statements with wit and grace."
    prompt = setting_prepend + usr_prepend + f'\n{author}: {message}\n' 
    if mimic_uname: prompt += f'{mimic_uname}:'
    print(prompt)

    response = chatbot_query(prompt)
    if response is not None:
        str_reponse =  get_resp_text(response)[0].strip()
        return str_reponse


if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser("GPT Chat bot")
    args.add_argument('-t', '--task', help="The task of the both")
    args = args.parse_args()
    openai.api_key = open("secret.txt").read()
    
    if args.task == "marv":
        user_in = str(input("Ask Marv a question: "))
        print(sassy_chatbot(user_in))
    elif args.task == "color":
        user_in = str(input("The CSS color pallete for "))
        print("\n".join(color_pallet(user_in))) # https://www.colorhexa.com/
    elif args.task == "discord":
        prompt = """brb banning marth mains from this discord
        James: 🔨😭"""
        resp = discord_user(prompt,"James")
        print(resp)
