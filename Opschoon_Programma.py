import numpy as np
import pandas as pd
import seaborn as sns

import plotly.graph_objects as go
from plotly.offline import plot

from datetime import datetime
import plotly.express as px
import streamlit as st

import urllib.request 
import urllib.parse

import requests
import json

#___________________________________________________________________________________________________________
# Import laadpaaldata & rdw data
laadpaaldata = pd.read_csv("laadpaaldata.csv")
rdw = pd.read_csv("Elektrische_voertuigen.csv") #rdw https://opendata.rdw.nl/Voertuigen/Elektrische-voertuigen/w4rt-e856
#___________________________________________________________________________________________________________
# laadpaaldata information to datetime

laadpaaldata = laadpaaldata.replace(to_replace = r"^2018-02-29", value = "2018-03-01", regex = True)

laadpaaldata["Started"] = pd.to_datetime(laadpaaldata["Started"])
laadpaaldata["Ended"] = pd.to_datetime(laadpaaldata["Ended"])

# Start (month & day)
laadpaaldata["Month_Started"] = pd.to_datetime(laadpaaldata["Started"]).dt.month
laadpaaldata["Day_started"] = pd.to_datetime(laadpaaldata["Started"]).dt.day
# End (month & day)
laadpaaldata["Month_Ended"] = pd.to_datetime(laadpaaldata["Ended"]).dt.month
laadpaaldata["Day_Ended"] = pd.to_datetime(laadpaaldata["Ended"]).dt.day

# Dagnamen
started = laadpaaldata['Started']
ended = laadpaaldata['Ended']
started = started.replace(to_replace=r'^2018-02-29',value='2018-03-01',regex=True)
ended = ended.replace(to_replace=r'^2018-02-29',value='2018-03-01',regex=True)

started = pd.to_datetime(started)
dagnaamstarted = started.dt.day_name()

ended = pd.to_datetime(ended)
dagnaamended = ended.dt.day_name()

laadpaaldata = laadpaaldata.merge(dagnaamstarted,left_index=True,right_index=True)
laadpaaldata = laadpaaldata.merge(dagnaamended,left_index=True,right_index=True)

#___________________________________________________________________________________________________________

# tijd niet opgeladen maar wel aan paal
laadpaaldata["Onnodig_gebruik"] = laadpaaldata["ConnectedTime"] - laadpaaldata["ChargeTime"]
laadpaaldata.drop(laadpaaldata[laadpaaldata["Onnodig_gebruik"] < 0].index, inplace = True)


#gemiddeld vermogen
laadpaaldata["gem_vermogen"] = laadpaaldata["TotalEnergy"]/laadpaaldata["ChargeTime"]
laadpaaldata.drop(laadpaaldata[laadpaaldata["ChargeTime"] < 0].index, inplace = True)



# #___________________________________________________________________________________________________________

# # optellen TotalEnergy per dag
# laadpaaldata["TotalEnergy_p_day"] = laadpaaldata.groupby("Date").agg({"TotalEnergy": "cumsum"})




#___________________________________________________________________________________________________________
#rdw Data inladen en opschonen

rdw.dropna(how='all', axis=1, inplace=True)

rdw.drop(['Voertuigsoort', 'Vervaldatum APK', 'Datum tenaamstelling', 'Bruto BPM', 'Tweede kleur', 'Massa ledig voertuig', 'Toegestane maximum massa voertuig',
          'Maximum massa trekken ongeremd', 'Maximum trekken massa geremd', 'Datum eerste toelating', 'Datum eerste tenaamstelling in Nederland',
          'Wacht op keuren', 'WAM verzekerd', 'Aantal wielen', 'Afstand hart koppeling tot achterzijde voertuig', 'Afstand voorzijde voertuig tot hart koppeling',
          'Europese voertuigcategorie', 'Plaats chassisnummer', 'Technische max. massa voertuig', 'Type', 'Type gasinstallatie', 'Typegoedkeuringsnummer',
          'Variant', 'Uitvoering', 'Volgnummer wijziging EU typegoedkeuring', 'Openstaande terugroepactie indicator', 'Maximum massa samenstelling',
          'Tellerstandoordeel', 'Code toelichting tellerstandoordeel', 'API Gekentekende_voertuigen_assen', 'Tenaamstellen mogelijk',
          'API Gekentekende_voertuigen_brandstof', 'API Gekentekende_voertuigen_carrosserie', 'Datum tenaamstelling DT', 'Datum eerste toelating DT',
          'API Gekentekende_voertuigen_carrosserie_specifiek', 'API Gekentekende_voertuigen_voertuigklasse', 'Verticale belasting koppelpunt getrokken voertuig',
          'Zuinigheidsclassificatie', 'Registratie datum goedkeuring (afschrijvingsmoment BPM)', 'Registratie datum goedkeuring (afschrijvingsmoment BPM) DT'],
         axis=1, inplace=True)

rdw["Vervaldatum APK DT"] = pd.to_datetime(rdw["Vervaldatum APK DT"])
rdw["Datum eerste tenaamstelling in Nederland DT"] = pd.to_datetime(rdw["Datum eerste tenaamstelling in Nederland DT"])


rdw['Merk'] = rdw['Merk'].replace(to_replace='FORD-CNG-TECHNIK',value='FORD')
rdw['Merk'] = rdw['Merk'].replace(to_replace='VOLKSWAGEN/ZIMNY',value='VOLKSWAGEN')
rdw['Merk'] = rdw['Merk'].replace(to_replace='BMW I',value='BMW')
rdw['Merk'] = rdw['Merk'].replace(to_replace='TESLA MOTORS',value='TESLA')
rdw['Merk'] = rdw['Merk'].replace(to_replace='MERCEDES-BENZ',value='MERCEDES')




#___________________________________________________________________________________________________________

# Locaties van laadpalen

key = "****"
countrycode = "NL"
boundingbox = "(53.560680765620994, 3.3583705373916324),(50.75134410042465, 7.225878100867432)" #boxing rondom Amsterdam
url = f"https://api.openchargemap.io/v3/poi/?key={key}?output=json&countrycode={countrycode}&&maxresults=8000&boundingbox={boundingbox}&town=amsterdamt&compact=true&verbose=false"

parameters = {
key: "****",
countrycode: "NL",
boundingbox: "(53.560680765620994, 3.3583705373916324),(50.75134410042465, 7.225878100867432)"}

response = requests.get(url, params=parameters)
data = json.loads(response.content)

df = pd.DataFrame(data[1:],columns=data[0])
df = pd.json_normalize(data, max_level = 3)

df.drop(['UUID', 'GeneralComments', 'AddressInfo.ContactTelephone1', 'AddressInfo.StateOrProvince', 'AddressInfo.AddressLine2','AddressInfo.AccessComments', 'AddressInfo.ContactEmail', 'MetadataValues'],axis=1, inplace=True)

#___________________________________________________________________________________________________________
# Export clean dataframes (csv)

laadpaaldata.to_csv("lp_data.csv")
rdw.to_csv("rdw_data.csv")
df.to_csv('opencharge_data.csv')

#___________________________________________________________________________________________________________