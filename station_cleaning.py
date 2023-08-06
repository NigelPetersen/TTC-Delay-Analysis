import numpy as np
import pandas as pd
import sklearn
import matplotlib as plt
import seaborn as sns
from itertools import compress

Delays_2023 = pd.read_csv("https://raw.githubusercontent.com/NigelPetersen/TTTC-Delay-Analysis/main/ttc-subway-delay-data-2023.csv")

true_stations = [
    "Finch",
    "North York Centre",
    "Sheppard-Yonge",
    "York Mills",
    "Lawrence",
    "Eglinton",
    "Davisville",
    "St. Clair",
    "Summerhill",
    "Rosedale",
    "Bloor-Yonge",
    "Wellesley",
    "College",
    "Dundas",
    "Queen",
    "King",
    "Union",
    "St. Andrew",
    "Osgoode",
    "St. Patrick",
    "Queen's Park",
    "Museum",
    "St. George",
    "Spadina",
    "Dupont",
    "St. Clair West",
    "Eglinton West",
    "Glencairn",
    "Lawrence West",
    "Yorkdale",
    "Wilson",
    "Sheppard West",
    "Downsview Park",
    "Finch West",
    "York University",
    "Pioneer Village",
    "Highway 407",
    "Vaughan",
    "Kipling",
    "Islington",
    "Royal York",
    "Old Mill",
    "Jane",
    "Runnymede",
    "High Park",
    "Keele",
    "Dundas West",
    "Lansdowne",
    "Dufferin",
    "Ossington",
    "Christie",
    "Bathurst",
    "Bay",
    "Sherbourne",
    "Castle Frank",
    "Broadview",
    "Chester",
    "Pape",
    "Donlands",
    "Greenwood",
    "Coxwell",
    "Woodbine",
    "Main Street",
    "Victoria Park",
    "Warden",
    "Kennedy",
    "Lawrence East",
    "Ellesmere",
    "Midland",
    "Scarborough Centre",
    "McCowan",
    "Bayview",
    "Bessarion",
    "Leslie",
    "Don Mills"
]
true_station_names = [(station+" station").upper() for station in true_stations]

# Removing missing data
# majority of missing entries are in the "Bound" column

Delays_2023 = Delays_2023.dropna()
Delays_2023 = Delays_2023.reset_index()

# Removing entries where the station is unusable
removing_indices = [i for i in range(len(Delays_2023)) if (("LINE" in Delays_2023["Station"][i])
            or (Delays_2023['Station'][i] in ["LYTTON EE", "MCBRIEN BUILDING", "DUNCAN BUILDING", "BIRCHMOUNT EE"]))]

Delays_2023 = Delays_2023.drop(removing_indices)
Delays_2023 = Delays_2023.reset_index()

# cleaning up station names coded with other station names using a connective
for i in range(len(Delays_2023)):
    station_name = Delays_2023["Station"][i]
    if " TO " in station_name:
        Delays_2023["Station"] = Delays_2023["Station"].replace(station_name, station_name[:station_name.index(" TO ")])
    if "(TO " in station_name:
        Delays_2023["Station"] = Delays_2023["Station"].replace(station_name, station_name[:station_name.index("(TO ")])
    if " - " in station_name:
        Delays_2023["Station"] = Delays_2023["Station"].replace(station_name, station_name[:station_name.index(" - ")])
    if " AND " in station_name:
        Delays_2023["Station"] = Delays_2023["Station"].replace(station_name, station_name[:station_name.index(" AND ")])

# Helper functions

obs_station_names = list(Delays_2023["Station"].unique())

def get_alt_station_names(name:str):
    """
    Given a true station name "name", return a list of all recorded station names from the data set that contain "name"
    """
    name = name.upper()
    return list(compress(obs_station_names, [name in obs_station_names[i] for i in range(len(obs_station_names))]))

def drop_duplicates(L:list):
    """
    given a list, return the list with unique entries
    """
    return list(dict.fromkeys(L))

def get_words(s:str):
    """
    given a string s containing a sentence, return a list of strings consisting of each word in the sentence s
    """
    cut = s
    words = []
    if "-" in cut:
        cut = cut[:cut.index("-")] + " " + cut[cut.index("-")+1:]
    while " " in cut:
        i = cut.index(" ")
        words.append(cut[:i])
        cut = cut[i+1:]
    words.append(cut)
    return words

def get_search_words(s:str):
    """
    Given a station name s that consists of multiple words, return the words in the name that are useful for searching.
    Ignore the "st" in names like "St. George station"
    """
    words = get_words(s)[:-1]
    if words[0] == "ST.":
        words = words[1:]
    return words

def delete_entries(L:list, remove:list):
    """
    Given a list L and a list "remove" of entries in the list L, deleta all entries in L that are in "remove"
    """
    return [item for item in L if item not in remove]

# create dictionary with true station names as the keys and a list of the observed station names at the values

special_cases = list(compress(true_station_names,[" " in station_name[:len(station_name) - len("station")-1] for
    station_name in true_station_names]))
special_cases.extend(list(compress(true_station_names,["-" in station_name for station_name in true_station_names])))
non_special_cases = [station_name for station_name in true_station_names if station_name not in special_cases]

special_case_search_words = [get_search_words(station_name) for station_name in special_cases]
special_case_search_words[special_case_search_words.index(["QUEEN'S", 'PARK'])].append("QUEENS")


