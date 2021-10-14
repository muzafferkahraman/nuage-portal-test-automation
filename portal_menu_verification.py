##################################################################
#
# JIRA2 NCMSDWANT-109
# Develop UI QA test automation for framework apps
# Subtask-3 v1.0
#
# by Muzaffer Kahraman Nokia IPO NME June 2021
#
##################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import logging
import time

def web():
 global driver
# Add headless option to make it work without Chrome popup
 op = webdriver.ChromeOptions()
 op.add_argument('--ignore-certificate-errors')
# op.add_argument("--start-maximized")
# Below 8 statements is needed to make the script work at linux
 op.add_argument('--headless')
 op.add_argument("window-size=1920x1080")
 op.add_argument('--disable-gpu')
 op.add_argument("--no-sandbox")
 op.add_argument("--disable-dev-shm-usage")
 from pyvirtualdisplay import Display
 display = Display(visible=0, size=(1920, 1080))
 display.start()
 driver = webdriver.Chrome("/usr/bin/chromedriver",options=op)
# Below is for windows
# driver = webdriver.Chrome(options=op)


def checkubrmng(tab,keys,item,statement):

      global s2


      if tab != "no tab":

         inputElement = driver.find_element_by_id(tab)
         driver.execute_script("arguments[0].click();", inputElement)

         time.sleep(4)

         element = driver.find_element_by_id("dataGrid")
         s2=element.text

      if ("No entries match the filter" not in s2):

         rows = driver.find_elements_by_class_name("ag-center-cols-viewport")
         s=rows[0].text
         A=s.split("\n")
         s=A[0]

         if keys=="no keys":

           inputElement = driver.find_element_by_xpath("//input[@class='ag-floating-filter-input']")
           inputElement.send_keys(s)
           time.sleep(5)
           rows = driver.find_elements_by_class_name("ag-center-cols-viewport")
           s1=rows[0].text
           A=s1.split("\n")
           s1=A[0]


         else:

           inputElement = driver.find_element_by_xpath("//input[@class='ag-floating-filter-input']")
           inputElement.send_keys(32 * Keys.BACKSPACE)
           inputElement.send_keys(keys)
           time.sleep(4)
           element = driver.find_element_by_id("dataGrid")
           s=(element.text)

           s1="No entries match the filter"



         statement=(item+statement).ljust(85,".")
         if s1 in s:
           print(statement,"complied")
         else:
           print(statement,"Not complied!")

      else:

          statement=(item+"cannot be checked since no object is provisioned").ljust(85,".")
          print(statement,"Not Applicable")

def checknsgupg(tab,rowidx,arridx,headeridx,keys,item,statement):

    global s2

    if tab != "no tab":

         inputElement = driver.find_element_by_id(tab)
         driver.execute_script("arguments[0].click();", inputElement)


         time.sleep(1)
         inputElement = driver.find_element_by_xpath("//div[@class='csfWidgets progress-bar-indeterminate__bar--second']")
         WebDriverWait(driver,60).until(ec.staleness_of(inputElement))
         WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.ID,"dataGrid")))

         element = driver.find_element_by_id("dataGrid")
         s2=element.text

    if ("No entries match the filter" not in s2):


        time.sleep(2)


        if keys=="no keys":

           rows = driver.find_elements_by_id("dataGrid-actions-header-0")
           s=((rows[rowidx].text).split("\n"))[arridx]

           WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//div[@id='dataGrid-header-"+ headeridx +"']//input[@class='ag-floating-filter-input']")))

           inputElement = driver.find_element_by_xpath("//div[@id='dataGrid-header-"+ headeridx +"']//input[@class='ag-floating-filter-input']")
           inputElement.send_keys(s)

           time.sleep(4)
           rows = driver.find_elements_by_id("dataGrid-actions-header-0")
           s1=((rows[rowidx].text).split("\n"))[arridx]

        else:

           inputElement = driver.find_element_by_xpath("//div[@id='dataGrid-header-"+ headeridx +"']//input[@class='ag-floating-filter-input']")
           inputElement.send_keys(32 * Keys.BACKSPACE)
           inputElement.send_keys(keys)

           time.sleep(4)
           element = driver.find_element_by_id("dataGrid")
           s=(element.text)


           s1="No entries match the filter"

        statement=(item+statement).ljust(85,".")
        if s1 in s:
           print(statement,"complied")
        else:
           print(statement,"Not complied!")

    else:

          statement=(item+"cannot be checked since no object is provisioned").ljust(85,".")
          print(statement,"Not Applicable")





