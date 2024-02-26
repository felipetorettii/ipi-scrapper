class NcmIpi:
    def __init__(self, ncm: str, aliquota: float):
        self.ncm = ncm
        self.aliquota = aliquota
    
    def __str__(self) -> str:
        return f"NCM: {self.ncm} | Alíquota: {self.aliquota}"