import sqlite3
from shooter.settings import *
from shooter.score import Score

class BDD:
    def __init__(self):
        self.db_name = DB_NAME
        self._dbConnexion()

    def _dbConnexion(self):
        self.con = sqlite3.connect(self.db_name)
        try:
            cur = self.con.cursor()
            player1 = 'create table player1(ID INT PRIMARY KEY NOT NULL, MANEUVERABILITY REAL, ACCELERATION REAL, BULLET_SPEED REAL, HEALTH INTEGER, DELAY_SHOOT REAL, POWER_SHOOTING INTEGER)'
            player2 = 'create table player2(ID INT PRIMARY KEY NOT NULL, MANEUVERABILITY REAL, ACCELERATION REAL, BULLET_SPEED REAL, HEALTH INTEGER, DELAY_SHOOT REAL, POWER_SHOOTING INTEGER)'
            score = 'create table score(ID INT PRIMARY KEY NOT NULL, PSEUDO TEXT, SCORE INTEGER)'
            cur.execute(player1)
            cur.execute(player2)
            cur.execute(score)
            dataInsert = [1, 3, 2.5, 7, 5, 0.75, 1]
            self._insertSettings("player1" ,dataInsert)
            self._insertSettings("player2" ,dataInsert)
            self._setUpScore()
            cur.close()
        except sqlite3.Error as e:
            print ("Error in connection", e)

    def _insertSettings(self, player, data):
        try:
            cur = self.con.cursor()
            cur.execute(f"insert into {player} (ID, MANEUVERABILITY, ACCELERATION, BULLET_SPEED, HEALTH, DELAY_SHOOT, POWER_SHOOTING) values (?, ?, ?, ?, ?, ?, ?)", data)
            print("qq")
            cur.close()
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error in connection", e)

    def updateSettings(self, player, data):
        try:
            cur = self.con.cursor()
            if player == "player1":
                sql = ''' UPDATE player1
                        SET MANEUVERABILITY = ?,
                            ACCELERATION = ?, 
                            BULLET_SPEED = ?, 
                            HEALTH = ?, 
                            DELAY_SHOOT = ?,
                            POWER_SHOOTING = ? 
                    WHERE id = ?'''
            else :
                sql = ''' UPDATE player2
                        SET MANEUVERABILITY = ?,
                            ACCELERATION = ?, 
                            BULLET_SPEED = ?, 
                            HEALTH = ?, 
                            DELAY_SHOOT = ?,
                            POWER_SHOOTING = ? 
                    WHERE id = ?'''
            cur.execute(sql, data)
            cur.close()
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error in connection", e)

    def insertScore(self, data):
        try:
            cur = self.con.cursor()
            Id = self.getNextId("SCORE")
            cur.execute(f"insert into score (ID, PSEUDO, SCORE) values ({Id}, ?, ?)", data)
            cur.close()
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error in connection", e)
    
    def selectScore(self, id):
        try:
            cur = self.con.cursor()
            cur.execute(f"select * FROM score WHERE ID = {id}")
            row = cur.fetchone()
            cur.close()
            self.con.commit()
            return Score(row)
        except sqlite3.Error as e:
            print ("Error in connection", e)

    def _setUpScore(self):
        try:
            cur = self.con.cursor()
            dataScore = [1, "toto le fou malade", 1]
            cur.execute("insert into score (ID, PSEUDO, SCORE) values (?, ?, ?)", dataScore)
            cur.close()
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error in connection", e)
            
    def select(self, request):
        cur = self.con.cursor()
        cur.execute(request)
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(Score(row))
        return data
    
    def selectSetting(self, player):
        cur = self.con.cursor()
        cur.execute(f"select * FROM {player} WHERE ID = 1")
        rows = cur.fetchone()
        cur.close()
        return(rows)

    def getNextId(self, table):
        cur = self.con.cursor()
        cur.execute(f'SELECT * FROM {table} order by ID DESC')
        rows = cur.fetchone()
        cur.close()
        lastId = rows[0]
        return(lastId+1)
