"""推送脚本到 Telegram"""
import requests

text = open('output/本周脚本_AI人才断层悖论.md', 'r', encoding='utf-8').read()
bot_token = '8215333535:AAHQFfKtFNvdEKt0NS5q-1ggaDOpB43nYPE'
chat_id = '8483451023'
url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

# Split into chunks of ~4000 chars
parts = []
current = ''
for line in text.split('\n'):
    if len(current) + len(line) + 1 > 4000:
        parts.append(current)
        current = line
    else:
        current = current + '\n' + line if current else line
if current:
    parts.append(current)

print(f'Total: {len(text)} chars, {len(parts)} parts')

for i, part in enumerate(parts):
    resp = requests.post(url, json={'chat_id': chat_id, 'text': part})
    data = resp.json()
    if data.get('ok'):
        msg_id = data['result']['message_id']
        print(f'Part {i+1}/{len(parts)} sent (msg_id: {msg_id})')
    else:
        print(f'Part {i+1} failed: {data}')

print('Done')
