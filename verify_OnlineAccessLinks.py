import re
import csv
import boto3
import requests
import xml.etree.ElementTree as ET


cmr_search_url = 'https://cmr.maap-project.org/search/granules?granule_ur='
def Check_URL_OnlineAccess(input, output):
    f_o = open(output, 'w')
    with open("badurls_fixed.csv", "r") as csvinput:
        data = csv.DictReader(csvinput)
        for granule_info in data:
            granule_ur = granule_info['granule_ur']
            granule_search_url = f"{cmr_search_url}{granule_ur}"
            xml_text = requests.get(
                url=granule_search_url,
                headers={'Accept': 'application/echo10+xml'}
            ).text
            root = ET.fromstring(xml_text)
            link_element = root.find("result/Granule/OnlineAccessURLs/OnlineAccessURL[URLDescription='File to download']/URL")
            f_o.write(granule_ur + ": " + link_element.text)
            if(link_element.text == granule_info['updated_link']):
                print(f"Successfully verify {granule_ur} at {granule_info['updated_link']}")
            else:
                print(f"Failed to verify {granule_ur} at {granule_info['updated_link']}")
    f_o.close()
    return

if __name__ == "__main__":
    print("Start....\n")
    Check_URL_OnlineAccess("badurls_fixed.csv", "check_onlineaccess.csv")
    print("\nDone!")