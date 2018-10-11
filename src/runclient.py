import sys
import pjsua as pj
import threading
import bothelper as bot
import time 
import time
import bing_speach
import sys

current_call = None
recorderid = None
playerid = None
call_slot = None
dt=[]
#userid = sys.argv[1]


verify = 0
ip = "13.71.90.171"
#ip = "192.168.0.165"
#ip = "192.168.43.173"
#ip = "ethotic.cc.ownpages.com"
def log_cb(level, str, len):
    print str,

class MyAccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account):
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()

    def on_incoming_call(self, call):
	global current_call
	if current_call:
	    call.answer(486, "Busy")
	    return

	print "Incoming call from ", call.info().remote_uri
	
	current_call = call

	call_cb = MyCallCallback(current_call)
	current_call.set_callback(call_cb)
#	call.transfer('sip:7002 at 192.168.0.204')
	current_call.answer(180)
	# Hold ringing tone for 3 seconds
#	time.sleep(3)
	current_call.answer(200)    
	dir(current_call)
	time.sleep(2)
	# Listen to user and respond
	listen_and_respond()
#import datetime
import os
import soundfile as sf
import response_checking
import aws_polly
def listen_and_respond():
    global current_call
    aws_polly.text_to_voice("Good Evening... My name is Singularity.... and this is a verification call on behalf of HDFC Life for your Secure your life plan..., purchased from HDFC Bank recently. May I speak to... Ankur Jyoti please","Raveena")
#    aws_polly.text_to_voice("Good Evening","Raveena")
    play_recording("output.wav",call_slot)
#    try:
#        text = recorder(call_slot)
#        print "#"*20
#        print text
#        reply = response_checking.text_got(text)
#        print reply,"%"*20
#    except:
#        reply = None
    text = recorder(call_slot)
    print text
    reply = response_checking.text_got(text)
    
    print reply
    print "11"*10
    if reply == "1":
        nextquestion(call_slot)
    elif reply == "2":
        end_the_call(call_slot)
    else:
        get_dtmf_answer(call_slot)
    current_call.hangup()
    current_call =None
    
def play_recording(Audiofile,call_slot):
    playerid = lib.create_player(Audiofile,loop=False)
    playerslot = lib.player_get_slot(playerid)
    f = sf.SoundFile(Audiofile)
    # Connect the audio player to the call
    lib.conf_connect(playerslot,call_slot)
    time.sleep((int(len(f) / f.samplerate))+2)    
    
def nextquestion(call_slot):
    aws_polly.text_to_voice("Ankur jyoti,  we are happy to welcome you to the HDFC Life family...Sir..., please note this call may be recorded for our internal quality and training purposes.,For security purpose, please confirm your Date of Birth","Raveena")
    play_recording("output.wav",call_slot)
#    aws_polly.text_to_voice("Sir..., please note this call may be recorded for our internal quality and training purposes.,","Raveena")
#    play_recording("output.wav",call_slot)
#    aws_polly.text_to_voice("For security purpose, please confirm your Date of Birth","Raveena")
#    play_recording("output.wav",call_slot)
    try:
        text = recorder(call_slot)
        answer = response_checking.dob(text)
    except:
        answer = None
    print answer
    if answer == "1":
         verified_phone(call_slot)
#        aws_polly.text_to_voice("Sir.., please also confirm your mailing address with the pin code.","Raveena")
#        play_recording("output.wav",call_slot)#        next_question(call_slot)
#        text = recorder(call_slot)
#        answer = response_checking.dob(text)
    elif answer == "2":
        verify_dob_year(call_slot)
    elif answer == "3":
        verify_dob_month(call_slot)
    else:
        repeat_dob(call_slot)
#        aws_polly.text_to_voice("I am sorry, i didn't get that. Please use your phone touch pad and enter your date of birth. For example, if your date of birth is 31st August 1986 then press 3... 1... 0... 8... 1... 9... 8... 6... ","Raveena")
#        play_recording("output.wav",call_slot)#        next_question(call_slot)
#        sorry_intent(call_slot)
#        get_dob_dtmf(call_slot)
def repeat_dob(call_slot):
    aws_polly.text_to_voice("I am sorry can you repeat again","Raveena")
    play_recording("output.wav",call_slot)
    try:
        text = recorder(call_slot)
        answer = response_checking.dob(text)
    except:
        answer = None
    print answer
    if answer == "1":
         verified_phone(call_slot)
