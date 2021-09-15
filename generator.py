from requests.models import Response
from email_verificator import EmailVerifier
from httpx import Client
from discord_build_info_py import *
from base64 import b64encode as b
from hcapbypass import bypass

import json
import urllib3
import random
import string
import time
import discum

urllib3.disable_warnings()


class TokenGenerator:
    def __init__(self, verbose, proxy):
        self.VerboseOutput = verbose
        self.UsedProxy = proxy
        self.session = Client(proxies={"https://": f"http://{self.UsedProxy}"})

        dcfduid, sdcfduid = self.GetDcfduid()
        if self.VerboseOutput:
            print("[!] Obtained __dcfduid cookie! ({})".format(dcfduid))
            print("[!] Obtained __sdcfduid cookie! ({})".format(sdcfduid))
        self.dcfduid = dcfduid
        self.sdcfduid = sdcfduid
        self.session.cookies['__dcfduid'] = dcfduid
        self.session.cookies['__sdcfduid'] = sdcfduid
        self.session.cookies['locale'] = 'it'

        fingerprint = self.GetFingerprint()
        if self.VerboseOutput:
            print("[!] Obtained fingerprint! ({})".format(fingerprint))
        self.fingerprint = fingerprint

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
        build_num, build_hash, build_id = getClientData('stable')

        self.super_properties = b(json.dumps({
            "os": "Windows",
            "browser": "Firefox",
            "device": "",
            "system_locale": "it-IT",
            "browser_user_agent": user_agent,
            "browser_version": "90.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": int(build_num),
            "client_event_source": None
        }, separators=(',', ':')).encode()).decode()

    def GetDcfduid(self):
        resp = self.session.get(
            'https://discord.com/register')
        return resp.cookies['__dcfduid'], resp.cookies['__sdcfduid']

    def GetFingerprint(self):
        return self.session.get("https://discordapp.com/api/v9/experiments", timeout=10).json()['fingerprint']

    def CreateAccount(self, payload, captcha=None):
        if captcha:
            payload['captcha_key'] = captcha

        headers = {
            'Accept':               '*/*',
            'Accept-Encoding':      'gzip, deflate, br',
            'Accept-Language':      'it',
            'Authorization':        'undefined',
            'Cache-Control':        'no-cache',
            'Connection':           'keep-alive',
            #'Content-Length':       str(len(str(payload).replace(' ', '').replace('None', 'null')) + 2),
            'Content-Type':         'application/json',
            'Cookie':               '__dcfduid=' + self.dcfduid + '; __sdcfduid=' + self.sdcfduid,
            'Host':                 'discord.com',
            'Origin':               'https://discord.com',
            'Pragma':               'no-cache',
            'Referer':              'https://discord.com/register',
            'Sec-Fetch-Dest':       'empty',
            'Sec-Fetch-Mode':       'cors',
            'Sec-Fetch-Site':       'same-origin',
            'TE':                   'Trailers',
            'User-Agent':           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            'X-Fingerprint':        self.fingerprint,
            'X-Super-Properties':   self.super_properties
        }

        return self.session.post('https://discord.com/api/v9/auth/register', headers=headers, json=payload).json()

    def GenerateToken(self):
        payload = {
            'fingerprint':      self.fingerprint,
            'email':            ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + '@gmail.com',
            'username':         ''.join(random.choice(string.ascii_letters) for _ in range(6)) + ' ',
            'password':         'DiscordIsShitIraq1944Servers',
            'invite':           None,
            'consent':          True,
            'date_of_birth':    "1999-11-01",
            'gift_code_sku_id': None,
            'captcha_key':      None
        }

        response = self.CreateAccount(payload)

        if 'captcha_key' in response:
            while 1:
                times = 0
                captcha_solved = bypass(
                    "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "discord.com", self.UsedProxy)
                if captcha_solved != False:
                    break
                times += 1
                if times >= 5: return '[!] Captcha Fail'
            response = self.CreateAccount(payload, captcha_solved)

        if 'retry_after' in response:
            print("[!] Rate limit! ({})".format(str(response['retry_after'])))
            return ""
            time.sleep((response['retry_after'] / 1000) + 5)
            response = self.CreateAccount(payload, bypass(
                "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "discord.com", self.UsedProxy))

        if 'token' not in response:
            return response

        token = response["token"]

        if self.VerboseOutput:
            print("[!] Generated token, veryfing it's email... ({})".format(token))
        email = EmailVerifier.GetEmail(self.UsedProxy,
            email=''.join(random.choice(string.ascii_lowercase) for _ in range(10)), verbose=self.VerboseOutput)

        payload = {
            'email': email.replace('%40', '@'),
            'password': 'DiscordIsShitIraq1944Servers'
        }

        headers = {
            'Host': 'discord.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            'Accept': '*/*',
            'Accept-Language': 'it',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-Super-Properties': self.super_properties,
            'x-fingerprint': self.fingerprint,
            #'Content-Length': str(len(str(payload))),
            'Origin': 'https://discord.com',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/channels/@me',
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            "sec-ch-ua-mobile": "?0",
            'TE': 'trailers'
        }
        check = self.session.patch('https://discord.com/api/v9/users/@me',
                           headers=headers, json=payload)
        if check.status_code == 403:
            return "[!] Token Locked!"
        elif check.status_code == 400:
            print(check.status_code)
            print(check.text)
        elif self.VerboseOutput:
            print("[!] Patch Request Succesfull") 

        first_part = 'Verifica e-mail: '
        second_part = '\\n\\n","html":"<!doctype html>\\n<html xmlns='
        verify_url = ''
        times = 0
        while 'http' not in verify_url:
            time.sleep(4)
            data = EmailVerifier.GetDiscordEmail(proxy=self.UsedProxy, email=email)
            verify_url = data[data.find(first_part) +
                              len(first_part):data.find(second_part)]
            times += 1
            if times >= 3: 
                print(verify_url)
                return '[!] Mail Verify Fail?'

        real_url = self.session.get(verify_url)
        email_token = str(real_url.url).split("=")[1]
        while 1:
            times = 0
            captcha_key = bypass(
                "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "discord.com", self.UsedProxy)
            if captcha_key != False: break
            times += 1
            if times >= 5: return '[!] Captcha Fail'

        if self.VerboseOutput:
            print("[!] Obtained email token! ({})".format(email_token))

        payload = {
            'captcha_key': captcha_key,
            'token': email_token
        }

        headers = {
            #'content-length': str(len(str(payload).replace(' ', '').replace('None', 'null'))),
            'accept': '*/*',
            'accept-Language': 'it',
            'content-Type': 'application/json',
            'referer': 'https://discord.com/verify',
            'origin': 'https://discord.com',
            'connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            'x-fingerprint': self.fingerprint,
            'X-Super-Properties': self.super_properties,
            'authorization': token
        }

        resp = self.session.post('https://discord.com/api/v9/auth/verify', json=payload, headers=headers, timeout=10)
        try:
            bot = discum.Client(token=resp.json()['token'], log=False)
            @bot.gateway.command
            def websocket_activate(resp):
                if resp.event.ready_supplemental:
                    bot.gateway.close()
            bot.gateway.run()
        except Exception as e:
            print(e)
            pass
        return resp.json()