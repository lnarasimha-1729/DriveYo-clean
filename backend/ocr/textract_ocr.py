# import boto3
# import re
# from config.aws_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION

# VIN_REGEX = r"\b(?:WBX|WBS|3MW)[A-HJ-NPR-Z0-9]{14}\b"

# # ============================
# # TEXTRACT CLIENT
# # ============================
# textract = boto3.client(
#     "textract",
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY,
#     region_name=REGION
# )


# def extract_quote(file):

#     response = textract.analyze_document(
#         Document={"Bytes": file.read()},
#         FeatureTypes=["FORMS", "TABLES"]
#     )

#     # Join OCR words
#     text_blob = " ".join(
#         [b.get("Text", "") for b in response["Blocks"] if b["BlockType"] == "WORD"]
#     )

#     print("\nOCR TEXT:", text_blob)

#     # VIN extraction
#     vin_match = re.search(r"VIN[:\s]*(" + VIN_REGEX + r")", text_blob)

#     if vin_match:
#         vin = vin_match.group(1)
#         print("VIN FOUND AFTER LABEL:", vin)
#         return {"vin": vin, "raw_text": text_blob}

#     # fallback regex search
#     match = re.search(VIN_REGEX, text_blob)

#     if not match:
#         raise Exception("VIN not found")

#     vin = match.group(0)
#     print("VIN FOUND BY FALLBACK:", vin)

#     return {"vin": vin, "raw_text": text_blob}


import boto3
import re
from config.aws_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
)

print(AWS_ACCESS_KEY_ID)


VIN_REGEX = r"\b[A-HJ-NPR-Z0-9]{17}\b"

textract = boto3.client(
    "textract",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def extract_quote(file):
    response = textract.analyze_document(
        Document={"Bytes": file.read()},
        FeatureTypes=["FORMS", "TABLES"]
    )

    text_blob = " ".join([b.get("Text", "") for b in response["Blocks"] if b["BlockType"] == "WORD"])
    match = re.search(VIN_REGEX, text_blob)

    if not match:
        raise Exception("VIN not found")

    return {"vin": match.group(0).strip().upper(), "raw_text": text_blob}
