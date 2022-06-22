import pyttsx3
import datetime
from soupsieve import match
import speech_recognition as sr
import wikipedia
import webbrowser
import re
import os 
import random
import time
from playsound import playsound
from subprocess import call
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.mixer.init()

boss = "Amanat Singh"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)

def playMusicOnly(pathOfMusic):
    pygame.mixer.music.load(pathOfMusic)
    TrackObject = pygame.mixer.Sound(pathOfMusic)
    pygame.mixer.music.play()
    time.sleep(float(TrackObject.get_length()))

class CallPy:

    def __init__(self , path):
        self.path = path

    def call_python_file(self):
        call(["C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python37\\python.exe" , f"{self.path}"])

def speak(toSpeak):
    '''
    speaks the toSpeak argument
    '''
    engine.say(toSpeak)
    engine.runAndWait()

def openFile(fileName , filePath):
    os.startfile(os.path.join(filePath , fileName))

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak(f"Good Morning!")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon!")
    else:
        speak(f"Good Evening!")
    speak("Amaanat Singh")
    
    # openFile("We Are Venom.wav" , "G:\\VSCode Projects\\Venom\\Sounds")
    # time.sleep(3.5)
    # for process in (process for process in psutil.process_iter() if process.name() == "Music.UI.exe"):
    #     process.kill()
    playMusicOnly("G:\\VSCode Projects\\Venom\\Sounds\\We Are Venom.wav")
    time.sleep(3.5)
    speak("World's best AI assistant at your service. How may i help you?")
       
def takeCommand(state = "normal"):
    '''
    It takes voice input and converts it into string and returns this string output
    '''
    command = sr.Recognizer()
    if state == "normal":
        with sr.Microphone() as source:
            print("Listening...")
            command.pause_threshold = 0.8
            command.energy_threshold = 2500
            command.non_speaking_duration = 0.4
            audio = command.listen(source)

            try:
                print("Recognizing...")
                userOrder = command.recognize_google(audio, language='en-in')
                print(f"You said : \n{userOrder}\n")

            except Exception as e:
                speak("Say that again please sir...")
                print("Say that again please sir...")
                return "None"
            # else:
            return userOrder
    elif state == "paused":
        with sr.Microphone() as source:
            command.pause_threshold = 0.8
            command.energy_threshold = 2500
            command.non_speaking_duration = 0.4
            audio = command.listen(source)

            try:
                userOrder = command.recognize_google(audio, language='en-in')
            except Exception as e:
                return "None"
            # else:
            return userOrder

def toPlaySoundWhenMoreThanOneDifferentCommandsGiven(pathOfSounds = "G:\\VSCode Projects\\Venom\\Sounds\\ifMoreThanOneDifferentCommandsGivenInOneUserOrder"):
    
    sounds = os.listdir(pathOfSounds)
    soundNumber = random.randint(0 , len(sounds) - 1)
    playMusicOnly(f"{pathOfSounds}\\{sounds[soundNumber]}")

def VenomLaugh(numberOfTimes = "oneTime" , pathOfSounds = "G:\\VSCode Projects\\Venom\\Sounds\\VenomLaughing"):
    sounds = os.listdir(pathOfSounds)
    soundNumber = random.randint(0 , len(sounds) - 1)
    # os.startfile(os.path.join(pathOfSounds , sounds[soundNumber]))
    # playsound(f"{pathOfSounds}\\{sounds[soundNumber]}")
    pygame.mixer.music.load(f"{pathOfSounds}\\{sounds[soundNumber]}")
    if numberOfTimes == "oneTime":
        TrackObject = pygame.mixer.Sound(f"{pathOfSounds}\\{sounds[soundNumber]}")
        pygame.mixer.music.play()
        time.sleep(float(TrackObject.get_length()))

    elif numberOfTimes == "infiniteTimes":
        while True:
                
            pygame.mixer.music.load(f"{pathOfSounds}\\{sounds[soundNumber]}")
            TrackObject = pygame.mixer.Sound(f"{pathOfSounds}\\{sounds[soundNumber]}")
            pygame.mixer.music.play()
            # time.sleep(float(TrackObject.get_length()))
            userDisturbance = takeCommand("paused").lower()
            # if userDisturbance != "None":
            #     pygame.mixer.music.load("G:\\VSCode Projects\\Venom\\Sounds\\userDisturbance\\Mai Bol Reha Tha Tha Maari Jandi Vich.mp3")
            #     TrackObject = pygame.mixer.Sound("G:\\VSCode Projects\\Venom\\Sounds\\userDisturbance\\Mai Bol Reha Tha Tha Maari Jandi Vich.mp3")
            #     pygame.mixer.music.play()
            #     time.sleep(float(TrackObject.get_length()))
            if "stop" in userDisturbance:
                pygame.mixer.music.stop()
                speak("ok sir as you wish")
                break

