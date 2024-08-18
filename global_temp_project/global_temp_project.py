
import pandas as pd 
import matplotlib.pyplot as mpl
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np
import requests
import os, sys
import logging as log

def main():
    temp_anomalies, export_emissions, countries_by_continents, disasters, sea_levels = load_dataframes()
    ## MATPLOTLIB
    temp = temp_anomalies_mean(temp_anomalies)
    carbon = export_emissions_mean(export_emissions, countries_by_continents)
    tech, nat = disasters_per_year(disasters)
    seas = sea_level_delta(sea_levels)
    disaster_types_per_year(disasters)
    ## SEABORN
    tempXsea(temp, seas)
    tempXcarbon(temp, carbon)
    tempXdisasters(temp, tech, nat)
    techXcarbon(tech, carbon)
    mpl.show()

def load_dataframes():
    api_get_file("https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv", ".\Data\\temp_means.csv")
    api_get_file("https://sealevel.colorado.edu/files/2023_rel2/gmsl_2023rel2_seasons_rmvd.txt", ".\Data\\sea_level_rise.txt")
    temp_anomalies = pd.read_csv(f'{file_path}temp_means.csv', header = 1, dtype={'pctapi': np.float64}, na_values=['***'])
    export_emissions = pd.read_csv(f'{file_path}export_emissions.csv')
    countries_by_continents = pd.read_csv(f'{file_path}continents.csv')
    disasters = pd.read_excel(f'{file_path}disaster_data_world.xlsx')
    sea_levels = pd.read_csv(f'{file_path}sea_level_rise.txt', header=None, delimiter=r"\s+", names=['Year', 'SeaLevelChange'],skiprows=1)
    sea_levels.to_csv(f'{file_path}sea_level_rise.csv', index=None)
    return temp_anomalies, export_emissions, countries_by_continents, disasters, sea_levels

