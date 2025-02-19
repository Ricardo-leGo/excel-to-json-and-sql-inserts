
import json
import math
from dotenv import load_dotenv

import os 

import pandas as pd

load_dotenv()

class Aplicativo:
    
    def __init___( self, Id, DisplayName ):
        self.Id=Id
        self.DisplayName = DisplayName
        
class AplicativoToinsert():
    
    def __init__(self, Aplicativos,  Estatus, Salud, Peso, Factor ):
        self.Aplicativos = Aplicativos
        self.Estatus = Estatus
        self.Salud =  f"{Salud}"
        self.Peso =  Peso
        self.Factor =  Factor
        
    def Createobj(self):
        return {
            "Aplicativos":self.Aplicativos,
            "Estatus": self.Estatus, 
            "Salud":self.Salud, 
            "Peso":self.Peso,
            "Factor":self.Factor
        }


FileName= os.getenv("FileName")

CatalogJson  = os.getenv("CatlogJson")

_relativePath =  os.path.dirname(os.path.abspath(__file__))
print(_relativePath)
mainPathFile = os.path.join(_relativePath, FileName)
print(mainPathFile)
jsonpathfile = os.path.join(_relativePath, CatalogJson)

def readfile():
    try:
        return pd.read_excel(mainPathFile)
    except Exception as e:
        print(f"Error al leer el archivo excel: {e}")
        return None


def readjson():
   with open(jsonpathfile, "r", encoding="utf-8") as file:
        return json.load(file)

jsonfile =  readjson()
rd =  readfile()

rowstring = ""


EstatusNuevos = []
 
def SetEstatus(Id, Estatus):
    

     EachAplicativo = Aplicativo()
     EachAplicativo.DisplayName = Estatus
     EachAplicativo.Id= Id
     
     
     if Id > 7 and  Estatus not in EstatusNuevos:
        EstatusNuevos.append(Estatus)         
     
     return EachAplicativo


def SetNewAplicativoJson(Aplicativos, Estatus, Salud, Peso, Factor):
    return AplicativoToinsert( Aplicativos, Estatus,Salud, Peso, Factor)

    


rowstring = ""

AplicativosJson = []

with open( os.path.join(_relativePath,  "resultado.json"), "w", encoding="utf-8") as insertjson:
    

    
    for index, row in rd.iterrows():
        
        EstatusObj = next(( SetEstatus(item["Id"], item["DisplayName"])  for item in jsonfile if item["DisplayName"] == row["Estatus"] ), SetEstatus(8, "Desarrollo") )
        
        Aplicativos = row["Applications"]
        Estatus = EstatusObj.DisplayName
        Salud =  0 if math.isnan( row["Salud"] ) else row["Salud"]
        Peso = 0 if row["Peso"]=="TBD" else row["Peso"]
        Factor =  Peso*Salud 
        
        print(Peso, Salud, Factor, Aplicativos)
        
        AplicativosJson.append( AplicativoToinsert( Aplicativos, Estatus,Salud, Peso, Factor) )
        
        
        rowstring += f"\nINSERT INTO Aplicativos ([Nombre], [Salud], Peso, Factor, IdEstatusAplicativoFK, Activa, Fecha) Values ('{Aplicativos}','{Salud}',{Peso},{Factor},{EstatusObj.Id},1, CURRENT_TIMESTAMP)"
        
    datadict = [ item.Createobj()  for item in AplicativosJson]
    
    
    insertjson.write( json.dumps(datadict, indent=4) ) 
    

with open( os.path.join(_relativePath,  "insertsql.sql"), "w", encoding="utf-8") as insertsql:
    insertsql.write( rowstring ) 