def AllAboutToPlayAnyTypeOfSingleMusicUsingUserOrder(userOrder , path_to_keep_all_folders_of_songs = f"G:\\Extra things\\music\\"):
    global numberOfCommandsGiven
    def funcWithInputAsUserOrderAndReturnsIfToPlaySongAndThePathOfTypeOfSong():
        userOrderToPlayTypeOfSongs = userOrder
        pattern = re.compile(r'play(\s\w+){0,8}?( motivational| religious| romantic| study| favourite)?( song| music| songs| musics)')
        matches = pattern.search(userOrderToPlayTypeOfSongs)
        if matches != None:
            if matches.group(2) != None:
                return [True , f"{path_to_keep_all_folders_of_songs}{matches.group(2).strip()} songs"]
            else:
                return [True , f"{path_to_keep_all_folders_of_songs}all songs"]
        else:
            return [False , None] 

    output = funcWithInputAsUserOrderAndReturnsIfToPlaySongAndThePathOfTypeOfSong()

    if output[0] == True:
        numberOfCommandsGiven = numberOfCommandsGiven + 1
        print(f"Path of the song is {output[1]}")
        songs = os.listdir(output[1])
        songNumber = random.randint(0,len(songs) - 1)
        print(f"Sir I am playing {songs[songNumber]}")
        speak(f"Sir I am playing {songs[songNumber]}")
        os.startfile(os.path.join(output[1] , songs[songNumber]))

def wikipediaSearch(userOrder):
    global numberOfCommandsGiven
    # global userOrder
    userOrderForWikipedia = userOrder
    listOfWordsForAccessingWikipedia = ["wikipedia" , "tell me about" , "tell me something about" , "tell me something on" , "tell me" , "tell about" , "give me some details on" , "give me some details" , "give details on" , "give details about" , "tell us about" , "enlighten me" , "put some light on"]
    listOfWordsToDeleteWhileAccessingWikipedia = [ "hey venom " , "hey venam " , "hey when i'm " , "oh venom " , "oh venam " , "oh when i'm " , "hey " , "oh" ,  "ok venom " , "ok venam " ,"ok when you " , "ok when i'm " , "okay venom " , "okay when i'm " , "hey you " , "please " , " so " , "about " , "venom" , "venam"] 
    listOfWordsForAccessingWikipediaInShort = ["in short" , "crisply" , "in a crisp manner" , "in brief" , "briefly"]
    listOfNumberOfLinesOfWikipediaToSay = ["in one line" ,  "in two lines" , "in three lines" , "in four lines" , "in five lines" , "in six lines" , "in seven lines" , "in eight lines" , "in nine lines" , "in ten lines" , "in 1 line" , "in 2 lines" , "in 3 lines" , "in 4 lines" , "in 5 lines" , "in 6 lines" , "in 7 lines" , "in 8 lines" , "in 9 lines" , "in 10 lines" , "in short" , "crisply" , "in a crisp manner" , "in brief" , "briefly"]

    def funcToGetNumberOfSentencesOfWikipedia(word):
        global numberOfCommandsGiven
        nonlocal listOfNumberOfLinesOfWikipediaToSay
        nonlocal listOfWordsForAccessingWikipediaInShort
        if word == listOfNumberOfLinesOfWikipediaToSay[0] or word == listOfNumberOfLinesOfWikipediaToSay[10]:
            return 1
        elif word == listOfNumberOfLinesOfWikipediaToSay[1] or word == listOfNumberOfLinesOfWikipediaToSay[11]:
            return 2
        elif word == listOfNumberOfLinesOfWikipediaToSay[2] or word == listOfNumberOfLinesOfWikipediaToSay[12]:
            return 3
        elif word == listOfNumberOfLinesOfWikipediaToSay[3] or word == listOfNumberOfLinesOfWikipediaToSay[13]:
            return 4
        elif word == listOfNumberOfLinesOfWikipediaToSay[4] or word == listOfNumberOfLinesOfWikipediaToSay[14]:
            return 5
        elif word == listOfNumberOfLinesOfWikipediaToSay[5] or word == listOfNumberOfLinesOfWikipediaToSay[15]:
            return 6
        elif word == listOfNumberOfLinesOfWikipediaToSay[6] or word == listOfNumberOfLinesOfWikipediaToSay[16]:
            return 7
        elif word == listOfNumberOfLinesOfWikipediaToSay[7] or word == listOfNumberOfLinesOfWikipediaToSay[17]:
            return 8
        elif word == listOfNumberOfLinesOfWikipediaToSay[8] or word == listOfNumberOfLinesOfWikipediaToSay[18]:
            return 9
        elif word == listOfNumberOfLinesOfWikipediaToSay[9] or word == listOfNumberOfLinesOfWikipediaToSay[19]:
            return 10
        elif word in listOfWordsForAccessingWikipediaInShort:
            return 1
        
    for word in listOfWordsForAccessingWikipedia:
        if word in userOrderForWikipedia:
            numberOfCommandsGiven = numberOfCommandsGiven + 1
            speak("Searching wikipedia Sir...")
            userOrderForWikipedia = userOrderForWikipedia.replace(word , "")
            for word in listOfWordsToDeleteWhileAccessingWikipedia:
                if word in userOrderForWikipedia:
                    userOrderForWikipedia = " " + userOrderForWikipedia
                    userOrderForWikipedia = userOrderForWikipedia.replace(word , "")
            userOrderForWikipedia = userOrderForWikipedia.lstrip()        
            
            for word in listOfNumberOfLinesOfWikipediaToSay:
                if word in userOrderForWikipedia:
                    userOrderForWikipedia = userOrderForWikipedia.replace(word , "")
                    numberOfSentences = funcToGetNumberOfSentencesOfWikipedia(word)
                    break
                else:
                    numberOfSentences = 3
                
            try:
                results = wikipedia.summary(userOrderForWikipedia , sentences = numberOfSentences)
                print(f"Final search in wikipedia is {userOrderForWikipedia}")
                speak(f"Dear Sir! I searched for {userOrderForWikipedia}")                         
                print(f"According to Wikipedia:\n{results}")                         
                speak("According to wikipedia")
                speak(results)
            except:
                print(f"Sorry Sir , i am unable to find your search on wikipedia. I searched for '{userOrderForWikipedia}'. It may be that i have understood it wrong , Can you please speak again?")
                speak(f"Sorry Sir , i am unable to find your search on wikipedia. I searched for '{userOrderForWikipedia}'. It may be that i have understood it wrong , Can you please speak again?")

