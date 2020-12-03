
import sqlite3


from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppFctPart31Modif(QDialog):

        # Constructeur
        def __init__(self, data: sqlite3.Connection, fct_part3_1):
            super(QDialog, self).__init__()
            self.myField = fct_part3_1
            self.ui = uic.loadUi("gui/fct_part3_1_modif.ui", self)
            self.data = data
            self.numEp = fct_part3_1.ui.numEp_Modification.currentText()
            self.numIn = fct_part3_1.ui.numIn_Modification.currentText()
            fct_part3_1.ui.numIn_Modification.clear()
            fct_part3_1.ui.numIn_Suppression.clear()
            self.init()


        def init(self):

            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                "SELECT distinct numEq FROM LesEquipes UNION SELECT distinct numSp FROM LesSportifs ")
            except Exception as e:
                display.refreshLabel(self.ui.titre,
                                        "Impossible de récupérer les sportifs et les équipes pour la modification : " + repr(e))

            else:
                for row_num, row_data in enumerate(result):
                    self.ui.numIn_Modification.addItem(str(row_data[0]))
                self.ui.numIn_Modification.setCurrentText(self.numIn)

            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT distinct numEp FROM LesEpreuves")
            except Exception as e:
                display.refreshLabel(self.ui.titre,"Impossible de récupérer les sportifs et les équipes pour l'ajout : " + repr(e))

            else:
                for row_num, row_data in enumerate(result):
                    self.ui.numEp_Modification.addItem(str(row_data[0]))
                self.ui.numEp_Modification.setCurrentText(self.numEp)





        @pyqtSlot()
        def modifierRes(self):
            try:
                from actions.action_fct_part3_1 import AppFctPart31
                cursor = self.data.cursor()
                cursor.execute("UPDATE LesInscriptions SET numEp = ?, numIn = ? WHERE numEp = ? AND numIn = ?",
                    [self.ui.numEp_Modification.currentText(), self.ui.numIn_Modification.currentText(),
                      self.numEp, self.numIn]
                )
            except Exception as e:
                display.refreshLabel(self.ui.titre, "Impossible de modifier l'inscription ")
            else:
                display.refreshLabel(self.ui.titre, "La modification a bien été effectuée")
                self.ui.bouton_Modification.setEnabled(False)


