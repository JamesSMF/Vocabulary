import sqlite3
import os
import re

class bcolors:
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
   WHITE = '\033[97m'
   PERFECTBLUE = '\033[96m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'

# connect withe the database
connection = sqlite3.connect("vocabulary.db")

# This statement removes 'u' at the beginning of the output
connection.text_factory = str
crsr = connection.cursor()

# if the database does not exist, create a new one.
# SQL command to create a table in the database
sql_command = """CREATE TABLE IF NOT EXISTS vocaTable (
"voc_Num" INTEGER PRIMARY KEY,
"unfamilarity" INTEGER,
"word" VARCHAR(32),
"synonym" VARCHAR(64));"""

# execute the statement
crsr.execute(sql_command)

while True:
   sql_command = raw_input("enter commands or q to exit: ")
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
         print bcolors.WHITE + str(i) + bcolors.ENDC

      print("")          # print a newline

   # ls
   elif chArray[0]=="ls":
      mess = "SELECT unfamilarity, word, synonym FROM vocaTable"
      if re.search("-s", sql_command):         # -s flag: sort by unfamilarity
         mess += " ORDER BY unfamilarity"
      if re.search("-al", sql_command):        # -al: sort alphabetically
         if not re.search("-s", sql_command):
            mess += " ORDER BY word"
         else:
            mess += ", word"

      crsr.execute(mess)
      ans = crsr.fetchall()
      for i in ans:
         print bcolors.WHITE + str(i) + bcolors.ENDC

      print("")          # print a newline

   # map
   elif chArray[0]=="map" or chArray[0]=="insert":
      crsr.execute("INSERT INTO vocaTable(unfamilarity, word, synonym) VALUES(" + "0,\"" + chArray[1] + "\",\""+" ".join(chArray[2:]) + "\")")
      print("")          # print a newline

   # inc
   elif chArray[0]=="inc" or re.search("\+\+", sql_command):
      sql_command = re.sub("inc ","",sql_command)
      sql_command = re.sub("[^a-z]","", sql_command)

      crsr.execute("SELECT unfamilarity FROM vocaTable WHERE word = \"" + sql_command +"\"")
      org = crsr.fetchall()
      orgNum = int(org[0][0]) + 1
      crsr.execute("UPDATE vocaTable SET unfamilarity = " + str(orgNum) + " WHERE word = \"" + sql_command + "\"")
      print("")          # print a newline

   # dec
   elif chArray[0]=="dec" or re.search("\-\-", sql_command):
      sql_command = re.sub("dec ","",sql_command)
      sql_command = re.sub("[^a-z]","", sql_command)

      crsr.execute("SELECT unfamilarity FROM vocaTable WHERE word = \"" + sql_command +"\"")
      org = crsr.fetchall()
      orgNum = int(org[0][0]) - 1
      if orgNum<0:
         orgNum = 0      # set to zero if it is less than zero
      crsr.execute("UPDATE vocaTable SET unfamilarity = " + str(orgNum) + " WHERE word = \"" + sql_command + "\"")
      print("")          # print a newline

   # nz
   elif sql_command=="nz" or sql_command=="nonzero":
      crsr.execute("SELECT unfamilarity, word, synonym FROM vocaTable WHERE unfamilarity != 0")
      ans = crsr.fetchall()
      for i in ans:
         print bcolors.WHITE + str(i) + bcolors.ENDC

      print("")          # print a newline

   # zero
   elif sql_command=="zero":
      crsr.execute("SELECT unfamilarity, word, synonym FROM vocaTable WHERE unfamilarity = 0")
      ans = crsr.fetchall()
      for i in ans:
         print bcolors.WHITE + str(i) + bcolors.ENDC

      print("")          # print a newline

   # i
   elif sql_command=='i':
      theWord = raw_input("Enter the word: ")
      theMeaning = raw_input("Enter the meaning: ")
      crsr.execute("INSERT INTO vocaTable(unfamilarity, word, synonym) VALUES(" + "0, " + theWord + "," + theMeaning)
      print("")          # print a newline

   # SELECT
   elif re.search("SELECT", sql_command) or re.search("select", sql_command) or re.search("Select", sql_command):
      try:
         crsr.execute(sql_command)
         ans = crsr.fetchall()
         for i in ans:
            print bcolors.WHITE + str(i) + bcolors.ENDC
      except:
         print("Please enter a valid SQL SELECT command.")

      print("")          # print a newline

   # rm
   elif chArray[0]=="rm" or chArray[0]=="del":
      crsr.execute("DELETE FROM vocaTable WHERE word = \"" + chArray[1] + "\"")
      print("")          # print a newline

   # peek
   elif chArray[0]=="peek":
      theWord = chArray[-1]
      crsr.execute("SELECT synonym FROM vocaTable WHERE word = \"" + theWord + "\"")
      meaning = crsr.fetchall()
      for i in meaning:
         print bcolors.WHITE + str(i[0]) + bcolors.ENDC
      print("")

   # test
   elif chArray[0]=='test':
      if chArray[1]=="mode":
         while True:                      # loop entil q is entered
            print("Enter y for yes, n for no, and q to quit: ")
            print("Do you know the word: ")
            test_word = crsr.execute("SELECT word FROM vocaTable ORDER BY RANDOM() LIMIT 1")
            test_word = crsr.fetchall()
            test_word = str(test_word[0][0])
            print("")
            test_mode_input=raw_input(test_word)
            if test_mode_input=="q":      #quit test mode
               break
            elif test_mode_input=="y" or test_mode_input=="yes":
               crsr.execute("SELECT unfamilarity FROM vocaTable WHERE word = \"" + test_word +"\"")
               org = crsr.fetchall()
               orgNum = int(org[0][0]) - 1
               if orgNum<0:
                  orgNum = 0              # set to zero if it is less than zero
               crsr.execute("UPDATE vocaTable SET unfamilarity = " + str(orgNum) + " WHERE word = \"" + test_word + "\"")
            elif test_mode_input=="n" or test_mode_input=="no":
               crsr.execute("SELECT unfamilarity FROM vocaTable WHERE word = \"" + test_word +"\"")
               org = crsr.fetchall()
               orgNum = int(org[0][0]) + 1
               crsr.execute("UPDATE vocaTable SET unfamilarity = " + str(orgNum) + " WHERE word = \"" + test_word + "\"")
            else:
               print("Please enter \"y\", \"n\", or \"q\"")
      else:
         mess = "SELECT word FROM vocaTable"
         if re.search("-nz", sql_command):
            mess += " WHERE unfamilarity != 0"
         elif re.search("-zero", sql_command):
            mess += " WHERE unfamilarity = 0"
         if re.search("[0-9]", sql_command):
            sql_command = re.sub("[^0-9]","",sql_command)
            mess = (mess + " ORDER BY RANDOM() LIMIT " + sql_command)
         crsr.execute(mess)
         ans = crsr.fetchall()
         for i in ans:
            print bcolors.WHITE + str(i[0]) + bcolors.ENDC

      print("")          # print a newline

   # answer
   elif sql_command == "Answer" or sql_command == "answer" or sql_command == "ans":
      try:
         for i in ans:
            crsr.execute("SELECT word, synonym FROM vocaTable WHERE word = \"" + str(i[0]) + "\"")
            meaning = crsr.fetchall()
            print bcolors.WHITE + str(meaning[0]) + bcolors.ENDC
      except:
         print("Please take a quiz before looking at the answer!")
         continue

   # else
   else:
      try:
         crsr.execute(sql_command)
         continue
      except:
         print("Please enter a valid operation. (See README)")
         print("")          # print a newline
         continue

# end while