def AllAboutOpeningWebsites(userOrder):
    userOrderForOpeningWebsites = userOrder
    
    def checkWebsiteNamesInUserOrderIfAny():
        global listOfWebsitesToOpen

        pattern = re.compile(r'(\w+)(\.\w+)+')
        matches = pattern.finditer(userOrderForOpeningWebsites)

        listOfWebsitesToOpen = []

        for match in matches:
            listOfWebsitesToOpen.append(match.group(0))

    checkWebsiteNamesInUserOrderIfAny()
    
    if len(listOfWebsitesToOpen) > 0:

        def openWebsite(listOfWebsitesToOpen):
            global numberOfCommandsGiven
            for WebsiteName in listOfWebsitesToOpen:
                listOfWordsToOpenAWebsite = [f"{i} {WebsiteName}" for i in ["start" , "open" , "and" , "load" , "start the" , "open the" , "and the" , "load the"]]
                NumberOfWebsitesOpened = 0
                for word in listOfWordsToOpenAWebsite:
                    if word in userOrderForOpeningWebsites:
                        numberOfCommandsGiven = numberOfCommandsGiven + 1
                        if NumberOfWebsitesOpened == 0:
                            print(f"List of websites to open: {listOfWebsitesToOpen}")
                        NumberOfWebsitesOpened = NumberOfWebsitesOpened + 1
                        print(f"Opening {WebsiteName}")
                        speak(f"Opening {WebsiteName}")
                        webbrowser.open(WebsiteName)
                        break

        openWebsite(listOfWebsitesToOpen)

def AllAboutJoiningAGoogleMeetInVenom(userOrder):

    if "join" in userOrder or "start" in userOrder and "meeting" in userOrder:
        pathOftry2 = "G:\\VSCode Projects\\Venom\\try2.py"
        try2 = CallPy(pathOftry2)
        try2.call_python_file()

def AllAboutVenomLaugh(userOrder):
    if "start" in userOrder and "laugh" in userOrder:
        speak("Sir I am starting laughing now")
        VenomLaugh("infiniteTimes")

    elif "laugh" in userOrder and ("venom" in userOrder or "venam" in userOrder or "when i'm" in userOrder):
        speak("Sir I am laughing now")
        VenomLaugh("oneTime")
    
