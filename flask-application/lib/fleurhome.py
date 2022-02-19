#import modules in volgorde van gebruiken
import sys
import speech_recognition
import pyaudio
import sqlite3
import re as regex
from text_to_speech import speak
from flask import flash

#define classes and functions
class Input():

    def get_method(self):
        method = input("Wil je tekst of spraak? ") #vraag: wil je tekst of spraak?
        self.methode = method #zorg ervoor dat dezelfde methode gebruikt kan worden voor class Output
        if str.lower(method) == "tekst": #als je tekst hebt gekokzen:
            self.get_tekst() #run de functie get_tekst().
        elif str.lower(method) == "spraak": #als je spraak hebt gekozen:
            self.get_audio() #run de functie get_audio()
        else: #Als je geen van beide hebt gekozen:
            print("Not valid value entered. Program will now quit") #print dat je het niet goed hebt gedaan
            sys.exit() #stop het script

    def get_audio(self):
        with speech_recognition.Microphone(device_index=1) as source: #open de microfoon
            r = speech_recognition.Recognizer() #initialiseer de microfoon
            print("Zeg het volgende: wat is het huiswerk voor <vak> op <dag> (dag zondag, maandag en niet vandaag, morgen, etc.)") #print hoe het gezegd moet worden.
            audio = r.listen(source) #luister naar wat ik zeg (hier is het nog mp3)
            try:
                said = r.recognize_google(audio, language="nl_NL") #probeer te kijken in de google speech library of je het herkent in het nederlands. Hier wordt de mp3 van line 31 omgezet in tekst.
                print(said) #herhaal wat je hebt gezegd, net zoals bij google assistent.
                self.gezegd = said #zorg ervoor dat wat je gezegd gebruikt kan worden in class Sql.
            except Exception as e:
                print('Ik heb het niet verstaan. Het programma sluit nu.') #zeg dat je het niet verstaan hebt.
                sys.exit() #stop het script

    def get_tekst(self):
        input_huiswerk = input("Typ het volgende over: wat is het huiswerk voor <vak> op <dag> (dag zondag, maandag en niet vandaag, morgen, etc.) ") #print hoe het gezegd moet worden en vraag een antwoord.
        self.gezegd = input_huiswerk #zorg ervoor dat wat je gezegd hebt, gebruikt kan worden in de class Sql.

class Sql():
    def __init__(self):
        
        self.database = sqlite3.connect('fleur_home_huiswerk_assistent.db') #initialiseer de database
        cursor = self.database.cursor() #maak een cursor aan. Deze cursor kan dingen in de database lezen en veranderen.
        cursor.execute('CREATE TABLE IF NOT EXISTS maandag (id INT PRIMARY KEY NOT NULL, uur INT, vak TEXT, huiswerk TEXT)') #maak tabel maandag aan als hij nog niet bestaat, met als kolommen id (integer, primary key, mag niet niks zijn), uur (int), vak (tekst) en huiswerk (tekst)
        cursor.execute('CREATE TABLE IF NOT EXISTS dinsdag (id INT PRIMARY KEY NOT NULL, uur INT, vak TEXT, huiswerk TEXT)') #maak tabel dinsdag aan als hij nog niet bestaat, met als kolommen id (integer, primary key, mag niet niks zijn), uur (int), vak (tekst) en huiswerk (tekst)
        cursor.execute('CREATE TABLE IF NOT EXISTS woensdag (id INT PRIMARY KEY NOT NULL, uur INT, vak TEXT, huiswerk TEXT)') #maak tabel woensdag aan als hij nog niet bestaat, met als kolommen id (integer, primary key, mag niet niks zijn), uur (int), vak (tekst) en huiswerk (tekst)
        cursor.execute('CREATE TABLE IF NOT EXISTS donderdag (id INT PRIMARY KEY NOT NULL, uur INT, vak TEXT, huiswerk TEXT)') #maak tabel donderdag aan als hij nog niet bestaat, met als kolommen id (integer, primary key, mag niet niks zijn), uur (int), vak (tekst) en huiswerk (tekst)
        cursor.execute('CREATE TABLE IF NOT EXISTS vrijdag (id INT PRIMARY KEY NOT NULL, uur INT, vak TEXT, huiswerk TEXT)') #maak tabel vrijdag aan als hij nog niet bestaat, met als kolommen id (integer, primary key, mag niet niks zijn), uur (int), vak (tekst) en huiswerk (tekst)
        vakken = [ #maak een enorme lijst aan, die ervoor zorgt dat alle values op éém plek staan. De tabel is opgebouwd uit [dag][vakid]
        [[0,2,"aardrijkskunde", "H2"], [1,3,"muziek",""],[2,5,"geschiedenis", ""],[3,6,'duits',''],[4,7,'natuurkunde', ''],[5,8,'drama','Monoloog']], #dit is de dag maandag.
        [[0,1,'beeldende vorming',''],[1,3,'frans',''], [2,4,'duits',''],[3,5,'engels',''],[4,6,'wiskunde','']], #dit is de dag dinsdag.
        [[0,1,'nederlands',''], [1,2,'grieks',''],[2,3,'wiskunde',''],[3,4,'duits',''],[4,5,'lichamelijke opvoeding',''], [5,7,'mentoruur','']], #dit is de dag woensdag.
        [[0,1,'latijn',''],[1,2,'aardrijkskunde',''],[2,3,'nederlands',''],[3,4,'geschiedenis',''],[4,5,'engels',''],[5,7,'frans','']], #dit is de dag donderdag.
        [[0,1,'latijn',''],[1,2,'wiskunde',''],[2,3,'engels', ''], [3,4,'nederlands',''],[4,5,'natuurkunde',''], [5,6,'grieks','']] #dit is de dag vrijdag.
        ] #einde van de lijst


        for i in vakken[0]:
            cursor.execute('INSERT OR IGNORE INTO maandag VALUES (?, ?, ?, ?)', (i[0],i[1],i[2],i[3])) #vul de tabel maandag
        for i in vakken[1]:
            cursor.execute('INSERT OR IGNORE INTO dinsdag VALUES (?, ?, ?, ?)', (i[0],i[1],i[2],i[3])) #vul de tabel dinsdag
        for i in vakken[2]:
            cursor.execute('INSERT OR IGNORE INTO woensdag VALUES (?, ?, ?, ?)', (i[0],i[1],i[2],i[3])) #vul de tabel woensdag
        for i in vakken[3]:
            cursor.execute('INSERT OR IGNORE INTO donderdag VALUES (?, ?, ?, ?)', (i[0],i[1],i[2],i[3])) #vul de tabel donderdag
        for i in vakken[4]:
            cursor.execute('INSERT OR IGNORE INTO vrijdag VALUES (?, ?, ?, ?)', (i[0],i[1],i[2],i[3])) #vul de tabel vrijdag
        cursor.close()
    def get_dagvak(self, input_huiswerk):
        pattern = regex.compile(r'wat is het huiswerk voor (\w+) op (\w+)') #initialiseer regex

        x = input_huiswerk.lower() #zorg dat alle letters kleine letters worden.
        match = pattern.match(x) #komt het overeen?
        if regex.compile(r'wat is het huiswerk voor (\w+) op (\w+)').search(x) is not None: #ja, het komt overeen (match = True)
            self.vak, self.dag = match.groups() #haal de self.vak en self.dag uit de regex. En zorg ervoor dat ze in andere functies gebruikt kunnen worden.
        else:
            print("Je hebt je niet aan de zin gehouden die hierboven is beschreven. Het programma sluit nu.") #print dat je het niet goed gedaan hebt.
            sys.exit() #stop het script.

    def sql_processing(self, vak, dag):
        cursor = self.database.cursor() #open een cursor
        self.vak = vak
        self.dag = dag
        cursor.execute("select vak, huiswerk from "+dag) #run de select sql query, waardoor het vak en huiswerk geselecteerd worden.
        huiswerklijst = cursor.fetchall() #zorg ervoor dat de select query in een variabele komt.
        for huiswerkitem in huiswerklijst: #voor elk item in huiswerklijst:
            if huiswerkitem[0].lower() == vak: #als het eerste (vak) overeen komt met het vak wat is gevraagd:
                self.huiswerk = huiswerkitem[1] #zorg ervoor dat het in class Output gebruikt kan worden.
            else:
                self.huiswerk = "error"

    def close(self):
        self.database.commit()
        self.database.close() #sluit de database, zodat alles opgeslagen wordt.
        


