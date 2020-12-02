import sqlite3

from actions.action_fct_part3_1_modif import AppFctPart31Modif
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppFctPart31(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part3_1.ui", self)
        self.data = data
        self.fct_part3_1_modif_dialog = None
        self.init()

    # Fonction de mise à jour de l'affichage

    def init(self):
        self.ui.numIn_Ajout.clear()
        self.ui.numIn_Modification.clear()
        self.ui.numIn_Suppression.clear()
        self.ui.numEp_Ajout.clear()
        self.ui.numEp_Modification.clear()
        self.ui.numEp_Suppression.clear()

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEq FROM LesEquipes UNION SELECT distinct numSp FROM LesSportifs ")
        except Exception as e:
            display.refreshLabel(self.ui.titre, "Impossible de récupérer les sportifs et les équipes pour l'ajout : " + repr(e))

        else:
            display.refreshGenericCombo(self.ui.numIn_Ajout, result)

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numIn FROM LesInscriptions")
        except Exception as e:
            display.refreshLabel(self.ui.titre, "Impossible de récupérer les sportifs et les équipes pour la modification / suppression : " + repr(e))

        else:
            for row_num, row_data in enumerate(result):
                self.ui.numIn_Modification.addItem(str(row_data[0]))
                self.ui.numIn_Suppression.addItem(str(row_data[0]))

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesEpreuves")
        except Exception as e:
            display.refreshLabel(self.ui.titre, "Impossible de récupérer les épreuves pour l'Ajout: " + repr(e))
        else:
            for row_num, row_data in enumerate(result):
                self.ui.numEp_Ajout.addItem(str(row_data[0]))

    @pyqtSlot()
    def changedModification(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesInscriptions WHERE numIn = ?",
                           [self.ui.numIn_Modification.currentText()]
                           )

        except Exception as e:
            display.refreshLabel(self.ui.titre, "Erreur de modification dans la table: " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.numEp_Modification, result)

    @pyqtSlot()
    def changedSuppression(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesInscriptions WHERE numIn = ?",
                                    [self.ui.numIn_Suppression.currentText()]
                                    )

        except Exception as e:
            display.refreshLabel(self.ui.titre, "Erreur de suppression dans la table: " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.numEp_Suppression, result)


    @pyqtSlot()
    def ajouterRes(self):

        try:
            cursor = self.data.cursor()
            cursor.execute("INSERT INTO  LesInscriptions(numIn,numEp) VALUES (?,?) ",
                           [self.ui.numIn_Ajout.currentText(), self.ui.numEp_Ajout.currentText()]
                           )

        except Exception as e:
            display.refreshLabel(self.ui.titre, "Erreur d'ajout dans la table: " + repr(e))
        else:
            display.refreshLabel(self.ui.titre, "L'ajout a bien été effectué")

    @pyqtSlot()
    def supprimerRes(self):

        try:
            cursor = self.data.cursor()
            cursor.execute("DELETE FROM LesInscriptions WHERE numIn = ? AND numEp = ? ",
                           [self.ui.numIn_Suppression.currentText(), self.ui.numEp_Suppression.currentText()]
                           )

        except Exception as e:
            display.refreshLabel(self.ui.titre, "Erreur de suppression dans la table: " + repr(e))
        else:
            display.refreshLabel(self.ui.titre, "Suppression effectuée")

    @pyqtSlot()
    def modifierRes(self):
        self.open_fct_part3_1_modif()

    def open_fct_part3_1_modif(self):
        if self.fct_part3_1_modif_dialog is not None:
            self.fct_part3_1_modif_dialog.close()
        self.fct_part3_1_modif_dialog = AppFctPart31Modif(self.data, self)
        self.fct_part3_1_modif_dialog.show()

    def closeEvent(self, event):
        if (self.fct_part3_1_modif_dialog is not None):
            self.fct_part3_1_modif_dialog.close()
