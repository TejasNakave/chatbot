#!/usr/bin/env python3
"""Test HTML rendering in Streamlit"""

import streamlit as st

st.set_page_config(page_title="HTML Test", layout="wide")

st.title("🧪 HTML Rendering Test")

# Test 1: Simple HTML outside columns
st.subheader("Test 1: Simple HTML (Outside Columns)")
simple_html = """
<div style="background: #1e1e1e; border-radius: 15px; padding: 15px; color: white;">
    <h3 style="color: #28a745;">🚀 Test Card</h3>
    <p>This should render as HTML, not text.</p>
</div>
"""
st.markdown(simple_html, unsafe_allow_html=True)

# Test 2: HTML inside columns
st.subheader("Test 2: HTML Inside Columns")
cols = st.columns(3)

with cols[0]:
    st.markdown(simple_html, unsafe_allow_html=True)

with cols[1]:
    st.markdown(simple_html, unsafe_allow_html=True)

with cols[2]:
    st.markdown(simple_html, unsafe_allow_html=True)

# Test 3: Complex HTML like our subscription cards
st.subheader("Test 3: Complex HTML (Like Subscription Cards)")
complex_html = """
<div style="background: #1e1e1e; border-radius: 15px; padding: 15px; margin-bottom: 20px; color: white; box-shadow: 0 0 15px #28a745; position: relative; min-height: 300px;">
    <h3 style="color: #28a745; margin-bottom: 10px;">🚀 Explorer</h3>
    <h4 style="margin-bottom: 15px;">₹299 /month</h4>
    <hr style="border: 1px solid #444; margin: 15px 0;">
    <p style="margin-bottom: 10px;"><strong>🌟 Features:</strong></p>
    <ul style="line-height: 1.6; padding-left: 15px; margin-bottom: 15px;">
        <li style='margin-bottom: 5px;'>📊 10 questions per day</li>
        <li style='margin-bottom: 5px;'>💾 1 document limit</li>
        <li style='margin-bottom: 5px;'>👥 1 user(s)</li>
        <li style='margin-bottom: 5px;'>⚡ Fast response time</li>
    </ul>
</div>
"""

cols2 = st.columns(3)
with cols2[0]:
    st.markdown(complex_html, unsafe_allow_html=True)
with cols2[1]: 
    st.markdown(complex_html, unsafe_allow_html=True)
with cols2[2]:
    st.markdown(complex_html, unsafe_allow_html=True)
