#TODO implementation of class XMLReader
import xml.dom.minidom
import datetime
import pymong as py

#XMLFileReader Class bekommt einen XML Link und gibt uns die gewünschten Daten mithilfe von Funktionen zurück
class XMLFileReader:
    def __init__(self,xmlFile):
        self.day = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag"] #für bestimmung des Wochentag
        self.doc = xml.dom.minidom.parse(xmlFile)                          #öffnen des XML-File
        self.row = self.doc.getElementsByTagName("ROW")                    #auswahl aller ROW Elemente


    def get_weekday(self,essen):                                                                                    #Hilffunktion für Wochentagsbestimmung
        date_splitted = str(essen.getAttribute("PRODDATUM")).split(".")                                             #nimmt sich das Element PRODDATUM vom momentanen ROW-Element und trennt es am Punkt
        intDay = datetime.date(int(date_splitted[2]), int(date_splitted[1]), int(date_splitted[0])).weekday() - 1   #Die Liste intDay enthält dann die Nummer des Tages 0 = Montag usw.
        print(self.day[intDay])


    def get_data(self):                                                    #"Hauptfunktion"
        for essen in self.row:
            if essen.getAttribute("DPORTNAME") == "Mensa Worms":           #for schleife die über alle ROW Elemente itteriert & alle Elemente mit Attribut (DPORTNAME") == "Mensa Worms" auswertet
                print(essen.getAttribute("PRODDATUM"))
                self.get_weekday(essen)
                print(essen.getAttribute("DPARTNAME"))
                print(essen.getAttribute("ZSNAMEN"))
                for i in range(1,8):                                        #geschachtelte for Schleife die mehrere Elemente ausliest
                    print(essen.getAttribute("ATEXTOHNEZSZ" + str(i)))


"""Die extra Zeilenumbrüche im Output kommen durch die leeren Elemente in der verschachtelten for-Schleife zustande.
sollte später aber kein Probem sein da wir warscheinlich hier sowieso keine Ausgabe machen sondern die Ergebnisse direkt in die
Datenbank weitergeben an der Stelle an der sie ermittelt werden. Eine andere Möglichkeit wäre es noch Hier eine Liste mit allem
zurück zu geben man anschließend anhand dieser die Elemente in die Datenbank überträgt (maybe schöner)?
"""

