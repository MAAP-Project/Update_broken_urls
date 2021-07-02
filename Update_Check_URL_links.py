import re
import csv
import boto3
from botocore.errorfactory import ClientError
#import urllib.request
#import xml.etree.ElementTree as ET
#import pandas

def fix_broken_url(url):
    result = url.replace("cumulus-map-internal", "nasa-maap-data-store", 1).\
    replace("maap-cumulus-dev-internal", "nasa-maap-data-store", 1).\
    replace("chuckulus2", "nasa-map", 1).\
    replace("aimee", "nasa-map", 1).\
    replace("slesa", "nasa-map", 1).\
    replace("maap-prod", "nasa-map", 1)

    #Note:
    # 1.  "aimee", maap-prop and "slesa" sub-directories are completely empty --> nasa-map
    # 2. The following granules are missing in the GCC Ops:
    #   - 
    #    2: s3://nasa-maap-data-store/file-staging/nasa-map/LVISF1B___001/LVISF1B_GEDI2019_0521_R2003_075511.h5
    #    3: s3://nasa-maap-data-store/file-staging/nasa-map/LVISF1B___001/LVISF1B_GEDI2019_0521_R2003_088052.h5
    #    4: s3://nasa-maap-data-store/file-staging/nasa-map/LVISF1B___001/LVISF1B_GEDI2019_0521_R2003_091010.h5

    # 3. The following granules are missing as well:
    #   0: s3://nasa-maap-data-store/file-staging/nasa-map/kb_reprj_biomass___1/kb_most_awesome_output.out.tif
    #   1: s3://nasa-maap-data-store/file-staging/nasa-map/Landsat7_SurfaceReflectance___1/LE071820612019041601T1-SC20190528131738.tar.gz
    #                                                       Landsat7_SurfaceReflectance___1/LE071820612019041601T1-SC20190601103618.tar.gz
    #                                                       Landsat7_SurfaceReflectance___1/LE071820612019041601T1-SC20190602001106.tar.gz

    
    #Dealing with the special case
    result = result.replace("S1B_IW_GRDH_1SDV_20170720T104532_20170720104557_006570_00B8E0_D8A3", \
    "S1B_IW_GRDH_1SDV_20170720T104532_20170720T104557_006570_00B8E0_D8A3", 1) #The granule_ur name is different in GCC Ops, i.e., missing T in the name


    return result
    
def Update_URL_links(inputfile, outputfile):
    csvoutput = open(outputfile, 'w')
    with open(inputfile, 'r') as csvinput:
        csvreader = csv.reader(csvinput, delimiter = ',')
        for row in csvreader:
            new_row3 = fix_broken_url(row[3])
            print("The new row is: " + row[0] + ", " + row[1] + ", " + row[2] + ", " + new_row3)
            csvoutput.write(row[0] + "," + row[1] + "," + row[2] + "," + new_row3 + "\n")
    csvoutput.close()
    return

def Check_URL_links(inputfile):
    s3 = boto3.client('s3')
    list_broken_links = []
    list_fixed_links = []
    with open (inputfile, 'r') as csvinput:
        csvreader = csv.reader(csvinput, delimiter = ',')
        for row in csvreader:
            #check the status of the link
            print(row[3] + "\n")
            bucket_name = row[3][5: row[3].find('/', 5)]
            key_path = row[3][row[3].find('/', 5) + 1: len(row[3])]
            try:
                s3.head_object(Bucket=bucket_name, Key=key_path)
                list_fixed_links.append(row[3])
            except ClientError:
                list_broken_links.append(row[3])
                pass
    
    f_o = open("List_Fixed_urls.csv", "w")
    for i in range (0, len(list_fixed_links)):
        f_o.write(str(i) + ": " + list_fixed_links[i] + "\n")
    f_o.close()
    if(not list_broken_links):
        print("All links are good!")
    else:
        print("There are some broken links that need to be fixed!\n")
        f_e = open("List_broken_links.csv", "w")
        for i in range(0, len(list_broken_links)):
            print(str(i) + ": " + (list_broken_links[i]) + "\n")
            f_e.write(str(i) + ": " + (list_broken_links[i]) + "\n")
        f_e.close()
    print ("\nFor the debugging purposes:")
    print("\n\tAll broken links are written in List_broken_links.csv\n")
    print("\n\tAll Fixed links are written in List_Fixed_urls.cvs\n")

    return

if __name__ == "__main__":
    print("Start....\n")
    Update_URL_links("badurls.csv", "badurls_fixed.csv")
    Check_URL_links("badurls_fixed.csv")
    print("\nUpdated urls are in badurls_fixed.csv\n")
    print("\nDone!")