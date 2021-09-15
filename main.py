from hcapbypass import bypass
from generator import TokenGenerator
from discord_webhook import DiscordWebhook
import proxy_processor
import threading
import json
from itertools import cycle
import os
import time

verbose = True

with open("webhooks.json") as whs:
    webhooks = json.loads(whs.read())
    
pool = cycle(webhooks)
genned = 0

def title_worker():
    global genned
    while True:
        os.system(f"title Tokens Generated: {genned}")
        time.sleep(0.1)

thread = threading.Thread(target=title_worker, args=(), daemon=True)
thread.start()
        

def SendToken(token):
    global pool, webhooks, genned
    wh = next(pool)
    if wh == webhooks[0]:
        with open("webhooks.json") as whs:
            webhooks = json.loads(whs.read())
        pool = cycle(webhooks)
        wh = next(pool)
    
    webhook_url = wh
    webhook = DiscordWebhook(url=webhook_url, content=f'{token}')
    webhook.execute()
    with open('tokens.txt', 'a') as t:
        t.write(token + '\n')
    genned += 1

def GenerateToken():
    while True:
        try:
            proxy = proxy_processor.GetProxy()
            print("[!] Used proxy: {}".format(proxy))
            gen = TokenGenerator(verbose, proxy)
            res = gen.GenerateToken()
            if 'token' in res:
                generatedToken = res["token"]
                print("[!] Generated Token: " + generatedToken)
                SendToken(generatedToken)
            else: print(res)
        except Exception as e:
            print(e)
            continue


def main():
    thread_list = []

    for i in range(120):
        thread = threading.Thread(target=GenerateToken, args=(), daemon=True)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

if __name__ == '__main__':
    main()
