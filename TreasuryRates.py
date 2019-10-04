import csv
import requests
import datetime
import xml.etree.ElementTree as ET


def load_page():

    # url of Treasury XML page
    url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%202019'

    # create HTTP response
    resp = requests.get(url)

    # save the XMl file
    with open('/Users/ricky/Documents/Python/Treasury-Yield-Curve-XML/TreasuryRates.xml', 'wb') as f:
        f.write(resp.content)


def parse_XML(xmlFile):

    load_page()
    
    # create element tree object
    tree = ET.parse(xmlFile)

    # get root element
    root = tree.getroot()

    # Dictionary object of important tags in the Treasury Rates XML file
    tags = {'NEW_DATE': '{http://schemas.microsoft.com/ado/2007/08/dataservices}NEW_DATE',
            '1MONTH': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_1MONTH',
            '2MONTH': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_2MONTH',
            '3MONTH': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_3MONTH',
            '6MONTH': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_6MONTH',
            '1YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_1YEAR',
            '2YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_2YEAR',
            '3YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_3YEAR',
            '5YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_5YEAR',
            '7YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_7YEAR',
            '10YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_10YEAR',
            '20YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_20YEAR',
            '30YEAR': '{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_30YEAR'}
    
    # Create dictionary with all the data, keys are the keys in the tags dictionary above.
    rates_data = {}
    
    for key in tags.keys():
        place_holder = {}
        for rate_id, rate  in enumerate(root.iter(tags[key])):
            place_holder[rate_id] = rate.text
        rates_data[key] = place_holder

    # Loop that goes through each day of data and calculates the 2s10s spread or 3mo10yr. We can use this to capture the dates the spread turned negative
    date_format = '%Y-%m-%dT%H:%M:%S'
    
    for key in rates_data['NEW_DATE']:
        # format date to mm-dd-yyyy
        date_converted = datetime.datetime.strptime(rates_data['NEW_DATE'][key], date_format)
        date_reformatted = date_converted.strftime('%m-%d-%Y')
        
        # calculate the 2s10s spread
        spread = float(rates_data['10YEAR'][key]) - float(rates_data['2YEAR'][key])

        # only print out inverted (negative spreads)
        if spread < 0:
            print('Curve inversion on:', date_reformatted, '2s10s spread:', str(round(spread, 2)))


    # Testing below for output on different methods 

    # for child in root.iter():
    #     print(child.tag)
    #
    # for child in root.iter():
    #     print(child.child)
    #
    # for child in root.iter():
    #     print(child.text)
    # for key in tags:
    #     for child in root.iter(tags[key]):
    #         print(key, child.text)
##    for key in tags.keys():
##        for child in root.iter(tags[key]):
##            print(key, child.text)


parse_XML('/Users/ricky/Documents/Python/Treasury-Yield-Curve-XML/TreasuryRates.xml')
