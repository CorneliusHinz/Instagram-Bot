# This is a Bot to control Instagram with  a Chrome Driver
# Check Chrome version or it may not work
# Chrome Version: 97.0.4692.99
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Account import *
from selenium.webdriver.common.keys import Keys
import time
import random

class InstagramBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.browser = webdriver.Chrome("./chromedriver.exe ")

        self.dalyLikeCount = 0
        self.dalyFollowedCount = 0
        self.dayCounter = int(self.loadDayCounter())

    def loadDayCounter(self):
        filename = "dayCounter.txt"
        with open(filename, "r") as file:
            day = []
            for line in file:
                day.append(line)
            return day[0]

    def increasDayCounter(self):
        day = self.dayCounter + 1
        filename = "dayCounter.txt"
        with open(filename, "w") as file:
            file.write(str(day) + "\n")

    def waitForObject(self, type, string):
        return WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((type, string)))

    def waitForObjects(self, type, string):
        return WebDriverWait(self.browser, 3).until(EC.presence_of_all_elements_located((type, string)))

    # login account
    def login(self):
        self.browser.get("https://www.instagram.com/accounts/login")
        # Cookies Akzeptieren
        self.waitForObject(By.CSS_SELECTOR, "button.aOOlW.bIiDR").click()
        # Einloggen in Insatgram
        loginObjects = self.waitForObjects(By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP")
        # Nutzername eingeben
        loginObjects[0].send_keys(self.username)
        # Password eingeben
        loginObjects[1].send_keys(self.password)
        # Bestätigen
        self.waitForObject(By.CSS_SELECTOR, "button.sqdOP.L3NKy.y3zKF").click()
        # login-informationen speichern
        time.sleep(3)
        self.waitForObject(By.CSS_SELECTOR, "button.sqdOP.L3NKy.y3zKF").click()
        # Benachrichtigungen aktivieren
        time.sleep(3)
        self.waitForObject(By.CSS_SELECTOR, "button.aOOlW.HoLwm ").click()
        time.sleep(3)
    # like Hastag
    def likeHashtag(self, hashtag, count):
        try:
            self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            self.likePictures(self.loadPictures(), count)
        except:
            print("Error: try again")
            self.likeHashtag(hashtag, count)

    # search and open User
    def openUser(self, username):
        # serch for user
        try:
            self.browser.get(f"https://www.instagram.com/{username}/")
            time.sleep(5)
        except:
            print("Nutzer konnte nicht geladen werden")

    # lade alle bilder auf einer seite und gebe sie als Array zurück
    def loadPictures(self):
        # scrolle über die seite um so viele Bilder wie möglich zu laden
        try:
            self.browser.execute_script("window.scrollTo(0, 40000)")
            # gebe die Bilder als Array zurück
            return self.waitForObjects(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")
        except:
            print("Es konnten keine Bilder geladen werden")
            #self.loadPictures()

    # like bestimmte Anzahl an Bildern
    def likePictures(self, pictures, count):
        try:
            for i in range(count):
                self.likePicture(pictures[i])
        except:
            print("Bilder konnten nicht geliked werden")

    # like ein Bild auf einer seite
    def likePicture(self, picture):
        # open Picture
        try:
            picture.click()
            time.sleep(3)
            # like picture
            self.waitForObject(By.CSS_SELECTOR, "[aria-label='Gefällt mir']").click()
            self.dalyLikeCount += 1
            time.sleep(3)
            # close pictue
            self.waitForObject(By.CSS_SELECTOR, "[aria-label='Schließen']").click()
            print("Vergebene Likes:", self.dalyLikeCount)
            # warte zwischen einer und 5 sekunden
            time.sleep(random.randint(1, 5))
        except:
            print("Bild konnte nicht geliket werden!")

    # like die Bilder eines bestimmten Nutzers
    def likePicturesFromUser(self, username, count):
        # öffne den nutzer
        self.openUser(username)
        # like die anzahl an Bildern
        print("Skip user?")
        skip = input()
        if skip == "j":
            print("skiped user")
        else:
            self.likePictures(self.loadPictures(), count)

    # like Bilder von mehreren Nutzern in einer Liste
    def likePicturesFromUsers(self, usernames):
        # gehe durch alle Nutzer in der Liste und Like eine zufällige anzahl an Bildern
        for user in usernames:
            if self.dalyLikeCount >= 150:
                break
            count = random.randint(1, 4)
            self.likePicturesFromUser(user, count)

    # Folge einem bestimmten Nutzer
    def followUser(self, username):
        # öffne den Nutzer
        self.openUser(username)
        # folge dem nutzer
        self.waitForObject(By.CSS_SELECTOR, "button._5f5mN.jIbKX._6VtSN.yZn4P").click()
        time.sleep(5)

    def unfollowUser(self, username):
        # öffne den Nutzer
        self.openUser(username)
        # entfolge dem Nutzer
        self.waitForObject(By.CSS_SELECTOR, "button._5f5mN.-fzfL._6VtSN.yZn4P").click()
        # entfolgen bestätigen
        self.waitForObject(By.CSS_SELECTOR, "button.aOOlW.-Cab_").click()
        time.sleep(5)

    # gibt die nutzernamen einer liste an nutzern zurück
    def usernamesInList(self, userList):
        usernameList = []
        for user in userList:
            username = user.find_element_by_css_selector('a').get_attribute('title')
            usernameList.append(username)
        return usernameList

    # gibt den nuternamen eines geöffneten Kontos aus
    def getUsername(self):
        username = user.find_element_by_css_selector('a').get_attribute('title')
        return username

    # gibt die aktuelle anzahl an Followern eines geöffneten Kontos aus
    def getFollowerCount(self):
        bar = self.waitForObjects(By.CSS_SELECTOR, "a.-nal3")
        followers = float(bar[0].find_element_by_css_selector('span').get_attribute('title'))
        return followers

    # gibt die aktuelle anzahl an gefolgten Konten eines geöffneten Kontos aus
    def getFollowedCount(self):
        bar = self.waitForObjects(By.CSS_SELECTOR, "a.-nal3")
        followed = float(bar[1].find_element_by_css_selector('span').text)
        return followed

    # gibt die aktuelle anzahl an Post eines geöffneten Kontos aus
    def getPostCount(self):
        bar = self.waitForObject(By.CSS_SELECTOR, "span.-nal3")
        posts = float(bar.find_element_by_css_selector('span').text)
        return posts

    # gibt die Bio eines geöffneten Nutzers aus
    def getBio(self):
        bio = ""
        return bio


    # erstelle eine liste an Nutzern aus den followern eines Nutzers
    def createUserListFromUser(self, username):
        # öffne den Nutzer
        self.openUser(username)
        # todo: methode um aktuelle follower anzahl zu bekommen!


        #followerNumber = self.getFollowerCount()
        #print("follower Number",followerNumber)
        # öffne follower Liste des Nutzers
        self.waitForObject(By.CSS_SELECTOR, "a.-nal3").click()

        lastUser = self.waitForObjects(By.CSS_SELECTOR, "span.Jv7Aj.mArmR.MqpiF")[0]

        #count = int(followerNumber/12)

        for i in range(500):
            try:
                follower = self.waitForObjects(By.CSS_SELECTOR, "span.Jv7Aj.mArmR.MqpiF")
                self.browser.execute_script("arguments[0].scrollIntoView();", follower[-1])
                if lastUser == follower[-1]:
                    break

                lastUser = follower[-1]
                time.sleep(1.5)
            except:
                print("fail")

        follower = self.waitForObjects(By.CSS_SELECTOR, "span.Jv7Aj.mArmR.MqpiF")
        followerNames = self.usernamesInList(follower)

        return followerNames

    def userInfo(self, username):
        userInfo = ""
        # ad username to userInfo
        userInfo += username
        for i in range(30 - len(userInfo)):
            userInfo += " "
        # open user
        self.openUser(username)
        # subscriber
        info = self.waitForObject(By.CSS_SELECTOR, "span.g47SY.lOXF2")
        # posts = info[0]
        # postcount = post.find_element_by_css_selector('span').get_attribute('title')
        #follower = info[1]
        #followerCount = follower.find_element_by_css_selector('span').get_attribute('title')
        #subscriber = [2]
        #subCount = subscriber.find_element_by_css_selector('span').get_attribute('title')
        #print(f"Username:{username}, Follower: {followerCount}, Aboniert: {subCount}")
        print("Info: ", info)
        # return userInfo

    def interactWithUser(self, username):
        # entscheiden ob der nutzer aboniert werden soll
        # todo: methode für abonemons erstellen!
        follow = False;
        self.openUser(username)

        if follow == True:
            # nutzer folgen
            self.followUser(username)
            # nutzer auf die gefolgt liste setzten
            # zähle die anzahl an followed in dalyFollowed
            self.dalyFollowedCount += 1

        # like eine zufällige Anzahl an Bildern
        count = random.randint(1, 3)
        self.likePicturesFromUser(username, count)
        # zähle die anzahl an likes in dalyCount
        self.dalyLikeCount += count
        # speicher die user Informatuion
        # todo: userInfo fertig stellen!



        # Method to wride to file

    def saveUsers(self, usernamesInfo):
        filename = f"followedListDay{self.dayCounter}.txt"
        with open(filename, "w") as file:
            for userInfo in usernamesInfo:
                file.write(userInfo + "\n")

    def loadUsers(self, day):
        filename = f"followedListDay{day}.txt"
        with open(filename, "r") as file:
            rdata = []
            for line in file:
                rdata.append(str(line).replace("\n",""))
        return (rdata)

class user:

    def __init__(self):
        self.info = ""
        self.follower = 0
        self.followed = 0
        self.posts = 0
        self.privacy = 0

    def setInfo(self, info):
        self.info = info


hashtag = ""
hashtagLink = f"https://www.instagram.com/explore/tags/{hashtag}/"
bildLink = "https://www.instagram.com/p/CRzEivGhUuA/"

# bot inizialisieren
Bot = InstagramBot(login, password)
# Login to Account
Bot.login()
#Bot.browser.get(bildLink)
#Bot.likePicturesFromUsers(Bot.loadUsers(0))
#Bot.createUserListFromUser("username")
#Bot.loadPictures()
#Bot.userInfo("username")
#Bot.createUserListFromUser("username")
#Bot.saveUsers(Bot.createUserListFromUser("username"))
#Bot.likeHashtag("zocken", 50)
#Bot.increasDayCounter()