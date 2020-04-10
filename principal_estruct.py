import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#Function to get population by country name "Data Source","World Development Indicators",
#Not Used
def population_by_country(country):
    df = pd.read_csv("data/population_worldwide.csv", skiprows=4)
    df = df.loc[df['Country Name'] == country]
    return df

#Function to recover COVID19 cases by country
#Data Source: European Centre for Disease Prevention and Contro
def covid19cases_by_country(country,min_total_cases):
    ##Choose data source online or offline
    #df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    df = pd.read_csv("data/06_04_2020.csv")
    #Recover rows by country name
    df = df.loc[df['countriesAndTerritories'] == country]
    #Apply reverse to dataframe
    df = df.iloc[::-1]
    #Create row of total_cases
    df = df.assign(total_cases=df.cases.cumsum())
    #Choose rows with total_cases > min_total_cases
    df = df[df['total_cases'] > min_total_cases]
    return df
#graph cases and total_cases vs date
def graph_cases_by_country(country,min_total_cases):
    df = covid19cases_by_country("Mexico",min_total_cases)
    df.plot(kind='bar',x='dateRep',y='cases',color='blue')
    ax1 = plt.gca()
    ax1.set_ylabel('Infected by day')
    ax1.set_xlabel("Days with virus over " + str(min_total_cases) +" cases"+"\n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")
    df.plot(kind='bar',x='dateRep',y='cases',color="blue",ax=ax1)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Total of infected')
    df.plot(kind='line',x='dateRep',y='total_cases', color='red', ax=ax2)
    plt.tight_layout()
    return plt.show()

def graph(objective,minc,date,limitdays):
    print(objective + "   "+str(minc)+"   "+date+"   "+str(limitdays))
    dataset = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    x=0
    indices_pais = []
    for country in dataset["countriesAndTerritories"]:
        if country == objective:
            indices_pais.append(x)
        x = x + 1

    country_min = min(indices_pais)
    country_max = max(indices_pais)
    country = dataset.loc[country_min:country_max]
    country_cases = []
    for dato in country["cases"]:
        country_cases.append(dato)
    country_cases.reverse()

    without_days = 0
    with_days = 0
    minncases = 0
    ncases = 0
    virus = []
    total_cases_by_day = []

    for cases in country_cases:
        ncases += cases
        if ncases > minc:
          with_days += 1
        else:
          without_days += 1
          minncases = ncases

    range_country = range(without_days,(with_days + without_days - 1))
    ###########################################################################
    count = 1
    if limitdays == 0:
        days = range(1,with_days)

        for cases in range_country:
            virus.append(country_cases[cases])

        total = 0
        counter = 0
        for cases in virus:
            if counter == 0:
                total = total + cases + minncases
                total_cases_by_day.append(total)
                counter = 1
            else:
                total = total + cases
                total_cases_by_day.append(total)
    else:
        if limitdays <= with_days:
            days = range(1,limitdays+1)
        else:
            print("Cantidad de dias muy grande")

        for cases in range_country:
            if count <= limitdays:
                virus.append(country_cases[cases])
                count += 1

        total = 0
        counter = 0
        for cases in virus:
            if counter == 0:
                total = total + cases + minncases
                total_cases_by_day.append(total)
                counter = 1
            else:
                total = total + cases
                total_cases_by_day.append(total)
    print(days)
    print(virus)
    print(total_cases_by_day)

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel("Days with virus over " + str(minc) +" cases"+"\n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")
    ax1.set_ylabel('Infected by day', color=color)
    ax1.bar(days, virus, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Total cases', color=color)  # we already handled the x-label with ax1
    ax2.plot(days, total_cases_by_day, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.suptitle("\n " + objective +"\n Cases at "+date)


    plt.show()

#array with coutries to evaluate
countries = ["Spain","Italy", "China","United_States_of_America","Mexico"]
#number of the minimal cases to show in graphic
from_minimal_cases = 100
#date to evaluate
date_csv= "09_04_2020"
#maximal day to show in graphic from the minimal cases detected
number_of_days_to_compare = 21
#print(covid19cases_by_country("Mexico"))
graph_cases_by_country("Mexico",from_minimal_cases)
exit()
for contry in countries:
    graph(country,from_minimal_cases,date_csv,number_of_days_to_compare)
