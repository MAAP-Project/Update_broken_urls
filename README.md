# Goals: 
update all the broken urls from the list in badurls.cvs to the existing ones in GCC Ops. 

Note: Some key paths of the links may be different

# Changes made:

## Buckets: 

- cumulus-map-internal and maap-cumulus-dev-internal were changed to nasa-maap-data-store

- All the sub-directory or sub-buckets with the name:

```
chuckulus2

aimee

slesa

aap-prod
```

Were updated to “nasa-maap”

## The granule_ur name is different in GCC Ops, i.e., it’s missing a ‘T’ character in its name.
```
s3://cumulus-map-internal/file-staging/nasa-map/SENTINEL-1B_DP_GRD_HIGH___1/S1B_IW_GRDH_1SDV_20170720T104532_20170720104557_006570_00B8E0_D8A3.zip
Was updated to:
s3://nasa-maap-data-store/file-staging/nasa-map/SENTINEL-1B_DP_GRD_HIGH___1/S1B_IW_GRDH_1SDV_20170720T104532_20170720T104557_006570_00B8E0_D8A3.zip
```

## Some granules are missing (or I cannot find a similar one in GCC Ops)
```
s3://nasa-maap-data-store/file-staging/nasa-map/kb_reprj_biomass___1/kb_most_awesome_output.out.tif

s3://nasa-maap-data-store/file-staging/nasa-map/Landsat7_SurfaceReflectance___1/LE071820612019041601T1-SC20190528131738.tar.gz

s3://nasa-maap-data-store/file-staging/nasa-map/LVISF1B___001/LVISF1B_GEDI2019_0521_R2003_075511.h5

s3://nasa-maap-data-store/file-staging/nasa-map/LVISF1B___001/LVISF1B_GEDI2019_0521_R2003_088052.h5

s3://nasa-maap-data-store/file-staging/nasa-map/LVISF1B___001/LVISF1B_GEDI2019_0521_R2003_091010.h5
```

# Run
```
python Update_Check_URL_links.py
```

Output is in the badurls_fixed.csv

For debugging purposes:
    - List of good urls are in List_Fixed_url.csv
    - List of bad urls are in List_broken_links.csv (See above information to know why those url links are still broken)