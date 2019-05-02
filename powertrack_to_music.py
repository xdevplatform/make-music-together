import requests
import json
import yaml


def handle_auth():
    with open("/Users/jgarson/Downloads/PyCon/secret.yaml", "r") as f:
        s = yaml.load(f)
    username = s["powertrack"]["username"]
    password = s["powertrack"]["password"]
    account_name = s["powertrack"]["account_name"]
    env_name = s["powertrack"]["env_name"]
    return username, password, account_name, env_name


def handle_response(account_name, env_name, username, password):
    response = requests.get(
        "https://gnip-stream.twitter.com/stream/powertrack/accounts/{}/publishers/twitter/{}.json".format(
            account_name, env_name
        ),
        auth=(username, password),
        stream=True,
    )
    print(response)
    return response


def process_response(response):
    if response.encoding is None:
        response.encoding = "utf-8"
    for data in response.iter_lines(decode_unicode=True):
        if data:
            jdata = json.loads(data)
            return jdata


def process_word(word):
    lower_word = word.lower()
    final_word = lower_word[14:]
    return final_word


def parse_to_word(jdata):
    text = jdata["text"]
    print(text)
    return text


def music_logic(word):
    options = [play("oxosff"), play("hi"), play("yo"), play("not_found")]
    final_word = process_word(word=word)
    if final_word == "hello":
        return options[0]
    elif final_word == "hi":
        return options[1]
    elif final_word == "yo":
        return options[2]
    else:
        return options[3]


print("hello")

username, password, account_name, env_name = handle_auth()

response = handle_response(account_name, env_name, username, password)

jdata = process_response(response)

word = parse_to_word(jdata)

p1 >> music_logic(word)
