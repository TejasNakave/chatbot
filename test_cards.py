import streamlit as st

st.title("Card Rendering Test")

# Your working example
st.markdown("## Working Example:")
st.markdown(
    """
    <div style="background: #1e1e1e; border-radius: 15px; padding: 20px; margin-bottom: 30px; color: white; box-shadow: 0 0 20px #f72585;">
        <h2 style="color: #f72585;">🚀 Premium Plan</h2>
        <h3>₹1,699 / month</h3>
        <hr style="border: 1px solid #444;">
        <p><strong>🌟 Features:</strong></p>
        <ul style="line-height: 1.7;">
            <li>👥 5 Users</li>
            <li>📦 All Modules + Hearing Assessment</li>
            <li>📊 Custom Reports</li>
            <li>🎧 Dedicated Helpdesk</li>
        </ul>
        <p><strong>📊 Usage Limits:</strong></p>
        <ul style="line-height: 1.7;">
            <li>📄 Questions: 500 per day</li>
            <li>📁 Documents: 50</li>
        </ul>
        <a href="#" style="display: inline-block; margin-top: 20px; background: #f72585; color: white; padding: 10px 25px; border-radius: 8px; text-decoration: none; font-weight: bold;">Choose Plan</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Our new implementation
st.markdown("## Our New Implementation:")
st.markdown("""
<div style="background: #1e1e1e; border-radius: 15px; padding: 20px; margin-bottom: 30px; color: white; box-shadow: 0 0 20px #28a745; position: relative;">
    <h2 style="color: #28a745;">🚀 Explorer Plan</h2>
    <h3>₹299 /month</h3>
    <hr style="border: 1px solid #444;">
    <p><strong>🌟 Features:</strong></p>
    <ul style="line-height: 1.7;">
        <li>📊 10 questions per day</li>
        <li>💾 1 document limit</li>
        <li>👥 1 user(s)</li>
        <li>⚡ Fast response time</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("If both cards render properly above, then the issue is fixed! 🎉")
