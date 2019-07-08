import csv
import requests
import xml.dom.minidom
import xml.etree.ElementTree as ET

def loadPage():

    # url of Treasury XML page
    url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%202019'

    # create HTTP response
    resp = requests.get(url)

    # save the XMl file
    with open('/Users/ricky/Documents/Python/Treasury-Yield-Curve-XML/XMLTreasuryRates.xml', 'wb') as f:
        f.write(resp.content)

loadPage()
def parseXML(xmlFile):

    # create element tree object
    tree = ET.parse(xmlFile)

    # get root element
    root = tree.getroot()

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
    for child in root.iter(tags['NEW_DATE']):
        print(child.text)

#
parseXML('/Users/ricky/Documents/Python/Treasury-Yield-Curve-XML/XMLTreasuryRates.xml')