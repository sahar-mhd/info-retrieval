from selenium import webdriver
import csv
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def getBooks(driver, collection_books, book_list):
    # Loop through each book element and extract information
    for book_elem in collection_books:
        a_tag = book_elem.find_element_by_tag_name("a")
        book_link = a_tag.get_attribute("href")
        # book_link = book_elem.parent.current_url
        driver.get(book_link)
        # Find the book details section
        book_details = driver.find_element(By.ID, 'BookDetails')
        book_rating = driver.find_element(By.CSS_SELECTOR, '.rating-options')
        # Extract the book details
        book = {}
        try:
            rate = book_rating.find_element(By.CSS_SELECTOR, '.small-rating-stars-value.golden')
            book["rate"] = round((rate.size['width'] * 5) / 90, 1)
        except:
            book["rate"] = 0
        try:
            s = book_rating.find_element(By.CSS_SELECTOR, '.small-rating-reviews-num').text
            match = re.search(r'\d+', s)
            book["comment-count"] = int(match.group())
        except:
            book["comment-count"] = 0
        try:
            book["topic"] = book_details.find_element(By.CSS_SELECTOR,'a[href*="book-category"]').text
        except:
            book["topic"] = ''
        try:
            book["name"] = book_details.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
        except:
            book["name"] = ''
        try:
            book["author"] = book_details.find_element(By.CSS_SELECTOR, '[itemprop="author"]').text
        except:
            book["author"] = ''
        try:
            book["translator"] = book_details.find_element(By.CSS_SELECTOR, '[itemprop="translator"]').text
        except:
            book["translator"] = ''
        try:
            book["publisher"] = book_details.find_element(By.CSS_SELECTOR, 'a[href*="publisher"]').text
        except:
            book["publisher"] = ''
        try:
            book["price"] = book_details.find_element(By.CSS_SELECTOR,".discounted-price").text
        except:
            book["price"] = ''
        try:
            book["publish-year"] = book_details.find_element(By.XPATH, '//tr[td="سال انتشار"]/td[2]').text
        except:
            book["publish-year"] = ''
        book_list.append(book)
        driver.back() 
    
url = "https://www.ketabrah.ir/"

chromedriver_path = "chromedriver/chromedriver.exe"
chrome_profile_path = 'C:/Users/faeze/AppData/Local/Google/Chrome/User Data'

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={chrome_profile_path}")
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
# driver = webdriver.Chrome()

driver.implicitly_wait(10)

driver.get(url)


try:
    categories = driver.find_element("id","RightCoulmnNavigatin")
    a_tags = categories.find_elements("tag name","a")
    for index in range(len(a_tags)):
        if index < 17: continue
                
        book_list = []
        start_time = time.time()
        
        categories = driver.find_element("id","RightCoulmnNavigatin")
        temp = categories.find_elements("tag name","a")
        temp2 = temp[index]
        driver.execute_script("arguments[0].scrollIntoView();", temp[index - 3])
        temp2.click()
        
        first_collection = driver.find_elements(By.CSS_SELECTOR,'a[href*="sort=populars"]')
        first_collection[0].click()
        collection_books = driver.find_elements(By.CSS_SELECTOR, '[itemscope="itemscope"]')
        
        getBooks(driver, collection_books, book_list)
        
        try:
            while True:
                # click on next button to go to the next page  
                driver.find_element(By.CSS_SELECTOR, '.item.next-page').click()
                collection_books = driver.find_elements(By.CSS_SELECTOR, '[itemscope="itemscope"]')
                getBooks(driver, collection_books, book_list)
        except:
            # if there was no next button
            end_time = time.time()
            runtime = end_time - start_time
            print("category ", index, "runtime: ", round(runtime, 2), "seconds")
            try:
                # Specify the CSV file name
                filename = 'book_info.csv'

                # Open the CSV file in write mode with encoding
                with open(filename, mode='a', encoding='utf-8', newline='') as file:

                    # Create a writer object
                    writer = csv.DictWriter(file, fieldnames=book_list[0].keys())

                    # Write the data rows
                    writer.writerows(book_list)
            except Exception as e:
                print("An error occurred in csv saving: ", e)
            driver.get(url)

        
    
except NoSuchElementException as e:
    print("Element not found: ", e)
except TimeoutException as e:
    print("Timeout occurred: ", e)
except Exception as e:
    print("An error occurred: ", e)


# Quit the driver
driver.quit()  