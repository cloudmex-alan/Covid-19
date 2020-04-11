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
#Data Source: European Centre for Disease Prevention and Control
def covid19cases_by_country(country,min_total_cases):
    ##Choose data source online or offline
    df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    #df = pd.read_csv("data/06_04_2020.csv")
    df_mex = df.copy()
    df_mex = df_mex.loc[df_mex['countriesAndTerritories'] == 'Mexico']
    df_mex = df_mex.iloc[::-1]
    df_mex = df_mex.assign(total_cases=df_mex.cases.cumsum())
    #Choose rows with total_cases > min_total_cases
    df_mex = df_mex[df_mex['total_cases'] > min_total_cases]
    count_rows_mex = len(df_mex.index)
    print(count_rows_mex)
    #Recover rows by country name
    df = df.loc[df['countriesAndTerritories'] == country]
    #Apply reverse to dataframe
    df = df.iloc[::-1]
    #Create row of total_cases
    df = df.assign(total_cases=df.cases.cumsum())
    df = df.assign(total_deaths=df.deaths.cumsum())
    #Choose rows with total_cases > min_total_cases
    df = df[df['total_cases'] > min_total_cases]
    df = df.head(count_rows_mex)
    return df

#graph cases and total_cases vs date
def graph_cases_by_country(country,min_total_cases):
    df = covid19cases_by_country(country,min_total_cases)
    df = df.assign(total_cases_by100k=(df.total_cases*100000/df.popData2018))
    df = df.assign(cases_by100k=(df.cases*100000/df.popData2018))
    print(df)
    #start plotting

    #Define axes on both sides of y
    ax1 = plt.gca()
    ax1.set_ylabel('New infected by every 100,000 habitants',color='blue')
    ax1.set_xlabel("Days with virus over " + str(min_total_cases) + " cases (" + str(len(df)) + ")" + "\n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")
    ax2 = ax1.twinx()
    ax2.set_ylabel('Total of infected by every 100,000 habitants',color='red')

    df.plot(kind='bar',y='cases_by100k',color="blue",ax=ax1)
    df.plot(kind='line',y='total_cases_by100k',x='dateRep', color='red', ax=ax2)

    plt.xticks(np.arange(len(df)), np.arange(1, len(df)+1))
    plt.suptitle(country +"\n Cases at " + df['dateRep'].iloc[-1])
    plt.tight_layout()
    return plt.show()

#graph total cases various contries
def graph_bar_cases_by_country(country1,country2,country3,country4,country5,min_total_cases):
    df1 = covid19cases_by_country(country1,min_total_cases)
    df1 = df1.assign(total_cases_by100k=(df1.total_cases*100000/df1.popData2018))
    df1 = df1.assign(cases_by100k=(df1.cases*100000/df1.popData2018))

    df2 = covid19cases_by_country(country2,min_total_cases)
    df2 = df2.assign(total_cases_by100k=(df2.total_cases*100000/df2.popData2018))
    df2 = df2.assign(cases_by100k=(df2.cases*100000/df2.popData2018))

    df3 = covid19cases_by_country(country3,min_total_cases)
    df3 = df3.assign(total_cases_by100k=(df3.total_cases*100000/df3.popData2018))
    df3 = df3.assign(cases_by100k=(df3.cases*100000/df3.popData2018))

    df4 = covid19cases_by_country(country4,min_total_cases)
    df4 = df4.assign(total_cases_by100k=(df4.total_cases*100000/df4.popData2018))
    df4 = df4.assign(cases_by100k=(df4.cases*100000/df4.popData2018))

    df5 = covid19cases_by_country(country5,min_total_cases)
    df5 = df5.assign(total_cases_by100k=(df5.total_cases*100000/df5.popData2018))
    df5 = df5.assign(cases_by100k=(df5.cases*100000/df5.popData2018))

    #Put last row from countries in a new data dataframe
    df_countries = pd.concat([df1.tail(1), df2.tail(1), df3.tail(1), df4.tail(1), df5.tail(1)])
    print(df_countries)
    #start plotting
    #df_countries[['total_cases_by100k','total_deaths_by100k']].plot(kind='bar',x='countriesAndTerritories', stacked=True)

    df_countries.plot(kind='bar',y='total_cases_by100k',x='countriesAndTerritories',color="blue")
    plt.suptitle("Total of cases at countries after " + str(len(df1)) + " days of first 100 cases \n by every 100,000 habitants")
    plt.tight_layout()
    return plt.show()

