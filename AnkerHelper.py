class AnkerHelper:

    def __init__(self) -> None:
        self.ankerRadius = 0
        self.ankerPosition = ""
        self.currentShipPosition = ""

    def GetAnkerRadius(self) -> int:
        return self.ankerRadius
    
    def SetAnkerRadius(self, newRadius: int) -> None:
        self.ankerRadius = newRadius 

    def GetAnkerPosition(self) -> str:
        return self.ankerPosition
    
    def SetAnkerPosition(self, newPosition: str) -> None:
        self.ankerPosition = newPosition
    
    def GetShipPosition(self) -> str:
        return self.currentShipPosition
    
    def SetShipPosition(self, newPosition: str) -> None:
        self.currentShipPosition = newPosition

    #ToDo: Ausprogrammieren => Zuerst herausfinden, wie mit Koordinaten gerechnet wird
    def CheckIfShipInRadius(self) -> bool:
        return False

    