import sys
import pjsua as pj
import threading
import bothelper as bot
import time

current_call = None
recorderid = None
playerid = None
call_slot = None

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

	current_call.answer(180)
	# Hold ringing tone for 3 seconds
	time.sleep(3)
	current_call.answer(200)
	print "@"*20
    
	dir(current_call)
	time.sleep(2)
	current_call.dial_dtmf("1")
	# Listen to user and respond
	listen_and_respond()
#import datetime
def listen_and_respond():
    recorderid = lib.create_recorder("/home/admin1/Desktop/dev/VoIPBot/src/input.wav")
    recorderslot = lib.recorder_get_slot(recorderid)

    # Connect sound device to wav record file
    lib.conf_connect(0, recorderslot)
    lib.conf_connect(call_slot, recorderslot)
    signal_while_active_call = []
    while True:
        time.sleep(0.1)
#        lib.on_dtmf_digit()
#        choice = sys.stdin.readline()
#        print choice
        signal_while_active_call.append(lib.conf_get_signal_level(recorderslot))
        print signal_while_active_call[-100:] < [(0.01,0.01) for x in range(100)]
#        print signal_while_active_call[-100:] , [(0.01,0.01) for x in range(100)]
        if signal_while_active_call[-100:] < [(0.01,0.01) for x in range(100)]:
            break

    print "#"*80
#    while True:
#        time.sleep(2)    
#        with open("/home/admin1/Desktop/dev/VoIPBot/src/input.wav" ,'r') as f:
#            print f.readlines()
#            with open("/home/admin1/Desktop/dev/VoIPBot/src/input1.wav")
    lib.recorder_destroy(recorderid)
    mybot = bot.BotHelper()
    mybot.generate_response()

    # Play wav file back to user

    #playerid = lib.create_player("/home/admin1/Desktop/dev/VoIPBot/src/39846769.wav",loop=False)
    playerid = lib.create_player("/home/admin1/Desktop/dev/VoIPBot/src/botresponse.wav",loop=False)
    playerslot = lib.player_get_slot(playerid)
    # Connect the audio player to the call
    lib.conf_connect(playerslot,call_slot)

	# Wait for the thing to be read for a few seconds then hang up
    time.sleep(13)
    
    

    current_call.hangup()
    

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
    acc = lib.create_account(pj.AccountConfig("192.168.0.201", "7003", "123"))

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
