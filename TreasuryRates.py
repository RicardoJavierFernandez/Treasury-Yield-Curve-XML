import csv
import requests
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

    # Create two dictionaries to store 1. The dates, and 2. The tenor's rates
    date = {}
    ten_year = {}

    for date_id, date_string in enumerate(root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices}NEW_DATE')):
        date[date_id] = date_string.text

    for date_id, date_string in enumerate(root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_10YEAR')):
        ten_year[date_id] = date_string.text

    for key in date.keys():
        print(date[key], ten_year[key])


parse_XML('/Users/ricky/Documents/Python/Treasury-Yield-Curve-XML/TreasuryRates.xml')
