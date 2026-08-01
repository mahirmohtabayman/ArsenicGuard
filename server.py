from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from xgboost import XGBClassifier

# ১. FastAPI অ্যাপ ইনিশিয়েট করা
app = FastAPI(title="ArsenicGuard AI Agent Core", description="Production API for Adaptive Groundwater Risk Assessment")

# ২. গ্লোবালি মডেল লোড করা
try:
    xgb_model = XGBClassifier()
    xgb_model.load_model('arsenic_guard_model.json')
except Exception as e:
    raise RuntimeError("❌ 'arsenic_guard_model.json' ফাইলটি পাওয়া যায়নি! আগে মডেল সেভ করুন।")

# ৩. ইনপুট ডেটার জন্য পাইড্যান্টিক (Pydantic) স্কিমা তৈরি
class WellInput(BaseModel):
    WELL_DEPTH: float
    Fe: float
    Mn: float
    LAT_DEG: float
    LONG_DEG: float
    well_age: int

# ৪. এপিআই এন্ডপয়েন্ট (POST Request)
@app.post("/predict")
def predict_arsenic_risk(data: WellInput):
    # ইনপুট ডেটাকে ডেটাফ্রেমে রূপান্তর
    input_df = pd.DataFrame([[
        data.WELL_DEPTH, data.Fe, data.Mn, data.LAT_DEG, data.LONG_DEG, data.well_age
    ]], columns=['WELL_DEPTH', 'Fe', 'Mn', 'LAT_DEG', 'LONG_DEG', 'well_age'])

    # প্রেডিকশন এবং প্রবাবিলিটি বের করা
    pred = int(xgb_model.predict(input_df)[0])
    prob_array = xgb_model.predict_proba(input_df)
    risk_prob = float(prob_array[0][1] * 100)
    safe_prob = float(prob_array[0][0] * 100)

    # 🌟 ADAPTIVE AI AGENT ENGINE (আচরণ পরিবর্তন লজিক)
    if risk_prob < 35.0:
        agent_level = "নিম্ন ঝুঁকি স্ট্র্যাটেজি (LOW RISK) 🟢"
        status_color = "#2ecc71"
        confidence = safe_prob
        explanation = "এই অঞ্চলের ভৌগোলিক স্থানাঙ্ক এবং নিয়ন্ত্রিত খনিজ উপাদানের কারণে ভূগর্ভস্থ পানি আর্সেনিকমুক্ত এবং নিরাপদ সীমার মধ্যে রয়েছে।"
        protocol_title = "বার্ষিক পর্যবেক্ষণ (Annual Monitoring)"
        guideline_1 = "WHO স্ট্যান্ডার্ড কমপ্লায়েন্স: পানিতে আর্সেনিকের মাত্রা বিশ্ব স্বাস্থ্য সংস্থার নির্ধারিত নিরাপদ সীমা (১০ µg/L) এর নিচে থাকার সম্ভাবনা অনেক বেশি। পানি পানের জন্য নিরাপদ।"
        guideline_2 = "গাইডলাইন অ্যাকশন: কোনো জরুরি ফিল্টার বা পরিশোধনের প্রয়োজন নেই। মাটির নিচের স্তরের দীর্ঘমেয়াদী পরিবর্তন ট্র্যাক করতে বার্ষিক পর্যবেক্ষণ চালু রাখুন।"
    elif 35.0 <= risk_prob <= 65.0:
        agent_level = "মাঝারি ঝুঁকি স্ট্র্যাটেজি (MEDIUM RISK) 🟡"
        status_color = "#f1c40f"
        confidence = risk_prob if risk_prob > 50 else safe_prob
        explanation = "বর্ডারলাইন বা রাসায়নিক অসঙ্গতি সনাক্ত হয়েছে। এজেন্ট তার সতর্কতার মাত্রা বাড়িয়েছে।"
        protocol_title = "সতর্কতামূলক পুনঃপরীক্ষা (Precautionary Retesting)"
        guideline_1 = "DPHE বাংলাদেশ স্ট্যান্ডার্ড অ্যালার্ট: পানির উপাদান বাংলাদেশের ডমেস্টিক বিপদসীমা (৫০ µg/L) এর কাছাকাছি পৌঁছাচ্ছে।"
        guideline_2 = "গাইডলাইন অ্যাকশন: শিশু এবং নবজাতকদের জন্য এই পানি সরাসরি পান করা সীমিত করুন। আর্সেনিকের ওঠানামা নিশ্চিত করতে আগামী ৬ মাস পর ল্যাব টেস্ট (Retest) করা বাধ্যতামূলূক।"
    else:
        agent_level = "উচ্চ ঝুঁকি স্ট্র্যাটেজি (HIGH RISK) 🔴"
        status_color = "#e74c3c"
        confidence = risk_prob
        explanation = f"উচ্চ Iron ({data.Fe} mg/L) এবং কম Depth ({data.WELL_DEPTH} m) এর যৌথ ভূগর্ভস্থ প্রভাবের কারণে এই এলাকায় পানির আর্সেনিক প্রেডিকশন ঝুঁকিপূর্ণ এসেছে।"
        protocol_title = "জরুরি হস্তক্ষেপ (Emergency Intervention)"
        guideline_1 = "ক্রিটিক্যাল ক্রাইটেরিয়া: পানি একই সাথে WHO (১০ µg/L) এবং বাংলাদেশের DPHE (৫০ µg/L) উভয়েরই নিরাপদ সীমা লঙ্ঘন করেছে।"
        guideline_2 = "জরুরি রিকমেন্ডেশন (Do Not Drink): কোনো অবস্থাতেই এই টিউবওয়েলের পানি পান করবেন না এবং রান্নার কাজে ব্যবহার করবেন না।"
        if data.Fe > 2.0:
            guideline_2 += f" পানিতে অতিরিক্ত আয়রনের উপস্থিতি রয়েছে, অবিলম্বে আয়রন রিমুভাল ফিল্টার (Iron Filter) স্থাপন করুন।"
        if data.WELL_DEPTH < 100:
            guideline_2 += f" টিউবওয়েলটি অত্যন্ত অগভীরে অবস্থিত, বদলে অন্তত ৫০০ ফুটের বেশি গভীর টিউবওয়েল স্থাপন করতে হবে।"

    # 🥉 Human Review Trigger
    human_trigger = False
    if 40.0 <= risk_prob <= 60.0:
        human_trigger = True

    # 🥇 Counterfactual Optimization Engine
    counterfactual_msg = "✨ পানির বর্তমান কন্ডিশন সম্পূর্ণ নিরাপদ সীমার মধ্যে রয়েছে। কোনো কাউন্টারফ্যাকচুয়াল পরিবর্তনের প্রয়োজন নেই।"
    if pred == 1 or risk_prob >= 35.0:
        cf_found = False
        for target_iron in np.arange(data.Fe, 0.0, -0.1):
            test_input = pd.DataFrame([[data.WELL_DEPTH, target_iron, data.Mn, data.LAT_DEG, data.LONG_DEG, data.well_age]], 
                                     columns=['WELL_DEPTH', 'Fe', 'Mn', 'LAT_DEG', 'LONG_DEG', 'well_age'])
            test_prob = float(xgb_model.predict_proba(test_input)[0][1] * 100)
            if test_prob < 35.0:
                counterfactual_msg = f"💡 পানির আয়রনের মাত্রা যদি {data.Fe:.1f} mg/L থেকে কমিয়ে {target_iron:.1f} mg/L-এ নামিয়ে আনা যায়, তবে এজেন্টের সিদ্ধান্ত বদলে সরাসরি নিরাপদ জোন বা LOW RISK STRATEGY-তে চলে যাবে।"
                cf_found = True
                break
        if not cf_found:
            counterfactual_msg = "💡 শুধুমাত্র কেমিক্যাল কমিয়ে লাভ হবে না, এই ভৌগোলিক জোনে টিউবওয়েলের গভীরতা (Depth) বৃদ্ধি করা ছাড়া পানি নিরাপদ করা সম্ভব নয়।"

    # এপিআই রেসপন্স রিটার্ন করা
    return {
        "prediction": pred,
        "risk_probability": round(risk_prob, 2),
        "agent_level": agent_level,
        "status_color": status_color,
        "confidence": round(confidence, 2),
        "human_trigger": human_trigger,
        "explanation": explanation,
        "protocol_title": protocol_title,
        "guideline_1": guideline_1,
        "guideline_2": guideline_2,
        "counterfactual": counterfactual_msg
    }
