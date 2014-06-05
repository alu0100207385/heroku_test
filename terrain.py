from django.core.management import call_command
from django.test.simple import DjangoTestSuiteRunner
 
from lettuce import before, after, world
from logging import getLogger
from pyvirtualdisplay import Display
from selenium import webdriver

#Info: before, after: each_feature, each_scenario, each_step, harvest, 
		     #each_app, runserver, handle_request
try:
	from south.management.commands import patch_for_test_db_setup
except:
	pass
 
logger = getLogger(__name__)
logger.info("Loading the terrain file...")


@before.runserver
def setup_database(actual_server):
	#This will setup your database, sync it, and run migrations if you are using South.
	#It does this before the Test Django server is set up.
	logger.info("Setting up a test database...")
 
	# Uncomment if you are using South
	# patch_for_test_db_setup()
 
	world.test_runner = DjangoTestSuiteRunner(interactive=False)
	DjangoTestSuiteRunner.setup_test_environment(world.test_runner)
	world.created_db = DjangoTestSuiteRunner.setup_databases(world.test_runner)
 
	call_command('syncdb', interactive=False, verbosity=0)
 
	# Uncomment if you are using South
	# call_command('migrate', interactive=False, verbosity=0)
'''
@after.runserver
def teardown_database(actual_server):
	#This will destroy your test database after all of your tests have executed.
	
	logger.info("Destroying the test database ...")
 
	DjangoTestSuiteRunner.teardown_databases(world.test_runner, world.created_db)
'''

display = Display(visible=0, size=(1024, 768))
display.start()

'''
@before.all
def setup_browser():
    world.browser = webdriver.Firefox()
    #world.browser = Client()
    
@after.all
def teardown_browser(total):
    world.browser.close()
    #world.browser.quit()
'''

# -*- coding: utf-8 -*-
from lettuce import step
#from lettuce import *
from django.test.client import Client
from nose.tools import assert_equals
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
#from selenium.selenium import selenium
from selenium import selenium
#from selenium import *
from django.utils import unittest

#Scenario: I can access urls
@step(u'I access url "([^"]*)"')
def i_am_at_url(step, url):
    world.browser = webdriver.Firefox()
    world.browser.get(url)
    ##world.browser.close()
    
@step(u'I should see "([^"]*)"')
##def setup_browser(step,self):
    ##world.browser = webdriver.Firefox()
    ##world.browser.quit()
def i_should_see_content(step, content):
    if content not in world.browser.find_element_by_id("content").text:
	raise Exception("Content not found.")
    world.browser.close()


@step(r'Server sends a ([0-9]+) response')
def set_browser(step,self):
    world.browser = Client()
def compare_server_response(step, expected_code):
    code = world.response.status_code
    assert_equals(int(expected_code), code)


##Scenario: I can sign Up & In
@step(u'I access main page "([^"]*)"')
def i_am_at_url(step, url):
    world.browser = webdriver.Firefox()
    world.browser.get(url)

##aqui falta sign up
@step(r'I am a logged-in user in CAN Sistemas')
def user_login(step):
    world.browser.find_element_by_id('username1').send_keys("jazer")
    elemen = world.browser.find_element_by_id('password1')
    elemen.send_keys("1234")
    #time.sleep(3)
    #world.browser.find_element_by_id('submit1').click()
    #elemen.send_keys(Keys.RETURN)
    #try:
	#Thread.sleep(2000)
    #selenium.wait_for_page_to_load("30000")
    #except:
	#time.sleep(3)

    
@step(r'waiting for the BBDD answer')
def wait_for_ajax(timeout=5000):
    #sel = selenium()
    #sel= selenium("localhost", 9000, "*firefox", "http://127.0.0.1:8000/")
    js_condition = "selenium.browserbot.getUserWindow().$.active == 0"
    #js_condition = "selenium.browserbot.getCurrentWindow().jQuery.active == 0"
    #js_condition = "selenium.browserbot.getUserWindow().Ajax.activeRequestCount.active == 0"
    #js_condition = "selenium.browserbot.getUserWindow().dojo.io.XMLHTTPTransport.inFlight.length == 0"
    #wait=WebDriverWait(js_condition, timeout)
    WebDriverWait(js_condition, timeout)
    #sel.wait_for_condition(js_condition, timeout)
    world.browser.find_element_by_id('submit1').click()
    #selenium.WaitForCondition(js_condition, timeout)
    #time.sleep(3)
    #wait.until(EC.element_to_be_clickable(By.ID,'submit1'))
    #selenium.wait_for_page_to_load("30000")
    time.sleep(3)
    #world.browser.close()
    
    #js_condition = "Selenium::Client::Driver.browserbot.getCurrentWindow().jQuery.active == 0"
    #world.browser.implicitly_wait(10) # second
    
'''
@step(r'Test login')
def test_login(step):
    sel = selenium
    #sel.wait_for_page_to_load("30000")
    sel.find_element_by_name('username1').send_keys("jazer")
    sel.find_element_by_name('password1').send_keys("1234")
    sel.find_element_by_name('submit1').click()
    #sel.type("id=username", "test")
    #sel.type("id=password", "test")
    #sel.click("css=input[type=\"submit\"]")
    sel.wait_for_page_to_load("3000")
    #sel.waitForPageToLoad("50000");
'''

@step(u'I am home cause I see "([^"]*)"')
def i_should_see_content(step, content):
    if content not in world.browser.find_element_by_id("content").text:
	raise Exception("Content not found.")
    #world.browser.close()




##aqui falta borrar usu
    
    #world.browser.close()


'''
def set_browser(step):
    world.browser = Client()
def loggin_user(step, **kwargs):
    user = User.objects.create_user('test', '1@1.com', 'testpass')
    world.browser.login(username='test', password='testpass')

@step(r'I can access url "([^"]*)"')
def set_browser(step,url):
    world.browser = webdriver.Firefox()
    world.browser.get(url)
    
@step(r'Log In')
def user_action(step):
    world.browser.find_element_by_name('username1').send_keys('jazer')
    world.browser.find_element_by_name('password1').send_keys('1234')
    world.browser.find_element_by_name('submit1').click()
    world.browser.close()

@step(u'I am home cause I see "([^"]*)"')
def i_should_see_content(step, content):
    if content not in world.browser.find_element_by_link_text("Profile").text:
	raise Exception("Content not found.")
    #world.browser.close()  
'''

display.stop()

'''
@step(r'I access url "(.*)"')
def access_url(step, url):
    world.response = world.browser.get(url)
	
@step(r'Server sends a ([0-9]+) response')
def compare_server_response(step, expected_code):
    code = world.response.status_code
    assert_equals(int(expected_code), code)

@step(r'I am a logged-in user in CAN Sistemas')
def loggin_user(step, **kwargs):
    user = User.objects.create_user('test', '1@1.com', 'testpass')
    world.browser.login(username='test', password='testpass')
'''