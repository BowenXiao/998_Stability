#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u

class AppStoreTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		if d(resourceId = 'com.smartisanos.appstore:id/appStatusIconView').wait.exists(timeout = 3000):
			d(resourceId = 'com.smartisanos.appstore:id/appStatusIconView').click.wait()
		u.tearDown()

	def testAppstore(self):
		#####################################################################################################
		# Download application from appstore                                                                #
		#####################################################################################################

		#Launch app store
		d.start_activity(component='com.smartisanos.appstore/.AppStoreActivity')
		assert d(text = '推荐').wait.exists(timeout = 5000),'Launch app store failed in 5s!'

		#Download app
		d(text = '榜单').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = '榜单').wait.exists(timeout = 5000),"Switch to '排行' view failed in 5s!"
		if d(text = '总排行').wait.exists(timeout = 5000):
			d(text = '总排行').click.wait()
		assert d(text = 'QQ').wait.exists(timeout = 30000),"Can not switch to 总排行 or QQ is not in the list!"
		d(text = 'QQ').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/appName',text = 'QQ').wait.exists(timeout = 15000),"Switch to app 'QQ' detail failed in 15s!"
		self._downloadOption()

		#####################################################################################################
		# Open downloaded application from appstore                                                         #
		#####################################################################################################
		assert d(text = '打开').wait.exists(timeout = 5000),'Application download did not finish!'
		d(text = '打开').click.wait()
		assert d(packageName = 'com.tencent.mobileqq').wait.exists(timeout = 5000),'Launch application from AppStore failed in 5s!'

		#####################################################################################################
		# Uninstall downloaded application from packagemanager                                              #
		#####################################################################################################
		d.press('home')
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		#Uninstall app
		u.selectOption('全局高级设置')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '全局高级设置').wait.exists(timeout = 5000),'Switch to advanced setting view failed in 5s!'
		u.selectOption('应用程序管理')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '应用程序管理').wait.exists(timeout = 5000),'Switch to app manager view failed in 5s!'
		u.selectOption('QQ')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '应用信息').wait.exists(timeout = 5000),'Switch to app details view failed in 5s!'
		d(text = '卸载').click.wait()
		assert d(textContains = '要卸载此应用吗').wait.exists(timeout = 5000),'Delete alarm does not pop-up in 5s!'
		d(text = '确定').click.wait()
		assert d(text = 'QQ').wait.gone(timeout = 5000),'Uninstall failed in 5s!'

	def testAppStoreDownload(self):
		#Launch app store
		d.start_activity(component='com.smartisanos.appstore/.AppStoreActivity')
		assert d(text = '推荐').wait.exists(timeout = 5000),'Launch app store failed in 5s!'

		#Download app
		d(text = '榜单').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = '榜单').wait.exists(timeout = 5000),"Switch to '排行' view failed in 5s!"
		if d(text = '总排行').wait.exists(timeout = 5000):
			d(text = '总排行').click.wait()
		d(text = 'QQ').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = 'QQ').wait.exists(timeout = 5000),"Switch to app 'QQ' failed in 5s!"
		d(text = '安装').click.wait()
		if d(text = '权限管理').wait.exists(timeout = 5000):
			d(text = '同意并安装').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/appStatusIconView').wait.exists(timeout = 5000),'App does not start downloading in 5s!'
		d.expect('Open_Icon.png', timeout=90)

	def testAppStoreOpen(self):
		#Launch app store
		d.start_activity(component='com.smartisanos.appstore/.AppStoreActivity')
		assert d(text = '推荐').wait.exists(timeout = 5000),'Launch app store failed in 5s!'

		#New
		d(text = '应用管理').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = '应用管理').wait.exists(timeout = 5000),'Switch to app manager failed in 5s!'
		d(text = '可更新').click.wait()
		assert d(text = '全部更新').wait.exists(timeout = 10000),'Update list does not show up in 10s!'

		#Open app
		d(text = '榜单').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = '榜单').wait.exists(timeout = 5000),"Switch to '排行' view failed in 5s!"
		if d(text = '总排行').wait.exists(timeout = 5000):
			d(text = '总排行').click.wait()
		d(text = 'QQ').click.wait()
		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = 'QQ').wait.exists(timeout = 5000),"Switch to app '微信' failed in 5s!"
		d(text = '打开').click.wait()
		assert d(packageName = 'com.tencent.mm').wait.exists(timeout = 5000),'Launch Wechat from AppStore failed in 5s!'
#		d(text = '我的应用').click.wait()
#		assert d(text = 'QQ').wait.exists(timeout = 5000),'Downloaded app does not in app list!'
#		d(text = 'QQ').click.wait()
#		assert d(resourceId = 'com.smartisanos.appstore:id/title_tv',text = 'QQ').wait.exists(timeout = 5000),"Switch to app 'QQ' failed in 5s!"
#		d(text = '打开').click.wait()
#		assert d(packageName = 'com.tencent.mobileqq').exists,'Open QQ failed!'

	def testUninstallApp(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		#Uninstall app
		self._selectOption('高级设置')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '高级设置').wait.exists(timeout = 5000),'Switch to advanced setting view failed in 5s!'
		self._selectOption('应用程序管理')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '应用程序管理').wait.exists(timeout = 5000),'Switch to app manager view failed in 5s!'
		self._selectOption('QQ')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '应用信息').wait.exists(timeout = 5000),'Switch to app details view failed in 5s!'
		d(text = '卸载').click.wait()
		assert d(textContains = '要卸载此应用吗').wait.exists(timeout = 5000),'Delete alarm does not pop-up in 5s!'
		d(text = '确定').click.wait()
		assert d(text = 'QQ').wait.gone(timeout = 5000),'Uninstall failed in 5s!'

	def _selectOption(self,option):
		i = 1
		while i:
			if d(text = option).exists:
				break
			d.swipe(540,1400,540,400,40)
			d.sleep(1)
			i+=1
			if d(text = option).exists or i==10:
				break
		d.sleep(1)
		d(text = option).click.wait()

	def _downloadOption(self):
		# check app download status 
		if d(text = '安装').wait.exists(timeout = 5000):
			d(text = '安装').click.wait()
			if d(text = '权限管理').wait.exists(timeout = 5000):
				d(text = '同意并安装').click.wait()
			assert d(resourceId = 'com.smartisanos.appstore:id/appStatusIconView').wait.exists(timeout = 5000),'App does not start downloading in 5s!'
			assert d(text = '打开').wait.exists(timeout = 120000), 'Download application failed in 2mins!'
			#d.expect('Open_Icon.png', timeout=90)
		elif d(resourceId = 'com.smartisanos.appstore:id/appStatusIconView').wait.exists(timeout = 5000):
			d(resourceId = 'com.smartisanos.appstore:id/appStatusIconView').click.wait()
			assert d(text = '打开').wait.exists(timeout = 120000), 'Download application failed in 2mins!'
			#d.expect('Open_Icon.png', timeout=90)
		else:
			pass
			#assert False, 'This application can not be Downloaded, pls check if it is already exists in DUT!'