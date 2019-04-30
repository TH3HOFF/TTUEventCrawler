from bs4 import BeautifulSoup
import requests
from firebase import firebase
import time

firebase = firebase.FirebaseApplication('https://techroute.firebaseio.com/')
source = requests.get('http://events.ttu.edu/cal/main/showMain.rdo').text

soup = BeautifulSoup(source, 'lxml')

name = 'Test'
locationName = 'Test'
locationSearchName = 'WIP'
locationLatitude = 'WIP'
locationLongitude = 'WIP'
whenMonth = 'Test'
whenDay = 'Test'
whenTimeStart = 'Test'
whenTimeEnd = 'Test'
descriptionFull = 'Test'
descriptionEventLink = 'Test'



while True:
    events = []
    count = 1
    
    firebase.delete('/Events', None)
    
    firebase.put('Events','Template',{
        'Name':'Test Event Name',
        'Location':{
            'Name': 'Test Building Name',
            'SearchName': 'Test Search Name',
            'Latitude': 'Test Latitude',
            'Longitude': 'Test Longitude'},
        'When':{
            'Month': 'Test Month',
            'Day': 'Test Day',
            'TimeStart': 'Test Start Time',
            'TimeEnd': 'Test End Time'},
        'Description': {
            'Full': 'Test Full Description',
            'Event Link': 'Test Link'}})




    for event in soup.find_all('tr'):

        

        eventLink = 'http://events.ttu.edu' + event.a['href']

        subsource = requests.get(eventLink).text
        subsoup = BeautifulSoup(subsource, 'lxml')

        singleEvent = subsoup.find('div', class_ = 'singleEvent')

        

        name = singleEvent.find('h2', class_ = 'bwStatusConfirmed eventTitle').text



        eventLoc = singleEvent.find('div', class_ = 'eventWhere').text

        locationName = eventLoc[7:]
    ##    locationSearchName = locationName
    ##    getLonLat(locationName)



        
        eventWhen = singleEvent.find('div', class_ = 'eventWhen').text
        
        whenSplit = eventWhen.split()
        whenMonth = whenSplit[2]
        whenDay = whenSplit[3][0:2]
        whenTimeStart = whenSplit[5] + whenSplit[6]
        whenTimeEnd = whenSplit[-2] + whenSplit[-1]

        if whenTimeEnd == '(allday)':
            whenTimeEnd = 'All Day'
            whenTimeStart = 'All Day'
            
        
        eventDescription = singleEvent.find('div', class_ = 'eventDescription').text
        descriptionFull = eventDescription[13:]
        descriptionEventLink = eventLink


        
        eventInfo = (
            name,
            locationName,
            locationSearchName,
            locationLongitude,
            locationLatitude,
            whenMonth,
            whenDay,
            whenTimeStart,
            whenTimeEnd,
            descriptionFull,
            descriptionEventLink)
        
        events.append(eventInfo)


    for event in events:
        firebase.put('Events','Event ' + str(count),{
            'Name': event[0],
            'Location':{
                'Name': event[1],
                'SearchName': event[2],
                'Latitude': event[3],
                'Longitude': event[4]},
            'When':{
                'Month': event[5],
                'Day': event[6],
                'TimeStart': event[7],
                'TimeEnd': event[8]},
            'Description': {
                'Full': event[9],
                'Event Link': event[10]}})
        count += 1
    time.sleep(86400)




