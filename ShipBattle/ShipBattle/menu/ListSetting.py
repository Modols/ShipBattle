class ListSetting():
    def __init__(self, liste, settingsListName):
        self.liste = liste
        self.settingsListName = settingsListName
        self.boatNumber = 3
        self.boatPngName = f"ship ({self.boatNumber})"
        self.listeSettingsAndName = []
        self._stockSettingsAttributes()

    def _stockSettingsAttributes(self):
        tmpListe = [self.boatNumber, "BOATNUMBER"]
        self.listeSettingsAndName.append(tmpListe)

        for idx, setting in enumerate(self.liste):
            if idx == 0:
                pass
            else:
                tmpListe = [self.liste[idx], self.settingsListName[idx-1]]
                self.listeSettingsAndName.append(tmpListe)

        tmpListe = ["NOT READY", "ACCEPTER"]
        self.listeSettingsAndName.append(tmpListe)
            
    def formatListeForBddUpdate(self):
        tmpListe = self.listeSettingsAndName
        data = [tmpListe[1][0],
                tmpListe[2][0],
                tmpListe[3][0],
                tmpListe[4][0],
                tmpListe[5][0],
                tmpListe[6][0],
                1,
        ]
        return data
