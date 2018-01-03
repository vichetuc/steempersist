#!/usr/bin/python3
from steempersist import SteemPersist
import mycredentials
from steemutils import must_vote
import steem
import syslog

class PayBots:
    def __init__(self,persistent):
        self.persistent = persistent
    def transfer(self,time,event):
        urlstart = "https://steemit.com/"
        memo = event["memo"]
        if urlstart in memo:
            bot = event["to"]
            if self.persistent["paybot"][bot] == None:
                self.persistent["paybot"][bot] = 0
            self.persistent["paybot"][bot] = self.persistent["paybot"][bot] + 1
            postlink = memo[len(urlstart):].split()[0]
            postlink = postlink.split("/",1)[1]
            if must_vote(mycredentials.account,9800):
                syslog.syslog("Downvoting "+postlink+ " because of "+ bot + "paybot usage")
                stm=steem.Steem([],keys=mycredentials.keys)
                try:
                    stm.vote(postlink,-7.0,mycredentials.account)
                except:
                    syslog.syslog("Failed to downvote. Possibly too low percentage set for downvoting.")
            else:
                syslog.syslog("NOT flagging '"+event["from"]+ "' for '"+ bot + "' paybot usage.")

sp = SteemPersist("paybothater")  
pb = PayBots(sp)
sp.set_handlers(pb)
sp()
