import pandas as pd

data_file = 'pinbot.txt'

lines = open(data_file).readlines()
chat_lines = [l for l in lines if len(l.strip()) > 0 and '@' in l]

df = pd.DataFrame()
df['raw'] = chat_lines

name_rx = r"@([\w ]+):"
msg_rx = r'@[\w ]+:(.*)\n'
df['name'] = df.raw.str.extract(name_rx)
df['message'] = df.raw.str.extract(msg_rx)

is_media = df.message.str.contains('Attachment only')
df_message_only = df[~is_media].reset_index()

df.to_csv('pinbot_full.csv')
df_message_only.to_csv('pinbot_msg.csv')
