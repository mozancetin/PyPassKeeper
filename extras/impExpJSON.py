import json
import sqlite3
import os

def exportData(path):
    try:
        data = {}
        data["Users"] = {}

        #Connect to the Database
        connection = sqlite3.connect("./passwordDatabase.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserName TEXT, Password TEXT)")
        connection.commit()

        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        for i in range(len(users)):

            #Add User Data
            data["Users"][users[i][0]] = str(users[i][1])
            data[users[i][0]] = {}
            data[users[i][0]]["Categories"] = []
            data[users[i][0]]["Passwords"] = {}

            #Add Password Data
            cursor.execute(f"SELECT * FROM {users[i][0]}")
            passwordData = cursor.fetchall()
            if passwordData != 0:
                for j in range(len(passwordData)):
                    data[users[i][0]]["Passwords"][passwordData[j][0]] = []
                    data[users[i][0]]["Passwords"][passwordData[j][0]].append(str(passwordData[j][1]))
                    data[users[i][0]]["Passwords"][passwordData[j][0]].append(str(passwordData[j][2]))
            
            #Add Category Data
            cursor.execute(f"SELECT * FROM {users[i][0]}C")
            categoryData = cursor.fetchall()
            if categoryData != 0:
                for k in range(len(categoryData)):
                    data[users[i][0]]["Categories"].append(str(categoryData[k][0]))
        
        #Write JSON File
        with open(path, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return True

    except Exception as e:
        print(e)
        return False

def importData(path):
    try:
        #Get data from JSON File
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        #Connect to the Database
        connection = sqlite3.connect("./passwordDatabase.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserName TEXT, Password TEXT)")
        connection.commit()

        #Get every user
        for user in data["Users"]:
            #Create tables
            cursor.execute("SELECT * FROM Users WHERE UserName = ?", (user,))
            isThereAny = cursor.fetchall()
            
            if len(isThereAny) == 0:
                cursor.execute("INSERT INTO Users VALUES(?, ?)", (user, data["Users"][user]))
                connection.commit()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {user} (Name TEXT, Password TEXT, Category TEXT)")
                connection.commit()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {user}C (Categories TEXT)")
                connection.commit()

            #Insert Password Data
            for program in data[user]["Passwords"]:
                cursor.execute(f"SELECT * FROM {user} WHERE Name = ?", (program,))
                isEmpty = cursor.fetchall()

                if len(isEmpty) == 0:
                    cursor.execute(f"INSERT INTO {user} VALUES(?, ?, ?)", (program, data[user]["Passwords"][program][0], data[user]["Passwords"][program][1]))
                    connection.commit()

            #Insert Category Data
            for category in data[user]["Categories"]:
                cursor.execute(f"SELECT * FROM {user}C WHERE Categories = ?", (category,))
                isEmpty2 = cursor.fetchall()

                if len(isEmpty2) == 0:
                    cursor.execute(f"INSERT INTO {user}C VALUES(?)", (category,))
                    connection.commit()

        return True

    except Exception as e:
        print(e)
        return False