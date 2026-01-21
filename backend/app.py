# from flask import Flask, render_template, request
# from ocr.textract_ocr import extract_quote
# from data.excel_loader import load_excels
# from llm.mistral_api import explain_quote
# import pandas as pd
# app = Flask(__name__)

# def get_dealer_and_market_offers(vin, jdp_df, user_df):
#     results = []

#     user_rows = user_df[user_df["vin"] == vin]

#     if user_rows.empty:
#         return []

#     for _, urow in user_rows.iterrows():

#         dealer_options = [
#             ("cash down 1", "monthly term1 cash1_quote"),
#             ("cash down 2", "monthly term1 cash2_quote"),
#             ("cash down 3", "monthly term1 cash3_quote"),
#         ]

#         for dp_col, monthly_col in dealer_options:

#             down_payment = urow.get(dp_col)
#             dealer_monthly = urow.get(monthly_col)

#             if pd.isna(down_payment) or pd.isna(dealer_monthly):
#                 continue

#             market_rows = jdp_df[
#                 (jdp_df["vin"] == vin) &
#                 (jdp_df["down payment"] == down_payment)
#             ]

#             if market_rows.empty:
#                 stackable = []
#                 market_offers = []
#             else:
#                 top3_market = market_rows.sort_values("payment").head(3)

#                 stackable = str(top3_market.iloc[0].get("stackable_with") or "").split(",")

#                 market_offers = [
#                     {
#                         "monthly": float(r["payment"]),
#                         "interest_rate": float(r["interset rate"]),
#                         "lender": r["lender"],
#                         "program": r["program name"]
#                     }
#                     for _, r in top3_market.iterrows()
#                 ]

#             results.append({
#                 "down_payment": int(down_payment),
#                 "dealer_monthly": float(dealer_monthly),
#                 "stackable_offers": stackable,
#                 "market_offers": market_offers
#             })

#     return results


# @app.route("/")
# def home():
#     return render_template("upload.html")


# @app.route("/analyze", methods=["POST"])
# def analyze():
#     file = request.files["quote"]

#     ocr_data = extract_quote(file)
#     vin = ocr_data["vin"]

#     jdp_df, user_df = load_excels()

#     offers = get_dealer_and_market_offers(vin, jdp_df, user_df)

#     payload = {
#         "vin": vin,
#         "offers": offers
#     }

#     result = explain_quote(payload)

#     return render_template("upload.html", vin=vin, result=result)


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr.textract_ocr import extract_quote
from data.excel_loader import load_excels
from llm.mistral_api import explain_quote
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load Excel once
jdp_df, user_df = load_excels()


def get_dealer_and_market_offers(vin, jdp_df, user_df):
    results = []

    user_rows = user_df[user_df["vin"] == vin]
    if user_rows.empty:
        return results

    dealer_options = [
        ("cash down 1", "monthly term1 cash1_quote"),
        ("cash down 2", "monthly term1 cash2_quote"),
        ("cash down 3", "monthly term1 cash3_quote"),
    ]

    for _, urow in user_rows.iterrows():
        for dp_col, monthly_col in dealer_options:
            down_payment = urow.get(dp_col)
            dealer_monthly = urow.get(monthly_col)

            if pd.isna(down_payment) or pd.isna(dealer_monthly):
                continue

            market_rows = jdp_df[
                (jdp_df["vin"] == vin) &
                (jdp_df["down payment"] == down_payment)
            ]

            if market_rows.empty:
                market_offers = []
                stackable = []
            else:
                top3_market = market_rows.sort_values("payment").head(3)
                stackable = str(
                    top3_market.iloc[0].get("stackable_with") or ""
                ).split(",")

                market_offers = [
                    {
                        "monthly": float(r["payment"]),
                        "interest_rate": float(r["interset rate"]),
                        "lender": r["lender"],
                        "program": r["program name"]
                    }
                    for _, r in top3_market.iterrows()
                ]

            results.append({
                "down_payment": int(down_payment),
                "dealer_monthly": float(dealer_monthly),
                "stackable_offers": stackable,
                "market_offers": market_offers
            })

    return results


@app.route("/analyze", methods=["POST"])
def analyze():
    if "quote" not in request.files:
        return jsonify({
            "vin": None,
            "offers": [],
            "analysis": "",
            "error": "No file uploaded"
        }), 400

    try:
        file = request.files["quote"]
        ocr_data = extract_quote(file)
        vin = ocr_data.get("vin")

        offers = get_dealer_and_market_offers(vin, jdp_df, user_df)

        analysis = ""
        try:
            analysis = explain_quote({
                "vin": vin,
                "offers": offers
            })
        except Exception as e:
            print("LLM error:", e)

        return jsonify({
            "vin": vin,
            "offers": offers,
            "analysis": analysis
        })

    except Exception as e:
        print("Analyze error:", e)
        return jsonify({
            "vin": None,
            "offers": [],
            "analysis": "",
            "error": "Processing failed"
        }), 500


if __name__ == "__main__":
    app.run(
        debug=False
    )
