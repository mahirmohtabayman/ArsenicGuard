import streamlit as st
import pandas as pd
import requests


st.set_page_config(page_title="ArsenicGuard Adaptive Agent", page_icon="🤖", layout="wide")
st.title("🤖 ArsenicGuard: অ্যাডাপ্টিভ ইন্টেলিজেন্ট এক্সএআই এজেন্ট")
st.write("ভূগর্ভস্থ পানির আর্সেনিক ঝুঁকি মূল্যায়ন, কাউন্টারফ্যাকচুয়াল রিজনিং এবং অ্যাডাপ্টিভ সিদ্ধান্ত স্ট্র্যাটেজি")
st.markdown("---")


col_input, col_dashboard = st.columns([1, 2])


with col_input:
    st.header("📥 ফিচার কন্ট্রোল")
    well_depth = st.slider("গভীরতা / Well Depth (meters)", 1.0, 500.0, 30.0, 1.0)
    iron = st.slider("আয়রণ / Iron - Fe (mg/L)", 0.0, 20.0, 7.4, 0.1)
    manganese = st.slider("ম্যাঙ্গানিজ / Manganese - Mn (mg/L)", 0.0, 5.0, 0.5, 0.1)
    lat = st.slider("অক্ষাংশ / Latitude_DEG", 20.0, 27.0, 23.50, 0.01)
    lon = st.slider("দ্রাঘিমাংশ / Longitude_DEG", 88.0, 93.0, 90.40, 0.01)
    well_age = st.slider("টিউবওয়েলের বয়স / Well Age (Years)", 0, 100, 8, 1)


with col_dashboard:
    st.subheader("📋 রিয়েল-টাইম অ্যাডাপ্টিভ অ্যানালিটিক্স")

    payload = {
        "WELL_DEPTH": well_depth, "Fe": iron, "Mn": manganese,
        "LAT_DEG": lat, "LONG_DEG": lon, "well_age": well_age
    }

    try:
        response = requests.post("http://localhost:8000/predict", json=payload)
        if response.status_code == 200:
            res_data = response.json()

            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**এজেন্টের বর্তমান অবস্থা:** <span style='color:{res_data['status_color']}; font-weight:bold; font-size:16px;'>{res_data['agent_level']}</span>", unsafe_allow_html=True)
            c2.metric(label="আর্সেনিকের ঝুঁকি (Probability)", value=f"{res_data['risk_probability']:.2f}%")
            c3.metric(label="এজেন্ট কনফিডেন্স স্কোর", value=f"{res_data['confidence']:.2f}%")

            st.markdown("---")

           
            if res_data['human_trigger']:
                st.error("⚠️ **হিউম্যান রিভিউ ট্রিগার (Human Review Trigger):** প্রেডিকশনে অনিশ্চয়তা দেখা দিয়েছে! পানির রাসায়নিক উপাদানগুলো একদম বর্ডারলাইনে আছে। চূড়ান্ত ব্যবহারের আগে সরকারি ল্যাবরেটরি থেকে কেমিক্যাল টেস্ট করিয়ে নিশ্চিত হওয়ার পরামর্শ দেওয়া হচ্ছে।")

          
            st.subheader("🧠 কগনিティブ এআই সিদ্ধান্ত ও গাইডলাইন")
            if "LOW RISK" in res_data['agent_level']:
                st.success(res_data['explanation'])
            elif "MEDIUM RISK" in res_data['agent_level']:
                st.warning(res_data['explanation'])
            else:
                st.error(res_data['explanation'])

            st.write(f"**🎯 অ্যাডাপ্টিভ প্রোটোকল ({res_data['protocol_title']}):**")
            st.markdown(f"- {res_data['guideline_1']}")
            st.markdown(f"- {res_data['guideline_2']}")

            st.markdown("---")

           
            st.subheader("🔮 কাউন্টারফ্যাকচুয়াল রিজনিং (What-If অপ্টিমাইজেশন)")
            if "SAFE" in res_data['counterfactual'] or "নিরাপদ" in res_data['counterfactual']:
                st.success(res_data['counterfactual'])
            else:
                st.info(res_data['counterfactual'])
        else:
            st.error("❌ FastAPI ব্যাকএন্ড সার্ভার থেকে ভুল রেসপন্স এসেছে!")
    except Exception as e:
        st.error("⏳ FastAPI ব্যাকএন্ড সার্ভারের সাথে কানেক্ট করা যাচ্ছে না... দয়া করে পাইপলাইন অটোমেশন সেলটি চালু করুন।")