class Output():
    def __init__(self, vak, dag, huiswerk, methode):
        self.vak = vak
        self.dag = dag
        self.methode = methode #initialiseer variabele methode
        if huiswerk == "": #als er geen huiswerk is:
            self.saying = "er is geen huiswerk voor "+vak+" op "+dag+"." #zoeg ervoor dat dit straks geoutput wordt
        elif huiswerk == "error":
            self.saying = "Dat vak heb je niet vandaag"
        else: #of anders:
            self.saying = "het huiswerk voor "+vak+" op "+dag+" is "+huiswerk+"." #zorg ervoor dat dit straks geoutput wordt


    def spraakoftekst(self):
        if self.methode.lower() == 'spraak': #als je bij Input voor spraak hebt gekozen:
            self.spraakoutput() #run de functie spraakoutput()
        elif self.methode.lower() == 'tekst': #als je daar voor tekst hebt gekozen:
            self.tekstoutput() #run de functie tekstoutput()

    def spraakoutput(self):
        speak(self.saying, "nl", save=False) #zeg self.saying (die in __init__ is aangemaakt)

    def tekstoutput(self):
        print(self.saying) #print self.saying (die in __init__ is aangemaakt)

def cmdrun():
        data = Input() #initialiseer Input class
        data.get_method() #hoe wil je het doen en doe het dan ook
        sqldata = Sql() #initialiseer Sql class
        sqldata.get_dagvak(data.gezegd) #krijg de dag en het vak
        sqldata.sql_processing(sqldata.vak, sqldata.dag) # lees uit de database welk huiswerk je moet hebben
        sqldata.close() #sluit de database
        output = Output(sqldata.vak, sqldata.dag, sqldata.huiswerk, data.methode) #initialiseer Output class
        output.spraakoftekst() #output het vervolgens.

class Webinput():
    def __init__(self, vak, dag):
        self.gezegd = 'wat is het huiswerk voor '+str(vak)+' op '+str(dag)

class Weboutput():
    def __init__(self, vak, dag, huiswerk):
        if huiswerk == "":
            self.saying = 'Er is geen huiswerk voor '+vak+' op '+dag
        elif huiswerk == "error":
            self.saying = "Je hebt dat vak niet op die dag."
        else:
            self.saying = 'Het huiswerk voor '+vak+' op '+dag+' is '+huiswerk


def webrun(vak, dag):
    sqldata = Sql()
    sqldata.sql_processing(vak, dag)
    sqldata.close()
    output = Weboutput(sqldata.vak, sqldata.dag, sqldata.huiswerk)
    flash(output.saying)

if __name__ == '__main__':
    cmdrun()
