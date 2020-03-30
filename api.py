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
import os
from prepare_covid_data import coord_dict,get_state_data
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
            template_folder = os.getcwd()+'/static/')

@app.route('/')
def index():
    # get_state_data()
    return render_template("charts.html")

@app.route('/map')
def map_route():
    #not required if we load on main page itself
    try:
        get_state_data()
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
    #res.headers.add('Access-Control-Allow-Origin', '*')
    locations = []
    count_per_location = []
    data = response_dict['data']['regional']
    for i in data:
        locations.append(i['loc'])
        count_per_location.append(i['confirmedCasesIndian'] + i['confirmedCasesForeign'])
    res = jsonify({'locations' : locations,\
                   'count' : count_per_location})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

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
    res = jsonify({'dates' : date,\
                    'count_per_day' : count_per_day})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

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
    res = jsonify({'dates' : date,\
                    'count_per_day' : count_per_day})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res
@app.route('/lab_maps')
def get_lab_map():
    #not required if we load on main page
    return app.send_static_file('lab_maps.html')

if __name__ == '__main__':
    app.run(debug=True)
