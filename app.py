# ------------ LIBRARIES ------------ #
import dash
from dash import dcc, html, clientside_callback, ClientsideFunction
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from feffery_markdown_components import FefferyMarkdown

import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
from plotly.express.colors import sample_colorscale




# ---- Places Dropdown ---- #
txt_file_url = "https://www2.census.gov/geo/docs/reference/codes2020/place/st06_ca_place2020.txt"

ca2020 = pd.read_csv(txt_file_url, sep='|', dtype = {'STATEFP': object, 'PLACEFP': object})
ca2020['PLACE_FIPS'] = ca2020['STATEFP'] + ca2020['PLACEFP']
ca2020['PLACENAME'] = ca2020['PLACENAME'].str.replace(' CDP', "")
ca2020['PLACENAME'] = ca2020['PLACENAME'].str.replace(' city', "")

ca2020 = ca2020[['STATEFP', 'PLACEFP', 'PLACE_FIPS', 'PLACENAME', 'COUNTIES', 'TYPE']]

SoCal2020 = ca2020[ca2020.COUNTIES.str.contains('Los Angeles County|Santa Barbara County|Ventura County|Orange County|San Bernardino County|Riverside County|San Diego County|Imperial County|San Luis Obispo County|Kern County')]

for FIPS_code, new_name in zip(['0639759', '0639766', '0630938', '0630944', '0665042'], ['Lakeside (Kern County)', 'Lakeside (San Diego County)', 'Greenacres (Kern County)', 'Green Acres (Riverside County)', 'San Buenaventura (Ventura County)']):
    SoCal2020.loc[SoCal2020['PLACE_FIPS'] == FIPS_code, 'PLACENAME'] = new_name

SoCal_keys = SoCal2020['PLACENAME'].str.replace(' town', " Town").to_list()
SoCal_values = SoCal2020['PLACENAME'].str.replace(' ', '').replace('LaCañadaFlintridge', 'LaCanadaFlintridge').to_list()
places_tuple = zip(SoCal_keys, SoCal_values)
places_options = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in places_tuple]

anomalous_places = ['AltaSierra', 'BakersfieldCountryClub', 'BentonPark', 'CaliforniaPolytechnicStateUniversity', 'CampPendletonMainside',
                    'CasaLoma', 'ChoctawValley', 'Cottonwood', 'DelDios', 'DiGiorgio', 'EastBakersfield', 'EasternGoletaValley', 'EastNiles',
                    'Edison', 'ElAdobe', 'ElCentroNavalAirFacility', 'ElfinForest', 'Fairfax', 'Glennville', 'Goodmanville', 'HarmonyGrove',
                    'Hillcrest', 'LaCresta', 'Lakeside(KernCounty)', 'Modjeska', 'MountainMeadows', 'OldeStockdale', 'OldRiver', 'OldStine',
                    'Pala', 'PepperdineUniversity', 'PotomacPark', 'PumpkinCenter', 'RanchoMissionViejo', 'RexlandAcres', 'RidgecrestHeights',
                    'Rivergrove', 'Sage', 'Silverado', 'Somis', 'Stebbins', 'Tarina', 'TrabucoCanyon', 'UniversityofCaliforniaSantaBarbara',
                    'WilliamsCanyon', 'Woody', 'Yermo']
places_options = [dict(item) for item in places_options if not any(item['value'] == place for place in anomalous_places)]

modified_values_1 = ['EastWhittier', 'JurupaValley', 'TemescalValley', 'Vincent', 'Whitewater']
modified_places_options_1 = [dict(item, **{'disabled': True}) if item['value'] in modified_values_1 else dict(item) for item in places_options]

modified_values_2 = ['EastWhittier', 'JurupaValley']
modified_places_options_2 = [dict(item, **{'disabled': True}) if item['value'] in modified_values_2 else dict(item) for item in places_options]




# ---- Years Dropdown ---- #
years_list = list(range(2010, 2024))

years_options = [{'label': html.Span([i], style = {'color': '#000000'}), 'value': i} for i in years_list]

modified_years_options_1 = [dict(item, **{'disabled': True}) if item['value'] in [2010] else dict(item) for item in years_options]

modified_years_options_2 = [dict(item, **{'disabled': True}) if item['value'] in [2010, 2011] else dict(item) for item in years_options]

modified_years_options_3 = [dict(item, **{'disabled': True}) if item['value'] in list(range(2010, 2015)) else dict(item) for item in years_options]




# ---- Measures Dropdown ---- #
measures_labels_list = ["Contract Rent",
                        "Rent Burden",
                        "Employment Statistics",
                        "Food Stamps",
                        "Health Insurance Coverage",
                        "Household Income",
                        "Housing and Occupancy",
                        "Poverty Estimates",
                        "Work Commute Estimates",
                        "Working Hours",
                        "Other Economic Measures",
                        "Population Estimates",
                        "Educational Attainment"
                       ]
measures_values_list = ['ContractRent',
                        'RentBurden',
                        'EmploymentStatistics',
                        'FoodStamps', 
                        'HealthInsuranceCoverage',
                        'HouseholdIncome',
                        'HousingUnitsandOccupancy',
                        'Poverty',
                        'TransportationMethodstoWork',
                        'WorkHours',
                        'CharacteristicsoftheEconomicPopulation',
                        'Population',
                        'Education'
                       ]
measures_tuple = zip(measures_labels_list, measures_values_list)
measures_options = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in measures_tuple]


modified_values = ['HealthInsuranceCoverage', 'Poverty', 'FoodStamps']
modified_measures_options_1 = [dict(item, **{'disabled': True}) if item['value'] in modified_values else dict(item) for item in measures_options]

modified_measures_options_2 = [dict(item, **{'disabled': True}) if item['value'] == 'FoodStamps' else dict(item) for item in measures_options]





# ---- Subcategory Measures Dropdown ---- #

submeasures_dict = dict()
    
# -- Contract Rent -- #
dummy_labels_list = ['Distribution of Contract Rents',
                     'Contract Rents Over Time'
                    ]
