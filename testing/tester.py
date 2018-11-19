from testing.imatch_matcher import IMatchMatcher

datasets = {
    "happy_path": {
        "dataset_file": "data/happy_path.csv",
        "columns": ["source_brgy", "source_municity", "source_prov"],
    },
    "lgu201": {
        "dataset_file": "data/lgu201.csv",
        "columns": ["LOCATION", "citymun_m", "province_m"],
    },
}

ds = datasets["happy_path"]
matcher = IMatchMatcher(ds["dataset_file"], ds["columns"], shared_dir='testing/shared')
all_matches = list(matcher.get_matches)
print("Matched {} rows.".format(len(all_matches)))
print(dict(all_matches[0]))
