
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.data = data
        self.refreshCatList()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        # TODO 1.7 : fonction à modifier pour que l'équipe ne propose que des valeurs possibles pour le pays choisi
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        if self.ui.comboBox_fct_4_equipe.count() != 0:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "SELECT numSp, nomSp, prenomSp, categorieSp, dateNaisSp FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE pays = ? AND numEq=?",
                    [self.ui.comboBox_fct_4_pays.currentText(),self.ui.comboBox_fct_4_equipe.currentText()]
                )
            except Exception as e:
                self.ui.table_fct_comp_4.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")
        else:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

    def refreshCombobox(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT numEq FROM LesEquipiers JOIN LesSportifs USING(numSp) where pays= ?",
                [self.ui.comboBox_fct_4_pays.currentText()]
            )
        except Exception as e:
            self.ui.comboBox_fct_4_equipe.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_equipe, result)

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT pays FROM LesSportifs_base ORDER BY pays")
        except Exception as e:
            self.ui.comboBox_fct_4_pays.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_pays, result)
