##################################################################
#
# JIRA2 NCMSDWANT-109
# Develop UI QA test automation for framework apps
# Subtask-2 v1.1
#
# by Muzaffer Kahraman Nokia IPO NME June 2021
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
import logging
import datetime
import time

def web():
 global driver
 op = webdriver.ChromeOptions()
 op.add_argument('--headless')
 op.add_argument('--ignore-certificate-errors')
 op.add_argument("--start-maximized")
 # Below 7 statements is needed to make the script work at linux
 op.add_argument('--disable-gpu')
 op.add_argument("--no-sandbox") 
 op.add_argument("--disable-dev-shm-usage")
 from pyvirtualdisplay import Display
 display = Display(visible=0, size=(800, 800))  
 display.start()
 driver = webdriver.Chrome("/usr/bin/chromedriver",options=op)
 # Below is for windows
 # driver = webdriver.Chrome(options=op)

def Measuretime(tab,statement):
 reqtime=datetime.datetime.now()
 inputElement = driver.find_element_by_id(tab)
 driver.execute_script("arguments[0].click();", inputElement)
 WebDriverWait(driver,60).until(ec.presence_of_element_located((By.ID,"dataGrid")))
 while True:
       element = driver.find_element_by_id("dataGrid")
       s=(element.text)[5:]
       if (s[0:27]=="No entries match the filter") or (s[0:16]!= "Nothing Selected"):
           break
 resptime=datetime.datetime.now()
 statement=statement.ljust(85,".")
 print(statement,str(resptime-reqtime))

if __name__ == "__main__":

 # Set the log file
 logging.basicConfig(filename='/tmp/whitelabeltest2.log',level=logging.INFO, format='%(asctime)s %(levelname)s  %(message)s')
 logging.info('Started')

 # Parses the /tmp/test.properties file to get the url and the credentials
 try:
  f = open("/tmp/test.properties","r")
 except FileNotFoundError:
  print("There is no test.properties file found under /tmp")

 A=f.readlines()
 numberofapps=len(A) // 5


 # Loops to execute the process to all apps
 
 for i in range (0,numberofapps):

  web()
  
  appname=A[i*5].partition("=")[2].replace('\n', '')
  if appname=="Portal":
      continue
  url=A[i*5+1].partition("=")[2].replace('\n', '')
  username=A[i*5+2].partition("=")[2].replace('\n', '')
  password=A[i*5+3].partition("=")[2].replace('\n', '')
  org=A[i*5+4].partition("=")[2].replace('\n', '')
  logging.info('Credentials parsed for '+appname)

  reqtime=datetime.datetime.now()
  
  # Connects to the page
  driver.get(url)

  logging.info('URL '+url+'requested')
  # Waits until the page title 
  WebDriverWait(driver,5060).until(ec.element_to_be_clickable((By.XPATH,"//input[@name='username']")))
                                                                 
  # Types the credentials
  inputElement = driver.find_element_by_xpath("//input[@name='username']")
  inputElement.send_keys(username)

  inputElement = driver.find_element_by_xpath("//input[@name='password']")
  inputElement.send_keys(password)

  inputElement = driver.find_element_by_xpath("//input[@name='orgName']")
  inputElement.send_keys(org)
 
  # Waits for the SIGN IN button be activated
  WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH,"//span[@class='MuiButton-label-206']")))

  # Clicks an the SIGN IN button
  inputElement = driver.find_element_by_xpath("//button[@type='submit']")
  inputElement.click()
 
  # Waits for the new page
  WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//h1[normalize-space()='SD-WAN']")))
 
  resptime=datetime.datetime.now()

  logging.info('Logged in')
  
  print("Application:",appname)
  print("-----------------------------------------------------------------------------------------------")                     

  # Checks if the OVERVIEW TAB is visible

  statement="Measurment-1 Duration from typing the url to get OVERVIEW tab opens".ljust(85,".")
  print(statement,str(resptime-reqtime))

  if appname=="Extended-Config":

      if username=="superAdmin":

        Measuretime("tab-2","Measurment-2 Duration of switching to UBR ALARMS page")   
        Measuretime("tab-3","Measurment-3 Duration of switching to UBR ASSIGNMENT page")
        Measuretime("tab-4","Measurment-4 Duration of switching to UBR GROUP ASSIGNMENTS page")
        Measuretime("tab-5","Measurment-5 Duration of switching to NSG GROUP MANAGEMENT page")
        Measuretime("tab-6","Measurment-6 Duration of switching to UBR PORT MANAGEMENT page")

      else:

        Measuretime("tab-2","Measurment-2 Duration of switching to UBR ALARMS page")   
        Measuretime("tab-3","Measurment-3 Duration of switching to UBR GROUP ASSIGNMENTS page")
        Measuretime("tab-4","Measurment-4 Duration of switching to NSG GROUP MANAGEMENT page")
        Measuretime("tab-5","Measurment-5 Duration of switching to UBR PORT MANAGEMENT page")


  if appname=="NSG-Upgrade":

    Measuretime("tab-2","Measurment-2 Duration of switching to INVENTORY page")
    Measuretime("tab-3","Measurment-3 Duration of switching to UPGRADE page")
    Measuretime("tab-4","Measurment-4 Duration of switching to OPERATIONS page")
    
  logging.info("Measurments completed for all tabs of the "+appname)
         
  # Logs out
  
  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-userAccount-content']")
  inputElement.click()

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-logout-content']")
  inputElement.click()

  reqtime=datetime.datetime.now()

  WebDriverWait(driver,5060).until(ec.element_to_be_clickable((By.XPATH,"//input[@name='username']")))
  resptime=datetime.datetime.now()

  if appname=="NSG-Upgrade":

     statement="Measurment-5 Duration of logging out".ljust(85,".")

  if appname=="Extended-Config":
     
     if username=="superAdmin":

        statement="Measurment-7 Duration of logging out".ljust(85,".")
        
     else:

        statement="Measurment-6 Duration of logging out".ljust(85,".")
      
    
  print(statement,str(resptime-reqtime))

  print()

  logging.info('Logged out')

  driver.close()
 
 logging.info('Stopped')








