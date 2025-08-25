import streamlit as st

# Test to verify plan data
st.title("Plan Data Verification")

plans = {
    "explorer": {
        "name": "Explorer",
        "limits": {
            "questions_per_day": 10,
            "documents": 1,
            "users": 1
        }
    },
    "starter": {
        "name": "Starter", 
        "limits": {
            "questions_per_day": 50,
            "documents": 5,
            "users": 1
        }
    },
    "professional": {
        "name": "Professional",
        "limits": {
            "questions_per_day": 100,
            "documents": 10,
            "users": 2
        }
    },
    "advanced": {
        "name": "Advanced",
        "limits": {
            "questions_per_day": 200,
            "documents": 20,
            "users": 3
        }
    }
}

st.markdown("## Plan Limits Verification:")

for plan_key, plan in plans.items():
    st.markdown(f"""
    **{plan['name']} Plan:**
    - 📊 {plan['limits']['questions_per_day']} questions per day
    - 💾 {plan['limits']['documents']} document limit
    - 👥 {plan['limits']['users']} user(s)
    """)
    st.markdown("---")

st.markdown("If you see different numbers above, then the plan data is correct!")
