#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u
import string

class PIMTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()

	def testCalendarEvent(self):
		#Launch calander
		d.start_activity(component='com.android.calendar/.AllInOneActivity')
		assert d(text='今天').wait.exists(timeout = 5000),'Launch calendar failed in 5s!'

		#Create event and edit event title and address
		d(text = '新建').click.wait()
		if  d(text = '请选择将任务保存至').exists:
			d(text = '本地账户').click.wait()
		assert d(text = '起始时间').wait.exists(timeout = 5000),'Switch to create event view failed in 5s!'
		d(text = '任务标题').set_text('Test Event')
		if  d(text = '更多选项').exists:
			d(text = '更多选项').click.wait()
		assert d(text = '地点').wait.exists(timeout=5000),'Switch detil edit view failed in 5s!'
		d(text = '地点').set_text('Motolora')
		d(text = '完成').click.wait()
		assert d(resourceId = "com.android.calendar:id/agenda_content").wait.exists(timeout=5000),'Event does not show on the screen in 5s!'
		d.sleep(2)

		#Delete event
		d(resourceId = "com.android.calendar:id/agenda_content").swipe.right(steps=10)
		d(resourceId = 'com.android.calendar:id/delete_icon').click.wait()
		assert d(textContains = '任务列表为空').exists,'Delete event failed'

	def testClock(self):
		#Launch clock
		d.start_activity(component='com.smartisanos.clock/.activity.ClockActivity')
		if d(textContains = '时钟需要获取定位数据').wait.exists(timeout=3000):
			d(text = '同意').click.wait()
		if d(text = '提醒').exists:
			d(text = '同意').click.wait()
		assert d(text = '闹钟').wait.exists(timeout=5000),'Launch clock failed in 5s!'

		d(text = '闹钟').click.wait()
		assert d(resourceId = 'com.smartisanos.clock:id/title',text = '闹钟').wait.exists(timeout=5000),'Switch to clock view failed in 5s!'

		#Create clock
		d(resourceId = 'com.smartisanos.clock:id/add').click.wait()
		assert d(resourceId = 'com.smartisanos.clock:id/hour').wait.exists(timeout=5000),'Switch to edit clock view failed in 5s!'
		d(resourceId = 'com.smartisanos.clock:id/hour').swipe.up(steps=10)
		d(text = '确定').click.wait()

		d(resourceId = 'com.smartisanos.clock:id/set').click.wait()
		assert d(text = '删除闹钟').wait.exists(timeout = 5000),'Switch to set clock view failed in 5s!'
		d(text = '删除闹钟').click.wait()
		assert d(packageName = 'com.smartisanos.clock').exists,'Clock is not show on the screen!'


	def testCreateNote(self):
		# Launch Note
		d.start_activity(component='com.smartisanos.notes/.NotesActivity')
		if d(text = '列表').exists:
			d(text = '列表').click.wait()
		assert d(resourceId = 'com.smartisanos.notes:id/relativelayout_title').wait.exists(timeout = 5000),'Launch Note failed in 5s!'
		d(resourceId = 'com.smartisanos.notes:id/add_button').click.wait()
		assert d(resourceId = 'com.smartisanos.notes:id/delete_insert_button').wait.exists(timeout = 5000),'Switch to note editer failed in 5s!'
		d(resourceId = 'com.smartisanos.notes:id/detail_note_editor').set_text('test content...')
		d(resourceId = 'com.smartisanos.notes:id/delete_insert_button').click.wait()
		d.sleep(1)
		d.click(900,1830)
		d.click('root_dir.png')
		d.sleep(1)
		# select first pic
		d.click(150,370)
		#d.click('image.png')
		d.click('done.png')
		assert d(resourceId = 'com.smartisanos.notes:id/detail_note_image').wait.exists(timeout = 5000),'Add pic to note failed in 5s!'
		d(resourceId = 'com.smartisanos.notes:id/send_finish_button').click.wait()
		d(resourceId = 'com.smartisanos.notes:id/send_finish_button').click.wait()
		assert d(text = '请选择操作').wait.exists(timeout = 5000),'Share selector does not pop-up in 5s!'
		d(text = '以图片形式分享').click.wait()
		assert d(text = '保存图片').wait.exists(timeout = 5000),'Switch to thumbs failed in 5s!'

		before = commands.getoutput('adb shell ls /sdcard/smartisan/notes/* | grep png | wc -l')
		d(text = '保存图片').click.wait()
		d.sleep(2)
		after = commands.getoutput('adb shell ls /sdcard/smartisan/notes/* | grep png | wc -l')
		result = string.atoi(after) - string.atoi(before)
		assert result == 1,'Save note as picture failed!'

		d(text = '取消').click.wait()
		assert d(resourceId = 'com.smartisanos.notes:id/delete_insert_button').wait.exists(timeout = 5000),'Switch to delete view failed in 5s!'
		d(resourceId = 'com.smartisanos.notes:id/delete_insert_button').click.wait()
		d(text = '确认删除').click.wait()
		commands.getoutput('adb shell rm -r /sdcard/smartisan/notes/*')