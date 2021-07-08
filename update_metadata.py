import boto3
import csv
import os
import requests
import xml.etree.ElementTree as ET

client = boto3.client('s3')
cmr_search_url = 'https://cmr.maap-project.org/search/granules?granule_ur='
cmr_ingest_url = 'https://cmr.maap-project.org/ingest/providers/NASA_MAAP/granules'
# (for testing, an example might be)
# granule_ur = '3B-HHR.MS.MRG.3IMERG.20180101-S000000-E002959.0000.V05B.HDF5'

with open('badurls_fixed.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    for granule_info in data:
        granule_ur = granule_info['granule_ur']
        granule_search_url = f"{cmr_search_url}{granule_ur}"
        xml_text = requests.get(
            url=granule_search_url,
            headers={'Accept': 'application/echo10+xml'}
        ).text
        root = ET.fromstring(xml_text)
        granule = root.findall('result/Granule')[0]
        link_element = root.find("result/Granule/OnlineAccessURLs/OnlineAccessURL[URLDescription='File to download']/URL")
        updated_link = granule_info['updated_link']
        bucket = 'nasa-maap-data-store'
        key = updated_link.split(f'{bucket}/')[1]
        key.replace('maap-prod', 'nasa-map')
        key.replace('chuckulus2', 'nasa-map')
        head_resp = client.head_object(Bucket=bucket, Key=key)
        if head_resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            link_element.text = updated_link
            granule_ur_or_native_id = granule_ur.replace('GEDI02_B.SC', 'SC')
            granule_ur_or_native_id = granule_ur.replace('GEDI01_B.SC', 'SC')
            granule_ur_or_native_id = granule_ur_or_native_id.replace('ATL08.SC', 'SC')
            print(f"updating {granule_ur_or_native_id}")           
            update_response = requests.put(
                url = f"{cmr_ingest_url}/{granule_ur_or_native_id}",
                data = ET.tostring(granule),
                headers = {
                    'Content-Type': 'application/echo10+xml',
                    # ADD ECHO TOKEN TO YOUR ENVIRONMENT
                    'Echo-Token': os.getenv('ECHO_TOKEN')
                })
            if update_response.status_code == 200:
                print(f"Successfully updated {granule_search_url} at s3://{bucket}/{key}")
            else:
                print(f"Failed to update {granule_search_url}")
                print(update_response)
        else:
            print(f"cannot find file at {bucket} and {key}")
            