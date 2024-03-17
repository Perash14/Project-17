from db import ChatDB


chat = ChatDB()
userid= chat.insert_user("nik")
print(userid)

chat.add_message("hello",userid)
