import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppFctPart32Modif(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection, fct_part3_2):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part3_2_modif.ui", self)
        self.data = data
        self.numEp = fct_part3_2.ui.numEpModif.currentText()
        self.init()

    def init(self):
        display.refreshLabel(self.ui.label_fct_part3_2_modif, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEp FROM LesEpreuves")
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_part3_2_modif, "Impossible de récupérer les épreuves : " + repr(e))
            return
        else:
            display.refreshGenericCombo(self.ui.numEpModif, result)

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEq as numIn FROM LesEquipes UNION SELECT numSp as numIn FROM LesSportifs")
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_part3_2_modif, "Impossible de récupérer les participants : " + repr(e))
            return
        else:
            for row_num, row_data in enumerate(result):
                self.ui.orModif.addItem(str(row_data[0]))
                self.ui.argentModif.addItem(str(row_data[0]))
                self.ui.bronzeModif.addItem(str(row_data[0]))

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT gold, silver, bronze FROM LesResultats WHERE numEp = ?",
                [self.numEp]
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_part3_2_modif, "Impossible de récupérer les résultats : " + repr(e))
            return
        else:
            for row_num, row_data in enumerate(result):
                self.ui.orModif.setCurrentText(str(row_data[0]))
                self.ui.argentModif.setCurrentText(str(row_data[1]))
                self.ui.bronzeModif.setCurrentText(str(row_data[2]))

        self.ui.numEpModif.setCurrentText(self.numEp)

    @pyqtSlot()
    def modifierRes(self):
        display.refreshLabel(self.ui.label_fct_part3_2_modif, "")
        try:
            cursor = self.data.cursor()
            cursor.execute(
                "UPDATE LesResultats SET numEp = ?, gold = ?, silver = ?,  bronze = ? WHERE numEp = ?",
                [self.ui.numEpModif.currentText(), self.ui.orModif.currentText(), self.ui.argentModif.currentText(),
                 self.ui.bronzeModif.currentText(), self.numEp]
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_part3_2_modif, "Impossible de modifier le résultat : " + repr(e))
            return
        else:
            display.refreshLabel(self.ui.label_fct_part3_2_modif, "La modification a bien été effectuée")