def temp_anomalies_mean(temp_anomalies):
    temp_anomalies["AnnualMeanTemp"] = temp_anomalies[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']].mean(axis=1)
    mpl.figure(figsize=(12, 6))
    mpl.plot(temp_anomalies['Year'], temp_anomalies['AnnualMeanTemp'], marker='o', color='red')
    mpl.title('Annual Global Surface Temperature Anomalies')
    mpl.xlabel('Year')
    mpl.ylabel('Temperature Anomaly (°C)')
    mpl.grid(True)
    return temp_anomalies

def export_emissions_mean(export_emissions, countries_by_continents):
    countries_by_continents = countries_by_continents.rename(columns={"Entity": "Country"})
    export_emissions = export_emissions.set_index('Year').transpose().iloc[: , :-2].reset_index().rename(columns={'index': 'Country', 'Year': ''}).merge(countries_by_continents, how = 'inner', on = 'Country')
    emissions_by_continents = export_emissions.drop(export_emissions.columns[0],axis=1).groupby('Continent').mean().transpose()
    mpl.figure(figsize=(12, 6))
    mpl.plot(emissions_by_continents)
    mpl.gca().xaxis.set_major_locator(mpl.MaxNLocator(5))
    mpl.title('Global Emissions since 1960')
    mpl.xlabel('Year')
    mpl.ylabel('Emissions (MtCO2)')
    mpl.legend(["Africa", "Asia", "Europe", "North America", "Oceania", "South America"])
    mpl.grid(True)
    return emissions_by_continents
    
def disasters_per_year(disasters):
    disasters['Year'] = disasters['Start Year']
    disasters = disasters.groupby('Disaster Group')
    tech_disasters = disasters.get_group('Technological').groupby('Year').size()
    nat_disasters = disasters.get_group('Natural').groupby('Year').size()
    mpl.figure(figsize=(12,6))
    ax = tech_disasters.plot(x='Year', y='Number of disasters')
    nat_disasters.plot(ax=ax, x='Year', y='Number of disasters')
    mpl.legend(['Technological Disasters', 'Natural Disasters'])
    mpl.title('Number of natural and technological disasters per year')
    mpl.ylabel('Number of disasters')
    mpl.grid(True)
    return tech_disasters, nat_disasters

def disaster_types_per_year(all_disasters):
    disasters = all_disasters.groupby('Disaster Subgroup')
    d_bio       = disasters.get_group('Biological').groupby('Start Year').size()
    d_clim      = disasters.get_group('Climatological').groupby('Start Year').size()
    d_geo       = disasters.get_group('Geophysical').groupby('Start Year').size()
    d_hydro     = disasters.get_group('Hydrological').groupby('Start Year').size()
    d_ind       = disasters.get_group('Industrial accident').groupby('Start Year').size()
    d_meteor    = disasters.get_group('Meteorological').groupby('Start Year').size()
    d_misc      = disasters.get_group('Miscellaneous accident').groupby('Start Year').size()
    d_trans     = disasters.get_group('Transport').groupby('Start Year').size()
    disasters = pd.DataFrame({
        'Biological': d_bio,
        'Climotological': d_clim,
        'Geophysical': d_geo,
        'Hydrological': d_hydro,
        'Industrial accident': d_ind,
        'Meteorological': d_meteor,
        'Miscellaneous accident': d_misc,
        'Transport': d_trans
    }, index=pd.unique(all_disasters['Start Year']))
    disasters = disasters.iloc[::5, :]
    ax = disasters.plot.bar(rot=0)
    mpl.legend(loc='upper right')
    mpl.title('Types of disasters per year')
    mpl.grid(True)

def sea_level_delta(sea_levels):
    sea_levels['Year'] = sea_levels['Year'].astype(int)
    mean_delta = sea_levels.groupby('Year')['SeaLevelChange'].mean()
    mpl.figure(figsize=(12,6))
    mpl.plot(mean_delta, marker='o', color='red')
    mpl.title('Average change in sea levels across the years')
    mpl.xlabel('Year')
    mpl.ylabel('Change in sea levels (mm)')
    mpl.grid(True)
    return sea_levels
    
def tempXsea(temp_anomalies, sea_levels):
    temp_anomalies = temp_anomalies.tail(-112)
    mpl.figure(figsize=(12, 6))
    ax1 = mpl.subplot()
    ax2 = ax1.twinx()
    sea_levels = sea_levels.groupby('Year', as_index=False)['SeaLevelChange'].mean()
    sns.lineplot(data=temp_anomalies, x='Year', y='AnnualMeanTemp', ax=ax1)
    sns.lineplot(data=sea_levels, x='Year', y='SeaLevelChange', color='red')
    ax2.tick_params(axis='y', colors='red')
    ax2.set(ylabel='Change in sea levels (mm)')
    ax1.set(ylabel='Annual Temperature Delta (°C)')
    blue = Line2D([0], [0], label='Temperature', color='blue')
    red = Line2D([0], [0], label='Sea Levels', color='red')
    mpl.legend(handles=[blue, red])
    mpl.title('Relationship between changes in average temperature and difference in sea levels')
    mpl.grid(True)

def tempXcarbon(temp_anomalies, carbon_emsissions):
    temp_anomalies = temp_anomalies.tail(-80).head(-2)
    carbon_emsissions['Year'] = carbon_emsissions.index
    carbon_emsissions = carbon_emsissions.astype({'Year':'int'})
    mpl.figure(figsize=(12, 6))
    ax1 = mpl.subplot()
    ax2 = ax1.twinx()
    sns.lineplot(data=temp_anomalies, x='Year', y='AnnualMeanTemp', ax=ax1, color='green')
    sns.lineplot(data=carbon_emsissions, x='Year', y='Africa', color='red', ax=ax2)
    sns.lineplot(data=carbon_emsissions, x='Year', y='Asia', color='yellow', ax=ax2)
    sns.lineplot(data=carbon_emsissions, x='Year', y='Europe', color='blue', ax=ax2)
    sns.lineplot(data=carbon_emsissions, x='Year', y='North America', color='black', ax=ax2)
    sns.lineplot(data=carbon_emsissions, x='Year', y='South America', color='pink', ax=ax2)
    sns.lineplot(data=carbon_emsissions, x='Year', y='Oceania', color='purple', ax=ax2)
    ax2.tick_params(axis='y', colors='red')
    ax2.set(xlabel='Year', ylabel='Emissions (MtCO2)')
    ax1.set(ylabel='Annual Temperature Delta(°C)')
    green = Line2D([0], [0], label='Avg Temperature', color='green')
    red = Line2D([0], [0], label='Africa', color='red')
    yellow = Line2D([0], [0], label='Asia', color='yellow')
    blue = Line2D([0], [0], label='Europe', color='blue')
    black = Line2D([0], [0], label='North America', color='black')
    pink = Line2D([0], [0], label='South America', color='pink')
    purple = Line2D([0], [0], label='Oceania', color='purple')
    mpl.legend(handles=[green, red, yellow, blue, black, pink, purple])
    mpl.title('Relationship between changes in average temperature and carbon emissions')
    mpl.grid(True)

def tempXdisasters(temp, tech, nat):
    temp = temp.tail(-120)
    mpl.figure(figsize=(12, 6))
    ax1 = mpl.subplot()
    ax2 = ax1.twinx()
    sns.lineplot(data=temp, x='Year', y='AnnualMeanTemp', ax=ax1, label='Avg Temperature')
    sns.lineplot(data=tech, color='red', ax=ax2, label='Technological Disasters')
    sns.lineplot(data=nat, color='yellow', ax=ax2, label='Natural Disasters')
    ax2.tick_params(axis='y', colors='red')
    ax1.set(ylabel='Annual Temperature Delta (°C)')
    ax2.set(ylabel='Number of Disasters')
    mpl.legend(loc='best')
    mpl.title('Relationship between changes in average temperature and disasters')
    mpl.grid(True)

def techXcarbon(tech, carbon):
    carbon['Year'] = carbon.index
    carbon = carbon.tail(-40)
    carbon = carbon.astype({'Year':'int'})
    mpl.figure(figsize=(12, 6))
    ax1 = mpl.subplot()
    ax2 = ax1.twinx()
    carbon["GlobalAvg"] = carbon[['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']].sum(axis=1)
    sns.lineplot(data=carbon, x='Year', y='GlobalAvg', ax=ax1, label='Global Carbon Emissions')
    sns.lineplot(data=tech, color='red', ax=ax2, label='Technological Disasters')
    ax2.tick_params(axis='y', colors='red')
    ax1.set(ylabel='Emissions (MtCO2)')
    ax2.set(ylabel='Number of Disasters')
    mpl.legend(loc='best')
    mpl.title('Relationship between carbon emissions and technological disasters')
    mpl.grid(True)

def api_get_file(source_url, save_as):
    r = requests.request('GET', source_url, allow_redirects=True)
    open(save_as, 'wb').write(r.content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        numeric_level = getattr(log, sys.argv[1].upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % sys.argv[1])
        log.basicConfig(level=numeric_level)
    else:
        numeric_level = 'INFO'
    file_path = f'{os.path.dirname(__file__)}\Data\\'
    main()