def generalCommunication(query):

    def replyToWhoAreYou():
        playMusicOnly("G:\\VSCode Projects\\Venom\\Sounds\\I Am Venom.mp3")
        time.sleep(5)

    def replyToHowAreYou():
        replies = ["doing well sir" , "i'm fine sir , what about you?" , "not bad!"]
        speak(replies[random.randint(0 , len(replies) - 1)])

    def replyToHello():
        speak("Hello")
        playMusicOnly("G:\\VSCode Projects\\Venom\\Sounds\\We Are Venom.wav")
        print("I am Venom and you are mine")
        time.sleep(3.5)

    def replyToCussWords():
        pathOfSounds = "G:\\VSCode Projects\\Venom\\Sounds\\replyToCussWords"
        sounds = os.listdir(pathOfSounds)
        soundNumber = random.randint(0,len(sounds) - 1)
        playMusicOnly(f"{pathOfSounds}\\{sounds[soundNumber]}")

    def replyToPraise():
        speak("Thank You Sir! I owe everything that I have to my developer 'Amaanat Singh'")

    global userOrder    

    if "f***" in query or "what the hell" in query or "madarchod" in query or "bhosdi " in query or "chutiye" in query or "son of a bitch" in query or "saala " in query or "s*************" in query or "harami" in query or "haramzada" in query or "cuss me" in query or "abuse me" in query or ("how" in query and ("abuse" in query or "cuss" in query)) or ("kutta" in userOrder and "kmina" in userOrder): 
        replyToCussWords()
        userOrder = "None"
    elif "how are you" in query:
        replyToHowAreYou()
        userOrder = "None"
    elif "hello" in query:
        replyToHello()
        userOrder = "None"
    elif ("who" in query and "are you" in query) or (("tum" in query or "aap" in query) and ("kaun ho" in query)) :
        replyToWhoAreYou()
        userOrder = "None"
    elif "you are doing good" in query or "well done" in query or "good job" in query:
        replyToPraise()
        userOrder = "None"
    
if __name__ == "__main__":
    speak("Good morning ")
    # wishMe()

    while True:
        numberOfCommandsGiven = 0
        differentCommandsGivenSoundPlayed = False
        toBreak = False
        userOrder = takeCommand().lower()
        # userOrder = "venom laugh"
        userOrderForJoiningMeet = userOrder
        with open("userOrderForJoiningMeet.txt" , 'w') as textFileObject:
            textFileObject.write(userOrderForJoiningMeet)
        '''
        Now further code for executing tasks based on user's orders
        '''

        generalCommunication(userOrder)
        wikipediaSearch(userOrder)
        AllAboutOpeningWebsites(userOrder)
        AllAboutToPlayAnyTypeOfSingleMusicUsingUserOrder(userOrder)
        AllAboutJoiningAGoogleMeetInVenom(userOrder)
        AllAboutVenomLaugh(userOrder)
        
        if "pause" in userOrder or "stop for now" in userOrder:
            pygame.mixer.music.stop()
            print("Ok sir I am pausing now. You can wake me up by saying \"ok Venom\" or \"Wake up Venom\"")
            speak("Ok sir I am pausing now. You can wake me up by saying \"ok Venom\" or \"Wake up Venom\"")
            numberOfCommandsGiven = numberOfCommandsGiven + 1
            while True:
                userOrderWhilePaused = takeCommand("paused").lower()
                # wordsToWake = ["venom" , "venam" , "when i'm"]
                if ("venom" in userOrderWhilePaused or "venam" in userOrderWhilePaused or "when i'm" in userOrderWhilePaused) and ("wake" in userOrderWhilePaused or "ok" in userOrderWhilePaused or "okay" in userOrderWhilePaused):
                    print("At your service sir")
                    speak("At your service sir")
                    break

        else:
            listOfWordsToQuitVenom = ["venom quit", "venom exit", "venom stop", "venam quit", "venam exit", "venam stop", "ruk ja", "bro stop" , "quit now" , "exit now" , "stop now" , "when i'm stop" , "when i'm exit" , "when i'm quit" , "chup kar ja" , "band ho ja" , "you may leave now" , "now you may leave" , "you may leave" , "please go away" , "go away venom" , "go away venam" , "go away when i'm" , "go away now" , "now go away"]  

            for word in listOfWordsToQuitVenom:
                if word in userOrder:
                    toBreak = True
                    break
            if toBreak == True:
                print("Okay Sir As you wish ,I am stopping now. Good Bye Sir!!")
                speak("Okay Sir As you wish ,I am stopping now. Good Bye Sir!!")
                numberOfCommandsGiven = numberOfCommandsGiven + 1
                break

    