alt_station_names = {}
for station_name in non_special_cases:
    alt_station_names[station_name] = get_alt_station_names(station_name[:len(station_name) - len("station")-1])

for i in range(len(special_cases)):
    alt_names = []
    for j in range(len(get_search_words(special_cases[i]))):
        alt_names.extend(get_alt_station_names(get_search_words(special_cases[i])[j]))
    alt_station_names[special_cases[i]] = alt_names

# Some station names are part of others, particularly those that contain the words "EAST", "WEST" or "PARK"

east_west_stations = [station_name for station_name in true_station_names if ("WEST" in station_name or "EAST" in station_name)]
east_west_stations = list(compress(east_west_stations,
            [east_west_stations[i][:-len(" east station")]+" STATION" in true_station_names for i in range(len(east_west_stations))]))
ew_prefix_stations = [station[:-len(" east station")]+" station".upper() for station in east_west_stations]

for i in range(1,len(ew_prefix_stations)):
    J = alt_station_names[ew_prefix_stations[i]]
    alt_station_names[ew_prefix_stations[i]] = [name for name in J if ("EAST" not in name and "WEST" not in name)]

    prefix = ew_prefix_stations[i][:-len(" station")]
    alt_station_names[east_west_stations[i]] = [n for n in alt_station_names[east_west_stations[i]] if (prefix in n and ("EAST" in n or "WEST" in n))]

park_stations = [station_name for station_name in true_station_names if "PARK" in station_name]
for i in range(len(park_stations)):
    J = alt_station_names[park_stations[i]]
    alt_station_names[park_stations[i]] = [name for name in J if
                    (("PARK" in name) and park_stations[i][:-len(" park station")] in name )]

york_stations = [name for name in true_station_names if "YORK" in name]
mills_stations = [name for name in true_station_names if "MILL" in name]
key_words = {}
key_words["NORTH YORK CENTRE STATION"] = "NORTH"
key_words["YORK MILLS STATION"] = "YORK MILLS"
key_words["YORKDALE STATION"] = "DALE"
key_words["YORK UNIVERSITY STATION"] = "UNIVERSITY"
key_words["ROYAL YORK STATION"] = "ROYAL"
key_words["OLD MILL STATION"] = "OLD"
key_words["DON MILLS STATION"] = "DON MILLS"

for station_name in york_stations + mills_stations:
    J = alt_station_names[station_name]
    alt_station_names[station_name] = [name for name in J if key_words[station_name] in name]

# Manual fixes

alt_station_names["QUEEN STATION"] = delete_entries(alt_station_names["QUEEN STATION"], "QUEEN'S PARK STATION")
alt_station_names["KING STATION"] = delete_entries(alt_station_names["KING STATION"], "UNION STATION-KING")
alt_station_names['BAY STATION'] = delete_entries(alt_station_names["BAY STATION"], "BAYVIEW STATION")
alt_station_names["LAWRENCE EAST STATION"] = [name for name in alt_station_names["LAWRENCE EAST STATION"] if "EAST" in name]
alt_station_names["LAWRENCE WEST STATION"] = [name for name in alt_station_names["LAWRENCE WEST STATION"] if "WEST" in name]
alt_station_names["LAWRENCE STATION"] = [name for name in alt_station_names["LAWRENCE STATION"] if ("EAST" not in name and "WEST" not in name)]
alt_station_names["SHEPPARD WEST STATION"] = [name for name in alt_station_names["SHEPPARD WEST STATION"] if "SHEPPARD WEST" in name]
alt_station_names["YORK UNIVERSITY STATION"] = delete_entries(alt_station_names["YORK UNIVERSITY STATION"], 'YONGE UNIVERSITY SPADI')
alt_station_names['SPADINA STATION'].append('YONGE UNIVERSITY SPADI')
alt_station_names["SCARBOROUGH CENTRE STATION"] = [name for name in alt_station_names["SCARBOROUGH CENTRE STATION"] if "SCARBOROUGH" in name]
alt_station_names["SHEPPARD-YONGE STATION"] = [name for name in alt_station_names["SHEPPARD-YONGE STATION"] if ("SHEPPARD" in name and "YONGE" in name)]
alt_station_names["BLOOR-YONGE STATION"] = [name for name in alt_station_names["BLOOR-YONGE STATION"] if "BLOOR" in name]
alt_station_names["ST. CLAIR STATION"] = [name for name in alt_station_names["ST. CLAIR STATION"] if "WEST" not in name]
alt_station_names["ST. CLAIR WEST STATION"] = [name for name in alt_station_names["ST. CLAIR WEST STATION"] if "CLAIR WEST" in name]

good_names = []
for name in alt_station_names:
    good_names.extend(drop_duplicates(alt_station_names[name]))

good_names = drop_duplicates(good_names)

missing_names = []
for name in obs_station_names:
    if name not in good_names:
        missing_names.append(name)
missing_names

alt_station_names["BLOOR-YONGE STATION"].extend([missing_names[0], missing_names[-1]])
alt_station_names["SHEPPARD-YONGE STATION"].append(missing_names[1])
alt_station_names['MCCOWAN STATION'].append(missing_names[2])
alt_station_names['GLENCAIRN STATION'].append(missing_names[3])
alt_station_names['KING STATION'].append(missing_names[4])

# update the names in the data set based on alt_station_names
for station_name in alt_station_names:
    Delays_2023["Station"] = Delays_2023["Station"].replace(alt_station_names[station_name], station_name)

