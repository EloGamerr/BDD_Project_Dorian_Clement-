import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from actions.action_fct_part3_2_modif import AppFctPart32Modif

class AppFctPart32(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part3_2.ui", self)
        self.data = data
        self.fct_part3_2_modif_dialog = None
        self.init(True)

    def init(self, updateLabel):
        self.ui.numEpAjout.clear()
        self.ui.orAjout.clear()
        self.ui.argentAjout.clear()
        self.ui.bronzeAjout.clear()
        self.ui.numEpModif.clear()
        self.ui.numEpSupp.clear()

        if updateLabel:
            display.refreshLabel(self.ui.label_fct_part3_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEp FROM LesEpreuves")
        except Exception as e:
            if updateLabel:
                display.refreshLabel(self.ui.label_fct_part3_2, "Impossible de récupérer les épreuves : " + repr(e))
            return
        else:
            display.refreshGenericCombo(self.ui.numEpAjout, result)

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEq as numIn FROM LesEquipes UNION SELECT numSp as numIn FROM LesSportifs")
        except Exception as e:
            if updateLabel:
                display.refreshLabel(self.ui.label_fct_part3_2, "Impossible de récupérer les participants : " + repr(e))
            return
        else:
            for row_num, row_data in enumerate(result):
                self.ui.orAjout.addItem(str(row_data[0]))
                self.ui.argentAjout.addItem(str(row_data[0]))
                self.ui.bronzeAjout.addItem(str(row_data[0]))

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEp FROM LesResultats")
        except Exception as e:
            if updateLabel:
                display.refreshLabel(self.ui.label_fct_part3_2, "Impossible de récupérer les résultats : " + repr(e))
            return
        else:
            for row_num, row_data in enumerate(result):
                self.ui.numEpModif.addItem(str(row_data[0]))
                self.ui.numEpSupp.addItem(str(row_data[0]))

    @pyqtSlot()
    def ajouterRes(self):
        display.refreshLabel(self.ui.label_fct_part3_2, "")
        try:
            cursor = self.data.cursor()
            cursor.execute(
                "INSERT INTO LesResultats (numEp, gold, silver, bronze) VALUES (?, ?, ?, ?)",
                [self.ui.numEpAjout.currentText(), self.ui.orAjout.currentText(), self.ui.argentAjout.currentText(), self.ui.bronzeAjout.currentText()]
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_part3_2, "Impossible d'ajouter le résultat' : " + repr(e))
            return
        else:
            display.refreshLabel(self.ui.label_fct_part3_2, "L'ajout a bien été effectué")
            self.init(False)

    @pyqtSlot()
    def ouvrirModifierRes(self):
        self.open_fct_part3_2_modif()

    @pyqtSlot()
    def supprimerRes(self):
        display.refreshLabel(self.ui.label_fct_part3_2, "")
        try:
            cursor = self.data.cursor()
            cursor.execute(
                "DELETE FROM LesResultats WHERE numEp = ?",
                [self.ui.numEpSupp.currentText()]
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_part3_2, "Impossible de supprimer le résultat : " + repr(e))
            return
        else:
            display.refreshLabel(self.ui.label_fct_part3_2, "La suppression a bien été effectuée")
            self.init(False)

    def open_fct_part3_2_modif(self):
        if self.fct_part3_2_modif_dialog is not None:
            self.fct_part3_2_modif_dialog.close()
        self.fct_part3_2_modif_dialog = AppFctPart32Modif(self.data, self)
        self.fct_part3_2_modif_dialog.show()

    def closeEvent(self, event):
        if (self.fct_part3_2_modif_dialog is not None):
            self.fct_part3_2_modif_dialog.close()
