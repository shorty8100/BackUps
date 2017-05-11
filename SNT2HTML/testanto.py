from SNT2CSV import *

sino = Sinoptico()
sino.carregarSNT("Sinop - Condidicionantes.snt") # Ou sino.abrir("MenuPrincipal.snt", "01")
sino.SAVEasCSV()
sino.SAVEasSNT()

#**********************************************************************************

