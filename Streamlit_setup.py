# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:02:46 2022

@author: lpnnr
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

laadpaaldata = pd.read_csv("lp_data.csv", sep = ",")
rdw = pd.read_csv("rdw_data.csv", sep = ",")
ocm = pd.read_csv("opencharge_data.csv" , sep = ",")



# object naar datetime
laadpaaldata["Started_x"] = pd.to_datetime(laadpaaldata["Started_x"])
laadpaaldata["Month_Started"] = pd.to_datetime(laadpaaldata["Started_x"]).dt.month


# Aanmaken nieuwe dataframe per maand(nummer)
df = laadpaaldata.groupby("Month_Started").agg({"Started_x":"count"})
df = df.reset_index()

# Lijndiagram aanmaken (fig) via plotly
fig = go.Figure()

fig.add_trace(go.Scatter(x = df["Month_Started"], y = df["Started_x"], mode = "lines"))


# toevoegen van title en as benamingen (go.Figure())
fig.update_layout(
    title = "Som van het gebruik van laadpalen per maand",
    xaxis_title = "Maanden",
    yaxis_title = "Gebruikt aantal keer laadpaal",
)

st.header("Som van het gebruik van laadpalen per maand")

# Creeëren van fig in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Text wat op streamlit zichbaar wordt over laadpaaldata
st.write("Er is in 2018 totaal 10.109 keer gebruik gemaakt van de laadpalen.")


#___________________________________________________________________________________________________________
# Plotly staafdiagram (bar chart) voor de totale som van het aantal keer dat een laadpaal is gebruikt per dag van de week

# Schrijven van een beetje text op streamlit over de staafdiagram
# st.write("Ook kan er per dag van de week aangegeven worden hoevaak ze zijn gebruikt, zoals te zien is in de staafdiagram.")

st.header("Totaal aantal keer gebruik van laadpalen in 2018 weergegeven per dag")

# Het aanmaken van een nieuwe dataset genaamd laadpaal_per_dag voor het totaal gebruik van de laadpalen per dag in de week
MaZo = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
laadpaal_per_dag = laadpaaldata.groupby("Started_y").agg({"Started_x":"count"}).reset_index()
laadpaal_per_dag = laadpaal_per_dag.groupby(laadpaal_per_dag["Started_y"]).mean().reindex(MaZo)
laadpaal_per_dag = laadpaal_per_dag.reset_index()

# Stellen van het aantal dagen (van de week) in 2018
laadpaaldata["Year_Month_Day"] = laadpaaldata["Started_x"].dt.strftime("%Y-%m-%d")
x = laadpaaldata.groupby('Started_y')['Year_Month_Day'].nunique()
# x = x.groupby(x["Started_y"]).mean().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
x = x.reset_index()


# Het samenvoegen van laadpaal_data_per_dag en x
laadpaal_per_dag = laadpaal_per_dag.merge(x, on = "Started_y", how = "left")
# Veranderen van de benaming van de kolomen van het dataframe laatpaal_per_dag
laadpaal_per_dag.set_axis(["Weekday", "Total_count", "Count_Amount_Of_Days"], axis = 1, inplace = True)

# Aanmaken figuur voor staafdiagram (fig6)
fig6 = go.Figure()
fig6.add_trace(go.Bar(x = laadpaal_per_dag["Weekday"], y = laadpaal_per_dag["Total_count"],
                      hovertext = laadpaal_per_dag["Count_Amount_Of_Days"] ))

# Veranderen van de kleur van de staven
fig6.update_traces(marker_color='rgb(66, 245, 170)')

# Toevoegen title en benaming van assen
fig6.update_layout(
    title = "Totaal aantal keer gebruik van laadpalen in 2018 weergegeven per dag",
    xaxis_title = "Dagen",
    yaxis_title = "Gebruikt aantal keer laadpaal",
)


# Creeëren van fig6 in Streamlit
st.plotly_chart(fig6, use_container_width=True)

# Toevoegen van wat text op streamlit over fig6
# st.write("De hoeverdata die zichtbaar wordt wanneer je er met je muis op blijft hangen laat zien welke dag van de week het is, hoevaak de laadpalen gebruikt zijn op die dag binnen haakjes en hoevaak de dag  is voorgekomen in het jaar")

#___________________________________________________________________________________________________________
## Plotly lijndiagram van het aantal voertuigen per maand, rdw data(met as-benamingen en titel)

# Streamlit info
st.header("Aantal aangeschafte elektrische en hybride voertuigen")


# Veranderen naar datetime 
rdw["Vervaldatum APK DT"] = pd.to_datetime(rdw["Vervaldatum APK DT"])
rdw["Datum eerste tenaamstelling in Nederland DT"] = pd.to_datetime(rdw["Datum eerste tenaamstelling in Nederland DT"])
# Aanmaken kkolomen met jaar, maand en jaar+maand
rdw["Jaar"] = pd.to_datetime(rdw["Datum eerste tenaamstelling in Nederland DT"]).dt.year
rdw["Maand"] = pd.to_datetime(rdw["Datum eerste tenaamstelling in Nederland DT"]).dt.month
rdw["Jaar_Maand"] = rdw["Datum eerste tenaamstelling in Nederland DT"].dt.strftime("%Y-%m")

# Het maken van een nieuwe dataframe met data per "Jaar_Maand"
df2 = rdw.groupby("Jaar_Maand").agg({"Datum eerste tenaamstelling in Nederland DT":"count"})
df2 = df2.reset_index()
# Creëren van de kolom met jaar
df2["Jaar"] = pd.to_datetime(df2["Jaar_Maand"]).dt.year
df2 = df2.drop(df2[df2['Jaar'] <= 1999].index)



