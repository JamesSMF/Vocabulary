# Python code to demonstrate SQL to fetch data.

# importing the module
import sqlite3
import os
import re

# connect withe the myTable database
connection = sqlite3.connect("vocabulary.db")

# This statement removes 'u' at the beginning of the output
connection.text_factory = str
crsr = connection.cursor()

# if the database does not exist, create a new one.
# SQL command to create a table in the database
sql_command = """CREATE TABLE IF NOT EXISTS vocaTable (
"voc_Num" INTEGER PRIMARY KEY,
"unfamilarity" INTEGER,
"word" VARCHAR(30),
"synonym" VARCHAR(40));"""

# execute the statement
crsr.execute(sql_command)

while True:
   sql_command = raw_input("enter sql commands or q to exit: ")
   chArray = sql_command.split()

   # q
   if sql_command == 'q':
      # To save the changes in the files. Never skip this.
      # If we skip this, nothing will be saved in the database.
      connection.commit()

      # close the connection
      connection.close()
      break

   # ls -a
   elif sql_command=="la" or sql_command=="ls -a":
      crsr.execute("SELECT * FROM vocaTable")
      ans = crsr.fetchall()
      for i in ans:
         print i

   # ls
   elif chArray[0]=="ls":
      mess = "SELECT unfamilarity, word, synonym FROM vocaTable"
      if re.search("-s", sql_command):         # -s flag: sort by unfamilarity
         mess += " ORDER BY unfamilarity DESC"
      if re.search("-al", sql_command):        # -al: sort alphabetically
         mess += " ORDER BY word"

      crsr.execute(mess)
      ans = crsr.fetchall()
      for i in ans:
         print i

   # map
   elif chArray[0]=="map" or chArray[0]=="insert":
       crsr.execute("INSERT INTO vocaTable(unfamilarity, word, synonym) VALUES(" + "0,\"" + chArray[1] + "\",\""+" ".join(chArray[2:]) + "\")")

   # i
   elif sql_command=='i':
      theWord = raw_input("Enter the word: ")
      theMeaning = raw_input("Enter the meaning: ")
      crsr.execute("INSERT INTO vocaTable(unfamilarity, word, synonym) VALUES(" + "0, " + theWord + "," + theMeaning)

   # SELECT
   elif re.search("SELECT", sql_command) or re.search("select", sql_command) or re.search("Select", sql_command):
      crsr.execute(sql_command)
      ans = crsr.fetchall()
      for i in ans:
         print i

   # rm
   elif re.search("rm", sql_command) or re.search("del", sql_command):
      crsr.execute("DELETE FROM vocaTable where word = \"" + chArray[1] + "\"")

   # test
   elif chArray[0]=='test':
      crsr.execute("SELECT word FROM vocaTable")
      ans = crsr.fetchall()
      for i in ans:
         print i

   # else
   else:
      crsr.execute(sql_command)
