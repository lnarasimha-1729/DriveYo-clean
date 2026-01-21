# import pandas as pd
# import re


# def normalize_vin(v):
#     if pd.isna(v):
#         return None
    
#     # Clean VIN but DO NOT change its length
#     v = str(v).upper().strip()
#     v = re.sub(r"[^A-Z0-9]", "", v)
#     return v


# def load_excels():
#     jdp = pd.read_excel("data/jdp.xlsx", dtype=str)
#     quote = pd.read_excel("data/driveyo.xlsx", dtype=str)

#     jdp.columns = jdp.columns.str.lower().str.strip()
#     quote.columns = quote.columns.str.lower().str.strip()

#     jdp["vin"] = jdp["vin"].apply(normalize_vin)
#     quote["vin"] = quote["vin"].apply(normalize_vin)

#     print("DriveYo VINs:", quote["vin"].tolist())
#     print("JDP VINs:", jdp["vin"].tolist())

#     return jdp, quote


# def clean_types(d):
#     for k, v in d.items():
#         if hasattr(v, "isoformat"):
#             d[k] = v.isoformat()
#     return d


# def lookup_vin(vin, jdp, quote):
#     vin = normalize_vin(vin)

#     jdp_match = jdp[jdp["vin"] == vin]
#     quote_match = quote[quote["vin"] == vin]

#     if jdp_match.empty:
#         raise Exception(f"{vin} not found in JD Power")

#     if quote_match.empty:
#         raise Exception(f"{vin} not found in User Quote Excel")

#     return clean_types(jdp_match.iloc[0].to_dict()), clean_types(quote_match.iloc[0].to_dict())



import pandas as pd

def load_excels():
    jdp = pd.read_excel("data/jdp.xlsx")
    quote = pd.read_excel("data/driveyo.xlsx")

    jdp["vin"] = jdp["vin"].astype(str).str.upper().str.strip()
    quote["vin"] = quote["vin"].astype(str).str.upper().str.strip()

    return jdp, quote


def clean_types(d):
    for k, v in d.items():
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()
    return d


def lookup_vin(vin, jdp, quote):
    jdp_match = jdp[jdp["vin"] == vin]
    quote_match = quote[quote["vin"] == vin]

    if jdp_match.empty:
        raise Exception(f"{vin} not found in JD Power")

    if quote_match.empty:
        raise Exception(f"{vin} not found in User Quote Excel")

    return clean_types(jdp_match.iloc[0].to_dict()), clean_types(quote_match.iloc[0].to_dict())