#        aws_polly.text_to_voice("Sir.., please also confirm your mailing address with the pin code.","Raveena")
#        play_recording("output.wav",call_slot)#        next_question(call_slot)
#        text = recorder(call_slot)
#        answer = response_checking.dob(text)
    elif answer == "2":
        verify_dob_year(call_slot)
    elif answer == "3":
        verify_dob_month(call_slot)
    else:
        aws_polly.text_to_voice("I am sorry, i didn't get that. Please use your phone touch pad and enter your date of birth. For example, if your date of birth is 31st August 1986 then press 3... 1... 0... 8... 1... 9... 8... 6... ","Raveena")
        play_recording("output.wav",call_slot)#        next_question(call_slot)
#        sorry_intent(call_slot)
        get_dob_dtmf(call_slot)        
def verify_dob_month(call_slot):
    aws_polly.text_to_voice("I am sorry, i didn't get the month. Which month were you born in?","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    try:
        text = recorder(call_slot)
        answer = response_checking.take_dob_month(text)
    except:
        answer = None
    if answer == "1":
        verified_phone(call_slot)
    else:
        aws_polly.text_to_voice("I am sorry, i didn't get that. Please use your phone touch pad and enter your birth month if you birth month is august then press 0.. 8..","Raveena")
        play_recording("output.wav",call_slot)#        next_question(call_slot)
#        sorry_intent(call_slot)
        get_dob_month_dtmf(call_slot)
def verify_dob_year(call_slot):
    aws_polly.text_to_voice("I am sorry, i didn't get the year. Which year were you born in?","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    try:
        text = recorder(call_slot)
        answer = response_checking.take_dob_year(text)
    except:
        answer = None
    if answer == "1":
        verified_phone(call_slot)
    else:
        aws_polly.text_to_voice("I am sorry, i didn't get that. Please use your phone touch pad and enter your date of birth. For example, if your date of birth is 31st August 1986 then press 3... 1... 0... 8... 1... 9... 8... 6... ","Raveena")
        play_recording("output.wav",call_slot)#        next_question(call_slot)
#        sorry_intent(call_slot)
        get_dob_dtmf(call_slot)
def end_the_call(call_slot):
    aws_polly.text_to_voice("What is the best time to speak to him","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    try:
        answer = recorder(call_slot)
        print answer
    except:
        aws_polly.text_to_voice("I am sorry, i didn't get that Please repeat that","Raveena")
        play_recording("output.wav",call_slot)#        next_question(call_slot)
        try:
            answer = recorder(call_slot)
            print answer
        except:
            saleguywillcallback(call_slot)
    play_recording("./voice/thanksyoucallbacklater.wav",call_slot)

def recorder(call_slot):
    print "recording started"
    recorderid = lib.create_recorder("/home/admin1/Desktop/dev/VoIPBot/src/input.wav")
    recorderslot = lib.recorder_get_slot(recorderid)

    # Connect sound device to wav record file
    lib.conf_connect(0, recorderslot)
    lib.conf_connect(call_slot, recorderslot)
    signal_while_active_call = []
    signal = 0
    timestamp1 = time.time()
    while signal < 15:
        time.sleep(0.1)
        print lib.conf_get_signal_level(recorderslot)
#        if time.time()-timestamp1>=4:
#            aws_polly.text_to_voice("I am sorry, i didn't heard anything","Raveena")
#            play_recording("output.wav",call_slot)#        next_question(call_slot)
#            #lib.recorder_destroy(recorderid)
            #recorder(call_slot)
#        print lib.conf_get_signal_level(recorderslot)[0] > 0.1
        if lib.conf_get_signal_level(recorderslot)[0]>0.12:
            tone = True
            signal +=1
            break
    lower_flag=0
    increament=0
    while tone:            
        time.sleep(0.1)
        if lib.conf_get_signal_level(recorderslot)[0]<0.12:
            print increament, lib.conf_get_signal_level(recorderslot)
            increament=increament+1
            if increament>20:
                break
        else:
            increament=0
#        signal_while_active_call.append(lib.conf_get_signal_level(recorderslot))
#        print signal_while_active_call[-100:] < [(0.1,0.00) for x in range(100)]

#        new_list = []
#        for x in range(100):
#            new_list.append((0.1,0.0))
#        print signal_while_active_call[-20:]
#        if signal_while_active_call[-100:] < new_list:
#            signal_while_active_call = []
#            break

    print "#"*80
    lib.recorder_destroy(recorderid)
    mybot =bing_speach.handler()
    answer = mybot
#    mybot = bot.BotHelper()
#    answer = mybot.generate_response()
    print answer,"form recorder"
    return answer

def get_dob_month_dtmf(call_slot):
    global dt
    print dt
    while True:
        if len(dt) >= 2:
            break
        print dt
    dob = "".join(str(x) for x in dt)
    print dob,"$ richie rich"
    print type(dob)
    if dob=="08":
        dt=[]
        verified_phone(call_slot)
    else:
        dt=[]
        unverified_dob(call_slot)
def get_dob_year_dtmf(call_slot):
    global dt
    print dt
    while True:
        if len(dt) >= 4:
            break
        print dt
    dob = "".join(str(x) for x in dt)
    print dob,"$ richie rich"
    print type(dob)
    if dob=="1986":
        dt=[]
        verified_phone(call_slot)
    else:
        dt=[]
        unverified_dob(call_slot)

def get_dob_dtmf(call_slot):
    global dt
    print dt
    while True:
        if len(dt) >= 8:
            break
        print dt
    dob = "".join(str(x) for x in dt)
    print dob,"$ richie rich"
    print type(dob)
    if dob=="31081986":
        dt=[]
        verified_phone(call_slot)
    else:
        unverified_dob(call_slot)

#def verified_dob(call_slot):
#    play_recording("./voice/address.wav",call_slot)
#    answer = recorder(call_slot)
#    print answer
#    if answer == "yes":
#        verified_phone(call_slot)
#    else:
#        unverified_address(call_slot)
def verified_phone(call_slot):
    aws_polly.text_to_voice("Sir.., please also confirm your phone number.","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    try:
        text = recorder(call_slot)
        answer = response_checking.phonenumber(text)
    except:
        answer = None
    if answer == "1":
        verify_email(call_slot)
    else:
        get_dtmf_phone(call_slot)
#        play_recording("./voice/unabletoverify.wav")

def verify_email(call_slot):
    global verify
    if verify < 1:
        aws_polly.text_to_voice("Sir.., please confirm your email address for example if your email address is info@gmail.com, then say india. november. foxtort, oscar at gmail dot com.","Raveena")
        play_recording("output.wav",call_slot)#        next_question(call_slot)
        try:
            text = recorder(call_slot)
            answer = response_checking.email(text)
        except:
            answer = None
        if answer == "1":
            verified_everything(call_slot)
        else:
            aws_polly.text_to_voice("I didn't get that , please try again","Raveena")
            play_recording("output.wav",call_slot)#        next_question(call_slot)
            #verify_email(call_slot)
            try:
                text = recorder(call_slot)
                answer = response_checking.email(text)
            except:
                answer = None
            if answer == "1":
                verified_everything(call_slot)                
                verify += 1
            else:
                aws_polly.text_to_voice("I am sorry, I am unable to verify","Raveena")
                play_recording("output.wav",call_slot)#        next_question(call_slot)
                saleguywillcallback(call_slot)        
    else:
        aws_polly.text_to_voice("I am sorry, I am unable to verify","Raveena")
        play_recording("output.wav",call_slot)#        next_question(call_slot)
        saleguywillcallback(call_slot)        
def verified_everything(call_slot):
    aws_polly.text_to_voice("The premium amount is INR 20,000 which you need to pay for 10 years. The next premium will be due after every 3 months from the policy issue date. We request you to pay the premium for the entire term. In absence of same fund value may impact due to charges applicable.","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    aws_polly.text_to_voice("Sir, I would also like to inform you that life insurance is a stand alone product and is neither a fixed deposit nor loan nor is it linked to any other banking products. to confirm the policy say, I agree... else no","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    try:
        text = recorder(call_slot)
        answer = response_checking.agree(text)
    except:
        answer = None
    if answer == "1":
        thankyouintent(call_slot)
    elif answer == "2":
        saleguywillcallback(call_slot)
    else:
        get_dtmf_confirmation(call_slot)
def get_dtmf_confirmation(call_slot):
#    def get_dtmf_answer(call_slot):
    global dt
    aws_polly.text_to_voice("Please press 1 for yes and press 2 for no or to speak to a representative press 0","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
#    print dt
    while True:
        if len(dt) >= 1:
            break
        print dt
    if dt[0] == "1":
        dt =[]
        thankyouintent(call_slot)
    elif dt[0] == "2":
        dt = []
        saleguywillcallback(call_slot)
    elif dt[0] == "0":
        dt=[]
        transfer_to_agent()
def thankyouintent(call_slot):
    aws_polly.text_to_voice("Sir, We take your agreements to the terms of the policy and verification is completed. Thank you for your valuable time. Have a great day","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    global current_call
    current_call.hangup()
    resetAll()
def saleguywillcallback(call_slot):
    aws_polly.text_to_voice("One of our sale representative will call back to resolve your query , Thank you have a great day","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    global current_call
    current_call.hangup()
    resetAll()
    
def unverified_address(call_slot):
    play_recording("./voice/unabletoverify.wav",call_slot)

def unverified_dob(call_slot):
    play_recording("./voice/invaliddob.wav",call_slot)
    saleguywillcallback(call_slot)
def transfer_to_agent():
    global current_call
    global ip
    current_call.transfer("sip:7003@"+ip)
def get_dtmf_phone(call_slot):
    global dt
    aws_polly.text_to_voice("I am sorry, Please use your phone touch pad and enter your 10 digits phone number","Raveena")
    play_recording("output.wav",call_slot)#        next_question(call_slot)
    while True:
        if len(dt) >= 10:
            break
        print dt
    phone = "".join(str(x) for x in dt)
    if phone=="9920482274":
        dt = []
        verify_email(call_slot)
    else:
        unverified_phone(call_slot)
def unverified_phone(call_slot):
    pass
def get_dtmf_answer(call_slot):
    global dt
    play_recording("./voice/Option.wav",call_slot)
    time.sleep(3)    
#    print dt
    while True:
        if len(dt) >= 1:
            break
        print dt
    if dt[0] == "1":
        dt =[]
        nextquestion(call_slot)
    elif dt[0] == "2":
        dt = []
        end_the_call(call_slot)
    elif dt[0] == "0":
        dt=[]
        transfer_to_agent()
    
class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
	pj.CallCallback.__init__(self,call)

    def on_state(self):
		global current_call
#		import
		print "Call with", self.call.info().remote_uri,
		print "is", self.call.info().state_text,
		print "last code = ", self.call.info().last_code,
		print "(" + self.call.info().last_reason + ")"

		if self.call.info().state == pj.CallState.DISCONNECTED:
			resetAll()
			print 'Current call is', current_call
    def onDtmfDigit(self,prm):
        print prm
    def on_dtmf_digit(self, digits):
        #print "hello"
        global dt
        print digits
        dt.append(digits)
        #self.sHelper.dtmf_queue = self.sHelper.dtmf_queue + digits
        #self.sHelper.send_dtmf(digits)
        print "received"
    def on_media_state(self):
		global speech_rec
		global recorderid
		global playerid
		global call_slot
		if self.call.info().media_state == pj.MediaState.ACTIVE:
			# connect call to sound device
			call_slot = self.call.info().conf_slot
			pj.Lib.instance().conf_connect(call_slot, 0)
			pj.Lib.instance().conf_connect(0, call_slot)
			lib.set_snd_dev(0, 0)
			print "Media is now active"

		else:
			playerslot = lib.player_get_slot(playerid)
			lib.conf_disconnect(playerslot,0)
			lib.conf_disconnect(0, recorderslot)
			lib.conf_disconnect(call_slot, recorderslot)
			print "Media is inactive"

def resetAll():
	current_call = None
	recorderid = None
	playerid = None
	call_slot = None

lib = pj.Lib()

try:
    mediaconfig = pj.MediaConfig()
    mediaconfig.no_vad = False
    print '@'*20
    print mediaconfig.no_vad
#    import pdb
#    pdb.set_trace()
    mediaconfig.quality = 10
    lib.init(log_cfg = pj.LogConfig(level=4, callback=log_cb),media_cfg = mediaconfig)
    transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig())
    lib.start()

	# Put your sIP client credentials here
    acc = lib.create_account(pj.AccountConfig(ip, "9002", "123"))

    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    print "\n"
    print "Registration complete, status=", acc.info().reg_status, \
          "(" + acc.info().reg_reason + ")"
    
    if len(sys.argv) > 1:
        lck = lib.auto_lock()

    my_sip_uri = "sip:" + transport.info().host + \
		 ":" + str(transport.info().port)

    # Menu loop
    while True:
        print "My SIP URI is", my_sip_uri
        print "Menu: h=hangup call, q=quit"

        input = sys.stdin.readline().rstrip("\r\n")

        if input == "h":
            if not current_call:
                print "There is no call"
                continue
                  
            current_call.hangup()
            resetAll()

        elif input == "q":
            break

    # shutdown the library
    transport = None

    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None
