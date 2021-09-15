from requests import Session
import random, string

class EmailVerifier:

	def GetEmail(proxy, email = None, verbose = False):
		s = Session()
		NOT_ALLOWED_DOMAINS = ['digital10network.com', 'savageattitude.com', 'conisocial.it']
		headers = {
		'Host': 'tempmailo.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'RequestVerificationToken': 'CfDJ8CwjmCxqHotIibiRD-dO2dhYOBDNmxE_5dcenJX8hnKjJIM4iPthS8dMfji36mprjDe5mHHNhfmv6rWv1NBFqNV2_ZNo2wHgMzhWLMPrh3aALGsJtAQTBXrT0CAdcno8etKtkgK1aGonCOaG3KKjWFQ',
		'X-Requested-With': 'XMLHttpRequest',
		'Alt-Used': 'tempmailo.com',
		'Connection': 'keep-alive',
		'Referer': 'https://tempmailo.com/',
		'Cookie': '.AspNetCore.Antiforgery.dXyz_uFU2og=CfDJ8CwjmCxqHotIibiRD-dO2dg11qCjJ1N2BZh54WxTh3cuLXBbTrFbOrZC52bXrQMj8TkL538yjwpttyQmdRnM5U0ny3-xThaVuvxPk3nStMNY22_zlA5t6En434ZwCT9N6JIN9NgdjU1wFlms_4SU6m8; _ym_uid=1628709940284016213; _ym_isad=1',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'TE': 'trailers'
		}
		email = s.get('https://tempmailo.com/changemail?_r=0.7377127168150278', headers=headers, proxies={'https': 'http://'+proxy}).text
		if len(email) > 50:
			email = s.get('https://tempmailo.com/changemail?_r=0.7377127168150278', headers=headers).text
		while email.split("@")[1] in NOT_ALLOWED_DOMAINS:
			return EmailVerifier.GetEmail(proxy, email, verbose)
		else:
			if verbose:
				print("[!] Got Email: "+email) 
			return email

	def GetDiscordEmail(proxy, email):
		s = Session()
		payload = {"mail":email}
		headers = {
			'Host': 'tempmailo.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
			'Accept': 'application/json, text/plain, */*',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate, br',
			'RequestVerificationToken': 'CfDJ8CwjmCxqHotIibiRD-dO2dhYOBDNmxE_5dcenJX8hnKjJIM4iPthS8dMfji36mprjDe5mHHNhfmv6rWv1NBFqNV2_ZNo2wHgMzhWLMPrh3aALGsJtAQTBXrT0CAdcno8etKtkgK1aGonCOaG3KKjWFQ',
			'X-Requested-With': 'XMLHttpRequest',
			'Alt-Used': 'tempmailo.com',
			'Connection': 'keep-alive',
			'Content-Length': str(len(str(payload))),
			'Content-Type': 'application/json;charset=utf-8',
			'Referer': 'https://tempmailo.com/',
			'Cookie': '.AspNetCore.Antiforgery.dXyz_uFU2og=CfDJ8CwjmCxqHotIibiRD-dO2dg11qCjJ1N2BZh54WxTh3cuLXBbTrFbOrZC52bXrQMj8TkL538yjwpttyQmdRnM5U0ny3-xThaVuvxPk3nStMNY22_zlA5t6En434ZwCT9N6JIN9NgdjU1wFlms_4SU6m8; _ym_uid=1628709940284016213; _ym_isad=1',
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'TE': 'trailers'
		}
		req = s.post('https://tempmailo.com/', headers=headers, json=payload, proxies={'https': 'http://'+proxy})
		return req.text
	
if __name__ == '__main__':
	import time

	email = EmailVerifier.GetEmail(proxy='tkqdsjhw-rotate:i61glfoo9t0a@104.227.29.234:80', verbose=True)
	print(email)
	time.sleep(20)
	print(EmailVerifier.GetDiscordEmail('tkqdsjhw-rotate:i61glfoo9t0a@104.227.29.234:80', email))

