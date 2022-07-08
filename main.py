from re import I
from flask import Flask, render_template, request, jsonify
from numpy.core.numeric import cross
import RoboFund.screener as screener
import RoboFund.predictions as predictions
import RoboFund.nlp as nlp
import RoboFund.sectors as sectors_map
import RoboFund.portfolio_optimisation as portfolio_optimisation
import RoboFund.cross_correlation as cross_correlation
from flask_cors import CORS



app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def home_page():
    return render_template("new.html")

@app.route("/generate-portfolio_get_stocks", methods=["POST"])
def generate_portfolio_get_stocks():
    if request.method == "POST":
        # Use NLP to perform scan on sector
        # Do check if result is positive or negative, if negative, break
        # Do second check on cross correlation
        # Do check if result is positive or negative, if negative, break
        # Use screener to get undervalued stocks
        # Take the stock list and send it into predictive engine
        # Take stocks with expected growth and put into portfolio optimisation engine
        # Add data to database
        # Return the portfolio and stocks omitted as JSON object
        
        # data {"sector": ["Financials","Technology"], "num_of_stocks": 5, "timehorizon": 365, "risk":5, "expected_annualised_gains":0.2}
        # add mapping for the sectors as global variable?
        
        # scan each sector and get sentiment score
        sectors = request.json["sector"]
        sector_to_drop = []
        for i in sectors:
            sector_score = nlp.get_sentiment_score(sectors_map.funds[i])
            # if sentiment is bad, drop it
            print(f"{i} Sentiment Score: {sector_score}")
            if sector_score < 0.05:
                sector_to_drop.append(i)
        
        # drop sectors with poor scores
        for i in sector_to_drop:
            sectors.remove(i)
        
        good_stocks = screener.get_stocks(sectors)
        return jsonify(good_stocks)

@app.route("/generate-portfolio_get_stocks_finviz", methods=["POST"])
def generate_portfolio_get_stocks_finviz():
    if request.method == "POST":
        all_stocks = request.json["stocks"]
        good_stocks = screener.get_stocks_from_finviz(all_stocks)
        return jsonify(good_stocks)

@app.route("/generate-portfolio_get_refined_stocks", methods=["POST"])
def generate_portfolio_get_refined_stocks():
    if request.method == "POST":
        all_stocks = request.json["stocks"]
        good_stocks = screener.get_refined_stonks(all_stocks)
        return jsonify(good_stocks)

@app.route("/generate-portfolio_predict", methods=["POST"])
def generate_portfolio_predict():
    if request.method == "POST":
        
        # data {"stocks": [('C',60),('GS',400)], "num_stocks": 5, "timehorizon": 365, "risk":5, "expected_annualised_gains":0.2}
        print(">>> incoming json for predict: ",request.json)
        good_stocks = request.json["stocks"]
        num_stocks = int(request.json["num_stocks"])
        time_horizon = int(request.json["time_horizon"])
        if good_stocks:
            #use this code for real, but for demo gotta cut short
            #stocks_with_returns, predictedValues = predictions.get_predictions(good_stocks,time_horizon)
            stocks_with_returns, predictedValues = predictions.get_predictions(good_stocks[:num_stocks*3],time_horizon)
            out = {"stocks_with_returns":stocks_with_returns,"predicted_values":predictedValues}
            return jsonify(out)
        return jsonify({"message":"No predictions"})

@app.route("/generate-portfolio_optimise", methods=["POST"])
def generate_portfolio_optimise():
    if request.method == "POST":
        
        # data {"stocks_with_returns": [('C',0.2),('GS',0.1)], "num_of_stocks": 5, "timehorizon": 365, "risk":5, "expected_annualised_gains":0.2}
        stocks_with_returns = request.json["stocks_with_returns"]["stocks_with_returns"]
        print(">> stocks with returns type", type(stocks_with_returns))
        print(stocks_with_returns)
        predicted_values = request.json["stocks_with_returns"]["predicted_values"]
        expected_annualised_gains = request.json["expected_annualised_gains"]
        risk_appetite = request.json["risk"]

        optimised_portfolio = portfolio_optimisation.optimise_portfolio(stocks_with_returns[:int(request.json["num_stocks"])],predicted_values,risk_appetite,expected_annualised_gains)
        return jsonify(optimised_portfolio)
        
@app.route("/generate-portfolio_get_sector_sentiment", methods=["GET"])
def generate_portfolio_get_sector_sentiment():
    # generate sentiment scores for each sector
    # sector = request.json["sector"]
    sector_score = nlp.get_all_sentiment_score()
    return jsonify(sector_score)

@app.route("/generate-portfolio_get_cross_corr",methods=["GET"])
def generate_portfolio_get_cross_corr():
    output = cross_correlation.get_cross_corr()
    final_out = []
    for i,j in output.items():
        final_out.append((sectors_map.sectors_ticker_to_name[i[0]],sectors_map.sectors_ticker_to_name[i[1]],j))
    print(final_out)
    top_five = sorted(final_out, key= lambda x:abs(x[2]),reverse=True)[:5]
    bottom_five = sorted(final_out, key= lambda x:abs(x[2]),reverse=False)[:5]
    to_send = top_five + bottom_five
    print(to_send)
    return jsonify(to_send)

@app.route("/generate-portfolio_get_cross_corr_bond_gold",methods=["GET"])
def generate_portfolio_get_cross_corr_bond_gold():
    output = cross_correlation.get_cross_corr_gold_bond()
    final_out = []
    for i,j in output:
        final_out.append((sectors_map.sectors_ticker_to_name[i[0]],sectors_map.sectors_ticker_to_name[i[1]],j))
    return jsonify(sorted(final_out, key= lambda x:abs(x[2]),reverse=True)[:10])