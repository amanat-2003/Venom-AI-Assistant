import pyttsx3
from soupsieve import match
import speech_recognition as sr
import webbrowser
import re
import os 
from time import sleep
import pyautogui as auto
import schedule
from playsound import playsound
import re
from Venom import speak
from Venom import takeCommand
# from meetautomatetest import joinmeetonly
# from meetautomatetest import JoinScheduledMeeting
import sys



engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def speak(toSpeak):
    '''
    speaks the toSpeak argument
    '''
    engine.say(toSpeak)
    engine.runAndWait()


startMeetFunc = False
endMeetFunc = False

def joinmeetonly(link):
    global startMeetFunc
    webbrowser.open_new_tab(link)
    sleep(10)
    auto.hotkey('ctrl' , 'd')
    auto.hotkey('ctrl' , 'e')
    auto.click(992,404)


def JoinScheduledMeeting(link , timeToStart):
    try:
        def joinMeet():
            global startMeetFunc
            webbrowser.open_new_tab(link)
            sleep(7)
            auto.hotkey('ctrl' , 'd')
            auto.hotkey('ctrl' , 'e')
            auto.click(992,404)
            startMeetFunc = True

        schedule.every().day.at(timeToStart).do(joinMeet)
        print(f"Sir the meeting has been scheduled to run")
        speak(f"Sir the meeting has been scheduled to run")
        while True:
            schedule.run_pending()
            sleep(1)
            if startMeetFunc == True:
                break
    except Exception as exc:
        print(exc)



def AllAboutJoiningAGoogleMeet(userOrder):

    # if "join" in userOrder or "start" in userOrder and "meeting" in userOrder:
    def AskForLink():
        
        try:
            speak("Sir please type the meeting link: ")
            link = input("Sir please type the meeting link: ")
            pattern = re.compile(r'\w{3}-\w{4}-\w{3}')
            matches = pattern.search(link)
            if matches != None:
                linkFinal = f"https://meet.google.com/{matches.group(0)}"
                speak("Success! link has been processed")
                return linkFinal
            else:
                speak("Sir you have typed an invalid link")
                AskForLink()
        except Exception as exc:
            speak("May be due to a problem Sir you have to again enter the meeting link. Sorry for the inconvenience sir")
            AskForLink()

    link = AskForLink()

    if "now" in userOrder:
        joinmeetonly(link)
        speak("The meeting has been joined")
    else:
        def AskForStartingTime():
            global timeToStart
            global finalStartingTime
            try:
                finalStartingTime = None
                print(f"Sir please tell when to start the meeting: ")
                speak(f"Sir please tell when to start the meeting: ")
                timeInput = takeCommand().lower()
                if "now" in timeInput or "instantly" in timeInput:
                    joinmeetonly(link)
                else:
                    pattern = re.compile(r'(\d{1,2}):?\s?(\d{1,2})?\s?(a.m.|p.m.|pm|am)?')
                    matches = pattern.search(timeInput)

                    if matches != None:
                        hours = matches.group(1)
                        minutes = matches.group(2)
                        amOrpm = matches.group(3)
                        if amOrpm == "p.m." or amOrpm == "pm":
                            if minutes == None:
                                if int(hours) >= 0 and int(hours) <= 12:
                                    finalStartingTime = f"{12 + int(hours)}:00"
                            elif int(minutes) >= 0 and int(minutes) < 60:
                                if int(hours) >= 0 and int(hours) <= 12:
                                    finalStartingTime = f"{12 + int(hours)}:{minutes}"
                        elif amOrpm == "a.m." or amOrpm == "am":
                            if minutes == None:
                                if int(hours) >= 0 and int(hours) <= 9:
                                    finalStartingTime = f"0{hours}:00"
                                elif int(hours) >= 10 and int(hours) <= 12:
                                    finalStartingTime = f"{hours}:00"
                            elif int(minutes) >= 0 and int(minutes) < 60:
                                if int(hours) >= 0 and int(hours) <= 9:
                                    finalStartingTime = f"0{hours}:{minutes}"
                                elif int(hours) >= 10 and int(hours) <= 12:
                                    finalStartingTime = f"{hours}:{int(minutes)}"
                        elif amOrpm == None:
                            if int(hours) >= 0 and int(hours) <= 9: 
                                if minutes == None:
                                    finalStartingTime = f"0{hours}:00"
                                elif int(minutes) >= 0 and int(minutes) < 60:
                                    finalStartingTime = f"0{hours}:{minutes}"
                            elif int(hours) >= 10 and int(hours) <= 23: 
                                if minutes == None:
                                    finalStartingTime = f"{hours}:00"
                                elif int(minutes) >= 0 and int(minutes) < 60:
                                    finalStartingTime = f"{hours}:{minutes}"
                        if finalStartingTime != None:
                            # timeToStart = finalStartingTime
                            # JoinScheduledMeeting(link , timeToStart)
                            return finalStartingTime
                        elif finalStartingTime == None:
                            speak("Sir you have spoke an invalid time.")
                            AskForStartingTime()
                    else:
                        speak("Sir you have spoke an invalid time.")
                        AskForStartingTime()

            except Exception as exc:
                speak(f"May be due to a problem Sir you have to again enter the starting time. Sorry for the inconvenience sir")
                AskForStartingTime()                     
        AskForStartingTime()
        if finalStartingTime != None:
            timeToStart = finalStartingTime
            JoinScheduledMeeting(link , timeToStart)
            print("Sir I have asked the host to let you in the meeting")
            speak("Sir I have asked the host to let you in the meeting")


with open("userOrderForJoiningMeet.txt" , 'r') as textFileObject:
    userOrderForJoiningMeet = textFileObject.read()
try:
    AllAboutJoiningAGoogleMeet(userOrderForJoiningMeet)
finally:
    # This block is crucial to avoid having issues with
    # Python spitting non-sense thread exceptions. We have already
    # handled what we could, so close stderr and stdout.
    if not os.environ.get('CEPH_DEPLOY_TEST'):
        try:
            sys.stdout.close()
        except:
            pass
        try:
            sys.stderr.close()
        except:
            pass
