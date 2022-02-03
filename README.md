# DSA: Semesterprojekt
(von Andrej Alpatov, Marco Ohnesorg und Danny Staus im Wintersemester 2021/22)

## Beschreibung
Das Projekt `Mensa Skill` ist ein Skill für die Amazon Alexa. Er dient als *digitaler Sprachassistent*, 
um Daten der *Mensa der Hochschule Worms* abzufragen. Die Daten wurden auf der *Cloud-Datenbank MongoDB Atlas* gespeichert. 
Das Programm greift auf diese Daten zu. Die Daten werden vom Betreiber der Mensa regelmäßig auf einen FTP-Server hochgeladen.

## Funktionalität
Beispielfragen zum Skill:
- Wie bediene ich diesen Skill?
- Wann kann ich in die Mensa essen gehen?
- Ab wie viel Uhr kann man in der Mensa essen?
- Bis wie viel Uhr kann ich in die Mensa gehen?
- Welche Produkte gibt es am Kiosk zum essen?
- Gibt es Coca Cola am Kiosk?
- Darf ich am Kaffeeautomaten meinen eigenen Becher befüllen?
- Zu welcher Organisation gehört die Mensa?
- Was sind die Themen des Studierendenwerks Vorderpfalz?
- Betreibt das Studierendenwerk der Vorderpfalz noch weitere Mensen?
- Kannst du mir etwas zum Betreiber der Mensa sagen?
- Wie viel Euro kostet das Essen für Gäste?
- Was kann ich heute essen?
- Was gibt es morgen an Ausgabe 1 zu essen?
- Was gibt es am 03.02.2022 zum essen?
- Was gibt es in zwei Tagen zum essen?

## Projektstruktur
### Quellcode:
Der Quellcode befindet sich im Ordner `src`. Er besteht aus:
- Datenbank-Funktionen
- Intent-Handlern
- Handlern für den FTP-Server
- Handlern für XML-Dateien

### Resourcen:
Die Resourcen befinden sich zum Einen im Ordner `res` und zum Anderen in der `Cloud-Datenbank MongoDB Atlas`.
#### res:
- APL-Dokumente *(json-Format)*
- XML-Datei *(Daten vom FTP-Server)*

#### Cloud-Datenbank MongoDB Atlas:
- Daten des Speiseplans *(gefiltert aus der XML-Datei im Ordner `res`)*
- Antworten/Output für die Intent-Handler

### Dokumention:
Die Dokumentation besteht aus *zwei* Teilen:
#### 1. Externe Dokumentation:
Die Dateien der externen Dokumentation wurden per Mail übergeben um im Folgenden aufgelistet:
- Freitext *(Datei: `Dokumentation.pdf`)*
- Rasa Ergebnisse *(Datei: `RASA_accuracy.pdf`)*
- Demo-Video *(Datei: `Demo_Video.mp4`)*
#### 2. Interne Code-Dokumentation:
Die interne Dokumentation ist eine Code-Dokumentation und wurde mit `pdoc3` umgesetzt. Die zugehörigen *HTML-Dateien* befinden sich im Ordner `doc`.
