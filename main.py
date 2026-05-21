from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
import time, os

URL = 'https://appbrewery.github.io/gym/'
BOOKING_URL = 'https://appbrewery.github.io/gym/my-bookings/'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

user_data_dir = os.path.join(os.getcwd(), "gym_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=URL)

#click join today btn..
join_btn = driver.find_element(By.CSS_SELECTOR,".Home_heroButton__3eeI3")
join_btn.click()
webdriver_wait = WebDriverWait(driver,5)
wait_till_login_url = webdriver_wait.until(EC.url_to_be('https://appbrewery.github.io/gym/login/'))


def retry(func,descr,retries=7):

    for retries in range(1,retries+1):
        if func():
            return True
        print(descr + f" Attempt : {retries}")

    print("⚠️ Re-attempt failed while : ",descr)
    return False

def login():     
    try:
        #login using credentials
        ACCOUNT_EMAIL = "sahil@test.com"
        ACCOUNT_PASSWORD = "Sahil@@123"
        #find email textbox using name attr
        email_input = driver.find_element(By.CSS_SELECTOR,value="#email-input")
        email_input.clear()
        email_input.send_keys(ACCOUNT_EMAIL)
        #find password textbox using name attr
        pass_input = driver.find_element(By.CSS_SELECTOR,value="#password-input")
        pass_input.clear()
        pass_input.send_keys(ACCOUNT_PASSWORD)
        #submit login btn
        login_btn = driver.find_element(By.CSS_SELECTOR,value="#submit-button")
        login_btn.submit()
        try:
            webdriver_wait.until(EC.url_contains('schedule'))
            # print(login_error.text)
            return True
        except:
            return False
        
    except NoSuchElementException:
        print('Element not found in DOM.')

retry(login,retries=7,descr="Retrying Login")

try:
    wait_till_url = webdriver_wait.until(EC.url_to_be('https://appbrewery.github.io/gym/schedule/'))

    #parse classes day wise and look for tuesdays
    schedule_page = driver.find_element(By.CSS_SELECTOR,"#schedule-page")
    day_groups = schedule_page.find_elements(By.CSS_SELECTOR,"div[id^='day-group-']")
    classes = []
    for group in day_groups:
        if 'tue' in group.get_property('id') or 'thu' in group.get_property('id'):
            class_names = group.find_elements(By.CSS_SELECTOR,"h3[id^='class-name-']")
            start_times = group.find_elements(By.CSS_SELECTOR,"p[id^='class-time']")
            day_n_date = group.find_element(By.CSS_SELECTOR,"h2")
            availability = group.find_elements(By.CSS_SELECTOR,"p[id^='class-availability-']")
            book_button = group.find_elements(By.CSS_SELECTOR,"button[id^='book-button-']")
            # convert day/date: OLD: Tomorrow (Tue, May 5) -> NEW: ['Tue', 'May 5']

            if '(' in day_n_date.text:
                split_day_n_date = day_n_date.text.split('(')[1].split(')')[0]
                split_day_n_date = [x.strip() for x in split_day_n_date.split(',')]
            else:
                split_day_n_date = [x.strip() for x in day_n_date.text.split(',')]

            for n,t,a,b_btn in zip(class_names,start_times,availability,book_button):
                classes.append({
                        'name':n.text,  
                        'time': t.text.replace('Time: ',''),
                        'date' : split_day_n_date[1],
                        'day' : split_day_n_date[0],
                        'availability' : a.text.split(':')[0],
                        'book_btn_elmnt' : b_btn,
                    })
except Exception as e:
    print("\nNo classes were found :",e)


total_6pm_classes = 0

def book_class():
    try:
        global total_6pm_classes
        for avail_classes in classes[:]:         
            if avail_classes['time'] == '6:00 PM':
                try:
                    btn_status = avail_classes['book_btn_elmnt'].text
                    
                    if btn_status == 'Booked':
                        #already booked
                        # already_booked_waitlisted += 1
                        print(f"\nAlready booked: {avail_classes['name']} on {avail_classes['day']} {avail_classes['date']}, at {avail_classes['time']}.")
                        classes.remove(avail_classes)
                        total_6pm_classes += 1
                    elif btn_status == 'Waitlisted':
                        #on waitlist
                        # already_booked_waitlisted += 1
                        print(f"\nAlready on waitlist for: {avail_classes['name']} on {avail_classes['day']} {avail_classes['date']}, at {avail_classes['time']}.")
                        classes.remove(avail_classes)
                        total_6pm_classes += 1
                    elif btn_status == 'Join Waitlist':
                        #Join waitlist
                        # waitlist_joined += 1
                        avail_classes['book_btn_elmnt'].click()
                        while avail_classes['book_btn_elmnt'].get_attribute('aria-busy') == 'true':
                            time.sleep(0.2)

                        if avail_classes['book_btn_elmnt'].text == 'Waitlisted':
                            print(f"\nWaitlisted: {avail_classes['name']} on {avail_classes['day']} {avail_classes['date']}, at {avail_classes['time']}.")
                            classes.remove(avail_classes)
                            total_6pm_classes += 1
                        else:

                            return False
                      
                    elif btn_status == 'Book Class':
                        # classes_booked += 1
                        avail_classes['book_btn_elmnt'].click()
                        while avail_classes['book_btn_elmnt'].get_attribute('aria-busy') == 'true':
                            time.sleep(0.2)

                        if avail_classes['book_btn_elmnt'].text == 'Booked':
                            print(f"\nBooked: {avail_classes['name']} on {avail_classes['day']} {avail_classes['date']}, at {avail_classes['time']}.")
                            classes.remove(avail_classes)
                            total_6pm_classes += 1
                        else:

                            return False
                    else:
                        print(f"\n⚠️ Unknown button state: {btn_status}")

                except StaleElementReferenceException:
                    print("Element was not found in DOM")
                except NoSuchElementException:
                    print("Btn element was not found")
        return True
    except NoSuchElementException as e:
        print('Element not found in DOM.',e)



def verify_booking():
    try:              
        driver.get(url=BOOKING_URL)
        webdriver_wait.until(EC.url_to_be(BOOKING_URL))
        total_confirmed_classes = 0
        total_waitlisted_classes = 0 
        verification_res = False
        
        print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_6pm_classes} ---")
        print(f"\n--- VERIFYING ON MY BOOKINGS PAGE ---")
        try:
            confirmed_classes_list = []
            confirmed_booking_sec = driver.find_elements(By.CSS_SELECTOR,"div[data-booking-status='confirmed']")
            for c_classes in confirmed_booking_sec:
                confirmed_classes_list.append(c_classes.find_element(By.CSS_SELECTOR,"h3[id^='booking-class-name-']"))
            total_confirmed_classes = len(confirmed_classes_list)
            
            for c_bookings in confirmed_classes_list:
                print(f"  ✓ Verified: {c_bookings.text}")
            
            waitlisted_classes_list = []
            waitlisted_booking_sec = driver.find_elements(By.CSS_SELECTOR,"div[data-booking-status='waitlisted']")
            
            for w_classes in waitlisted_booking_sec:
                waitlisted_classes_list.append(w_classes.find_element(By.CSS_SELECTOR,"h3[id^='waitlist-class-name-']"))
            total_waitlisted_classes = len(waitlisted_classes_list)

            for w_bookings in waitlisted_classes_list:
                print(f"  ✓ Verified: {w_bookings.text}")

        except NoSuchElementException:
            pass
        try:
            print(f"\n--- VERIFICATION RESULT ---")
            total_bookings_on_my_bookings = total_confirmed_classes + total_waitlisted_classes
            print(f"Expected: {total_6pm_classes} bookings")
            if total_bookings_on_my_bookings == total_6pm_classes:
                verification_res = True
                print(f"Found: {total_bookings_on_my_bookings} bookings")
            else:
                print(f"❌ MISMATCH: Missing {total_6pm_classes-total_bookings_on_my_bookings} bookings\n")
            if verification_res:
                print("✅ SUCCESS: All bookings verified!\n")
        except:
            print("Verification Failed!")
            
        
    except NoSuchElementException as e:
        print('Element not found in DOM.',e)


retry(book_class,retries=7,descr="Booking Attempt")

verify_booking()