#graph total cases various contries
def graph_bar_deaths_by_country(country1,country2,country3,country4,country5,min_total_cases):
    df1 = covid19cases_by_country(country1,min_total_cases)
    df1 = df1.assign(total_deaths_by100k=(df1.total_deaths*100000/df1.popData2018))
    df1 = df1.assign(deaths_by100k=(df1.deaths*100000/df1.popData2018))

    df2 = covid19cases_by_country(country2,min_total_cases)
    df2 = df2.assign(total_deaths_by100k=(df2.total_deaths*100000/df2.popData2018))
    df2 = df2.assign(deaths_by100k=(df2.deaths*100000/df2.popData2018))

    df3 = covid19cases_by_country(country3,min_total_cases)
    df3 = df3.assign(total_deaths_by100k=(df3.total_deaths*100000/df3.popData2018))
    df3 = df3.assign(deaths_by100k=(df3.deaths*100000/df3.popData2018))

    df4 = covid19cases_by_country(country4,min_total_cases)
    df4 = df4.assign(total_deaths_by100k=(df4.total_deaths*100000/df4.popData2018))
    df4 = df4.assign(deaths_by100k=(df4.deaths*100000/df4.popData2018))

    df5 = covid19cases_by_country(country5,min_total_cases)
    df5 = df5.assign(total_deaths_by100k=(df5.total_deaths*100000/df5.popData2018))
    df5 = df5.assign(deaths_by100k=(df5.deaths*100000/df5.popData2018))

    #Put last row from countries in a new data dataframe
    df_countries = pd.concat([df1.tail(1), df2.tail(1), df3.tail(1), df4.tail(1), df5.tail(1)])
    print(df_countries)
    #start plotting
    #df_countries[['total_cases_by100k','total_deaths_by100k']].plot(kind='bar',x='countriesAndTerritories', stacked=True)

    df_countries.plot(kind='bar',y='total_deaths_by100k',x='countriesAndTerritories',color="blue")
    plt.suptitle("Total of deaths at countries after " + str(len(df1)) + " days of first 100 cases \n by every 100,000 habitants")
    plt.tight_layout()
    return plt.show()

#graph cases and total_cases vs date
def graph_deaths_by_country(country,min_total_cases):
    df = covid19cases_by_country(country,min_total_cases)
    df = df.assign(total_deaths_by100k=(df.total_deaths*100000/df.popData2018))
    df = df.assign(deaths_by100k=(df.deaths*100000/df.popData2018))
    print(df)
    #start plotting

    #Define axes on both sides of y
    ax1 = plt.gca()
    ax1.set_ylabel('New deaths by every 100,000 habitants',color='blue')
    ax1.set_xlabel("Days with virus over " + str(min_total_cases) + " cases (" + str(len(df)) + ")" + "\n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")
    ax2 = ax1.twinx()
    ax2.set_ylabel('Total of deaths by every 100,000 habitants',color='red')

    df.plot(kind='bar',y='deaths_by100k',color="blue",ax=ax1)
    df.plot(kind='line',y='total_deaths_by100k',x='dateRep', color='red', ax=ax2)

    plt.xticks(np.arange(len(df)), np.arange(1, len(df)+1))
    plt.suptitle(country +"\n Deaths at " + df['dateRep'].iloc[-1])
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
    ax1.set_ylabel('Infected by day', color=color)
    ax1.bar(days, virus, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlabel("Days with virus over " + str(minc) +" cases"+"\n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")

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
#graph_deaths_by_country(countries[0],from_minimal_cases)
graph_bar_deaths_by_country("Spain","Italy", "China","United_States_of_America","Mexico",100)
#graph_bar_cases_by_country("Spain","Italy", "China","United_States_of_America","Mexico",100)
exit()
for contry in countries:
    graph(country,from_minimal_cases,date_csv,number_of_days_to_compare)
