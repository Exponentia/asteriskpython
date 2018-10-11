#[internal]
#exten => s,1,Answer()
#exten => s,n,PlayBack(custom-draalincom)
#exten => s,n,PlayBack(custom-menuoptions)
#
#exten => s,n,Background(vm-press)
#exten => s,n,Background(digits/1)
#exten => s,n,Background(vm-for)
#exten => s,n,Background(custom-work)
#
#exten => s,n,Background(vm-press)
#exten => s,n,Background(digits/2)
#exten => s,n,Background(vm-for)
#exten => s,n,Background(custom-cell)
#
#exten => s,n,Background(vm-press)
#exten => s,n,Background(digits/3)
#exten => s,n,Background(vm-for)
#exten => s,n,Background(custom-home)
#
#exten => s,n,WaitExten()
#
#exten => 1,1,Dial(SIP/7001,60)
#exten => 2,1,Dial(SIP/9053338888@voipms)
#exten => 3,1,Dial(SIP/9054447777@voipms)
#
#exten => 7001,1,Answer()	      
#exten => 7001,2,Dial(SIP/7001,60)	
#exten => 7001,3,Playback(vm-nobodyavail)  
#exten => 7001,4,VoiceMail(7001@main)
#exten => 7001,5,Hangup()       
#
#exten => 7002,1,Answer()
#exten => 7002,2,Dial(SIP/7002,60)      
#exten => 7002,3,Playback(vm-nobodyavail) 
#exten => 7002,4,VoiceMail(7002@main)
#exten => 7002,5,Hangup()                
#
#exten => 8001,1,VoicemailMain(7001@main)
#exten => 8001,2,Hangup()
#
#exten => 8002,1,VoicemailMain(7002@main)
#exten => 8002,2,Hangup()
#
#include => voipms-inbound
#include => voipms-outbound
#
#[voipms-outbound]
#exten => _1NXXNXXXXXX,1,Dial(SIP/${EXTEN}@voipms)
#exten => _1NXXNXXXXXX,n,Hangup()
#exten => _NXXNXXXXXX,1,Dial(SIP/1${EXTEN}@voipms)
#exten => _NXXNXXXXXX,n,Hangup()
#exten => _011.,1,Dial(SIP/${EXTEN}@voipms)
#exten => _011.,n,Hangup()
#exten => _00.,1,Dial(SIP/${EXTEN}@voipms)
#exten => _00.,n,Hangup()
#
#[voipms-inbound]
#exten => 2892229999,1,Answer()

#for i in range(10,16):
#    print "exten => 70{},1,Answer()\nexten => 70{},2,Dial(SIP/70{},60)\nexten => 70{},3,Playback(vm-nobodyavail) \nexten => 70{},4,VoiceMail(70{}@main)\nexten => 70{},5,Hangup()\n\n".format(i,i,i,i,i,i,i)
    
for i in range(10,16):
    print "exten => 80{},1,VoicemailMain(70{}@main)\nexten => 80{},2,Hangup()\n\n".format(i,i,i)
    