if __name__ == "__main__":

 # Set the log file
 logging.basicConfig(filename='/tmp/whitelabeltest3.log',level=logging.INFO, format='%(asctime)s %(levelname)s  %(message)s')
 logging.info('Started')

 # Parses the /tmp/test3.properties file to get the url and the credentials
 f = open("/tmp/test3.properties","r")

 A=f.readlines()
 numberofapps=len(A) // 5


 # Loops to execute the process to all apps

 for i in range (0,numberofapps):

  web()

  appname=A[i*5].partition("=")[2].replace('\n', '')
  url=A[i*5+1].partition("=")[2].replace('\n', '')
  username=A[i*5+2].partition("=")[2].replace('\n', '')
  password=A[i*5+3].partition("=")[2].replace('\n', '')
  org=A[i*5+4].partition("=")[2].replace('\n', '')
  logging.info('Credentials parsed for '+appname)


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

  print("Application:",appname)
  print("-----------------------------------------------------------------------------------------------")


  # Waits for the SIGN IN button be activated
  WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH,"//span[@class='MuiButton-label-206']")))

  statement="Criteria-1 SIGN IN Button was greyed-out before all creds are typed".ljust(85,".")
  print(statement,"complied")


  # Clicks an the SIGN IN button
  inputElement = driver.find_element_by_xpath("//button[@type='submit']")
  inputElement.click()

  # Waits for the new page
  WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//h1[normalize-space()='SD-WAN']")))

  logging.info('Logged in')


  if appname=="Extended-Config":

      logging.info('Extended-Config tests started')

      checkubrmng("tab-3","no keys","Criteria-2 ","UBR Assignment tab filters are working as it should")
      checkubrmng("no tab","!*?/muzo","Criteria-3 ","UBR Assignment tab filters are not matching irrelevant strings")

      logging.info('UBR Assignment tab filters checked')

      checkubrmng("tab-4","no keys","Criteria-4 ","UBR Group Assignment tab filters are working as it should")
      checkubrmng("no tab","!*?/muzo","Criteria-5 ","UBR Group Assignment tab filters are not matching irrelevant strings")

      logging.info('UBR Group Assignment tab filters checked')

      checkubrmng("tab-5","no keys","Criteria-6 ","NSG Group Management tab filters are working as it should")
      checkubrmng("no tab","!*?/muzo","Criteria-7 ","NSG Group Management tab filters are not matching irrelevant strings")

      logging.info("NSG Group Management tab filters checked")

      checkubrmng("tab-6","no keys","Criteria-8 ","UBR Port Management tab filters are working as it should")
      checkubrmng("no tab","!*?/muzo","Criteria-9 ","UBR Port Management tab filters are not matching irrelevant strings")

      logging.info('UBR Port Management tab filters checked')

      print()

  if appname=="NSG-Upgrade":

      logging.info('NSG-Upgrade tests started')

      checknsgupg("tab-2",1,1,"14","no keys","Criteria-2 ","NSG INVENTORY tab filters are working as it should")
      checknsgupg("no tab",1,1,"14","!*?/muzo","Criteria-3 ","NSG INVENTORY tab filters are not matching irrelevant strings")

      logging.info('NSG INVENTORY tab filters checked')

      checknsgupg("tab-3",0,0,"7","no keys","Criteria-4 ","NSG UPGRADE tab filters are working as it should")
      checknsgupg("no tab",0,0,"7","!*?/muzo","Criteria-5 ","NSG UPGRADE tab filters are not matching irrelevant strings")

      logging.info("NSG UPGRADE tab filters checked")

  # Logs out

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-userAccount-content']")
  inputElement.click()

  inputElement = driver.find_element_by_xpath("//div[@id='csfWidgets-banner-appBanner-userAccountSummaryButton-logout-content']")
  inputElement.click()

  logging.info('Logged out')

  driver.close()

logging.info('Stopped')

