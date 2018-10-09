from testing.imatch_matcher import IMatchMatcher

datasets = {
    "happy_path": {
        "dataset_file": "data/happy_path.csv",
        "columns": ["source_brgy", "source_municity", "source_prov"],
    }
}

ds = datasets["happy_path"]
matcher = IMatchMatcher(ds["dataset_file"], ds["columns"])
matcher.get_matches()