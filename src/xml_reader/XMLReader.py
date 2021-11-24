import datetime
from pymongo import MongoClient
import xml.dom.minidom
import os

# XMLFileReader Class bekommt einen XML Link und gibt uns die gewünschten Daten mithilfe von Funktionen zurück
class XMLFileReader:
    def __init__(self, xml_file):
        self.day = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        self.doc = xml.dom.minidom.parse(xml_file)
        self.row = self.doc.getElementsByTagName("ROW")
        self.CONNECTION_STRING = \
            "mongodb+srv://" + DB_USER + ":" + DB_PASS + "@mensaskill.2yqml.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        
        self.client = MongoClient(self.CONNECTION_STRING)
        self.client = MongoClient(self.CONNECTION_STRING)
        self.database = self.client.get_database("MensaSkill")

    def get_weekday(self, essen):
        date_splitted = str(essen.getAttribute("PRODDATUM")).split(".")
        int_day = datetime.date(int(date_splitted[2]), int(date_splitted[1]), int(date_splitted[0])).weekday() - 1
        return self.day[int_day]

    @staticmethod
    def calc_calender_week(essen):
        date_splitted = str(essen.getAttribute("PRODDATUM")).split(".")
        str_calender_week = datetime.date(int(date_splitted[2]), int(date_splitted[1]), int(
            date_splitted[0])).isocalendar()[1]
        return str_calender_week

    # "Hauptfunktion"
    def get_data(self):
        for essen in self.row:
            if essen.getAttribute("DPORTNAME") == "Mensa Worms":
                component_list = []

                for i in range(1, 8):
                    component_list.append(essen.getAttribute("ATEXTOHNEZSZ" + str(i)))

                get_coll = self.database.getCollection(self.calc_calender_week(essen))
                get_coll.insertOne(
                    {"date": essen.getAttribute("PRODDATUM"), "weekday": self.get_weekday(essen),
                     "ausgabe": essen.getAttribute("DPARTYP"), "zusatzstoffe": essen.getAttribute("ZSNAMEN"),
                     "menue": component_list}
                )