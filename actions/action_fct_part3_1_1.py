import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppFctPart311(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part3_1_1.ui", self)
        self.data = data
        self.refreshNumInCmbbox()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshNumInCmbbox(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT disctinct numSp FROM LesSportifs UNION SELECT disctinct numEq FROM LesEquipes ")
        except Exception as e:
            self.ui.numIn_Ajout.clear()
            self.ui.numIn_Modification.clear()
            self.ui.numIn_Supression.clear()
        else:
            display.refreshGenericCombo(self.ui.numIn_Ajout, result)
            display.refreshGenericCombo(self.ui.numIn_Modification, result)
            display.refreshGenericCombo(self.ui.numIn_Supression, result)

    @pyqtSlot()
    def refreshNumEpCmbbox_Ajout(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct numEp FROM LesEpreuves NATURAL JOIN LesInscriptions WHERE numIn IS NOT ?",
                [self.ui.numIn_Ajout.currentText()]
                )
        except Exception as e:
            self.ui.numEp_Ajout.clear()
        else:
            display.refreshGenericCombo(self.ui.numEp_Ajout, result)

    @pyqtSlot()
    def refreshNumEpCmbbox_Modification(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesInscriptions WHERE numIn = ?",
                                    [self.ui.numIn_Modification.currentText()]
                                    )
        except Exception as e:
            self.ui.numEp_Modification.clear()
        else:
            display.refreshGenericCombo(self.ui.numEp_Modification, result)

    @pyqtSlot()
    def refreshNumEpCmbbox_Supression(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesInscriptions WHERE numIn = ?",
                                    [self.ui.numIn_Supression.currentText()]
                                    )
        except Exception as e:
            self.ui.numEp_Ajout.clear()
        else:
            display.refreshGenericCombo(self.ui.numEp_Modification, result)

    @pyqtSlot()
    def refreshNumEpCmbbox_Ajout(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct numEp FROM LesEpreuves NATURAL JOIN LesInscriptions WHERE numIn IS NOT ?",
                [self.ui.numIn_Ajout.currentText()]
                )
        except Exception as e:
            self.ui.numEp_Ajout.clear()
        else:
            display.refreshGenericCombo(self.ui.numEp_Ajout, result)

    @pyqtSlot()
    def refreshNumEpCmbbox_Modification(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesInscriptions WHERE numIn = ?",
                                    [self.ui.numIn_Modification.currentText()]
                                    )
        except Exception as e:
            self.ui.numEp_Modification.clear()
        else:
            display.refreshGenericCombo(self.ui.numEp_Modification, result)

    @pyqtSlot()
    def onClick_Ajout(self):

        try:
            cursor = self.data.cursor()
            cursor.execute("INSERT INTO  LesInscriptions(numIn,numEp) VALUES (?,?) ",
                           [self.ui.numIn_Ajout.currentText(), self.ui.numEp_Ajout.currentText()]
                           )

        except Exception as e:
            display.refreshLabel(self.ui.titre, "Erreur d'ajout dans la table")
