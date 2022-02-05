import datetime
import xml.dom.minidom
from src.data_bank_functions.file_for_internal_usage import client_mongoDB


# XMLFileReader Class bekommt einen XML Link und gibt uns die gewünschten Daten mithilfe von Funktionen zurück
class XMLFileReader:
    """ Class to Read XML Files """

    def __init__(self):
        """ Initialisition for XMLFileReader Class

            day(stringArray): Array with all Values of Weekdays besides Saturday and Sunday
            self.client = establishes a connection with the connection string in the file_for_internal_usage
            self.database = getting access to MensaSkill Database

        """
        self.day = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        self.client = client_mongoDB
        self.database = self.client.get_database("MensaSkill")

    def get_weekday(self, essen):
        """
        Function to get the date from the xml file where the essen is provided and calculate the weekday for the date

        Args:
            essen: the current row of the xml document which is selected in the main function of the class.

        Returns:
            The weekday that the meal (essen) is provided by the mensa
        """
        date_splitted = str(essen.getAttribute("PRODDATUM")).split(".")
        int_day = datetime.date(int(date_splitted[2]), int(date_splitted[1]), int(date_splitted[0])).weekday() - 1
        return self.day[int_day]

    @staticmethod
    def calc_calender_week(essen):
        """
        A function to calculate the calenderweek by looking at the essen argument from the xml document with
        .getAttribute("PRODDATUM") which returns the calender date on which the meal (essen) is served

        Args:
            essen: the current row of the xml document which is selected in the main function of the class.

        Returns:
            A valid Calender date fitting to the PRODDATUM
        """
        date_splitted = str(essen.getAttribute("PRODDATUM")).split(".")
        str_calender_week = datetime.date(int(date_splitted[2]), int(date_splitted[1]), int(
            date_splitted[0])).isocalendar()[1]
        return str_calender_week

    # "Hauptfunktion"
    def get_data(self, xml_file):
        """
        The get_data function scans the XML File row by row and picks all rows where the Attribute DPORTNAME is equal
        to Mensa Worms. This Row with its arguments will be used to create our database entry in the Database Document
        with the CalenderWeek the meal is provided in.

        Args:
            xml_file: A valid XML File

        Returns:
            void
        """
        doc = xml.dom.minidom.parse(xml_file)
        row = doc.getElementsByTagName("ROW")
        #loop that iterates over all rows of the document
        for essen in row:
            #picks all rows where DPORTNAME is Mensa Worms
            if essen.getAttribute("DPORTNAME") == "Mensa Worms":
                component_list = []

                # for loop that arranges the components of a meal
                for i in range(1, 8):
                    component_list.append(essen.getAttribute("ATEXTOHNEZSZ" + str(i)))

                #insertion of a document into the database collection of the according calender week
                get_coll = self.database.getCollection(self.calc_calender_week(essen))
                get_coll.insertOne(
                    {"date": essen.getAttribute("PRODDATUM"), "weekday": self.get_weekday(essen),
                     "ausgabe": essen.getAttribute("DPARTYP"), "zusatzstoffe": essen.getAttribute("ZSNAMEN"),
                     "menue": component_list}
                )
