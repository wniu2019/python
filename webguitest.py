from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
'''
test code for simple gui test with selenium (chrome)
"https://www.demoblaze.com"
'''
class TestCase:
    def __init__(self,url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(10)
        time.sleep(2)

    def test_signup(self,username,userpwd):
        self.driver.find_element(By.ID,'signin2').click()
        time.sleep(1)
        self.driver.find_element(By.ID,'sign-username').send_keys(username)
        self.driver.find_element(By.ID,'sign-password').send_keys(userpwd)
        self.driver.find_element(By.XPATH,'//button[contains(@onclick,"register")]').click()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        if alert.text == 'Sign up successful.':
            print(alert.text)
            time.sleep(2)
            alert.accept()
        elif alert.text == 'This user already exist.':
            print(alert.text)
            time.sleep(2)
            alert.accept()
            self.driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[1]').click()
        else:
            print("Sign Up Failed!!!")
            
        
    def test_login(self,username,userpwd):
        #username='testuser' #not be able to log in
        self.driver.find_element(By.ID,'login2').click()
        time.sleep(1)
        self.driver.find_element(By.ID,'loginusername').send_keys(username)
        self.driver.find_element(By.ID,'loginpassword').send_keys(userpwd)
        self.driver.find_element(By.XPATH,'//button[contains(@onclick,"logIn")]').click()
        time.sleep(1)
        try:
           WebDriverWait(self.driver, 5).until (EC.alert_is_present())
           alert = self.driver.switch_to.alert
           alert.accept()
           print("Log in Failed")
           time.sleep(2)
           self.driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[1]').click()
        except TimeoutException:
           print("Log in successful")
           nameofuser = self.driver.find_element(By.ID,'nameofuser')

    def test_logout(self):
        nameofuser = self.driver.find_element(By.ID,'nameofuser')
        if nameofuser.text.find('Welcome') >=0:
            self.driver.find_element(By.ID,'logout2').click()
            
    def test_add(self,item):
        self.driver.find_element(By.PARTIAL_LINK_TEXT,'Home').click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT,item).click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, 'Add to cart').click()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        print(f'{item} {alert.text}')
        alert.accept()
        time.sleep(1)

    def test_verify(self,items):
        self.driver.find_element(By.LINK_TEXT,'Cart').click()
        time.sleep(1)
        item_in_table = self.driver.find_elements(By.XPATH,"//table/tbody/tr")
        #list all items in the table
        one_to_one = [0]*len(items)
        #place holder to check if there is a one to one match
        if len(items) == len(item_in_table):
            for i in range(len(items)):
                for item in item_in_table:
                    if items[i] in item.text:
                        one_to_one[i] = 1

            if sum(one_to_one) == len(items):
                print(f'{len(items)} items match the cart')
            else:
                print("some item does not match items in the cart")
        else:
            print("items number does not match the cart")

    def test_delete(self,item):
        self.driver.find_element(By.LINK_TEXT,'Cart').click()
        time.sleep(1)
        item_in_table = self.driver.find_elements(By.XPATH,"//table/tbody/tr")
        for it in item_in_table:
            if item in it.text:
                it.find_element(By.LINK_TEXT,'Delete').click()
                print(item + ' deleted')
            
        
if __name__ == "__main__":
    url = "https://www.demoblaze.com"
    username = "user_test_123"
    userpwd = "pass123456789"
    items = ['Samsung galaxy s7','Sony xperia z5']
    
    case = TestCase(url)

    case.test_signup(username,userpwd)

    case.test_login(username,userpwd)

    for item in items:
        case.test_add(item)

    case.test_verify(items)

    #delete one
    case.test_delete(items[1])
    items.remove(items[1])
    case.test_verify(items)

    #delete another one
    case.test_delete(items[0])
    items.remove(items[0])
    #empty list
    case.test_verify(items)

    case.test_logout()

    case.test_login(username,userpwd)
    case.test_verify(items)

    #items list is empty now, add one item
    items.append('Nokia lumia 1520')

    case.test_add(items[0])
    case.test_verify(items)
    
    case.test_delete(items[0])
    items.remove(items[0])
    case.test_verify(items)

    case.test_logout()

    case.test_login(username,userpwd)

    case.test_verify(items)

    case.test_logout()
    
    case.driver.quit()
    
