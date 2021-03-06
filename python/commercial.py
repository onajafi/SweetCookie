import sqlite3
from inits import bot,feedBack_target_chat

def broadcast_POST(message):
    if(message.chat.id == feedBack_target_chat):
        with sqlite3.connect("../users.sqlite") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            DB_table = cur.fetchall()
            print DB_table
            success = 0
            crashes = 0
            for elem in DB_table:
                try:
                    print bot.forward_message(elem[0],message.chat.id,message.json[u'message_id'])
                    success = success + 1
                except:
                    print '--------'
                    crashes = crashes + 1
                    # traceback.print_exc()
                    try:# Added this to make sure every thing is running as smooth as possible
                        bot.send_message(feedBack_target_chat,"This guy blocked the bot:\n" +
                                         str(elem[2]) + "\n" +
                                         str(elem[3]) + "\n" +
                                         str(elem[0])) #remove this markup after the first announcement
                    except:
                        pass

            bot.send_message(feedBack_target_chat,"Finished the announcement\nPassed: " +
                             str(success)+
                             "\nFailed: "+
                             str(crashes))


def erase_last_30_MSGs(userID):
    if (userID == feedBack_target_chat):
        with sqlite3.connect("../users.sqlite") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            DB_table = cur.fetchall()
            print DB_table
            success = 0
            crashes = 0
            for elem in DB_table:
                try:
                    tempMSG = bot.send_message(elem[0],"test",disable_notification=True)
                    MSGnum = tempMSG.json[u'message_id']
                    i = 0
                    while(i < 30):
                        try:
                            bot.delete_message(elem[0], MSGnum - i)
                        except:
                            pass
                        i += 1
                        if(i==1):
                            success = success + 1
                except:
                    print '--------'
                    crashes = crashes + 1
                    # traceback.print_exc()
                    try:  # Added this to make sure every thing is running as smooth as possible
                        bot.send_message(feedBack_target_chat, "This guy blocked the bot:\n" +
                                         str(elem[2]) + "\n" +
                                         str(elem[3]) + "\n" +
                                         str(elem[0]))  # remove this markup after the first announcement
                    except:
                        pass

            bot.send_message(feedBack_target_chat, "Finished the announcement\nPassed: " +
                             str(success) +
                             "\nFailed: " +
                             str(crashes))