dummy_values_list = ['ContractRent_LONG',
                     'ContractRent_TIME'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['ContractRent'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Rent Burden -- #
dummy_labels_list = ['Rent/Severe Rent Burden Over Time', 'Rent Burden and Severe Rent Burden',
                     'Rent Burden by Age (Over Time)', 'Rent Burden by Age',
                     'Rent Burden by Income (Over Time)', 'Rent Burden by Income',
                    ]
dummy_values_list = ['RentBurden_TIME', 'RentBurden_LONG',
                     'RentBurden_AGE_TIME', 'RentBurden_AGE_LONG',
                     'RentBurden_INCOME_TIME', 'RentBurden_INCOME_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['RentBurden'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Employment Statistics -- #
dummy_labels_list = ['Unemp. Rate by Race (Over Time)', 'Unemployment Rate by Race',
                     'LFPR by Race (Over Time)', 'LFPR by Race',
                     'EPOP by Race (Over Time)', 'EPOP by Race',
                     'Unemp. Rate by Sex (Over Time)', 'Unemployment Rate by Sex',
                     'LFPR by Sex (Over Time)', 'LFPR by Sex',
                     'EPOP by Sex (Over Time)', 'EPOP by Sex',
                     'Unemp. Rate by Education (Over Time)', 'Unemployment Rate by Education',
                     'LFPR by Education (Over Time)', 'LFPR by Education',
                     'EPOP by Education (Over Time)', 'EPOP by Education',
                    ]
dummy_values_list = ['EmploymentStatistics_UNEMP_RACE_TIME', 'EmploymentStatistics_UNEMP_RACE_LONG',
                     'EmploymentStatistics_LFPR_RACE_TIME', 'EmploymentStatistics_LFPR_RACE_LONG',
                     'EmploymentStatistics_EPOP_RACE_TIME', 'EmploymentStatistics_EPOP_RACE_LONG',
                     'EmploymentStatistics_UNEMP_SEX_TIME', 'EmploymentStatistics_UNEMP_SEX_LONG',
                     'EmploymentStatistics_LFPR_SEX_TIME', 'EmploymentStatistics_LFPR_SEX_LONG',
                     'EmploymentStatistics_EPOP_SEX_TIME', 'EmploymentStatistics_EPOP_SEX_LONG',
                     'EmploymentStatistics_UNEMP_EDUCATIONALSTATUS_TIME', 'EmploymentStatistics_UNEMP_EDUCATIONALSTATUS_LONG',
                     'EmploymentStatistics_LFPR_EDUCATIONALSTATUS_TIME', 'EmploymentStatistics_LFPR_EDUCATIONALSTATUS_LONG',
                     'EmploymentStatistics_EPOP_EDUCATIONALSTATUS_TIME', 'EmploymentStatistics_EPOP_EDUCATIONALSTATUS_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['EmploymentStatistics'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Food Stamps -- #
dummy_labels_list = ['Food Stamps Recipients (by Race)',
                     'Food Stamps Recipients (by Poverty Status)',
                     'Food Stamps Recipients (by Disability Status)',
                     'Food Stamps Recipients (by Working Status)',
                    ]
dummy_values_list = ['FoodStamps_RACE_LONG',
                     'FoodStamps_POVERTY_LONG',
                     'FoodStamps_DISABILITYSTATUS_LONG',
                     'FoodStamps_WORKINGSTATUS_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['FoodStamps'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Household Income -- #
dummy_labels_list = ['Income Distribution (for Households)',
                     'Income Distribution (for Families)',
                     'Income Distribution (for Married Couples)',
                     'Income Distribution (for Nonfamily Households)',
                    ]
dummy_values_list = ['HouseholdIncome_HOUSEHOLDS_LONG',
                     'HouseholdIncome_FAMILIES_LONG', 
                     'HouseholdIncome_MARRIEDCOUPLEFAMILIES_LONG',
                     'HouseholdIncome_NONFAMILYHOUSEHOLDS_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['HouseholdIncome'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Housing Units and Occupancy -- #
dummy_labels_list = ['Home Values (Owner-Occupied Units)',
                     'Occupied Housing Units by Race',
                     'Occupied Housing Units by Age',
                     'Housing Units by Year Built',
                     'Rooms in Housing Units',
                     'Bedrooms in Housing Units',
                     'House Heating Fuel',
                     'Select Units Lacking Facilities',
                     'Occupants Per Room',
                     'Monthly Owner Costs for Units with Mortgage',
                     'Year Householder Moved In'
                    ]
dummy_values_list = ['HousingUnitsandOccupancy_HOMEVALUE_LONG',
                     'HousingUnitsandOccupancy_RACE_HOUSINGUNITS_LONG',
                     'HousingUnitsandOccupancy_AGE_HOUSINGUNITS_LONG',
                     'HousingUnitsandOccupancy_YEARBUILT_LONG',
                     'HousingUnitsandOccupancy_UNITROOMS_LONG',
                     'HousingUnitsandOccupancy_UNITBEDROOMS_LONG',
                     'HousingUnitsandOccupancy_HEATINGFUEL_LONG',
                     'HousingUnitsandOccupancy_LACKINGFACILITIES_LONG',
                     'HousingUnitsandOccupancy_OCCUPANTSPERROOM_LONG',
                     'HousingUnitsandOccupancy_MORTGAGESMOC_LONG',
                     'HousingUnitsandOccupancy_YEARMOVEDIN_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['HousingUnitsandOccupancy'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Poverty -- #
dummy_labels_list = ['Poverty by Race',
                     'Poverty by Sex (Coming Soon!)',
                     'Poverty by Age (Coming Soon!',
                     'Poverty by Employment (Coming Soon!)',
                    ]
dummy_values_list = ['Poverty_RACE_LONG',
                     'Poverty_SEX_LONG',
                     'Poverty_AGE_LONG',
                     'Poverty_EMPLOYMENT_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Poverty'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

disabled_values = ['Poverty_SEX_LONG', 'Poverty_AGE_LONG', 'Poverty_EMPLOYMENT_LONG']
submeasures_dict['Poverty']  = [dict(item, **{'disabled': True}) if item['value'] in disabled_values else dict(item) for item in submeasures_dict['Poverty'] ]




# -- Health Insurance Coverage -- #
dummy_labels_list = ['Coverage by Race',
                     'Coverage by Sex (Coming Soon!)',
                     'Coverage by Citizenship Status (Coming Soon!)',
                     'Coverage by Educational Status (Coming Soon!)'
                    ]
dummy_values_list = ['HealthInsuranceCoverage_RACE_LONG',
                     'HealthInsuranceCoverage_SEX_LONG',
                     'HealthInsuranceCoverage_CITIZEN_LONG',
                     'HealthInsuranceCoverage_EDUCATIONALSTATUS_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['HealthInsuranceCoverage'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

disabled_values = ['HealthInsuranceCoverage_CITIZEN_LONG', 'HealthInsuranceCoverage_SEX_LONG', 'HealthInsuranceCoverage_EDUCATIONALSTATUS_LONG']
submeasures_dict['HealthInsuranceCoverage']  = [dict(item, **{'disabled': True}) if item['value'] in disabled_values else dict(item) for item in submeasures_dict['HealthInsuranceCoverage'] ]




# -- Transportation Methods to Work -- #
dummy_labels_list = ['Commute Methods to Work',
                     'Departure Times',
                     'Travel Times',
                     'Vehicles Available'
                    ]
dummy_values_list = ['TransportationMethodstoWork_METHODSTOWORK_LONG',
                     'TransportationMethodstoWork_DEPARTURE_LONG',
                     'TransportationMethodstoWork_TRAVEL_LONG',
                     'TransportationMethodstoWork_VEHICLESAVAILABLE_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['TransportationMethodstoWork'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]



# -- Work Hours -- #
dummy_labels_list = ['Usual Hours Worked Weekly',
                     'Mean Hours Worked Weekly',
                     'Mean Hours Worked Weekly (Over Time)',
                    ]
dummy_values_list = ['WorkHours_USUALHOURS_LONG',
                     'WorkHours_MEANHOURS_LONG',
                     'WorkHours_MEANHOURS_TIME',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['WorkHours'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]



# -- Characteristics of the Economic Population -- #
dummy_labels_list = ['Civilian Workers by Industry',
                     'Civilian Workers by Occupation',
                     'Civilian Workers by Sector',
                     'Median Earnings for All Workers by Industry',
                     'Median Earnings for Full-Time Workers by Industry',
                     'Gender Pay Gap, Full-Time Workers (Coming Soon!)',
                     'Gender Pay Gap, All Workers (Coming Soon!)'
                    ]
dummy_values_list = ['CharacteristicsoftheEconomicPopulation_INDUSTRY_LONG',
                     'CharacteristicsoftheEconomicPopulation_OCCUPATION_LONG',
                     'CharacteristicsoftheEconomicPopulation_CLASS_LONG',
                     'CharacteristicsoftheEconomicPopulation_INDUSTRYEARNINGS_LONG',
                     'CharacteristicsoftheEconomicPopulation_INDUSTRYFULLEARNINGS_LONG',
                     'CharacteristicsoftheEconomicPopulation_GENDERPAYGAPFULL_LONG',
                     'CharacteristicsoftheEconomicPopulation_GENDERPAYGAPALL_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['CharacteristicsoftheEconomicPopulation'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

disabled_values = ['CharacteristicsoftheEconomicPopulation_GENDERPAYGAPFULL_LONG', 'CharacteristicsoftheEconomicPopulation_GENDERPAYGAPALL_LONG']
submeasures_dict['CharacteristicsoftheEconomicPopulation']  = [dict(item, **{'disabled': True}) if item['value'] in disabled_values else dict(item) for item in submeasures_dict['CharacteristicsoftheEconomicPopulation'] ]


# -- Population -- #
dummy_labels_list = ['Population by Age',
                     'Population by Race',
                     'Hispanic/Latino Population',
                     'Asian Population',
                     'American Indian and Alaska Native Population',
                     'Native Hawaiian and Pacific Islander Population',
                    ]
dummy_values_list = ['Population_AGE_LONG',
                     'Population_RACE_LONG',
                     'Population_HISPANICLATINO_LONG',
                     'Population_ASIAN_LONG',
                     'Population_INDIGENOUS_LONG',
                     'Population_NATIVEHAWAIIANPACIFICISLANDER_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Population'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]



# -- Education -- #
dummy_labels_list = ['Attainment by Citizenship',
                     'Attainment, White',
                     'Attainment, Black',
                     'Attainment, American Indian & Alaska Native',
                     'Attainment, Asian',
                     'Attainment, Native Hawaiian & Pacific Islander',
                     'Attainment, Some Other Race',
                     'Attainment, Two or More Races',
                     'Attainment, White (Not Hispanic/Latino)',
                     'Attainment, Hispanic/Latino',
                     'Attainment, 18 to 24',
                     'Attainment, 25 to 34',
                     'Attainment, 35 to 44',
                     'Attainment, 45 to 64',
                     'Attainment, 65 and Older',
                    ]
dummy_values_list = ['Education_CITIZENSHIP_LONG',
                     'Education_RACE_WHITE_LONG',
                     'Education_RACE_BLACK_LONG',
                     'Education_RACE_INDIGENOUS_LONG',
                     'Education_RACE_ASIAN_LONG',
                     'Education_RACE_NATIVEHAWAIIANPACIFICISLANDER_LONG',
                     'Education_RACE_SOMEOTHERRACE_LONG',
                     'Education_RACE_TWOORMORERACES_LONG',
                     'Education_RACE_WHITENOTHISPANIC_LONG',
                     'Education_RACE_HISPANIC_LONG',
                     'Education_AGE_18to24_LONG',
                     'Education_AGE_25to34_LONG',
                     'Education_AGE_35to44_LONG',
                     'Education_AGE_45to64_LONG',
                     'Education_AGE_65andOlder_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Education'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]








# ---- ------------ ---- #
# ---- Color Scales ---- #
# ---- ------------ ---- #


# -- Discrete Colors -- #
discrete_color_dict = dict()

discrete_color_dict['YlOrRd_9'] = ['rgb(255, 255, 204)', 'rgb(255, 237, 160)', 'rgb(254, 217, 118)', 'rgb(254, 178, 76)',
                                   'rgb(253, 141, 60)', 'rgb(252, 78, 42)', 'rgb(227, 26, 28)', 'rgb(189, 0, 38)', 'rgb(128, 0, 38)']

discrete_color_dict['YlOrRd_12'] = ['rgb(255, 255, 204)', 'rgb(255, 242, 172)', 'rgb(255, 228, 141)', 'rgb(254, 210, 110)',
                                    'rgb(254, 182, 80)', 'rgb(253, 154, 66)', 'rgb(253, 118, 53)', 'rgb(250, 73, 41)',
                                    'rgb(232, 35, 31)', 'rgb(206, 12, 33)', 'rgb(172, 0, 38)', 'rgb(128, 0, 38)']

discrete_color_dict['Reds_2'] = ['#F69697', '#FF0500']
discrete_color_dict['Same_Reds_5'] = ['#F69697'] * 5
discrete_color_dict['Same_Reds_8'] = ['#F69697'] * 8

discrete_color_dict['D3_5'] = px.colors.qualitative.D3[0:5]
discrete_color_dict['D3_7'] = px.colors.qualitative.D3[0:7]
discrete_color_dict['Okabe_8'] = ['#000000', '#CC79A7', '#D55E00', '#0072B2', '#F0E442', '#009E73', '#56B4E9', '#E69F00']

discrete_color_dict['G10'] = px.colors.qualitative.G10

discrete_color_dict['Greens_10'] = px.colors.sequential.Greens + ['rgb(0,65,26)']

discrete_color_dict['Viridis'] = px.colors.sequential.Viridis
discrete_color_dict['Magma'] = px.colors.sequential.Magma

discrete_color_dict['Oranges'] = px.colors.sequential.Oranges[0:7] + ['rgb(149, 49, 3)', 'rgb(133, 43, 2)']
discrete_color_dict['GnBu'] = px.colors.sequential.GnBu
discrete_color_dict['Pastel2'] = px.colors.qualitative.Pastel2 + ['rgb(179,205,227)']
discrete_color_dict['Set3'] = px.colors.qualitative.Set3 + ['rgb(251,180,174)']
discrete_color_dict['Blues'] = ['rgb(247,251,255)', 'rgb(222, 238, 255)', 'rgb(197, 226, 255)', 'rgb(172, 213, 255)', 'rgb(147, 201, 255)',
                                'rgb(121, 188, 255)', 'rgb(96, 176, 255)', 'rgb(71, 163, 255)', 'rgb(46, 151, 255)', 'rgb(21, 138, 255)',
                                'rgb(0, 125, 251)', 'rgb(0, 113, 226)', 'rgb(0, 100, 201)']


# Colorblind-safe colors: https://colorbrewer2.org/
# More colorblind-safe colors: https://www.nceas.ucsb.edu/sites/default/files/2022-06/Colorblind%20Safe%20Color%20Schemes.pdf




# -- Continuous Colors -- #
continuous_color_dict = dict()

continuous_color_dict['YlGnBu'] = sorted([ [1 - i/8, px.colors.sequential.YlGnBu[i]] for i in list(range(0, 9)) ])
continuous_color_dict['YlGn'] = sorted([ [1 - i/8, px.colors.sequential.YlGn[i]] for i in list(range(0, 9)) ])
continuous_color_dict['deep'] = sorted([ [1 - i/11, px.colors.sequential.deep[i]] for i in list(range(0, 12)) ])
continuous_color_dict['Emrld'] = sorted([ [1 - i/6, px.colors.sequential.Emrld[i]] for i in list(range(0, 7)) ])
continuous_color_dict['Mint'] = sorted([ [1 - i/6, px.colors.sequential.Mint[i]] for i in list(range(0, 7)) ])
continuous_color_dict['PuBuGn'] = sorted([ [1 - i/8, px.colors.sequential.PuBuGn[i]] for i in list(range(0, 9)) ])
continuous_color_dict['DarkMint'] = sorted([ [1 - i/6, px.colors.sequential.Darkmint[i]] for i in list(range(0, 7)) ])
continuous_color_dict['Magma'] = sorted([ [i/9, px.colors.sequential.Magma[i]] for i in list(range(0, 10)) ])
continuous_color_dict['Hot'] = sorted([ [i/3, px.colors.sequential.Hot[i]] for i in list(range(0, 4)) ])
continuous_color_dict['OrRd'] = sorted([ [1 - i/8, px.colors.sequential.OrRd[i]] for i in list(range(0, 9)) ])
continuous_color_dict['matter'] = sorted([ [1 - i/11, px.colors.sequential.matter[i]] for i in list(range(0, 12)) ])



# Uncomment to see all built-in colors in plotly's qualitative color schemes
# px.colors.qualitative.swatches()

# Uncomment to see all built-in colors in plotly's continuous color schemes
# px.colors.sequential.swatches_continuous()







# --------------- #
# ----- APP ----- #
# --------------- #

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, 
                                                "assets/style.css"]
               )
server = app.server
app.title = 'SoCal Socioeconomic Profile'


app.layout = html.Div([
    html.Div(className = "row", children = [
        # ---- LEFT ---- #
        html.Div(className = "four columns", children = [
            html.H3("Southern California Socioeconomic Profile"),
            html.P("Using the American Community Survey, this website allows you to visualize various socioeconomic measures for cities in SoCal.",
                   className = 'text-p'),
            html.P("Use the dropdowns to navigate your selection process.",
                   className = 'text-p'),
            dcc.Dropdown(
                id          = 'place-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a place',
                options     = places_options,
                value       = 'LongBeach',
                clearable   = False
            ),
            dcc.Dropdown(
                id          = 'year-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a year',
                options     = years_options,
                value       = 2023,
                clearable   = False
            ),
            dcc.Dropdown(
                id          = 'measure-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a measure',
                options     = measures_options,
                value       = 'ContractRent',
                clearable   = False
            ),
            dcc.Dropdown(
                id          = 'submeasure-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a submeasure',
                clearable   = True,
                searchable  = False
            ),
            dbc.Row(className = 'fmt-button', children = [
                dbc.Col(width = 3, children = [
                    dbc.Button("Help?",
                               id         = "open-offcanvas",
                               outline    = True,
                               color      = 'primary',
                               n_clicks   = 0)],
                         className = 'help-button'
                        ),
                dbc.Col(width = 3, children = [
                    dbc.Button("Data",
                               id         = "data-button",
                               outline    = True,
                               color      = 'danger',
                               # external_link = False,
                               n_clicks   = 0)],
                        ),
                dbc.Col(width = 3, children = [
                    dbc.Button("Code",
                               id         = "code-button",
                               outline    = True,
                               color      = 'secondary',
                               href       = 'https://github.com/ramindersinghdubb/Los-Angeles-County-Socioeconomic-Profile',
                               n_clicks   = 0)],
                        ),
            ]),
            dbc.Offcanvas(
                FefferyMarkdown(id          = "help-text",
                                renderHtml  = True,
                                className  = 'offcanvas-body'
                               ),
                id      = "offcanvas",
                title   = html.H3("Help"),
                is_open = False,
                class_name = 'four columns'
            )
        ]),
        # ---- RIGHT ---- #
        html.Div(className= "eight columns chart-layout",
                 children = [dcc.Loading(id        = 'loading-sign',
                                         className = 'loading',
                                         color     = '#F8F8FF',
                                         display   = 'show',
                                        ),
                             dcc.Graph(id     = 'map',
                                       config = {'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'resetview'], 'displaylogo': False, 'displayModeBar': False},
                                       clear_on_unhover = True
                                      ),
                             dcc.Tooltip(id        = 'tooltip',
                                         children  = [dcc.Graph(id               = "tooltip-graph",
                                                                config           = {'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'resetview'], 'displaylogo': False},
                                                                clear_on_unhover = True
                                                               )],
                                         direction = 'bottom',
                                         background_color = '#FEF9F3',
                                        )
                            ]
                )
    ]),
    # ---- DATA ---- #
    dcc.Store(id = "masterfile"),
    dcc.Store(id = "tooltip_file"),
    dcc.Store(id = "mapfile"),
    dcc.Store(id = "discrete_color_dict",    data = discrete_color_dict),
    dcc.Store(id = "continuous_color_dict",  data = continuous_color_dict),
    dcc.Store(id = "places-dict",            data = places_options),
    dcc.Store(id = "modified-places-dict-1", data = modified_places_options_1),
    dcc.Store(id = "modified-places-dict-2", data = modified_places_options_2),
    dcc.Store(id = "years-dict",             data = years_options),
    dcc.Store(id = "modified-years-dict-1",  data = modified_years_options_1),
    dcc.Store(id = "modified-years-dict-2",  data = modified_years_options_2),
    dcc.Store(id = "modified-years-dict-3",  data = modified_years_options_3),
    dcc.Store(id = "measures-dict",          data = measures_options),
    dcc.Store(id = "modified-measures-dict-1", data = modified_measures_options_1),
    dcc.Store(id = "modified-measures-dict-2", data = modified_measures_options_2),
    dcc.Store(id = "submeasures-dict",       data = submeasures_dict)
])









# ---- ---- DROPDOWNS ---- ----#

# ---- ------------------------------------------------------- ---- #
# ---- Disabling/Enabling Place Options Based on Selected Year ---- #
# ---- ------------------------------------------------------- ---- #

app.clientside_callback(
    """
    function(selected_year, places_options, modified_places_options_1, modified_places_options_2) {
        var places_options = places_options;

        if ( selected_year == 2010 ) {
            var places_options = modified_places_options_1;
        }
        if ( selected_year == 2011 ) {
            var places_options = modified_places_options_2;
        }
        
        return places_options
    }
    """,
    Output('place-dropdown', 'options'),
    Input('year-dropdown', 'value'),
    Input('places-dict', 'data'),
    Input('modified-places-dict-1', 'data'),
    Input('modified-places-dict-2', 'data')
)

# ---- ------------------------------------------------------- ---- #
# ---- Disabling/Enabling Year Options Based on Selected Place ---- #
# ---- ------------------------------------------------------- ---- #

app.clientside_callback(
    """
    function(selected_place, selected_measure, years_options, modified_years_options_1, modified_years_options_2, modified_years_options_3) {
        var years_options = years_options;
        var selected_place = `${selected_place}`;

        if ( ['TemescalValley', 'Vincent', 'Whitewater'].includes(selected_place) ) {
            var years_options = modified_years_options_1;
        }
        if ( ['EastWhittier', 'JurupaValley'].includes(selected_place) ||  ['HealthInsuranceCoverage', 'Poverty'].includes(selected_measure) ) {
            var years_options = modified_years_options_2;
        }
        if ( ['FoodStamps'].includes(selected_measure) ) {
            var years_options = modified_years_options_3;
        }
        
        return years_options
    }
    """,
    Output('year-dropdown', 'options'),
    Input('place-dropdown', 'value'),
    Input('measure-dropdown', 'value'),
    Input('years-dict', 'data'),
    Input('modified-years-dict-1', 'data'),
    Input('modified-years-dict-2', 'data'),
    Input('modified-years-dict-3', 'data')
)

# ---- ---------------------------------------------------------- ---- #
# ---- Disabling/Enabling Measures Options Based on Selected Year ---- #
# ---- ---------------------------------------------------------- ---- #

app.clientside_callback(
    """
    function(selected_year, measures_options, modified_measures_options_1, modified_measures_options_2) {
        var measures_options = measures_options;
        
        if ( [2010, 2011].includes(selected_year) ) {
            var measures_options = modified_measures_options_1;
        }
        if ( [2012, 2013, 2014].includes(selected_year) ) {
            var measures_options = modified_measures_options_2;
        }
        
        return measures_options
    }
    """,
    Output('measure-dropdown', 'options'),
    Input('year-dropdown', 'value'),
    Input('measures-dict', 'data'),
    Input('modified-measures-dict-1', 'data'),
    Input('modified-measures-dict-2', 'data')
)


# ---- ------------------- ---- #
# ---- Submeasures Options ---- #
# ---- ------------------- ---- #

app.clientside_callback(
    """
    function(selected_measure, submeasures_dict) {
        return submeasures_dict[selected_measure];
    }
    """,
    Output('submeasure-dropdown', 'options'),
    Input('measure-dropdown', 'value'),
    Input('submeasures-dict', 'data')
)



# ---- ------------------------------ ---- #
# ---- Displaying the Help Off-Canvas ---- #
# ---- ------------------------------ ---- #

app.clientside_callback("""
    function (n_clicks, is_open) {
        var canvas_state = is_open;
        
        if ( n_clicks ) {
            var canvas_state = true;
        }
        
        return canvas_state;
    }
    """,
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("offcanvas", "is_open")
)


# ---- ----------------------------------------- ---- #
# ---- Changing the Help Text for the Off-Canvas ---- #
# ---- ----------------------------------------- ---- #
app.clientside_callback("""
    function (selected_measure) {
        if ( selected_measure == 'ContractRent' ) {
            return `<span style='font-size:22px;'>Contract Rent</span></u><br>
            <span style='color:#85BCC7;'>Contract rents</span> are defined as "the monthly rent agreed to or contracted for, regardless
            of any furnishings, utilities, fees, meals, or services that may be included" (2024 American Community Survey Design & Methodology Report, Chapter 6).<br><br><br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'RentBurden' ) {
            return `<span style='font-size:22px;'>Rent Burden</span></u><br>
            Renters who are <span style='color:#DC143C;'>rent-burdened</span> pay <u style='color:#DC143C;'><span style='color:#DC143C;'>over 30%</span></u> of their household income to rent.<br><br>
            Renters who are <span style='color:#B22222;'>severely rent-burdened</span> pay <u style='color:#B22222;'><span style='color:#B22222;'>over 50%</span></u> of their household income to rent.<br><br>
            Rent burden and severe rent burden is found by taking the percentage of household income going to gross rent. <span style='color:#85BCC7;'>Gross rent</span> is defined as
            "[the monthly rent agreed to or contracted for, regardless of any furnishings, utilities, fees, meals, or services that may be included] plus the estimated average monthly cost of utilities and fuels,
            if these are paid by the renter" (2024 American Community Survey Design & Methodology Report, Chapter 6). <br><br><br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'EmploymentStatistics' ) {
            return `<span style='font-size:22px;'>Employment Statistics</span></u><br>
            The <span style='color:#85BCC7;'>unemployment rate</span> is defined as the proportion of persons in the labor force who did not work in the reference period under question but were actively searching for work
            during the reference period in question.<br><br>
            The <span style='color:#85BCC7;'>labor force participation rate</span> (or <span style='color:#85BCC7;'>LFPR</span>) is defined as the proportion of working-aged (16 and older) persons who are
            working or actively searching for work.<br><br>
            The <span style='color:#85BCC7;'>employment-to-population ratio</span> (or <span style='color:#85BCC7;'>EPOP</span>) is defined as the proportion of working-aged (16 and older) persons who are
            working.<br><br>
            Per the 2024 American Community Survey Design & Methodology Report, questions regarding labor force status are designed to identify the following: <br><br>
            1) people who worked at any time during the reference week; <br>
            2) people on temporary layoff who were available for work; <br>
            3) people who did not work during the reference week but who had jobs or businesses from which they were temporarily absent (excluding layoffs); <br>
            4) people who did not work but were available during the reference week, and who were looking for work during the last four weeks; and <br>
            5) people not in the labor force. <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'FoodStamps' ) {
            return `<span style='font-size:22px;'>Food Stamps</span></u><br>
            Per the 2024 American Community Survey Design & Methodology Report, "the Food and Nutrition Service of the U.S. Department of Agriculture (USDA) administers the <span style='color:#85BCC7;'>Supplemental Nutrition Assistance (Food Stamp) Program (SNAP)</span> through state and local welfare offices.
            This program is the major national income-support program for which all low-income and low-resource households, regardless of household characteristics, are eligible.
            This question asks if anyone in the households received SNAP benefits at any time during the 12-month period before the ACS interview."
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'HealthInsuranceCoverage' ) {
            return `<span style='font-size:22px;'>Health Insurance Coverage</span></u><br>
            Per the 2024 American Community Survey Design & Methodology Report, "[the insured and uninsured population is assessed] by asking about coverage through an employer, direct purchase from an insurance company, Medicare, Medicaid or
            other government-assistance health plans, military health care, Veterans Affairs health care, Indian Health Service, or other types of health insurance or coverage
            plans. Plans that cover only one type of health care (such as dental plans) or plans that only cover a person in case of an accident or disability are not included."
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'HouseholdIncome' ) {
            return `<span style='font-size:22px;'>Household Income</span></u><br>
            <span style='color:#85BCC7;'>Income</span> is defined as "the sum of the amounts reported separately for wage or salary income; net self-employment income; interest, dividends, or net rental or royalty income,
            or income from estates and trusts; social security or railroad retirement income; Supplemental Security Income; public assistance or welfare payments;
            retirement, survivor, or disability pensions; and all other income. Income is reported for the past 12 months from the date of the interview. The estimates
            are inflation-adjusted using the Consumer Price Index" (2024 American Community Survey Design & Methodology Report, Chapter 6). 
            <br><br>
            To adjust for changes in cost of living, adjustment to the 2023 Consumer Price Index ("constant dollars") was conducted for data years earlier than 2023 through the
            <u><a href='https://www.bls.gov/cpi/additional-resources/chained-cpi.htm'>Bureau of Labor Statistics Chained Consumer Price Index for All Urban Consumers (C-CPI-U)</a></u> series.
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            1) <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u><br>
            2) <u><a href='https://www.census.gov/topics/income-poverty/income/guidance/current-vs-constant-dollars.html'>Current versus Constant (or Real) Dollars</a></u>`;
        }
        
        if ( selected_measure == 'HousingUnitsandOccupancy' ) {
            return `<span style='font-size:22px;'>Housing and Occupancy</span></u><br>
            The reference person, or <span style='color:#85BCC7;'>householder</span>, is usually "the person, or one of the people,
            in whose name the home is owned, being bought, or rented and who is listed as 'Person 1' on the survey questionnaire.
            If there is no such person in the household, any adult household member 15 and older can be designated" (2024 American Community Survey Design &
            Methodology Report, Chapter 6).
            <br><br><br>
            A property's <span style='color:#85BCC7;'>value</span> is computed based on: <br>
            "the respondent’s estimate of how much the property (house and lot, mobile home and lot, or condominium unit) would sell for.
            The information is collected for [housing units] that are owned or being bought and for vacant [housing units] that are for sale.
            If the house or mobile home is owned or being bought, but the land on which it sits is not, the respondent is asked to estimate the
            combined value of the house or mobile home and the land. For vacant [housing units], value is defined as the price asked for the
            property. This information is obtained from real estate agents, property managers, or neighbors" (ibis.). 
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'Poverty' ) {
            return `<span style='font-size:22px;'>Poverty Estimates</span></u><br>
            <span style='color:#85BCC7;'>Poverty</span> is not a directly asked question in the American Community Survey but formulated indirectly
            with the assistance of information regarding respondents' income and household composition (2024 American Community Survey Design & Methodology Report, Chapter 10).<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'TransportationMethodstoWork' ) {
            return `<span style='font-size:22px;'>Work Commute Estimates</span></u><br>
            <span style='color:#85BCC7;'>Commute methods to work</span> refer to "the principal mode of travel or type of conveyance
            that the worker usually used to get from home to work during the reference week" (2024 American Community Survey Design & Methodology Report, Chapter 6).<br><br>
            <span style='color:#85BCC7;'>Departure times</span> refer to "the time of day that the respondent usually
            left home to go to work during the reference week" (ibis.).<br><br>
            <span style='color:#85BCC7;'>Travel times</span> to work refer to the number of minutes it usually takes the respondent to get from home to
            work during the reference week (ibis.).<br><br>
            <span style='color:#85BCC7;'>Vehicles available</span> show
            <br>
            "the number of passenger cars, vans, and pickup or panel trucks of one-ton capacity or less kept at home and available
            for the use of household members. Vehicles rented or leased for one month or more, company vehicles, and police and
            government vehicles are included if kept at home and used for nonbusiness purposes. Dismantled or immobile vehicles 
            are excluded, as are vehicles kept at home but used only for business purposes" (ibis.). 
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'WorkHours' ) {
            return `<span style='font-size:22px;'>Working Hours</span></u><br>
            Estimates for <span style='color:#85BCC7;'>usual hours worked weekly</span> are reported for the civilian, 16 and older employed labor force.<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'CharacteristicsoftheEconomicPopulation' ) {
            return `<span style='font-size:22px;'>Other Economic Measures</span></u><br>
            Estimates are reported for the civilian, 16 and older employed labor force.<br><br>
            <span style='color:#85BCC7;'>Industry</span> refers to the particular sphere of trade a civilian worker is employed in.<br><br>
            <span style='color:#85BCC7;'>Occupation</span> relates to the services associated with a civilian worker's employment.<br><br>
            <span style='color:#85BCC7;'>Sector</span> refers to the relative jurisdiction under which a civilian worker's employment is conducted (i.e.
            'private-sector', 'public-sector', self-employed, and family work).<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'Population' ) {
            return `<span style='font-size:22px;'>Population Estimates</span></u><br>
            <span style='color:#85BCC7;'>Race</span> refers to the socio-political category that individuals report themselves as. Note that race
            is not rooted in science or biology. For instance, the fact that 'Black' (a color) and 'Asian' (a geographical point of
            reference) reflect popular contemporary understandings of race and racial taxonomies within the United States metropole are in no way
            symptomatic of any scientific consensus. Further, note too the vagueness of 'Asian': could it refer to individuals hailing from Iran just
            as much as others hailing from Laos, given their respective landmasses are located within the Asian continent, or does 'Asian' refer to a
            popular understanding of individuals from landmasses close to and/or bordering the eastern Pacific seaboard?<br><br>
            For these, and other reasons, population estimates segmented by race should instead be motivated by a socio-political-economic understanding
            of the ways in which certain peoples who have understood themselves distinctively as a community (or, loosely, "population") have come to be
            situated.<br><br>
            For purposes of demonstration, Punjab is taken as a point of reference. In what ways has im/migration policy affected the presence
            of members of the Punjabi community? How has economic precarity in Punjab affected Punjabi individuals situated along the metropole and their
            relationships with both Punjab and the metropole? In what ways have existing community groups and structures (e.g. <i>gurdwaras</i>) made
            certain places more favorable to Punjabi individuals and the making of the Punjabi community?<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'Education' ) {
            return `<span style='font-size:22px;'>Educational Attainment</span></u><br>
            <span style='color:#85BCC7;'>Educational attainment</span>, unless otherwise stated, is reported for the <span style='color:#85BCC7;'>25 year and older</span> population.<br><br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
    }
    """,
    Output("help-text", "markdownStr"),
    Input('measure-dropdown', 'value')
)




# ---- ---- DATA ---- ----#

# ---- --------------- ---- #
# ---- Masterfile Data ---- #
# ---- --------------- ---- #

app.clientside_callback(
    """
    async function(selected_year, selected_place, selected_measure) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_SocioeconomicIndicators/${selected_year}/${selected_measure}_${selected_place}_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    }
    """,
    Output('masterfile', 'data'),
    Input('year-dropdown', 'value'),
    Input('place-dropdown', 'value'),
    Input('measure-dropdown', 'value')
)

# ---- ------------ ---- #
# ---- Tooltip Data ---- #
# ---- ------------ ---- #

app.clientside_callback(
    """
    async function(selected_year, selected_place, selected_submeasure) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_SocioeconomicIndicators/${selected_year}/${selected_submeasure}_${selected_place}_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    }
    """,
    Output('tooltip_file', 'data'),
    Input('year-dropdown', 'value'),
    Input('place-dropdown', 'value'),
    Input('submeasure-dropdown', 'value')
)


# ---- -------------------- ---- #
# ---- Data Download Button ---- #
# ---- -------------------- ---- #

app.clientside_callback(
    """
    function(selected_year, selected_place, selected_measure, selected_submeasure) {
        if (selected_submeasure === undefined || selected_submeasure === null) {
            const url = `https://github.com/ramindersinghdubb/datasets/blob/main/SoCal_SocioeconomicIndicators/${selected_year}/${selected_measure}_${selected_place}_${selected_year}.csv`;
            return url;
        } else {
            const url = `https://github.com/ramindersinghdubb/datasets/blob/main/SoCal_SocioeconomicIndicators/${selected_year}/${selected_submeasure}_${selected_place}_${selected_year}.csv`;
            return url;
        }
    }
    """,
    Output('data-button', 'href'),
    Input('year-dropdown', 'value'),
    Input('place-dropdown', 'value'),
    Input('measure-dropdown', 'value'),
    Input('submeasure-dropdown', 'value')
)



# ---- ------------ ---- #
# ---- Mapfile Data ---- #
# ---- ------------ ---- #

app.clientside_callback(
    """
    async function(selected_year) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_CensusTract_Mapfiles/SoCal_LatLongPoints_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    }
    """,
    Output('mapfile', 'data'),
    Input('year-dropdown', 'value')
)

# ---- ------------------------------------------------------- ---- #
# ---- Safeguard Redundancy: Disable Tooltip if Submeasure DNE ---- #
# ---- ------------------------------------------------------- ---- #

app.clientside_callback(
    """
    function(selected_submeasure) {
        if (selected_submeasure === undefined || selected_submeasure === null) {
            return 'hidethis';
        } else {
            return '';
        }
    }
    """,
    Output('tooltip', 'className'),
    Input('submeasure-dropdown', 'value')
)


# ---- ---- ------- ---- ----#
# ---- ---- ------- ---- ----#
# ---- ---- FIGURES ---- ----#
# ---- ---- ------- ---- ----#
# ---- ---- ------- ---- ----#



# ---- ------------ ---- #
# ---- Map Callback ---- #
# ---- ------------ ---- #

app.clientside_callback(
    """
    function(selected_year, selected_place, selected_measure, selected_submeasure, masterfile, mapfile, color_dict, places_dict) {
        var my_array = masterfile.filter(item => item['YEAR'] === selected_year);

        var locations_array = my_array.map(({GEO_ID}) => GEO_ID);

        var customdata_array = my_array.map(({TRACT}) => TRACT);

        if (selected_measure == 'ContractRent') {
            var z_array = my_array.map(({ESTIMATE_Mediancontractrent}) => ESTIMATE_Mediancontractrent);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Contract Rent (" + item['YEAR'] + "): <b style='color:#A91B0D; font-size:14px;'>" + item['ESTIMATE_Mediancontractrent_string'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = 'YlOrRd';
            var colorbar_title_text = '<b>Median<br>Contract<br>Rents ($)</b>';
            var colorbar_tickprefix = '$';
            var colorbar_ticksuffix = '';

            var zmin = 0;
            var zmax = 3500;

            if (selected_year <= 2014){
                var zmin = 0;
                var zmax = 2000;
            }
            
            var zauto_bool = false;
        }
        
        if (selected_measure == 'RentBurden') {
            var z_array = my_array.map(({ESTIMATE_Totalrenters_RentBurden}) => ESTIMATE_Totalrenters_RentBurden);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percentage of Rent-Burdened&nbsp;&nbsp;<br>Renters (" + item['YEAR'] + "): <b style='color:#610C04; font-size:14px;'>" + item['ESTIMATE_Totalrenters_RentBurden'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = 'YlOrRd';
            var colorbar_title_text = '<b>Percentage of<br>Rent-Burdened<br>Individuals</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'EmploymentStatistics') {
            if (selected_submeasure != undefined && selected_submeasure.includes("UNEMP")){
                var z_array = my_array.map(({ESTIMATE_UNEMP_16andOlder}) => ESTIMATE_UNEMP_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Unemployment Rate (" + item['YEAR'] + "): <b style='color:#800000; font-size:14px;'>" + item['ESTIMATE_UNEMP_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'YlOrRd';
                var colorbar_title_text = '<b>Unemp.<br>Rate</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin = 0;
                var zmax = 20;
                var zauto_bool = false;
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("LFPR")){
                var z_array = my_array.map(({ESTIMATE_LFPR_16andOlder}) => ESTIMATE_LFPR_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Labor Force Participation Rate (" + item['YEAR'] + "): <b style='color:#7A4988; font-size:14px;'>" + item['ESTIMATE_LFPR_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'Viridis';
                var colorbar_title_text = '<b>Labor<br>Force<br>Participat.<br>Rate</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin;
                var zmax;
                var zauto_bool = true;
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("EPOP")){
                var z_array = my_array.map(({ESTIMATE_EPOP_16andOlder}) => ESTIMATE_EPOP_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Employment-to-Population Ratio (" + item['YEAR'] + "): <b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_EPOP_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'Greens';
                var colorbar_title_text = '<b>Employment-<br>to-Population<br>Ratio</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin = 20;
                var zmax = 80;
                var zauto_bool = false;
            }
            if (selected_submeasure == undefined) {
                var z_array = my_array.map(({ESTIMATE_UNEMP_16andOlder}) => ESTIMATE_UNEMP_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Unemployment Rate (" + item['YEAR'] + "): <b style='color:#800000; font-size:14px;'>" + item['ESTIMATE_UNEMP_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'YlOrRd';
                var colorbar_title_text = '<b>Unemp.<br>Rate</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin = 0;
                var zmax = 20;
                var zauto_bool = false;
            }
        }
        
        if (selected_measure == 'FoodStamps') {
            var z_array = my_array.map(({PERCENT_HouseholdsreceivingfoodstampsSNAP}) => PERCENT_HouseholdsreceivingfoodstampsSNAP);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percentage of Households Receiving&nbsp;&nbsp;<br>Food Stamps (" + item['YEAR'] + "): <b style='color:#559C9E; font-size:14px;'>" + item['PERCENT_HouseholdsreceivingfoodstampsSNAP'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['DarkMint'];
            var colorbar_title_text = '<b>Percentage of<br>Households<br>Receiving<br>Food Stamps</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'HouseholdIncome') {
            var z_array = my_array.map(({ESTIMATE_Households_Meanincomedollars}) => ESTIMATE_Households_Meanincomedollars);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Household Income (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>$" + item['ESTIMATE_Households_Meanincomedollars'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>Median<br>Household<br>Income</b>';
            var colorbar_tickprefix = '$';
            var colorbar_ticksuffix = '';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'HousingUnitsandOccupancy') {
            var z_array = my_array.map(({ESTIMATE_TotalHousingUnits}) => ESTIMATE_TotalHousingUnits);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Housing Units (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_TotalHousingUnits'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            
            var colorscale_color = 'Greens';
            var colorbar_title_text = '<b>Total<br>Housing<br>Units</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';

            if (selected_submeasure != undefined && selected_submeasure.includes("_HOMEVALUE_")){
                var z_array = my_array.map(({ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars}) => ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Owner-Occupied Home Value (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars_string'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['Emrld'];
                var colorbar_title_text = '<b>Median<br>Owner-<br>Occupied<br>Home<br>Value</b>';
                var colorbar_tickprefix = '$';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("SMOC")){
                var z_array = my_array.map(({ESTIMATE_SELECTEDMONTHLYOWNERCOSTSSMOC_Housingunitswithamortgage_Mediandollars}) => ESTIMATE_SELECTEDMONTHLYOWNERCOSTSSMOC_Housingunitswithamortgage_Mediandollars);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Monthly Owner Costs (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_SELECTEDMONTHLYOWNERCOSTSSMOC_Housingunitswithamortgage_Mediandollars'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                
                var colorscale_color = color_dict['Hot'];
                var colorbar_title_text = '<b>Median<br>Monthly<br>Owner<br>Costs</b>';
                var colorbar_tickprefix = '$';
                var colorbar_ticksuffix = '';
            }
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'Poverty') {
            var z_array = my_array.map(({ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined}) => ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percent Below Poverty Level (" + item['YEAR'] + "): <br><b style='color:#420C09; font-size:14px;'>" + item['ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Magma'];
            var colorbar_title_text = '<b>Percent<br>Below<br>Poverty<br>Level</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'HealthInsuranceCoverage') {
            var z_array = my_array.map(({PERCENT_Uninsured_Civiliannoninstitutionalizedpopulation}) => PERCENT_Uninsured_Civiliannoninstitutionalizedpopulation);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percentage Uninsured  (" + item['YEAR'] + "): <b style='color:#710C04; font-size:14px;'>" + item['PERCENT_Uninsured_Civiliannoninstitutionalizedpopulation'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Hot'];
            var colorbar_title_text = '<b>Percentage<br>Uninsured</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'TransportationMethodstoWork') {
            var z_array = my_array.map(({PERCENT_Total_Workers16yearsandoverwhodidnotworkfromhome_TRAVELTIMETOWORK_Meantraveltimetoworkminutes}) => PERCENT_Total_Workers16yearsandoverwhodidnotworkfromhome_TRAVELTIMETOWORK_Meantraveltimetoworkminutes);
            var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Average Work Commute Time (" + item['YEAR'] + "): <br><b style='color:#B2560D; font-size:14px;'>" + item['PERCENT_Total_Workers16yearsandoverwhodidnotworkfromhome_TRAVELTIMETOWORK_Meantraveltimetoworkminutes'] + " minutes </b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
            var colorscale_color = color_dict['OrRd'];
            var colorbar_title_text = '<b>Average<br>Travel<br>Time<br>(Mins.)</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '<br>mins.';
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'WorkHours') {
            var z_array = my_array.map(({ESTIMATE_Total_Population16to64years_Meanusualhoursworkedforworkers}) => ESTIMATE_Total_Population16to64years_Meanusualhoursworkedforworkers);
            var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Average Usual Hours Worked (" + item['YEAR'] + "): <br><b style='color:#070504; font-size:14px;'>" + item['ESTIMATE_Total_Population16to64years_Meanusualhoursworkedforworkers'] + " hours </b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
            var colorscale_color = color_dict['OrRd'];
            var colorbar_title_text = '<b>Average<br>Usual<br>Hours<br>Worked<br></b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '<br>hrs.';
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'CharacteristicsoftheEconomicPopulation') {
            var z_array = my_array.map(({ESTIMATE_EMPLOYMENTSTATUS_Population16yearsandover_Inlaborforce_Civilianlaborforce}) => ESTIMATE_EMPLOYMENTSTATUS_Population16yearsandover_Inlaborforce_Civilianlaborforce);
            var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Number of Civilian Employed Workers (" + item['YEAR'] + "): <br><b style='color:#070504; font-size:14px;'>" + item['ESTIMATE_EMPLOYMENTSTATUS_Population16yearsandover_Inlaborforce_Civilianlaborforce'] + " </b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>Civilian<br>Employed<br>Workers</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'Population') {
            var z_array = my_array.map(({ESTIMATE_SEXANDAGE_Totalpopulation}) => ESTIMATE_SEXANDAGE_Totalpopulation);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_SEXANDAGE_Totalpopulation'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            
            var colorscale_color = color_dict['deep'];
            var colorbar_title_text = '<b>Total<br>Population</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';

            if (selected_submeasure != undefined && selected_submeasure.includes("_HISPANICLATINO_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_HispanicorLatinoofanyrace}) => ESTIMATE_RACE_Totalpopulation_HispanicorLatinoofanyrace);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Hispanic/Latino Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_HispanicorLatinoofanyrace'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total<br>Hispanic<br>and Latino<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("_ASIAN_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_Onerace_Asian}) => ESTIMATE_RACE_Totalpopulation_Onerace_Asian);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Asian Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_Onerace_Asian'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total<br>Asian<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("_INDIGENOUS_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_Onerace_AmericanIndianandAlaskaNative}) => ESTIMATE_RACE_Totalpopulation_Onerace_AmericanIndianandAlaskaNative);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total American Indian and Alaska Native Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_Onerace_AmericanIndianandAlaskaNative'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total<br>American<br>Indian and<br>Alaska<br>Native<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("_NATIVEHAWAIIANPACIFICISLANDER_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_Onerace_NativeHawaiianandOtherPacificIslander}) => ESTIMATE_RACE_Totalpopulation_Onerace_NativeHawaiianandOtherPacificIslander);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Native Hawaiian and Pacific Islander Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_Onerace_NativeHawaiianandOtherPacificIslander'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total Native<br>Hawaiian<br>and Pacific<br>Islander<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'Education') {
            var z_array = my_array.map(({ESTIMATE_TOTAL_CITIZENSHIPSTATUS}) => ESTIMATE_TOTAL_CITIZENSHIPSTATUS);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Total 25 and Older Population (" + item['YEAR'] + "): <br><b style='color:#070504; font-size:14px;'>" + item['ESTIMATE_TOTAL_CITIZENSHIPSTATUS'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>25 and<br>Older<br>Population</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';
            var zmin;
            var zmax;
            var zauto_bool = true;

            if (selected_submeasure != undefined && selected_submeasure.includes("_AGE_")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_AGE}) => ESTIMATE_TOTAL_AGE);
                var colorbar_title_text = '<b>18 and<br>Older<br>Population</b>';
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("_WHITE_")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_White}) => ESTIMATE_TOTAL_RACE_White);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("BLACK")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_BlackorAfricanAmerican}) => ESTIMATE_TOTAL_RACE_BlackorAfricanAmerican);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("INDIGENOUS")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_AmericanIndianandAlaskaNative}) => ESTIMATE_TOTAL_RACE_AmericanIndianandAlaskaNative);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("ASIAN")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_Asian}) => ESTIMATE_TOTAL_RACE_Asian);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("NATIVEHAWAIIANPACIFICISLANDER")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_NativeHawaiianandOtherPacificIslander}) => ESTIMATE_TOTAL_RACE_NativeHawaiianandOtherPacificIslander);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("SOMEOTHERRACE")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_Someotherrace}) => ESTIMATE_TOTAL_RACE_Someotherrace);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("TWOORMORERACES")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_Twoormoreraces}) => ESTIMATE_TOTAL_RACE_Twoormoreraces);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("WHITENOTHISPANIC")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_WhitenotHispanicorLatino}) => ESTIMATE_TOTAL_RACE_WhitenotHispanicorLatino);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("_HISPANIC_")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_HispanicorLatinoofanyrace}) => ESTIMATE_TOTAL_RACE_HispanicorLatinoofanyrace);
            }
            
        }


        
        

        var geometry_url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_CensusTract_Mapfiles/${selected_year}/mastergeometry_${selected_place}_${selected_year}.geojson`;

        
        var main_data = {
            'type': 'choroplethmap',
            'customdata': customdata_array,
            'geojson': geometry_url,
            'locations': locations_array,
            'featureidkey': 'properties.GEO_ID',
            'colorscale': colorscale_color,
            'reversescale': true,
            'z': z_array,
            'zmin': zmin, 'zmax': zmax, 'zauto': zauto_bool,
            'marker': {'line': {'color': '#020403', 'width': 1.75}, 'opacity': 0.6},
            'text': strings,
            'colorbar': {'outlinewidth': 2,
                         'ticklabelposition': 'outside bottom',
                         'tickprefix': colorbar_tickprefix,
                         'ticksuffix': colorbar_ticksuffix,
                         'title': {'font': {'color': '#020403', 'weight': 500}, 'text': colorbar_title_text},
                         'tickfont': {'weight': 500}},
            'hoverlabel': {'bgcolor': '#FAFAFA', 'bordercolor': '#BEBEBE', 'font': {'color': '#020403'}},
            'hovertemplate': '%{text}'
        };

        var map_array = mapfile.filter(item => item['PLACE'] === selected_place);

        var long_array = map_array.map(({LON}) => LON);
        var long_center = long_array.reduce((a, b) => a + b) / long_array.length;
        const lon_center = parseFloat(long_center.toFixed(7));
        
        var lat_array = map_array.map(({LAT}) => LAT);
        var lati_center = lat_array.reduce((a, b) => a + b) / lat_array.length;
        const lat_center = parseFloat(lati_center.toFixed(7));

        var layout = {
            'autosize': true,
            'hoverlabel': {'align': 'left'},
            'map': {'center': {'lat': lat_center, 'lon': lon_center}, 'style': 'streets', 'zoom': 11},
            'margin': {'b': 0, 'l': 0, 'r': 0, 't': 0},
            'paper_bgcolor': '#FEF9F3',
            'plot_bgcolor': '#FEF9F3',
        };

        

        if (selected_submeasure !== undefined && selected_submeasure !== null) {
            main_data['hoverinfo'] = 'none';
            main_data['hovertemplate'] = null;
        }
        if (selected_submeasure === null) {
            main_data['hoverinfo'] = 'all';
            main_data['hovertemplate'] = '%{text}';
        }

        return {'data': [main_data], 'layout': layout};

    }
    """,
    Output('map', 'figure'),
    Input('year-dropdown', 'value'),
    Input('place-dropdown', 'value'),
    Input('measure-dropdown', 'value'),
    Input('submeasure-dropdown', 'value'),
    Input('masterfile', 'data'),
    Input('mapfile', 'data'),
    Input('continuous_color_dict', 'data'),
    Input('places-dict', 'data')
)

# ---- ---------------- ---- #
# ---- Tooltip Callback ---- #
# ---- ---------------- ---- #

app.clientside_callback(
    """
    function(selected_year, selected_submeasure, hoverData, tooltip_data, discrete_color_dict, selected_place, places_dict) {
        if (!hoverData) {
            return [false, window.dash_clientside.no_update, window.dash_clientside.no_update];
        }

        if (!selected_submeasure) {
            return [false, window.dash_clientside.no_update, window.dash_clientside.no_update];
        } else {
            var tract_name = hoverData['points']['0']['customdata'];
            
            var dummy_var = places_dict.find(item => item['value'] === selected_place);
            var city_string = Object.values(dummy_var['label']['props']['children']);

            var barmode;
            
            if ( selected_submeasure.includes("LONG") ) {
                var my_array = tooltip_data.filter(item => item['YEAR'] == selected_year && item['TRACT'] == tract_name);
                
                var x_array = my_array.map(({variable}) => variable);
                var xaxis_standoff = 10;
                

                if ( selected_submeasure.startsWith("ContractRent") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                    });
                    
                    if (selected_year < 2015){
                        var color_array = discrete_color_dict['YlOrRd_9'];
                    } else {
                        var color_array = discrete_color_dict['YlOrRd_12'];
                    }
                    var xaxis_title_text = '<b>Contract Rent</b>';
                    
                    var yaxis_title_text = '<b>Number of Units</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                    var xlabels_size = 9;
                    
                    var title_text = `<b>Distribution of Contract Rents, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("RentBurden") && !selected_submeasure.includes("AGE") && !selected_submeasure.includes("INCOME") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Reds_2'];

                    var xaxis_title_text = '<b>Rent Burden Categories</b>';
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Percentage of Renters by Rent Burden Severity, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("AGE_LONG") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Same_Reds_5'];

                    var xaxis_title_text = '<b>Age Groups</b>';
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Percentage of Rent-Burdened Renters by Age, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("INCOME_LONG") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Same_Reds_8'];

                    var xaxis_title_text = '<b>Income Categories</b>';
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Percentage of Rent-Burdened Renters by Income, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("RACE_LONG")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['G10'];

                    var xaxis_title_text = '<b>Racial Categories</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 9;
                    var x_tickvals = ['Overall (16 and Older)', 'White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin (of any race)', 'White, not Hispanic or Latino'];
                    var x_ticktext = ['Overall (16 and<br>Older)', 'White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Race, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Race, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Race, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }
                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("SEX_LONG")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['D3_7'];

                    var xaxis_title_text = '<b>Sex and Women with Children</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 9;
                    var x_tickvals = ['Overall (20 to 64)', 'Male', 'Female', 'Female (With children under 6 years old)', 'Female (With children under 18 years old)', 'Female (With children under 17 years old)', 'Female (With children 6 to 17 years old)'];
                    var x_ticktext = ['Overall (20 to 64)', 'Male', 'Female', 'Female (With children<br>under 6 years old)', 'Female (With children<br>under18 years old)', 'Female (With children<br>under 17 years old)', 'Female (With children<br>6 to 17 years old)'];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Sex, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Sex, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Sex, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }
                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("EDUCATIONALSTATUS_LONG")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['D3_5'];

                    var xaxis_title_text = '<b>Educational Attainment </b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 10;
                    var x_tickvals = ['Overall (25 to 64)', 'Less than high school graduate', 'High school graduate (includes equivalency)', "Some college or associate's degree", "Bachelor's degree or higher"];
                    var x_ticktext = ['Overall (25 to 64)', 'Less than high<br>school graduate', 'High school graduate<br>(or equivalent)', "Some college or<br>associate's degree", "Bachelor's degree<br>or higher"];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Educational Attainment, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Educational Attainment, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Educational Attainment, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }
                if ( selected_submeasure.startsWith("FoodStamps")  ) {
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_YES}) => value_YES);
                    var y2_array = my_array.map(({value_NO}) => value_NO);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';

                    var yaxis_title_text = '<b>Percentage of Households</b>';

                    if ( selected_submeasure.includes("RACE") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "%</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin (of any race)', 'White, not Hispanic or Latino'];
                        var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Race, ${selected_year}</b>`;
                    }
                    if ( selected_submeasure.includes("POVERTY") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Poverty Status</b>';
                        var xaxis_standoff = 15;
                        
                        var x_tickvals = ['Below poverty level', 'At or above poverty level'];
                        var x_ticktext = ['Below poverty level', 'At or above poverty level'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Poverty Status, ${selected_year}</b>`;
                    }
                    if ( selected_submeasure.includes("DISABILITYSTATUS") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Disability Status</b>';
                        var xaxis_standoff = 15;
                        
                        var x_tickvals = ['With one or more people with a disability', 'With no people with a disability',];
                        var x_ticktext = ['With one or more<br>people with a disability', 'With no people<br>with a disability'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Disability Status, ${selected_year}</b>`;
                    }
                    if ( selected_submeasure.includes("WORKINGSTATUS") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Working Status</b>';
                        var xaxis_standoff = 15;
                        
                        var x_tickvals = ['No workers in past 12 months', '1 worker in past 12 months', '2 or more workers in past 12 months'];
                        var x_ticktext = ['No workers in<br>the past 12 months', 'One worker in the<br>past 12 months', 'Two or more workers<br>in the past 12 months'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Working Status, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'Recipients',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(179,226,205)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Non-Recipients',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(253,205,172)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2];
                    
                }

                if ( selected_submeasure.startsWith("HouseholdIncome")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size = 9;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Greens_10'];

                    var xaxis_title_text = '<b>Income</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 10;
                    var x_tickvals = ['Less than $10,000', '$10,000 to $14,999', '$15,000 to $24,999', '$25,000 to $34,999', '$35,000 to $49,999', '$50,000 to $74,999', '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 to $199,999', '$200,000 or more'];
                    var x_ticktext = ['Less than $10k', '$10k to 14.9k', '$15k to 24.9k', '$25k to 34.9k', '$35k to 49.9k', '$50k to 74.9k', '$75k to 99.9k', '$100k to 149.9k', '$150k to 199.9k', '$200k or more'];

                    if (selected_submeasure.includes("HOUSEHOLDS_LONG")){
                        var yaxis_title_text = '<b>Percent of Households</b>';
                        var title_text = `<b>Income Distribution for Households, ${selected_year}</b>`;
                    }
                    if (selected_submeasure.includes("FAMILIES_LONG")){
                        var yaxis_title_text = '<b>Percent of Families</b>';
                        var title_text = `<b>Income Distribution for Families, ${selected_year}</b>`;
                    }
                    if (selected_submeasure.includes("MARRIEDCOUPLEFAMILIES_LONG")){
                        var yaxis_title_text = '<b>Percent of Married-Couple<br>Families</b>';
                        var title_text = `<b>Income Distribution for Married-Couple Families, ${selected_year}</b>`;
                    }
                    if (selected_submeasure.includes("NONFAMILYHOUSEHOLDS_LONG")){
                        var yaxis_title_text = '<b>Percent of Nonfamily Households</b>';
                        var title_text = `<b>Income Distribution for Nonfamily Households, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("HousingUnitsandOccupancy")  ) {
                    if (selected_submeasure.includes("HOMEVALUE_LONG")){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Greens_10'];
    
                        var xaxis_title_text = '<b>Home Values</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 10;
                        
                        var x_tickvals = ['Less than $50,000', '$50,000 to $99,999', '$100,000 to $149,999', '$150,000 to $199,999', '$200,000 to $299,999', '$300,000 to $499,999', '$500,000 to $999,999', '$1,000,000 or more'];
                        var x_ticktext = ['Less than $50k', '$50k to 99.9k', '$100k to<br>149.9k', '$150k to<br>199.9k', '$200k to<br>299.9k', '$300k to<br>499.9k', '$500k to<br>999.9k', '$1 million<br>or more'];
                        
                        var yaxis_title_text = '<b>Number of Households</b>';
                        var title_text = `<b>Home Values for Owner-Occupied Housing Units, ${selected_year}</b>`;
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if (selected_submeasure.includes("_HOUSINGUNITS_")){
                        var barmode = 'group';
                        var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                        var y2_array = my_array.map(({value_OWNER}) => value_OWNER);
                        var y3_array = my_array.map(({value_RENTER}) => value_RENTER);
                        
                        var xlabels_size;
                        var x_ticktext;
                        var x_tickvals;
                        
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
    
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
    
                        if ( selected_submeasure.includes("RACE") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y3_text = y3_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            
                            var xlabels_size = 9;
                            var xaxis_title_text = '<b>Racial Categories</b>';
                            
                            var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin', 'White alone, not Hispanic or Latino'];
                            var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];
                            var title_text = `<b>Occupied Housing Units by Householder Race, ${selected_year}</b>`;
                        }
    
                        if ( selected_submeasure.includes("AGE") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y3_text = y3_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            
                            var xlabels_size = 10;
                            var xaxis_title_text = '<b>Age</b>';
    
                            var x_tickvals = ['Under 35 years', '35 to 44 years', '45 to 54 years', '55 to 64 years', '65 to 74 years', '75 to 84 years', '85 years and over'];
                            var x_ticktext = ['Under 35<br>years', '35 to 44', '45 to 54', '55 to 64', '65 to 74', '75 to 84', '85 years and<br>Older'];
                            var title_text = `<b>Occupied Housing Units by Householder Age, ${selected_year}</b>`;
                        }
    
                        data1 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y1_array,
                            name: 'Total Occupied<br>Housing Units',
                            'text': y1_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': 'rgb(179,226,205)'
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
                        
                        data2 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y2_array,
                            name: 'Owner-Occupied<br>Units',
                            'text': y2_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': 'rgb(253,205,172)'
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        data3 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y3_array,
                            name: 'Renter-Occupied<br>Units',
                            'text': y3_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': 'rgb(203,213,232)'
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        var data = [data1, data2, data3];

                    }

                    if ( selected_submeasure.includes("YEARBUILT") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Oranges'];
    
                        var xaxis_title_text = '<b>Year Housing Unit Built</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 10;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Year Built, ${selected_year}</b>`;
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("UNITROOMS") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['GnBu'];
    
                        var xaxis_title_text = '<b>Rooms in Housing Unit</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Number of Rooms, ${selected_year}</b>`;

                        var x_tickvals = ['1 room', '2 rooms', '3 rooms', '4 rooms', '5 rooms', '6 rooms', '7 rooms', '8 rooms', '9 rooms or more'];
                        var x_ticktext = ['1 room', '2 rooms', '3 rooms', '4 rooms', '5 rooms', '6 rooms', '7 rooms', '8 rooms', '9 rooms<br>or more'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("UNITBEDROOMS") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['GnBu'];
    
                        var xaxis_title_text = '<b>Bedrooms in Housing Unit</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 11;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Number of Bedrooms, ${selected_year}</b>`;
                        var x_tickvals = ['No bedroom', '1 bedroom', '2 bedrooms', '3 bedrooms', '4 bedrooms', '5 or more bedrooms'];
                        var x_ticktext = ['No bedrooms', '1 bedroom', '2 bedrooms', '3 bedrooms', '4 bedrooms', '5 or more<br>bedrooms'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("HEATINGFUEL") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Pastel2'];
    
                        var xaxis_title_text = '<b>House Heating Fuel</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 10;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by House Heating Fuel, ${selected_year}</b>`;
                        var x_tickvals = ['Utility gas', 'Bottled, tank, or LP gas', 'Electricity', 'Fuel oil, kerosene, etc.', 'Coal or coke', 'Wood', 'Solar energy', 'Other fuel', 'No fuel used'];
                        var x_ticktext = ['Utility gas', 'Bottled, tank,<br>or LP gas', 'Electricity', 'Fuel oil, kerosene,<br>etc.', 'Coal or coke', 'Wood', 'Solar energy', 'Other fuel', 'No fuel used'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("LACKINGFACILITIES") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Pastel2'];
    
                        var xaxis_title_text = '<b>Type of Facilities</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        var xaxis_standoff = 20;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Lacking Facilities, ${selected_year}</b>`;
                        var x_tickvals = ['Lacking complete plumbing facilities', 'Lacking complete kitchen facilities', 'No telephone service available'];
                        var x_ticktext = ['Lacking complete<br>plumbing facilities', 'Lacking complete<br>kitchen facilities', 'No telephone service<br>available'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("OCCUPANTSPERROOM") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Pastel2'];
    
                        var xaxis_title_text = '<b>Occupants Per Room</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Occupants Per Room, ${selected_year}</b>`;
                        var xaxis_standoff = 20;
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("MORTGAGESMOC") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['YlOrRd_9'];
    
                        var xaxis_title_text = '<b>Monthly Owner Costs</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        var xaxis_standoff = 20;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units (with Mortgages) by Monthly Owner Costs, ${selected_year}</b>`;
                        var x_tickvals = ['Less than $500', '$500 to $999', '$1,000 to $1,499', '$1,500 to $1,999', '$2,000 to $2,499', '$2,500 to $2,999', '$3,000 or more', '$2,000 or more'];
                        var x_ticktext = ['Less than<br>$500', '$500 to<br>999', '$1,000 to<br>1,499', '$1,500 to<br>1,999', '$2,000 to<br>2,499', '$2,500 to<br>2,999', '$3,000 or<br>more', '$2,000 or<br>more'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                       'line': {'color': '#111111', 'width': 1.5}
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("YEARMOVEDIN") ){
                        if ( selected_year < 2017 ) {
                            var y_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                            
                            var text = y_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                            });
                            var color_array = discrete_color_dict['GnBu'];
        
                            var xaxis_title_text = '<b>Year Householder Moved In</b>';
                            var yaxis_tickprefix = '';
                            var yaxis_ticksuffix = '';
                            var xlabels_size = 12;
                            var xaxis_standoff = 20;
                            
                            var yaxis_title_text = '<b>Number of Housing Units</b>';
                            var title_text = `<b>Housing Units by Year Householder Built In, ${selected_year}</b>`;
                            var x_tickvals = ['1969 or earlier', '1970 to 1979', '1980 to 1989', '1990 to 1999', '2000 to 2004', '2005 or later', '2000 to 2009', '2010 or later', '1979 or earlier', '2010 to 2014', '2015 or later', '1989 or earlier', '2015 to 2016', '2017 or later', '2015 to 2018', '2019 or later', '2010 to 2017', '2018 to 2020', '2021 or later'];
                            var x_ticktext = ['1969 or<br>earlier', '1970 to<br>1979', '1980 to<br>1989', '1990 to<br>1999', '2000 to<br>2004', '2005 or<br>later', '2000 to<br>2009', '2010 or<br>later', '1979 or<br>earlier', '2010 to<br>2014', '2015 or<br>later', '1989 or<br>earlier', '2015 to<br>2016', '2017 or<br>later', '2015 to<br>2018', '2019 or<br>later', '2010 to<br>2017', '2018 to<br>2020', '2021 or<br>later'];
        
                            var data = [{
                                'type': 'bar',
                                'x': x_array,
                                'y': y_array,
                                'text': text,
                                'textposition': 'auto',
                                'marker': {'color': color_array,
                                           'line': {'color': '#111111', 'width': 1.5}
                                           },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            }];
                        }
                        if ( selected_year >= 2017 ) {
                            var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                            var y2_array = my_array.map(({value_OWNER}) => value_OWNER);
                            var y3_array = my_array.map(({value_RENTER}) => value_RENTER);
                            
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var y3_text = y3_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
        
                            var xaxis_title_text = '<b>Year Householder Moved In</b>';
                            var yaxis_tickprefix = '';
                            var yaxis_ticksuffix = '';
                            var xlabels_size = 12;
                            var xaxis_standoff = 20;
                            
                            var yaxis_title_text = '<b>Number of Housing Units</b>';
                            var title_text = `<b>Housing Units by Year Householder Built In, ${selected_year}</b>`;
                            var x_tickvals = ['1969 or earlier', '1970 to 1979', '1980 to 1989', '1990 to 1999', '2000 to 2004', '2005 or later', '2000 to 2009', '2010 or later', '1979 or earlier', '2010 to 2014', '2015 or later', '1989 or earlier', '2015 to 2016', '2017 or later', '2015 to 2018', '2019 or later', '2010 to 2017', '2018 to 2020', '2021 or later'];
                            var x_ticktext = ['1969 or<br>earlier', '1970 to<br>1979', '1980 to<br>1989', '1990 to<br>1999', '2000 to<br>2004', '2005 or<br>later', '2000 to<br>2009', '2010 or<br>later', '1979 or<br>earlier', '2010 to<br>2014', '2015 or<br>later', '1989 or<br>earlier', '2015 to<br>2016', '2017 or<br>later', '2015 to<br>2018', '2019 or<br>later', '2010 to<br>2017', '2018 to<br>2020', '2021 or<br>later'];

                            data1 = {
                                'type': 'bar',
                                'x': x_array,
                                'y': y1_array,
                                name: 'Total Housing<br>Units',
                                'text': y1_text,
                                'textposition': 'auto',
                                'marker': {'line': {'color': '#111111', 'width': 1.5},
                                           'color': 'rgb(179,226,205)'
                                           },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            };
                        
                            data2 = {
                                'type': 'bar',
                                'x': x_array,
                                'y': y2_array,
                                name: 'Owner-Occupied<br>Units',
                                'text': y2_text,
                                'textposition': 'auto',
                                'marker': {'line': {'color': '#111111', 'width': 1.5},
                                           'color': 'rgb(253,205,172)'
                                           },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            };
        
                            data3 = {
                                'type': 'bar',
                                'x': x_array,
                                'y': y3_array,
                                name: 'Renter-Occupied<br>Units',
                                'text': y3_text,
                                'textposition': 'auto',
                                'marker': {'line': {'color': '#111111', 'width': 1.5},
                                           'color': 'rgb(203,213,232)'
                                           },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            };
        
                            var data = [data1, data2, data3];
                        }
                    }
                    
                }

                if ( selected_submeasure.startsWith("Poverty") ) {
                    
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_BELOW}) => value_BELOW);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    var yaxis_title_text = '<b>Number of Individuals</b>';

                    if ( selected_submeasure.includes("RACE") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin (of any race)', 'White, not Hispanic or Latino'];
                        var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];
                        var title_text = `<b>Population Below Poverty Level by Race, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'Total Population',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(179,226,205)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Population Below<br>Poverty Level',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(251,180,174)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2];
                    
                }


                if ( selected_submeasure.startsWith("HealthInsuranceCoverage") ) {
                    
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_INSURED}) => value_INSURED);
                    var y3_array = my_array.map(({value_UNINSURED}) => value_UNINSURED);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    var yaxis_title_text = '<b>Number of Individuals</b>';

                    if ( selected_submeasure.includes("RACE") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'White, not Hispanic or Latino', 'Hispanic or Latino (of any race)'];
                        var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'White, not Hispanic<br>or Latino', 'Hispanic or Latino<br>(of any race)'];
                        var title_text = `<b>Insurance Coverage by Race, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'Total Population',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(179,226,205)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Insured',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(253,205,172)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    data3 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y3_array,
                        name: 'Uninsured',
                        'text': y3_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(203,213,232)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3];
                    
                }



                if ( selected_submeasure.startsWith("TransportationMethodstoWork") ) {
                    
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_MALE}) => value_MALE);
                    var y3_array = my_array.map(({value_FEMALE}) => value_FEMALE);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    var yaxis_title_text = '<b>Number of Workers</b>';

                    if ( selected_submeasure.includes("_METHODSTOWORK_") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 10;
                        var xaxis_title_text = '<b>Methods of Transportation</b>';
                        
                        var x_tickvals = ['Drove alone', 'Carpooled', 'Public transportation (excluding taxicab)', 'Walked', 'Bicycle', 'Taxicab, motorcycle, or other means', 'Worked from home'];
                        var x_ticktext = ['Drove alone', 'Carpooled', 'Public transport<br>(excluding taxicab)', 'Walked', 'Bicycle', 'Taxicab, motorcycle,<br>or other means', 'Worked from<br>home'];
                        var title_text = `<b>Methods of Transportation for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    if ( selected_submeasure.includes("_DEPARTURE_") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Departure Times</b>';
                        
                        var x_tickvals = ['12:00AM to 4:59AM', '5:00AM to 5:29AM', '5:30AM to 5:59AM', '6:00AM to 6:29AM', '6:30AM to 6:59AM', '7:00AM to 7:29AM', '7:30AM to 7:59AM', '8:00AM to 8:29AM', '8:30AM to 8:59AM', '9:00AM to 11:59PM'];
                        var x_ticktext = ['12:00AM<br>to<br>4:59AM', '5:00AM<br>to<br>5:29AM', '5:30AM<br>to<br>5:59AM', '6:00AM<br>to<br>6:29AM', '6:30AM<br>to<br>6:59AM', '7:00AM<br>to<br>7:29AM', '7:30AM<br>to<br>7:59AM', '8:00AM<br>to<br>8:29AM', '8:30AM<br>to<br>8:59AM', '9:00AM<br>to<br>11:59PM'];
                        var title_text = `<b>Departure Times for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    if ( selected_submeasure.includes("_VEHICLESAVAILABLE_") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Vehicles Availability</b>';
                        
                        var x_tickvals = ['No vehicle available', '1 vehicle available', '2 vehicles available', '3 or more vehicles available'];
                        var x_ticktext = ['No vehicle', '1 vehicle', '2 vehicles', '3 or more<br>vehicles'];
                        var title_text = `<b>Vehicles Available for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    if ( selected_submeasure.includes("TRAVEL") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 8;
                        var xaxis_title_text = '<b>Travel Times</b>';

                        var x_tickvals = ['Less than 10 minutes', '10 to 14 minutes', '15 to 19 minutes', '20 to 24 minutes', '25 to 29 minutes', '30 to 34 minutes', '35 to 44 minutes', '45 to 59 minutes', '60 minutes or more'];
                        var x_ticktext = ['Under 10 mins.', '10 to 14 mins.', '15 to 19 mins.', '20 to 24 mins.', '25 to 29 mins.', '30 to 34 mins.', '35 to 44 mins.', '45 to 59 mins.', '60 mins. or more'];
                        
                        
                        var title_text = `<b>Travel Times for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'All Workers',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(229,216,189)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Male Workers',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(179,205,227)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    data3 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y3_array,
                        name: 'Female Workers',
                        'text': y3_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(244,202,228)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3];
                    
                }

                if ( selected_submeasure.startsWith("WorkHours") && selected_submeasure.includes("USUALHOURS_LONG") ) {
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_MALE}) => value_MALE);
                    var y3_array = my_array.map(({value_FEMALE}) => value_FEMALE);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;

                    var xaxis_standoff = 20;
                    
                    var y1_text = y1_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                    });
                    var y2_text = y2_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                    });
                    var y3_text = y3_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                    });

                    var xaxis_title_text = '<b>Usual Hours Worked Weekly</b>';
                    
                    var yaxis_title_text = '<b>Number of Workers</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                    var x_tickvals = ['Usually worked 35 hours or more per week', 'Usually worked 15 to 34 hours per week', 'Usually worked 1 to 14 hours per week'];
                    var x_ticktext = ['35 hours or<br>more per week', '15 to 34 hours<br>per week', '1 to 14 hours<br>per week'];
                    
                    var title_text = `<b>Civilian Employed Workers by Usual Hours Worked, ${selected_year}</b>`;

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'All Workers',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(229,216,189)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Male Workers',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(179,205,227)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    data3 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y3_array,
                        name: 'Female Workers',
                        'text': y3_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                   'color': 'rgb(244,202,228)'
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3];
                }

                if ( selected_submeasure.startsWith("WorkHours") && selected_submeasure.includes("MEANHOURS_LONG") ) {
                    var y_array = my_array.map(({value}) => value);
                        
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "<br>hours</b>";
                    });

                    var xaxis_title_text = '<b></b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                    var xlabels_size = 12;
                    var xaxis_standoff = 20;
                    
                    var yaxis_title_text = '<b>Mean Hours Worked Weekly</b>';
                    var title_text = `<b>Civilian Employed Workers by Mean Hours Worked, ${selected_year}</b>`;
                    var x_tickvals = ['Total', 'Male', 'Female'];
                    var x_ticktext = ['All<br>Workers', 'Male<br>Workers', 'Female<br>Workers'];

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': ['rgb(229,216,189)', 'rgb(179,205,227)', 'rgb(244,202,228)'],
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("CharacteristicsoftheEconomicPopulation")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                    });

                    var yaxis_title_text = '<b>Number of Civilian Workers</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    if (selected_submeasure.includes("INDUSTRY_LONG")){
                        var title_text = `<b>Civilian Workers by Industry, ${selected_year}</b>`;
                        var color_array = discrete_color_dict['Set3'];
                        
                        var x_tickvals = ['Agriculture, forestry, fishing and hunting, and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation and warehousing, and utilities', 'Information', 'Finance and insurance, and real estate and rental and leasing', 'Professional, scientific, and management, and administrative and waste management services', 'Educational services, and health care and social assistance', 'Arts, entertainment, and recreation, and accommodation and food services', 'Other services, except public administration', 'Public administration'];
                        var x_ticktext = ['Agriculture, forestry,<br>fishing, hunting<br>and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation,<br>warehousing,<br>utilities', 'Information', 'Finance, insurance,<br>real estate, rental<br>and leasing', 'Professional, scientific,<br>management, admin.,<br>waste management', 'Education,<br>healthcare,<br>social assistance', 'Arts, entertainment,<br>recreation, shelter,<br>and food', 'Other services', 'Public<br>administration'];
                        var xlabels_size = 8;
                    
                    } else if (selected_submeasure.includes("OCCUPATION")){
                        var title_text = `<b>Civilian Workers by Occupation, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Occupation</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Management, business, science, and arts occupations', 'Service occupations', 'Sales and office occupations', 'Natural resources, construction, and maintenance occupations', 'Production, transportation, and material moving occupations'];
                        var x_ticktext = ['Managerial,<br>business,<br>science, and arts', 'Services', 'Sales and office', 'Natural resources,<br>construction,<br>maintenance', 'Production,<br>transportation,<br>material moving'];
                        var xlabels_size = 11;
                        var xaxis_standoff = 20;
                    
                    } else if (selected_submeasure.includes("CLASS")){
                        var title_text = `<b>Civilian Workers by Sector, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Sector</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Private wage and salaried workers', 'Government workers', 'Self-employed in own/unincorporated business workers', 'Unpaid family workers'];
                        var x_ticktext = ['Private wage and<br>salaried workers', 'Government<br>workers', 'Self-employed<br>workers', 'Unpaid family<br>workers'];
                        var xlabels_size = 12;
                        var xaxis_standoff = 20;
                        
                    } else if (selected_submeasure.includes("EARNINGS")){
                        var title_text = `<b>Median Earnings for All Civilian Workers by Industry, ${selected_year}</b>`;
                        if (selected_submeasure.includes("FULL")){
                            var title_text = `<b>Median Earnings for Full-Time Civilian Workers by Industry, ${selected_year}</b>`;
                        }
                        var color_array = discrete_color_dict['Set3'];

                        var yaxis_tickprefix = '$';
                        var y_array = my_array.map(({value_TOTAL}) => value_TOTAL);

                        var ystr_array = my_array.map(({value_TOTAL_string}) => value_TOTAL_string);
                        var text = ystr_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                        });
                        var yaxis_title_text = '<b>Earnings ($)</b>';
                        
                        var x_tickvals = ['Agriculture, forestry, fishing and hunting, and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation and warehousing, and utilities', 'Information', 'Finance and insurance, and real estate and rental and leasing', 'Professional, scientific, and management, and administrative and waste management services', 'Educational services, and health care and social assistance', 'Arts, entertainment, and recreation, and accommodation and food services', 'Other services, except public administration', 'Public administration'];
                        var x_ticktext = ['Agriculture, forestry,<br>fishing, hunting<br>and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation,<br>warehousing,<br>utilities', 'Information', 'Finance, insurance,<br>real estate, rental<br>and leasing', 'Professional, scientific,<br>management, admin.,<br>waste management', 'Education,<br>healthcare,<br>social assistance', 'Arts, entertainment,<br>recreation, shelter,<br>and food', 'Other services', 'Public<br>administration'];
                        var xlabels_size = 8;
                    
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("Population")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                    });

                    var yaxis_title_text = '<b>Population</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    if (selected_submeasure.includes("RACE")){
                        var title_text = `<b>Population by Race, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino (of any race)', 'White alone, not Hispanic or Latino'];
                        var x_ticktext = ['White', 'Black or<br>African American', 'American Indian<br>and Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White alone, not<br>Hispanic or Latino'];
                        var xlabels_size = 9;
                    
                    } else if (selected_submeasure.includes("ASIAN")){
                        var title_text = `<b>Asian Population, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Asian Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Asian Indian', 'Chinese', 'Filipino', 'Japanese', 'Korean', 'Vietnamese', 'Other Asian'];
                        var x_ticktext = ['Asian<br>Indian', 'Chinese', 'Filipino', 'Japanese', 'Korean', 'Vietnamese', 'Other<br>Asian'];
                        var xlabels_size = 13;
                        var xaxis_standoff = 20;
                    
                    } else if (selected_submeasure.includes("INDIGENOUS")){
                        var title_text = `<b>American Indian and Alaska Native Population, ${selected_year}</b>`;
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Cherokee', 'Chippewa', 'Navajo', 'Sioux', 'Aztec', 'Blackfeet Tribe of the Blackfeet Indian Reservation of Montana', 'Maya', 'Native Village of Barrow Inupiat Traditional Government', 'Navajo Nation', 'Nome Eskimo Community', 'Other American Indian and Alaska Native'];
                        var x_ticktext = ['Cherokee', 'Chippewa', 'Navajo', 'Sioux', 'Aztec', 'Blackfeet Tribe of the<br>Blackfeet Indian<br>Reservation of Montana', 'Maya', 'Native Village of<br>Barrow Inupiat<br>Traditional Government', 'Navajo Nation', 'Nome Eskimo<br>Community', 'Other American Indian<br>and Alaska Native'];
                        var xlabels_size = 9;
                        
                    } else if (selected_submeasure.includes("HISPANICLATINO")){
                        var title_text = `<b>Hispanic/Latino Population, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Hispanic/Latino Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Mexican', 'Puerto Rican', 'Cuban', 'Other Hispanic or Latino'];
                        var x_ticktext = ['Mexican', 'Puerto Rican', 'Cuban', 'Other Hispanic/<br>Latino'];
                        var xlabels_size = 14;
                        var xaxis_standoff = 20;
                    
                    } else if (selected_submeasure.includes("NATIVEHAWAIIANPACIFICISLANDER")){
                        var title_text = `<b>Native Hawaiian and Pacific Islander Population, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Native Hawaiian and Pacific Islander Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Native Hawaiian', 'Guamanian or Chamorro', 'Samoan', 'Other Pacific Islander', 'Chamorro', 'Other Native Hawaiian or Pacific Islander'];
                        var x_ticktext = ['Native Hawaiian', 'Guamanian or<br>Chamorro', 'Samoan', 'Other Pacific<br>Islander', 'Chamorro', 'Other Native Hawaiian<br>or Pacific Islander'];
                        var xlabels_size = 12;
                        var xaxis_standoff = 17;
                        
                    } else if (selected_submeasure.includes("_AGE_")){
                        var title_text = `<b>Population by Age Demographic, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Age Demographics</b>';
                        var color_array = discrete_color_dict['Blues'];
                        
                        var x_tickvals = ['Under 5', '5-9', '10-14', '15-19', '20-24', '25-34', '35-44', '45-54', '55-59', '60-64', '65-74', '75-84', '85+'];
                        var x_ticktext = ['Under 5', '5-9', '10-14', '15-19', '20-24', '25-34', '35-44', '45-54', '55-59', '60-64', '65-74', '75-84', '85+'];
                        var xlabels_size = 10;
                        var xaxis_standoff = 20;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                   'line': {'color': '#111111', 'width': 1.5}
                                   },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("Education") ) {
                    if ( selected_submeasure.includes("_AGE_") || selected_submeasure.includes("_RACE_") ) {
                        var y1_array = my_array.map(({value_MALE}) => value_MALE);
                        var y2_array = my_array.map(({value_FEMALE}) => value_FEMALE);
                        
                        var xlabels_size;
                        var x_ticktext;
                        var x_tickvals;
    
                        var xaxis_standoff = 20;
    
                        var xaxis_title_text = '<b>Educational Attainment</b>';
                        
                        var yaxis_title_text = '<b>Number of Individuals</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var x_tickvals = ['Less than 9th grade', '9th to 12th grade, no diploma', 'Less than high school diploma', 'High school graduate (includes equivalency)', 'Some college, no degree', "Some college or associate's degree", "Associate's degree", "Bachelor's degree", 'Graduate or professional degree', "Bachelor's degree or higher"];
                        var x_ticktext = ['Less than<br>9th grade', '9th to 12th grade<br>(No diploma)', 'Less than high<br>school graduate', 'High school graduate<br>(or equivalent)', 'Some college<br>(No degree)', "Some college or<br>associate's degree", "Associate's<br>degree", "Bachelor's<br>degree", 'Graduate or<br>professional<br>degree', "Bachelor's degree<br>or higher"];
                        
                        if ( selected_submeasure.includes("_AGE_") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                            });
                            var xlabels_size = 10;
                        }
                        if ( selected_submeasure.includes("_RACE_") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var xlabels_size = 11;
                        }
                        
                        var title_text = `<b>Individuals by Educational Attainment, ${selected_year}</b>`;
                        
                        data1 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y1_array,
                            name: 'Men',
                            'text': y1_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': 'rgb(179,205,227)'
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        data2 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y2_array,
                            name: 'Women',
                            'text': y2_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': 'rgb(244,202,228)'
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        var data = [data1, data2];
                    }

                    if ( selected_submeasure.includes("CITIZENSHIP") ) {
                        var y1_array = my_array.map(({value_BORNINSTATE}) => value_BORNINSTATE);
                        var y2_array = my_array.map(({value_BORNOUTSTATE}) => value_BORNOUTSTATE);
                        var y3_array = my_array.map(({value_NATIVEOUTSIDE}) => value_NATIVEOUTSIDE);
                        var y4_array = my_array.map(({value_FOREIGN}) => value_FOREIGN);

                        var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                            });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                        });
                        var y4_text = y4_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var x_ticktext;
                        var x_tickvals;
    
                        var xaxis_standoff = 10;
    
                        var xaxis_title_text = '<b>Educational Attainment</b>';
                        
                        var yaxis_title_text = '<b>Number of Individuals</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var x_tickvals = ['Less than high school graduate', 'High school graduate (includes equivalency)', "Some college or associate's degree", "Bachelor's degree", 'Graduate or professional degree'];
                        var x_ticktext = ['Less than high<br>school graduate', 'High school graduate<br>(or equivalent)', "Some college or<br>associate's degree", "Bachelor's<br>degree", 'Graduate or<br>professional<br>degree'];
                        
                        var title_text = `<b>Individuals by Educational Attainment, ${selected_year}</b>`;
                        
                        data1 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y1_array,
                            name: 'Born in-state',
                            'text': y1_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': discrete_color_dict['Pastel2'][0]
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        data2 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y2_array,
                            name: 'Born out-of-state',
                            'text': y2_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': discrete_color_dict['Pastel2'][1]
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };

                        data3 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y3_array,
                            name: 'Native (born<br>outside the U.S.)',
                            'text': y3_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': discrete_color_dict['Pastel2'][2]
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };

                        data4 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y4_array,
                            name: 'Foreign-born',
                            'text': y4_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                       'color': discrete_color_dict['Pastel2'][3]
                                       },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        var data = [data1, data2, data3, data4];
                    }
                }


                

                
                
        
                var layout = {
                    'margin': {'b': 100, 't': 100, 'r': 80},
                    'xaxis': {'title': {'text': xaxis_title_text, 'standoff': xaxis_standoff},
                              'tickfont': {'size': xlabels_size},
                              'tickvals': x_tickvals,
                              'ticktext': x_ticktext
                             },
                    'yaxis': {'title': {'text': yaxis_title_text, 'standoff': 10},
                              'ticklabelstandoff': 5,
                              'tickprefix': yaxis_tickprefix,
                              'ticksuffix': yaxis_ticksuffix,
                              },
                    'barmode': barmode,
                    'paper_bgcolor': '#FEF9F3',
                    'plot_bgcolor': '#FEF9F3',
                    'title': {'text': title_text,
                              'x': 0.05,
                              'subtitle': {'text': `${tract_name}, ${city_string}`}
                              }
                };
            }

            if ( selected_submeasure.includes("TIME") ) {
                var my_array = tooltip_data.filter(item => item['TRACT'] == tract_name);
                var x_array = my_array.map(({YEAR}) => YEAR);


                if ( selected_submeasure.startsWith("ContractRent") ) {
                    var y1_array = my_array.map(({Lowercontractrentquartile}) => Lowercontractrentquartile);
                    var y2_array = my_array.map(({Mediancontractrent}) => Mediancontractrent);
                    var y3_array = my_array.map(({Uppercontractrentquartile}) => Uppercontractrentquartile);
                     
                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': '25th Percentile<br>Contract Rent',
                         'line': {'color': '#E3242B', 'dash': 'dashdot'},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'Median Contract<br>Rent',
                         'line': {'color': '#990F02'},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': '75th Percentile<br>Contract Rent',
                         'line': {'color': '#551606', 'dash': 'dashdot'},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
    
                    var data = [data3, data2, data1];
                    
                    var yaxis_title_text = '<b>Contract Rents</b>';
                    var yaxis_tickprefix = '$';
                    var yaxis_ticksuffix = '';
                    
                    var title_text = `<b>Contract Rents, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;

                }

                

                if ( selected_submeasure.startsWith("RentBurden") && !selected_submeasure.includes("AGE") && !selected_submeasure.includes("INCOME") ) {
                    var y1_array = my_array.map(({ESTIMATE_Totalrenters_RentBurden}) => ESTIMATE_Totalrenters_RentBurden);
                    var y2_array = my_array.map(({ESTIMATE_Totalrenters_SevereRentBurden}) => ESTIMATE_Totalrenters_SevereRentBurden);
                     
                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'Rent Burden',
                         'line': {'color': discrete_color_dict['Reds_2'][0]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'Severe Rent Burden',
                         'line': {'color': discrete_color_dict['Reds_2'][1]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
    
                    var data = [data1, data2];
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Rent Burden Severity, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                }

                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("AGE") ) {
                    var y1_array = my_array.map(({ESTIMATE_Totalrenters_AGE_RentBurden}) => ESTIMATE_Totalrenters_AGE_RentBurden);
                    var y2_array = my_array.map(({ESTIMATE_Totalrenters_AGE_15to24_RentBurden}) => ESTIMATE_Totalrenters_AGE_15to24_RentBurden);
                    var y3_array = my_array.map(({ESTIMATE_Totalrenters_AGE_25to34_RentBurden}) => ESTIMATE_Totalrenters_AGE_25to34_RentBurden);
                    var y4_array = my_array.map(({ESTIMATE_Totalrenters_AGE_35to64_RentBurden}) => ESTIMATE_Totalrenters_AGE_35to64_RentBurden);
                    var y5_array = my_array.map(({ESTIMATE_Totalrenters_AGE_65andOlder_RentBurden}) => ESTIMATE_Totalrenters_AGE_65andOlder_RentBurden);

                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'Overall',
                         'line': {'color': discrete_color_dict['Okabe_8'][0]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': '15 to 24',
                         'line': {'color': discrete_color_dict['Okabe_8'][1]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': '25 to 34',
                         'line': {'color': discrete_color_dict['Okabe_8'][2]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data4 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y4_array,
                         'name': '35 to 64',
                         'line': {'color': discrete_color_dict['Okabe_8'][3]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data5 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y5_array,
                         'name': '65 and older',
                         'line': {'color': discrete_color_dict['Okabe_8'][5]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data = [data1, data2, data3, data4, data5];
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Rent-Burdened Renters by Age, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;

                }
                
                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("INCOME") ) {
                    var y1_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_RentBurden);
                    var y2_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_Lessthan10000_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_Lessthan10000_RentBurden);
                    var y3_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_10000to19999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_10000to19999_RentBurden);
                    var y4_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_20000to34999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_20000to34999_RentBurden);
                    var y5_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_35000to49999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_35000to49999_RentBurden);
                    var y6_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_50000to74999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_50000to74999_RentBurden);
                    var y7_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_75000to99999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_75000to99999_RentBurden);
                    var y8_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_100000ormore_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_100000ormore_RentBurden);

                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'Overall',
                         'line': {'color': discrete_color_dict['Okabe_8'][0]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'Less than $10k',
                         'line': {'color': discrete_color_dict['Okabe_8'][1]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': '$10k to 19.9k',
                         'line': {'color': discrete_color_dict['Okabe_8'][2]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data4 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y4_array,
                         'name': '$20k to 34.9k',
                         'line': {'color': discrete_color_dict['Okabe_8'][3]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data5 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y5_array,
                         'name': '$35k to 49.9k',
                         'line': {'color': discrete_color_dict['Okabe_8'][4]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data6 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y6_array,
                         'name': '$50k to 74.9k',
                         'line': {'color': discrete_color_dict['Okabe_8'][5]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data7 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y7_array,
                         'name': '$75k to 99.9k',
                         'line': {'color': discrete_color_dict['Okabe_8'][6]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data8 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y8_array,
                         'name': '$100k or more',
                         'line': {'color': discrete_color_dict['Okabe_8'][7]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data = [data1, data2, data3, data4, data5, data6, data7, data8];
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Rent-Burdened Renters by Income, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("RACE_TIME")  ) {
                    var y1_array = my_array.map(({Overall16andOlder}) => Overall16andOlder);
                    var y2_array = my_array.map(({White}) => White);
                    var y3_array = my_array.map(({BlackorAfricanAmerican}) => BlackorAfricanAmerican);
                    var y4_array = my_array.map(({AmericanIndianandAlaskaNative}) => AmericanIndianandAlaskaNative);
                    var y5_array = my_array.map(({Asian}) => Asian);
                    var y6_array = my_array.map(({NativeHawaiianandOtherPacificIslander}) => NativeHawaiianandOtherPacificIslander);
                    var y7_array = my_array.map(({Someotherrace}) => Someotherrace);
                    var y8_array = my_array.map(({Twoormoreraces}) => Twoormoreraces);
                    var y9_array = my_array.map(({HispanicorLatinooriginofanyrace}) => HispanicorLatinooriginofanyrace);
                    var y10_array = my_array.map(({WhitenotHispanicorLatino}) => WhitenotHispanicorLatino);

                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'Overall (16 and Older)',
                         'line': {'color': discrete_color_dict['G10'][0]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'White',
                         'line': {'color': discrete_color_dict['G10'][1]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': 'Black or African<br>American',
                         'line': {'color': discrete_color_dict['G10'][2]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data4 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y4_array,
                         'name': 'American Indian and<br>Alaska Native',
                         'line': {'color': discrete_color_dict['G10'][3]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data5 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y5_array,
                         'name': 'Asian',
                         'line': {'color': discrete_color_dict['G10'][4]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data6 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y6_array,
                         'name': 'Native Hawaiian and<br>Other Pacific Islander',
                         'line': {'color': discrete_color_dict['G10'][5]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data7 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y7_array,
                         'name': 'Some other race',
                         'line': {'color': discrete_color_dict['G10'][6]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data8 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y8_array,
                         'name': 'Two or more races',
                         'line': {'color': discrete_color_dict['G10'][7]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data9 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y9_array,
                         'name': 'Hispanic or Latino<br>(of any race)',
                         'line': {'color': discrete_color_dict['G10'][8]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data10 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y10_array,
                         'name': 'White, not Hispanic<br>or Latino',
                         'line': {'color': discrete_color_dict['G10'][9]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Race, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Race, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Race, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    }
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("SEX_TIME")  ) {
                    var y1_array = my_array.map(({Overall20to64}) => Overall20to64);
                    var y2_array = my_array.map(({Male}) => Male);
                    var y3_array = my_array.map(({Female}) => Female);
                    var y4_array = my_array.map(({FemaleWithchildrenunder6yearsold}) => FemaleWithchildrenunder6yearsold);
                    var y5_array = my_array.map(({FemaleWithchildrenunder18yearsold}) => FemaleWithchildrenunder18yearsold);
                    var y6_array = my_array.map(({FemaleWithchildrenunder17yearsold}) => FemaleWithchildrenunder17yearsold);
                    var y7_array = my_array.map(({FemaleWithchildren6to17yearsold}) => FemaleWithchildren6to17yearsold);

                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'Overall (20 to 64)',
                         'line': {'color': discrete_color_dict['D3_7'][0]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'Male',
                         'line': {'color': discrete_color_dict['D3_7'][1]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': 'Female',
                         'line': {'color': discrete_color_dict['D3_7'][2]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data4 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y4_array,
                         'name': 'Female (With children<br>under 6 years old)',
                         'line': {'color': discrete_color_dict['D3_7'][3]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data5 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y5_array,
                         'name': 'Female (With children<br>under 18 years old)',
                         'line': {'color': discrete_color_dict['D3_7'][4]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data6 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y6_array,
                         'name': 'Female (With children<br>under 17 years old)',
                         'line': {'color': discrete_color_dict['D3_7'][5]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data7 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y7_array,
                         'name': 'Female (With children<br>6 to 17 years old)',
                         'line': {'color': discrete_color_dict['D3_7'][6]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3, data4, data5, data6, data7];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Sex, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Sex, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Sex, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    }
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("EDUCATIONALSTATUS_TIME")  ) {
                    var y1_array = my_array.map(({Overall25to64}) => Overall25to64);
                    var y2_array = my_array.map(({Lessthanhighschoolgraduate}) => Lessthanhighschoolgraduate);
                    var y3_array = my_array.map(({Highschoolgraduateincludesequivalency}) => Highschoolgraduateincludesequivalency);
                    var y4_array = my_array.map(({Somecollegeorassociatesdegree}) => Somecollegeorassociatesdegree);
                    var y5_array = my_array.map(({Bachelorsdegreeorhigher}) => Bachelorsdegreeorhigher);

                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'Overall (25 to 64)',
                         'line': {'color': discrete_color_dict['D3_5'][0]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'Less than high<br>school graduate',
                         'line': {'color': discrete_color_dict['D3_5'][1]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': 'High school graduate<br>(or equivalent)',
                         'line': {'color': discrete_color_dict['D3_5'][2]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data4 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y4_array,
                         'name': "Some college or<br>associate's degree",
                         'line': {'color': discrete_color_dict['D3_5'][3]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data5 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y5_array,
                         'name': "Bachelor's degree<br>or higher",
                         'line': {'color': discrete_color_dict['D3_5'][5]},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3, data4, data5];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Educational Attainment, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Educational Attainment,<br>${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Educational Attainment,<br>${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    }
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                }

                if ( selected_submeasure.startsWith("WorkHours") && selected_submeasure.includes("MEANHOURS_TIME")  ) {
                    var y1_array = my_array.map(({Total}) => Total);
                    var y2_array = my_array.map(({Male}) => Male);
                    var y3_array = my_array.map(({Female}) => Female);

                    var data1 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y1_array,
                         'name': 'All<br>Workers',
                         'line': {'color': 'rgb(194, 163, 99)'},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data2 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y2_array,
                         'name': 'Male<br>Workers',
                         'line': {'color': 'rgb(90, 146, 194)'},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };

                    var data3 = {
                         'type': 'scatter',
                         'mode': 'lines+markers',
                         'x': x_array,
                         'y': y3_array,
                         'name': 'Female<br>Workers',
                         'line': {'color': 'rgb(221, 91, 172)'},
                         'hoverinfo': 'none',
                         'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3];

                    var yaxis_title_text = '<b>Mean Hours Worked Weekly</b>';
                    var title_text = `<b>Mean Hours Worked Weekly, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                }
                
                var layout = {
                    'margin': {'b': 100, 't': 100, 'r': 80},
                    'xaxis': {'title': {'text': '<b>Year</b>', 'standoff': 20},
                              'showgrid': false,
                              'tick0': Math.min(...x_array),
                              'dtick': 2
                              },
                    'yaxis': {'title': {'text': yaxis_title_text, 'standoff': 10},
                              'ticklabelstandoff': 5,
                              'gridcolor': '#E0E0E0',
                              'tickprefix': yaxis_tickprefix,
                              'ticksuffix': yaxis_ticksuffix,
                              },
                    'paper_bgcolor': '#FEF9F3',
                    'plot_bgcolor': '#FEF9F3',
                    'title': {'text': title_text,
                              'x': 0.05, 'y': 0.94,
                              'subtitle': {'text': `${tract_name}, ${city_string}`}
                              }
                };
            
            }

            var bbox = hoverData['points']['0']['bbox'];
    
            var fig = {'data': data, 'layout': layout};
    
            return [true, fig, bbox];
        }
    }
    """,
    [Output('tooltip', 'show'),
     Output('tooltip-graph', 'figure'),
     Output('tooltip', 'bbox'),
    ],
    Input('year-dropdown', 'value'),
    Input('submeasure-dropdown', 'value'),
    Input('map', 'hoverData'),
    Input('tooltip_file', 'data'),
    Input('discrete_color_dict', 'data'),
    Input('place-dropdown', 'value'),
    Input('places-dict', 'data')
)





# ---- ---- EXECUTE THE APP ---- ----#
if __name__ == '__main__':
    app.run(debug=False)

