#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import random
import util as u

THEME_LIST = ['经典','灰岩','青色','蓝色','紫色','褐色','浅灰','毛玻璃','橙色']

class SettingTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()

	def testSetTheme(self):
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'
		u.selectOption('主题、壁纸、图标')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '主题、壁纸、图标').wait.exists(timeout = 5000),'Switch to theme view failed in 5s!'
		u.selectOption('桌面主题')
		assert d(resourceId = 'com.smartisanos.launcher:id/tv_title',text = '桌面主题').wait.exists(timeout = 5000),'Switch to theme view failed in 5s!'
		for theme in THEME_LIST:
#			if theme == '经典':
#				u.selectOption(theme)
#				assert d(resourceId = 'smartisanos:id/tv_title',text = theme).wait.exists(timeout = 5000),'Switch to theme thumbnail failed in 5s!'
#				d(text = '设定').click.wait()
#				if d(text = '桌面主题').wait.exists(timeout = 5000):
#					continue
#				else:
#					assert d(resourceId = 'com.smartisanos.launcher:id/glview').wait.exists(timeout = 15000), 'Switch to launcher failed in 15s!'
#					
			if theme == '经典':
				d(resourceId = 'com.smartisanos.launcher:id/list_theme').swipe.down()
				d(resourceId = 'com.smartisanos.launcher:id/list_theme').swipe.down()
				d(resourceId = 'com.smartisanos.launcher:id/list_theme').swipe.down()
				d.sleep(1)
			u.selectOption(theme)
			assert d(resourceId = 'smartisanos:id/tv_title',text = theme).wait.exists(timeout = 5000),'Switch to theme thumbnail failed in 5s!'
			d(text = '设定').click.wait()
			assert d(text = '正在加载主题').wait.exists(timeout = 5000),'Loading theme view does not show up in 5s!'
			assert d(text = '正在加载主题').wait.gone(timeout = 10000),'Loading theme view does not disappeared in 10s!'
			assert d(resourceId = 'com.smartisanos.launcher:id/glview').wait.exists(timeout = 5000), 'Switch to launcher failed in 5s!'
			d.sleep(3)
			# exit theme setting
			d.start_activity(component='com.android.settings/.Settings')
			d.sleep(1)

	def testTurnOnOffWiFi(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		self._selectOption('无线网络')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '无线网络').wait.exists(timeout = 5000),'Switch to WIFI failed in 5s!'
		if d(text = '要查看可用网络，请打开无线网络').exists:
			print 'Current wifi status: Off'
			d(resourceId = 'com.android.settings:id/item_switch').swipe.right(steps = 5)
			d(text = '已连接').wait.exists(timeout = 15000)
		else:
			print 'Current wifi status: On'
			d(text = '已连接').wait.exists(timeout = 15000)
		#Turn off wifi
		d(resourceId = 'com.android.settings:id/item_switch').swipe.left(steps = 5)
		assert d(text = '要查看可用网络，请打开无线网络').wait.exists(timeout = 5000),'Turn off wifi failed in 5s!'
		#Turn on wifi
		d(resourceId = 'com.android.settings:id/item_switch').swipe.right(steps = 5)
		assert d(text = '已连接').wait.exists(timeout = 15000),'Turn on wifi failed in 15s!'

	def testTurnOnOffBT(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		self._selectOption('蓝牙')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '蓝牙').wait.exists(timeout = 5000),'Switch to BT failed in 5s!'
		if d(text = '范围内可配对设备').exists:
			print 'Current BT status: On'
			d(resourceId = 'com.android.settings:id/item_switch').swipe.left(steps = 5)
			d(text = '要查看可用蓝牙设备，请打开蓝牙功能').wait.exists(timeout = 5000)
		#Turn off BT
		d(resourceId = 'com.android.settings:id/item_switch').swipe.right(steps = 5)
		assert d(text = '范围内可配对设备').wait.exists(timeout = 5000),'Turn on BT failed in 5s!'
		#Turn on wifi
		d(resourceId = 'com.android.settings:id/item_switch').swipe.left(steps = 5)
		assert d(text = '要查看可用蓝牙设备，请打开蓝牙功能').wait.exists(timeout = 5000),'Turn off BT failed in 5s!'

	def testTurnOnOffNFC(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		self._selectOption('NFC')
		assert d(resourceId = 'smartisanos:id/tv_title',text = 'NFC').wait.exists(timeout = 5000),'Switch to NFC failed in 5s!'
		d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_nfc").child(className="smartisanos.widget.SwitchEx").swipe.right(steps = 5)
		d.sleep(3)
		assert d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_android_beam").child(className="smartisanos.widget.SwitchEx").info['enabled'],'Turn NFC failed in 3s!'
		#d(text="NFC").right(className="smartisanos.widget.SwitchEx").click()
		d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_nfc").child(className="smartisanos.widget.SwitchEx").swipe.left(steps = 5)
		assert not d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_android_beam").child(className="smartisanos.widget.SwitchEx").info['enabled'],'Turn NFC failed in 3s!'

	def _selectOption(self,option):
		i = 1
		while i:
			if d(text = option).exists:
				break
			d.swipe(540,1400,540,400,100)
			d.sleep(1)
			i+=1
			if d(text = option).exists or i==10:
				break
		d.sleep(1)
		d(text = option).click.wait()