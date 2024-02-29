
from kivy.core.audio import SoundLoader


class SoundHelper:

    #ToDo: Richtige Pfade speichern
    SoundDict = { "Work": "workPath", "Home": "homePath", "Other": "OtherPath", "Custom": ""}
    selectedSound = ""

    def __init__(self) -> None:
        pass

    def SetSelectedSound(self, newPath="") -> None:
        self.selectedSoundPath = newPath
        

    #ToDo: Ausprogrammieren
    def SetCutstomSoundPath(self, path: str) -> None:
        pass



    #ToDo: Ausprogrammieren
    def GetCustomSoundPath(self) -> str:
        pass

    def PlaySound(self) -> None:

        sound = SoundLoader.load(self.selectedSound)
        if sound:
            sound.play()
    