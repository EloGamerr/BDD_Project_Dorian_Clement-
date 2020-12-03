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

        # Chargements des inscrits
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct numEq FROM LesEquipes UNION SELECT distinct numSp FROM LesSportifs ")
        except Exception :
            display.refreshLabel(self.ui.titre, "Impossible de récupérer les sportifs et les équipes pour l'ajout")

        else:
            display.refreshGenericCombo(self.ui.numIn_Ajout, result)

        # Chargements des epreuves
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numEp FROM LesEpreuves")
        except Exception :
            display.refreshLabel(self.ui.titre, "Impossible de récupérer les épreuves")
        else:
            for row_num, row_data in enumerate(result):
                self.ui.numEp_Ajout.addItem(str(row_data[0]))
                self.ui.numEp_Modification.addItem(str(row_data[0]))
                self.ui.numEp_Suppression.addItem(str(row_data[0]))

        #Chargement des Inscrits de l'épreuve sélectionnée



    @pyqtSlot()
    def changedModification(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numIn FROM LesInscriptions WHERE numEp = ?",
                                    [self.ui.numEp_Modification.currentText()])

        except Exception as e:
            display.refreshLabel(self.ui.titre, "Erreur de chargement des champs modification : Inscrits" )
        else:
            display.refreshGenericCombo(self.ui.numIn_Modification, result)

    @pyqtSlot()
    def changedSuppression(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct numIn FROM LesInscriptions WHERE numEp = ?",
                                    [self.ui.numEp_Suppression.currentText()]
                                    )

        except Exception:
            display.refreshLabel(self.ui.titre, "Erreur de chargement des champs suppression : Inscrits")
        else:
            display.refreshGenericCombo(self.ui.numIn_Suppression, result)

    @pyqtSlot()
    def ajouterRes(self):

        try:
            cursor = self.data.cursor()
            cursor.execute("INSERT INTO  LesInscriptions(numIn,numEp) VALUES (?,?) ",
                           [self.ui.numIn_Ajout.currentText(), self.ui.numEp_Ajout.currentText()]
                           )

        except Exception:
            display.refreshLabel(self.ui.titre, "Attention, cette inscription existe déjà ")
        else:
            display.refreshLabel(self.ui.titre, "L'inscription à été ajoutée")
            self.changedSuppression()
            self.changedModification()

    @pyqtSlot()
    def supprimerRes(self):
        if self.ui.numIn_Suppression.currentText() != "":
            try:
                cursor = self.data.cursor()
                cursor.execute("DELETE FROM LesInscriptions WHERE numIn = ? AND numEp = ? ", [self.ui.numIn_Suppression.currentText(), self.ui.numEp_Suppression.currentText()])

            except Exception :
                display.refreshLabel(self.ui.titre, "Erreur de suppression dans la table ")
            else:
                display.refreshLabel(self.ui.titre, "Suppression effectuée")
                self.changedSuppression()
                self.changedModification()
        else:
            display.refreshLabel(self.ui.titre, "Il n'y a rien à supprimer")

    @pyqtSlot()
    def modifierRes(self):
        if self.ui.numIn_Modification.currentText() != "":
            self.open_fct_part3_1_modif()
        else:
            display.refreshLabel(self.ui.titre, "Veuillez choisir un numéro d'inscrit ET un numéro d'épreuve")

    def open_fct_part3_1_modif(self):
        if self.fct_part3_1_modif_dialog is not None:
            self.fct_part3_1_modif_dialog.close()
        self.fct_part3_1_modif_dialog = AppFctPart31Modif(self.data, self)
        self.fct_part3_1_modif_dialog.show()

    def close(self):
        if (self.fct_part3_1_modif_dialog is not None):
            self.fct_part3_1_modif_dialog.close()

