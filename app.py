# ------------ LIBRARIES ------------ #
import dash
from dash import dcc, html, clientside_callback, ClientsideFunction
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc

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

LA_County_FIPS = ca2020[ca2020.COUNTIES == 'Los Angeles County']
LA_County_keys = LA_County_FIPS['PLACENAME'].to_list()
LA_County_values = LA_County_FIPS['PLACENAME'].str.replace(' ', '').replace('LaCañadaFlintridge', 'LaCanadaFlintridge').to_list()

places_tuple = zip(LA_County_keys, LA_County_values)
places_options = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in places_tuple]
places_options = [dict(item) for item in places_options if item['value'] != 'PepperdineUniversity']

modified_values_1 = ['EastWhittier', 'Vincent']
modified_places_options_1 = [dict(item, **{'disabled': True}) if item['value'] in modified_values_1 else dict(item) for item in places_options]

modified_values_2 = ['EastWhittier']
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
                        # "Transportation Methods to Work",
                        # "Working Hours",
                        # "Other Economic Measures"
                       ]
measures_values_list = ['ContractRent',
                        'RentBurden',
                        'EmploymentStatistics',
                        'FoodStamps', 
                        'HealthInsuranceCoverage',
                        'HouseholdIncome',
                        'HousingUnitsandOccupancy',
                        'Poverty',
                        # 'TransportationMethodstoWork',
                        # 'WorkHours',
                        # 'CharacteristicsoftheEconomicPopulation'
                       ]
measures_tuple = zip(measures_labels_list, measures_values_list)
measures_options = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in measures_tuple]


modified_values = ['HealthInsuranceCoverage', 'Poverty', 'FoodStamps']
modified_measures_options_1 = [dict(item, **{'disabled': True}) if item['value'] in modified_values else dict(item) for item in measures_options]

modified_measures_options_2 = [dict(item, **{'disabled': True}) if item['value'] == 'FoodStamps' else dict(item) for item in measures_options]





# ---- Subcategory Measures Dropdown ---- #

