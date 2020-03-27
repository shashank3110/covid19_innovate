from flask import Flask,jsonify,redirect
from flask import render_template,request
import csv
import requests
from collections import defaultdict
import folium
import json
import pandas as pd
from bs4 import BeautifulSoup
import time

url = "https://www.worldometers.info/coronavirus/"
def scrape_data(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.select('tbody > tr')
    data = [ ]
    for row in rows[:]:
        data.append([th.text.rstrip() for th in row.find_all('td')])
    return data

app = Flask(__name__,\
            template_folder = '/home/dhirensr/open_source/covid19_innovate/static/')

@app.route('/')
def index():
    return render_template("charts.html")

@app.route('/map')
def map_route():
    response = requests.get('https://api.rootnet.in/covid19-in/stats/daily')

    response_dict = response.json()
    states = defaultdict(dict)

    status = response_dict['success']
    cases = []#defaultdict()

    state_list=['Sikkim','Andhra Pradesh', 'Bihar', 'Chhattisgarh','Arunachal Pradesh',\
         'Delhi', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Karnataka', \
        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Mizoram', \
        'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Tamil Nadu',\
         'Chandigarh', 'Jammu and Kashmir',  'Uttar Pradesh',\
        'Uttarakhand', 'West Bengal','Telengana','Tripura','Assam',
        'Goa','Nagaland','Lakshadweep','Dadra and Nagar Haveli', 'Daman and Diu',
        'Jharkhand','Meghalaya','Andaman and Nicobar Islands']
    try:
        daily_data = response_dict['data']
        # to get  latest day data
        latest_data = daily_data[-1]
        latest_regional_data = latest_data['regional']
        latest_date = latest_data['day']
        latest_summary = latest_data['summary']

        const=0
        for item  in latest_regional_data:
            if item['loc']=='Ladakh':
                const = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
                continue
            else:
                k = item.pop('loc')
                states[k] = item
                total_cases = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
                cases.append( {'State':k ,'Total_Cases': total_cases})

        state_geo_data=json.load(open('/home/dhirensr/open_source/covid19_innovate/indian_states.json'))

        m = folium.Map([20.5937, 78.9629],zoom_start=4.35) # centered on coordinates of india




        for st in state_list:
            if st not in states.keys():
                cases.append( {'State':st ,'Total_Cases': 0})
            states[st] = {'confirmedCasesIndian': 0, 'confirmedCasesForeign': 0, 'discharged': 0, 'deaths': 0}


        state_data = pd.DataFrame(cases,columns=['State','Total_Cases'])
        state_data.sort_values(by=['State'],inplace=True)

        state_data.loc[state_data['State']=='Jammu and Kashmir','Total_Cases']+=const
        for i,_ in enumerate(state_geo_data['features']):
            state_geo_data['features'][i]['id'] = state_geo_data['features'][i]['properties']['NAME_1']
            #state_data['State'][i]=state_geo_data['features'][i]['id']
        #state_data
        folium.Choropleth(
            geo_data=state_geo_data,
            name='choropleth',
            data=state_data,
            columns=['State', 'Total_Cases'],
            key_on= 'feature.properties.NAME_1',#'features.id',#'features.properties.NAME_1',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.9,
            legend_name='Total Covid 19 cases in India'
        ).add_to(m)
        m.save('static/Map.html')
        #print(state_geo_data)
        #response= requests.get('https://github.com/geohacker/india/blob/master/state/india_telengana.geojson')
        #counties = response.json()#json.loads(response)
    except Exception as e:
        print(e)
        print('Data load error')
    return app.send_static_file('Map.html')

@app.route('/countries/cases.', methods=['GET'])
def get_cases():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        response[i[0]] = int(i[1].replace(',',""))
    return jsonify({'cases': response})

@app.route('/countries/new-cases', methods=['GET'])
def get_new_cases():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[2].replace(',',"") if i[2] else i[2].replace('',"0")
        response[i[0]] = int(value)
    return jsonify({'new-cases': response})


@app.route('/countries/deaths', methods=['GET'])
def get_deaths():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[3].replace(',',"") if i[3] else i[3].replace('',"0")
        response[i[0]] = int(value)
    return jsonify({'deaths': response})

@app.route('/countries/new-deaths', methods=['GET'])
def get_new_deaths():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[4].replace('+',"") if i[4] else i[4].replace('',"0")
        response[i[0]] = int(value)
    return jsonify({'new-deaths': response})

@app.route('/countries/active-cases', methods=['GET'])
def get_active_cases():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[6].replace(',',"") if i[6] else i[6].replace('',"0")
        response[i[0]] = int(value)
    return jsonify({'active-cases': response})

@app.route('/countries/serious-critical', methods=['GET'])
def get_serious_critical():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[7].replace(',',"") if i[7] else i[7].replace('',"0")
        response[i[0]] = int(value)
    return jsonify({'serious-critical': response})

@app.route('/countries/recovered', methods=['GET'])
def get_recovered():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[5].replace(',',"") if i[5] else i[5].replace('',"0")
        response[i[0]] = int(value)
    return jsonify({'recovered': response})

@app.route('/countries/cases/million-population', methods=['GET'])
def get_cases_per_million_population():
    global url
    response = {}
    data = scrape_data(url)
    for i in data:
        value = i[8].replace(',',"") if i[8] else i[8].replace('',"0")
        response[i[0]] = float(value)
    return jsonify({'million-population': response})

@app.route('/india/cases-per-state', methods=['GET'])
def get_cases_per_state():
    response = requests.get('https://api.rootnet.in/covid19-in/stats/latest')
    response_dict = response.json()
    locations = []
    count_per_location = []
    data = response_dict['data']['regional']
    for i in data:
        locations.append(i['loc'])
        count_per_location.append(i['confirmedCasesIndian'] + i['confirmedCasesForeign'])
    return jsonify({'locations' : locations,\
                    'count' : count_per_location})

@app.route('/india/cases-per-day', methods=['GET'])
def get_cases_per_day():
    response = requests.get('https://api.rootnet.in/covid19-in/stats/history')
    response_dict = response.json()
    date = []
    count_per_day = []
    data = response_dict['data']
    for i in data:
        date.append(i['day'])
        count_per_day.append(i['summary']['total'])
    return jsonify({'dates' : date,\
                    'count_per_day' : count_per_day})

@app.route('/india/cases-per-day-per-state', methods=['GET'])
def get_cases_per_day_per_state():
    response = requests.get('https://api.rootnet.in/covid19-in/stats/history')
    response_dict = response.json()
    state = request.args.get('state')
    date = []
    count_per_day = []
    data = response_dict['data']
    for i in data:
        date.append(i['day'])
        for j in i['regional']:

            if(j['loc'] == state):
                count_per_day.append(j['confirmedCasesIndian'] + j['confirmedCasesForeign'])
    return jsonify({'dates' : date,\
                    'count_per_day' : count_per_day})


if __name__ == '__main__':
    app.run(debug=True)
