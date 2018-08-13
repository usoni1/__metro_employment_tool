import json
import pprint as pp

if __name__ == '__main__':
    ad = json.load(open('metropolitan_areas.json', 'r'))
    f = ad["features"]
    msa_l = []
    for _f in f:
        msa_id = _f["properties"]['GEOID']
        msa_l.append(msa_id)

    am = json.load(open('reduced_zcta_map.json', 'r'))
    f = am["features"]
    zcta_l = []
    for _f in f:
        zcta_id = _f["properties"]["ZCTA_ID"]
        zcta_l.append(zcta_id)

    msa_to_zcta = {}
    i = 0
    for msa in msa_l:
        msa_to_zcta[msa] = zcta_l[i]
        i += 1
        if i == len(zcta_l):
            i = 0
    # pp.pprint(msa_to_zcta)
    json.dump(msa_to_zcta, open('temp.json', 'w'), indent=4, separators=(',', ':'))