submeasures_dict = dict()
for place in LA_County_values:
    dummy_dict = dict()
    
    # -- Contract Rent -- #
    dummy_labels_list = ['Distribution of Contract Rents',
                         'Contract Rents Over Time'
                        ]
    dummy_values_list = [f'ContractRent_{place}_LONG',
                         f'ContractRent_{place}_TIME'
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['ContractRent'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]
    
    
    # -- Rent Burden -- #
    dummy_labels_list = ['Rent/Severe Rent Burden Over Time', 'Rent Burden and Severe Rent Burden',
                         'Rent Burden by Age (Over Time)', 'Rent Burden by Age',
                         'Rent Burden by Income (Over Time)', 'Rent Burden by Income',
                        ]
    dummy_values_list = [f'RentBurden_{place}_TIME', f'RentBurden_{place}_LONG',
                         f'RentBurden_{place}_AGE_TIME', f'RentBurden_{place}_AGE_LONG',
                         f'RentBurden_{place}_INCOME_TIME', f'RentBurden_{place}_INCOME_LONG',
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['RentBurden'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]
    
    
    # -- Employment Statistics -- #
    dummy_labels_list = ['Unemp. Rate by Race (Over Time)', 'Unemployment Rate by Race',
                         'LFPR by Race (Over Time)', 'Labor Force Part. Rate by Race',
                         'Employ./Pop. Ratio by Race (Over Time)', 'Employ./Population Ratio by Race',
                         'Unemp. Rate by Sex (Over Time)', 'Unemployment Rate by Sex',
                         'LFPR by Sex (Over Time)', 'Labor Force Part. Rate by Sex',
                         'Employ./Pop. Ratio by Sex (Over Time)', 'Employ./Population Ratio by Sex',
                         'Unemp. Rate by Education (Over Time)', 'Unemployment Rate by Education',
                         'LFPR by Education (Over Time)', 'Labor Force Part. Rate by Education',
                         'Empl./Pop. Ratio by Education (Over Time)', 'Empl./Population Ratio by Education',
                        ]
    dummy_values_list = [f'EmploymentStatistics_{place}_UNEMP_RACE_TIME', f'EmploymentStatistics_{place}_UNEMP_RACE_LONG',
                         f'EmploymentStatistics_{place}_LFPR_RACE_TIME', f'EmploymentStatistics_{place}_LFPR_RACE_LONG',
                         f'EmploymentStatistics_{place}_EPOP_RACE_TIME', f'EmploymentStatistics_{place}_EPOP_RACE_LONG',
                         f'EmploymentStatistics_{place}_UNEMP_SEX_TIME', f'EmploymentStatistics_{place}_UNEMP_SEX_LONG',
                         f'EmploymentStatistics_{place}_LFPR_SEX_TIME', f'EmploymentStatistics_{place}_LFPR_SEX_LONG',
                         f'EmploymentStatistics_{place}_EPOP_SEX_TIME', f'EmploymentStatistics_{place}_EPOP_SEX_LONG',
                         f'EmploymentStatistics_{place}_UNEMP_EDUCATIONALSTATUS_TIME', f'EmploymentStatistics_{place}_UNEMP_EDUCATIONALSTATUS_LONG',
                         f'EmploymentStatistics_{place}_LFPR_EDUCATIONALSTATUS_TIME', f'EmploymentStatistics_{place}_LFPR_EDUCATIONALSTATUS_LONG',
                         f'EmploymentStatistics_{place}_EPOP_EDUCATIONALSTATUS_TIME', f'EmploymentStatistics_{place}_EPOP_EDUCATIONALSTATUS_LONG',
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['EmploymentStatistics'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]
    
    
    # -- Food Stamps -- #
    dummy_labels_list = ['Food Stamps Recipients (by Race)',
                         'Food Stamps Recipients (by Poverty Status)',
                         'Food Stamps Recipients (by Disability Status)',
                         'Food Stamps Recipients (by Working Status)',
                        ]
    dummy_values_list = [f'FoodStamps_{place}_RACE_LONG',
                         f'FoodStamps_{place}_POVERTY_LONG',
                         f'FoodStamps_{place}_DISABILITYSTATUS_LONG',
                         f'FoodStamps_{place}_WORKINGSTATUS_LONG'
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['FoodStamps'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]
    
    
    # -- Household Income -- #
    dummy_labels_list = ['Income Distribution (for Households)',
                         'Income Distribution (for Families)',
                         'Income Distribution (for Married Couples)',
                         'Income Distribution (for Nonfamily Households)',
                        ]
    dummy_values_list = [f'HouseholdIncome_{place}_HOUSEHOLDS_LONG',
                         f'HouseholdIncome_{place}_FAMILIES_LONG', 
                         f'HouseholdIncome_{place}_MARRIEDCOUPLEFAMILIES_LONG',
                         f'HouseholdIncome_{place}_NONFAMILYHOUSEHOLDS_LONG'
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['HouseholdIncome'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

    # -- Housing Units and Occupancy -- #
    dummy_labels_list = ['Home Values (Owner-Occupied Units)',
                         'Occupied Housing Units by Race',
                         'Occupied Housing Units by Age'
                        ]
    dummy_values_list = [f'HousingUnitsandOccupancy_{place}_HOMEVALUE_LONG',
                         f'HousingUnitsandOccupancy_{place}_RACE_HOUSINGUNITS_LONG',
                         f'HousingUnitsandOccupancy_{place}_AGE_HOUSINGUNITS_LONG',
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['HousingUnitsandOccupancy'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

    # -- Poverty -- #
    dummy_labels_list = ['Distribution of Poverty by Race',
                        ]
    dummy_values_list = [f'Poverty_{place}_RACE_LONG',
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['Poverty'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

    # -- Health Insurance Coverage -- #
    dummy_labels_list = ['Insurance Coverage by Race',
                        ]
    dummy_values_list = [f'HealthInsuranceCoverage_{place}_RACE_LONG',
                        ]
    dummy_tuple = zip(dummy_labels_list, dummy_values_list)
    dummy_dict['HealthInsuranceCoverage'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

    
    submeasures_dict[place] = dummy_dict




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
app.title = 'Los Angeles County Socioeconomic Profile'


app.layout = html.Div([
    html.Div(className = "row", children = [
        # ---- LEFT ---- #
        html.Div(className = "four columns", children = [
            html.H3("Los Angeles County Socioeconomic Profile"),
            html.P("Using the American Community Survey, this website allows you to visualize various socioeconomic measures for cities in Los Angeles County.",
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

        if ( ['Vincent'].includes(selected_place) ) {
            var years_options = modified_years_options_1;
        }
        if ( ['EastWhittier'].includes(selected_place) ||  ['HealthInsuranceCoverage', 'Poverty'].includes(selected_measure) ) {
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
    function(selected_place, selected_measure, submeasures_dict) {
        return submeasures_dict[selected_place][selected_measure];
    }
    """,
    Output('submeasure-dropdown', 'options'),
    Input('place-dropdown', 'value'),
    Input('measure-dropdown', 'value'),
    Input('submeasures-dict', 'data')
)




# ---- ---- DATA ---- ----#

# ---- --------------- ---- #
# ---- Masterfile Data ---- #
# ---- --------------- ---- #

app.clientside_callback(
    """
    async function(selected_year, selected_place, selected_measure) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/LongBeachSocioeconomicIndicators/${selected_year}/${selected_measure}_${selected_place}_${selected_year}.json`;
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
    async function(selected_year, selected_submeasure) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/LongBeachSocioeconomicIndicators/${selected_year}/${selected_submeasure}_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    }
    """,
    Output('tooltip_file', 'data'),
    Input('year-dropdown', 'value'),
    Input('submeasure-dropdown', 'value')
)


# ---- ------------ ---- #
# ---- Mapfile Data ---- #
# ---- ------------ ---- #

app.clientside_callback(
    """
    async function(selected_year) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/LosAngelesCounty_Census_mapfiles/LosAngelesCounty_LatLongPoints_${selected_year}.json`;
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
        var dummy_var = places_dict.find(item => item['value'] === selected_place);
        var city_string = Object.values(dummy_var['label']['props']['children']);
        
        var my_array = masterfile.filter(item => item['YEAR'] === selected_year);

        var locations_array = my_array.map(({GEO_ID}) => GEO_ID);

        var customdata_array = my_array.map(({TRACT}) => TRACT);

        if (selected_measure == 'ContractRent') {
            var z_array = my_array.map(({ESTIMATE_Mediancontractrent}) => ESTIMATE_Mediancontractrent);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
            var z_array = my_array.map(({ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars}) => ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Owner-Occupied Home Value (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars_string'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>Median<br>Owner-<br>Occupied<br>Home<br>Value</b>';
            var colorbar_tickprefix = '$';
            var colorbar_ticksuffix = '';

            if (selected_submeasure != undefined && selected_submeasure.includes("_HOUSINGUNITS_")){
                var z_array = my_array.map(({ESTIMATE_TotalHousingUnits}) => ESTIMATE_TotalHousingUnits);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Housing Units (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_TotalHousingUnits'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                
                var colorscale_color = 'Greens';
                var colorbar_title_text = '<b>Total<br>Housing<br>Units</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'Poverty') {
            var z_array = my_array.map(({ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined}) => ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + city_string + "<br><br>"
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


        
        

        var geometry_url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/LosAngelesCounty_Census_mapfiles/${selected_year}/mastergeometry_${selected_year}_${selected_place}.json`;

        
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
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size = 9;
                    
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

                    if (selected_submeasure.includes("HOMEVALUE_LONG")){
                        var yaxis_title_text = '<b>Number of Households</b>';
                        var title_text = `<b>Home Values for Owner-Occupied Housing Units, ${selected_year}</b>`;
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

                if ( selected_submeasure.startsWith("HousingUnitsandOccupancy") && selected_submeasure.includes("_HOUSINGUNITS_") ) {
                    
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
                
                var layout = {
                    'margin': {'b': 100, 't': 100, 'r': 80},
                    'xaxis': {'title': {'text': '<b>Year</b>', 'standoff': 10},
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

