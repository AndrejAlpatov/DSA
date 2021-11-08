import pymongo          # Modul um auf eine MongoDB-Datenbank zugreifen zu koennen
import datetime         # Modul um das aktuelle Datum festzustellen

"""
    DatabaseInterface.py:

    In dieser Datei wird die Klasse "DatabaseInterface" implementiert.
    Sie ist die Schnittstelle zwischen dem Progamm mit der Hauptfunktion und der MongoDB
    Dankenbank, auf die zugegriffen wird.

        Funktionalitaet:
            - Datumueberpruefung:
                Wenn die Datenbank nicht mehr aktuell ist, wird sie geloescht und eine
                neue aufgebaut. Dafuer muss sie als die neuen Daten aus dem Modul ""
                uebergeben bekommen.
            - Aus der Datenbank soll gelesen werden. Fuer den Sprachassistenten vordefinierte
              Datenbankabfragen werden umgesetzt.

        Datenbankaufbau:
            - Collections:
                - Datum (zur Datumsueberpruefung)
                - Ausgabe (Informationen zu Gerichten)
                //- Kioskdaten
                //- Salatbardaten
                //- Studierendenwerkdaten
                //- Mensaguthaben, Favoriten, Personendaten...

            - Aufbau der Collections:
                - Datum:
                    "stand":""

                - Ausgabe:
                    "vegetarisch":""
                    "tagessuppe":""
                    "hauptgericht":""
                    "beilagen":""
                    "dessert":""
                    "zusatzstoffe":""
                    "kalorien":""
                    "naehrwerte":""
                    "preis":""
            
            Todo:
                - Datumerfassungsfomat von ddmmyyyy in kalenderwoche&jahreszahl aendern 
"""

class DatabaseInterface:

    # string mit Verbindungsdaten (Username/Password/Clustername)
    CONNECTION_STRING = "mongodb+srv://testuser:12345@cluster0.ti92d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    def __init__(self):
        ## Verbindungsherstellung zur Datenbank und Attributdeklarierungen
        self.client = pymongo.MongoClient(self.CONNECTION_STRING)       # Verbindung ueber Client herstellen
        self.database = self.client.get_database("speiseplan")          # Datenbank mittels Verbindung erstellen
        
        ## Datumueberpruefung
        datumpuffer = datetime.datetime.now()                           # aktuelles Datum erfassen und speichern (Form: 01012021)
        self.datumstr = str(str(datumpuffer.strftime("%d")) +
                            str(datumpuffer.strftime("%m")) +
                            str(datumpuffer.strftime("%Y")))

        vorhandeneCollections = self.database.list_collection_names()   # Liste der vorhandenen Collections erstellen
        
        if "datum" in vorhandeneCollections:                            # Check ob "datum" existiert
            self.datumcol = self.database["datum"]

            # Stand ueberpruefen
            document = self.datumcol.find({"stand":self.datumstr})      # Eintraege mit dem aktuellen Datum suchen und speichern
            
            # versuchen auf das Attribut "stand" zuzugreifen
            try:
                if self.datumstr == document[0].__getitem__("stand"):   # Check ob das Datum gleich ist
                    self.aktuell = True         # angeben, dass Datum aktuell ist
                else:
                    self.aktuell = False        # angeben, dass Datum nicht aktuell ist
            # falls kein Attribut vorhanden ist, ist das Datum nicht aktuell
            except:
                self.aktuell = False            # angeben, dass das Datum nicht aktuell ist
        else:
            ### Hier sollte zuerst noch alles geloescht werden, falls etwas da ist ###
            # Eine Collection "datum" mit dem aktuellen Datum erstellen
            self.datumcol = self.database["datum"]
            self.datumcol.insert_one({"stand":self.datumstr})
            self.aktuell = False                # angeben, dass Datum noch nicht aktuell ist

        ## Wenn festgestellt wurde, dass die Datenbank nicht aktuell ist, muss sie mit aktuellen Daten befuellt werden
        if self.aktuell == False:
            # Befuellung mit Daten
            pass

    def dropCols(self):
        # alle Collections loeschen
        vorhandeneCollections = self.database.list_collection_names()
        if "datum" in vorhandeneCollections:
            self.datumcol.drop()
        #if "ausgabe" in vorhandenenCollections:
        #if ...

    def dropDatumCol(self):
        # Datum Collection loeschen, falls vorhanden
        vorhandeneCollections = self.database.list_collection_names()
        if "datum" in vorhandeneCollections:
            self.datumcol.drop()
    
    #def dropAusgabeCol(self):
    #def drop....

# Test
if __name__ == "__main__":
    dbinterface = DatabaseInterface()
    dbinterface.dropCols()