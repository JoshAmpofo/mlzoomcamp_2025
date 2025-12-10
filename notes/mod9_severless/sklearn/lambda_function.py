import json
import pickle


with open("model.bin", "rb") as f_in:
    dv, model = pickle.load(f_in)


def predict_single(customer):
    # DictVectorizer expects a list of dicts; keep a single-row batch
    X = dv.transform([customer])
    result = model.predict_proba(X)[0, 1]
    return float(result)


def lambda_handler(event, context):
    print(f"Parameters: {event}")
    customer = event['customer']
    prob = predict_single(customer)

    return {
        'churn_probability': prob,
        'churn': bool(prob >= 0.5)
    }