# Aanmaken van een lijndiagram (fig2) van de jaren en maanden over het aantal voertuigen
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x = df2["Jaar_Maand"], y = df2["Datum eerste tenaamstelling in Nederland DT"], mode = "lines + markers"))

# Toevoegen van titel en as benamingen voor fig2
fig2.update_layout(
    title = "Som van voertuigen per maand",
    xaxis_title = "Maanden",
    yaxis_title = "Aantal voertuigen")

# Het creeëren en toevoegen aan fig2 van een tweeslider
fig2.update_layout(xaxis=dict(autorange=True, range=["2000-01-01", "2022-12-31"],
                             rangeslider= dict(autorange=True, range=["2000-01-01", "2022-12-31"], visible=True), 
                             type="date"))



#extra tijd? Ja, dan maken dropdown of buttons voor veranderen zichtbare jaren in de plot

# Creeëren van fig2 in Streamlit
st.plotly_chart(fig2, use_container_width=True)


#___________________________________________________________________________________________________________
## Plotly histogram van laadtijd (met as-benaming en titel + annotatie van gemiddelde en mediaan + benadering van kansdichtheidsfunctie)

# Streamlit info (als het nodig is)
st.header("Oplaadtijden")



# Verwijderen van outliers
laadpaaldata = laadpaaldata.drop(laadpaaldata[laadpaaldata["ChargeTime"] >= 40].index)
laadpaaldata = laadpaaldata.drop(laadpaaldata[laadpaaldata["ConnectedTime"] >= 40].index)

# Gemiddelde en mediaan berekenen
gem_charge = laadpaaldata["ChargeTime"].mean()
med_charge = laadpaaldata["ChargeTime"].median()

# Histogram maken (fig3) over laadtijden
fig3 = go.Figure()

# Toevoegen van de histogram data aan fig3
fig3.add_trace(go.Histogram(x = laadpaaldata["ConnectedTime"], name = "Totale tijd aan de laadpaal (uur)"))
fig3.add_trace(go.Histogram(x = laadpaaldata["ChargeTime"], name = "Totale tijd geladen (uur)"))

# Toevoegen annotatie voor het gemiddelde en mediaan
fig3.update_layout(
    annotations=[
        dict(text="Gemiddelde = 2.477", 
             showarrow = False,
             x = 30,
             y = 800),
        dict(text="Mediaan = 2.234", 
             showarrow = False,
             x = 30,
             y = 750)
    ]
)



# toevoegen van title en as benaminge
fig3.update_layout(
    title = "Histogram van laadtijden",
    xaxis_title = "Laadtijden (uur)",
    yaxis_title = "Aantalen",
    legend_title = "Verschillende data",
)

# Creeëren van fig3 in Streamlit
st.plotly_chart(fig3, use_container_width=True)
#___________________________________________________________________________________________________________
# Plotly histogram van onnodig aan laadpaal hangen

# Streamlit info (als het nodig is)
st.header("Onnodig aan de laadpaal hangen")

#weghalen van outliers
laadpaaldata0 = laadpaaldata.drop(laadpaaldata[laadpaaldata["Onnodig_gebruik"] >= 20].index)
# laadpaaldata0["Onnodig_gebruik"] = laadpaaldata0["Onnodig_gebruik"] * 60
# Het maken van de histogram (fig4) over onnodig aan de laadpaal hangen
fig4 = go.Figure()
fig4.add_trace(go.Histogram(x = laadpaaldata["Onnodig_gebruik"], name = "Gehele dataset"))
fig4.add_trace(go.Histogram(x = laadpaaldata0["Onnodig_gebruik"], name = "Zonder uitschieters"))

fig4.update_traces(xbins_start= 0 )
# toevoegen van title en as benaminge
fig4.update_layout(
    title = "Histogram over het onnodig verbonden zijn met laadpalen in uren",
    xaxis_title = "Laadtijden (uur)",
    yaxis_title = "Aantalen",
    legend_title = "Verschillende data")


# Creeëren van fig4 in Streamlit
st.plotly_chart(fig4, use_container_width=True)


st.header("Totaal aantal autos verkocht over de jaren per merk")

fig8 = px.ecdf(rdw, x = 'Datum eerste tenaamstelling in Nederland DT', color = 'Merk', ecdfnorm=None)



fig8.update_layout(xaxis = dict(autorange=False, range=["2015-01-01", "2022-12-31"],
                             rangeslider= dict(autorange=True, range=["2015-01-01", "2022-12-31"], visible=True),
                             type="date"))



st.plotly_chart(fig8,use_container_width=True)




#___________________________________________________________________________________________________________
st.header("Hoeveelheid automerken totaal verkocht")

hoeveelheidmerken = rdw['Merk'].value_counts()
hoeveelheidmerken = hoeveelheidmerken.iloc[::-1]

hoeveelheidmerken = pd.DataFrame(hoeveelheidmerken)
hoeveelheidmerken.reset_index(inplace=True)

tig2 = go.Figure()
tig2.add_trace(go.Bar(y=hoeveelheidmerken['Merk'],x=hoeveelheidmerken['index']))
tig2.update_yaxes(type="log")

st.plotly_chart(tig2,use_container_width=True)


#___________________________________________________________________________________________________________









#___________________________________________________________________________________________________________

st.header("interactieve map van alle laadpalen OpenChargeMap")

kaart = px.scatter_mapbox(ocm, lat=ocm["AddressInfo.Latitude"], lon=ocm["AddressInfo.Longitude"], hover_name="ID", hover_data=["AddressInfo.Title", "AddressInfo.Town" ],
                        color_discrete_sequence=["fuchsia"], zoom=10, height=1000, title = "Map Laadpaal")
kaart.update_layout(mapbox_style="open-street-map")
kaart.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



st.plotly_chart(kaart)
