
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppFctPart312(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part3_1_2.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_part2_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT pays, SUM(nbOr) as nbOr, SUM(nbArgent) as nbArgent, SUM(nbBronze) as nbBronze FROM "
                                    
                                    "(SELECT P.pays, COUNT(G.gold) as nbOr, 0 as nbArgent, 0 as nbBronze "
                                    "FROM (SELECT DISTINCT pays FROM LesSportifs) P "
                                    "LEFT JOIN (SELECT S.pays as gold FROM LesResultats R JOIN LesSportifs S ON R.gold=S.numSp) G ON P.pays=G.gold "
                                    "GROUP BY P.pays "
                                    "UNION ALL "
                                    "SELECT P.pays, 0 as nbOr, COUNT(S.silver) as ngArgent, 0 as nbBronze "
                                    "FROM (SELECT DISTINCT pays FROM LesSportifs) P "
                                    "LEFT JOIN (SELECT S.pays as silver FROM LesResultats R JOIN LesSportifs S ON R.silver=S.numSp) S ON P.pays=S.silver "
                                    "GROUP BY P.pays "
                                    "UNION ALL "
                                    "SELECT P.pays, 0 as nbOr, 0 as ngArgent, COUNT(B.bronze) as nbBronze "
                                    "FROM (SELECT DISTINCT pays FROM LesSportifs) P "
                                    "LEFT JOIN (SELECT S.pays as bronze FROM LesResultats R JOIN LesSportifs S ON R.bronze=S.numSp) B ON P.pays=B.bronze "
                                    "GROUP BY P.pays "
                                    
                                    "UNION ALL "
                                    
                                    "SELECT P.pays, COUNT(G.gold) as nbOr, 0 as nbArgent, 0 as nbBronze "
                                    "FROM (SELECT DISTINCT pays FROM LesSportifs) P "
                                    "LEFT JOIN (SELECT E.pays as gold FROM LesResultats R JOIN (SELECT DISTINCT numEq, pays FROM LesEquipiers JOIN LesSportifs USING(numSp)) E ON R.gold=E.numEq) G ON P.pays=G.gold "
                                    "GROUP BY P.pays "
                                    "UNION ALL "
                                    "SELECT P.pays, 0 as nbOr, COUNT(S.silver) as nbArgent, 0 as nbBronze "
                                    "FROM (SELECT DISTINCT pays FROM LesSportifs) P "
                                    "LEFT JOIN (SELECT E.pays as silver FROM LesResultats R JOIN (SELECT DISTINCT numEq, pays FROM LesEquipiers JOIN LesSportifs USING(numSp)) E ON R.silver=E.numEq) S ON P.pays=S.silver "
                                    "GROUP BY P.pays "
                                    "UNION ALL "
                                    "SELECT P.pays, 0 as nbOr, 0 as nbArgent, COUNT(B.bronze) as nbBronze "
                                    "FROM (SELECT DISTINCT pays FROM LesSportifs) P "
                                    "LEFT JOIN (SELECT E.pays as bronze FROM LesResultats R JOIN (SELECT DISTINCT numEq, pays FROM LesEquipiers JOIN LesSportifs USING(numSp)) E ON R.bronze=E.numEq) B ON P.pays=B.bronze "
                                    "GROUP BY P.pays) "
                                    
                                    "GROUP BY pays ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC")
        except Exception as e:
            self.ui.table_fct_part2_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_part2_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_part2_1, result)