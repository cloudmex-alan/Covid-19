import pandas as pd
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import matplotlib.pyplot as plt
from functools import reduce

#In this script we consider the first 40 days after first 100 COVID-19 infections
#in China, USA, Italy, Spain, South Korea, Germany and Japan
#This data is used for train ML/AI models for predictions on Mexico

#Function to recover COVID19 cases by country during the first 40 days after first 100 COVID-19 infections
#Data Source: European Centre for Disease Prevention and Control
def covid19cases_by_country(country,min_total_cases,n_days):
    ##Choose data source online or offline
    df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    #df = pd.read_csv("data/06_04_2020.csv")

    #Recover rows by country name
    df = df.loc[df['countriesAndTerritories'] == country]

    #Apply reverse to dataframe
    df = df.iloc[::-1]

    #Create row of total_cases
    df = df.assign(total_cases=df.cases.cumsum())
    df = df.assign(total_deaths=df.deaths.cumsum())

    #Choose rows with total_cases > min_total_cases
    df = df[df['total_cases'] > min_total_cases]

    #calculate cases and deaths by every 100,000 habitants
    df = df.assign(total_cases_by100k=(df.total_cases*100000/df.popData2018))
    df = df.assign(cases_by100k=(df.cases*100000/df.popData2018))
    df = df.assign(total_deaths_by100k=(df.total_deaths*100000/df.popData2018))
    df = df.assign(deaths_by100k=(df.deaths*100000/df.popData2018))

    #cutoff rows to first n days
    df = df.head(n_days)

    #Reset index
    df = df.reset_index(drop=True)
    return df
def graph_mean_cases(min_total_cases,n_days):
    df_countries = pd.concat([
    covid19cases_by_country("South_Korea",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Australia",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Estonia",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Canada",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Croatia",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Egypt",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Spain",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("United_States_of_America",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("France",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("China",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Japan",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Russia",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Afghanistan",min_total_cases,n_days)['cases_by100k'],
    covid19cases_by_country("Germany",min_total_cases,n_days)['cases_by100k']], axis=1)
    df_countries = pd.concat([df_countries,df_countries.mean(axis = 1, skipna = True)], axis=1)
    df_countries.rename(columns = {0:'mean'}, inplace = True)

    df_mex = covid19cases_by_country("Mexico",min_total_cases,n_days)

    print(df_countries)

    ax = plt.gca()
    ax.set_xlabel("First "+ str(n_days) +" days with virus over " + str(min_total_cases) + " cases  \n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")
    ax.set_ylabel('Mean of cases by every 100,000 habitants',color='red')
    ax.set_title('Mean of cases by COVID-19 of 14 countries VS deaths in Mexico (By every 100,000 habitant)')

    ax2 = ax.twinx()
    ax2.set_ylabel('Cases by every 100,000 habitants in Mexico',color='blue')
    ax2.set_yticklabels([])

    df_mex.plot(kind='line',y='cases_by100k',marker='o',color='blue',ax=ax)
    df_countries.plot(kind='bar',y='mean',use_index=True,color='red',ax=ax)

    plt.xticks(np.arange(len(df_countries)), np.arange(1, len(df_countries)+1))
    plt.grid()
    plt.tight_layout()

    return plt.show()

def graph_mean_deaths(min_total_cases,n_days):
    df_countries = pd.concat([
    covid19cases_by_country("South_Korea",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Australia",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Estonia",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Canada",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Croatia",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Egypt",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Spain",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("United_States_of_America",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("France",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("China",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Japan",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Russia",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Afghanistan",min_total_cases,n_days)['deaths_by100k'],
    covid19cases_by_country("Germany",min_total_cases,n_days)['deaths_by100k']], axis=1)
    df_countries = pd.concat([df_countries,df_countries.mean(axis = 1, skipna = True)], axis=1)
    df_countries.rename(columns = {0:'mean'}, inplace = True)

    df_mex = covid19cases_by_country("Mexico",min_total_cases,n_days)

    print(df_countries)

    ax = plt.gca()
    ax.set_xlabel("First "+ str(n_days) +" days with virus over " + str(min_total_cases) + " cases  \n Data collected from:\n European Centre for Disease Prevention and Control \n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide")
    ax.set_ylabel('Mean of deaths by every 100,000 habitants',color='red')
    ax.set_title('Mean of deaths by COVID-19 of 14 countries VS deaths in Mexico (By every 100,000 habitant)')

    ax2 = ax.twinx()
    ax2.set_ylabel('Deaths by every 100,000 habitants in Mexico',color='blue')
    ax2.set_yticklabels([])

    df_mex.plot(kind='line',y='deaths_by100k',marker='o',color='blue',ax=ax)
    df_countries.plot(kind='bar',y='mean',use_index=True,color='red',ax=ax)

    plt.xticks(np.arange(len(df_countries)), np.arange(1, len(df_countries)+1))
    plt.grid()
    plt.tight_layout()

    return plt.show()

#graph_mean_deaths(100,35)
graph_mean_cases(100,35)
