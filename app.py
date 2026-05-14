"""
app.py — Grand Horizon Airline Flight Booking System
Redesigned with professional animations & premium dark UI.
Run with:  streamlit run app.py
"""

import streamlit as st
from datetime import date, timedelta, datetime
import pandas as pd

import database as db
import utils

# ── Page Config (must be FIRST Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="Grand Horizon Airline",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS — Professional Aurora Midnight Theme + Animations
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── Variables ── */
:root {
    --bg-deep:      #060D1A;
    --bg-mid:       #0B1628;
    --bg-panel:     #0F1E35;
    --bg-card:      #132033;
    --bg-card2:     #182840;
    --border:       rgba(255,255,255,0.07);
    --border2:      rgba(255,255,255,0.13);
    --accent:       #1A6CF5;
    --accent-dim:   rgba(26,108,245,0.12);
    --accent-brd:   rgba(26,108,245,0.30);
    --gold:         #F5A623;
    --gold-dim:     rgba(245,166,35,0.12);
    --gold-brd:     rgba(245,166,35,0.30);
    --teal:         #00C8B4;
    --teal-dim:     rgba(0,200,180,0.12);
    --teal-brd:     rgba(0,200,180,0.30);
    --red:          #EF4444;
    --red-dim:      rgba(239,68,68,0.12);
    --green:        #22C55E;
    --green-dim:    rgba(34,197,94,0.12);
    --text:         #E2EAF5;
    --muted:        #6B84A3;
    --faint:        #344D6A;
}

/* ── Keyframes ── */
@keyframes fadeUp       { from{opacity:0;transform:translateY(24px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeLeft     { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }
@keyframes shimmer      { 0%{background-position:-300% 0} 100%{background-position:300% 0} }
@keyframes pulseRing    { 0%,100%{transform:scale(1);opacity:0.6} 50%{transform:scale(1.25);opacity:0} }
@keyframes pulseDot     { 0%,100%{transform:scale(1);opacity:1} 50%{transform:scale(1.7);opacity:0.4} }
@keyframes floatPlane   { 0%,100%{transform:translateY(0) rotate(0deg)} 50%{transform:translateY(-8px) rotate(2deg)} }
@keyframes glow         { 0%,100%{box-shadow:0 0 0 0 rgba(26,108,245,0)} 50%{box-shadow:0 0 24px 6px rgba(26,108,245,0.18)} }
@keyframes scanLine     { 0%{transform:translateY(-100%)} 100%{transform:translateY(800px)} }
@keyframes rotateRing   { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
@keyframes countUp      { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
@keyframes waveBar      { from{transform:scaleY(0);opacity:0} to{transform:scaleY(1);opacity:1} }
@keyframes borderFlow   { 0%,100%{border-color:var(--accent-brd)} 50%{border-color:var(--accent)} }
@keyframes goldShine    { 0%,100%{text-shadow:none} 50%{text-shadow:0 0 20px rgba(245,166,35,0.5)} }
@keyframes slideInLeft  { from{opacity:0;transform:translateX(-30px)} to{opacity:1;transform:translateX(0)} }
@keyframes slideInRight { from{opacity:0;transform:translateX(30px)}  to{opacity:1;transform:translateX(0)} }

/* Stagger helpers */
.a1{animation:fadeUp .55s ease both}
.a2{animation:fadeUp .55s .08s ease both}
.a3{animation:fadeUp .55s .16s ease both}
.a4{animation:fadeUp .55s .24s ease both}
.a5{animation:fadeUp .55s .32s ease both}
.a6{animation:fadeUp .55s .40s ease both}

/* ── Global reset ── */
html, body, [class*="css"], main,
[data-testid="stAppViewContainer"], .block-container {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-deep) !important;
    color: var(--text) !important;
}
.block-container { padding-top: 2rem !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-mid); }
::-webkit-scrollbar-thumb { background: var(--faint); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
#MainMenu, footer { visibility: hidden; }
.stDeployButton, [data-testid="stToolbar"] { display: none; }

/* ── App Header ── */
.stAppHeader {
    background: rgba(6,13,26,0.90) !important;
    backdrop-filter: blur(20px) !important;
    border-bottom: 1px solid var(--border) !important;
}
.stAppHeader::after {
    content: '';
    display: block; height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--accent) 40%, var(--teal) 60%, transparent 100%);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-panel) 0%, var(--bg-mid) 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    display: block; height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--teal), transparent);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 7px 2px !important;
    cursor: pointer !important;
    transition: color 0.2s !important;
}
[data-testid="stSidebar"] .stRadio label:hover { color: var(--gold) !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, var(--accent) 0%, #0e52c1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.4px !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
    animation: glow 4s infinite;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(26,108,245,0.35) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(26,108,245,0.15) !important;
}
.stTextInput label, .stSelectbox label,
.stDateInput label, .stNumberInput label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.1px !important;
    font-weight: 600 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    font-family: 'Sora', sans-serif !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"]  { background: var(--bg-card2) !important; color: white !important; }
.stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
    animation: fadeUp 0.5s ease both;
}
[data-testid="stMetric"]:hover {
    border-color: var(--accent-brd) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(26,108,245,0.12) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    color: var(--faint) !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Sora', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--gold) !important;
    animation: countUp 0.7s ease both;
}
[data-testid="stMetricDelta"] { color: var(--teal) !important; font-size: 0.8rem !important; }

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    animation: fadeUp 0.5s ease both;
}
[data-testid="stDataFrame"] th {
    background: rgba(26,108,245,0.08) !important;
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text) !important;
    font-size: 0.88rem !important;
    border-color: var(--border) !important;
}

/* ── Page block stagger ── */
[data-testid="stVerticalBlock"] > div                 { animation: fadeUp .45s ease both; }
[data-testid="stVerticalBlock"] > div:nth-child(2)    { animation-delay:.07s }
[data-testid="stVerticalBlock"] > div:nth-child(3)    { animation-delay:.14s }
[data-testid="stVerticalBlock"] > div:nth-child(4)    { animation-delay:.21s }
[data-testid="stVerticalBlock"] > div:nth-child(5)    { animation-delay:.28s }
[data-testid="stVerticalBlock"] > div:nth-child(6)    { animation-delay:.35s }

/* ══════════════════════════════════════
   CUSTOM HTML COMPONENTS
══════════════════════════════════════ */

/* ── Sidebar brand ── */
.brand-block {
    text-align: center;
    padding: 28px 16px 24px;
    border-bottom: 1px solid var(--border);
    position: relative;
}
.brand-plane {
    font-size: 3rem;
    display: block;
    animation: floatPlane 4s ease-in-out infinite;
    margin-bottom: 10px;
}
.brand-name {
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: white;
    letter-spacing: -0.4px;
}
.brand-sub {
    font-size: 0.68rem;
    color: var(--faint);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 4px;
}
.brand-tag {
    display: inline-block;
    margin-top: 14px;
    background: linear-gradient(90deg, var(--accent), var(--teal));
    color: white;
    font-family: 'Sora', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, var(--bg-panel) 0%, #0a2860 50%, var(--bg-panel) 100%);
    border: 1px solid var(--accent-brd);
    border-radius: 24px;
    padding: 52px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.6s ease both;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--teal), transparent);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(26,108,245,0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-scan {
    position: absolute;
    left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(26,108,245,0.4), transparent);
    animation: scanLine 5s linear infinite;
    pointer-events: none;
}
.hero-grid {
    position: absolute; inset: 0; pointer-events: none;
    background:
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,255,255,0.015) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.015) 40px);
}
.hero-eyebrow {
    font-family: 'Sora', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before {
    content: '';
    width: 24px; height: 1px;
    background: linear-gradient(90deg, var(--accent), var(--teal));
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #ffffff 30%, #93c5fd 70%, var(--teal) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeUp 0.6s ease both;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 300;
    line-height: 1.6;
    margin-bottom: 22px;
    animation: fadeUp 0.6s 0.1s ease both;
}
.hero-tagline {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg, rgba(26,108,245,0.15), rgba(0,200,180,0.15));
    border: 1px solid var(--accent-brd);
    color: #93c5fd;
    font-family: 'Sora', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    padding: 7px 18px;
    border-radius: 20px;
    animation: fadeUp 0.6s 0.2s ease both;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Sora', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    margin: 0 0 20px 0;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
    animation: fadeUp 0.5s ease both;
}
.section-heading::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 60px; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--teal));
    border-radius: 2px;
}

/* ── Stat card ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeUp 0.5s ease both;
}
.stat-card:hover {
    border-color: var(--accent-brd);
    transform: translateY(-4px);
    box-shadow: 0 8px 28px rgba(26,108,245,0.12);
}
.stat-card::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--teal));
    opacity: 0;
    transition: opacity 0.3s;
}
.stat-card:hover::before { opacity: 1; }
.stat-value {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--gold);
    animation: countUp 0.7s ease both;
}
.stat-label {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
}

/* ── Flight card ── */
.flight-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 26px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: fadeUp 0.5s ease both;
}
.flight-card:hover {
    border-color: var(--border2);
    transform: translateY(-3px);
    box-shadow: 0 10px 32px rgba(0,0,0,0.3);
}
.flight-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--accent), var(--teal));
    border-radius: 3px 0 0 3px;
}
.flight-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(26,108,245,0.3), transparent);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}

/* Flight card inner elements */
.fc-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.fc-airline-wrap { display: flex; align-items: center; gap: 12px; }
.fc-logo  { font-size: 1.6rem; }
.fc-airline { font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 700; color: white; }
.fc-number  { font-size: 0.75rem; color: var(--accent); font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }
.fc-badge   {
    display: inline-block;
    background: var(--accent-dim); border: 1px solid var(--accent-brd);
    color: #93c5fd; font-size: 0.7rem; font-weight: 700;
    padding: 4px 12px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.8px;
}
.fc-route   { display: flex; align-items: center; gap: 16px; margin: 16px 0; }
.fc-time    { font-family: 'Sora', sans-serif; font-size: 2.2rem; font-weight: 800; color: white; line-height: 1; }
.fc-city    { font-size: 0.8rem; color: var(--muted); margin-top: 4px; }
.fc-mid     { flex: 1; text-align: center; }
.fc-duration { font-size: 0.72rem; color: var(--muted); margin-bottom: 4px; }
.fc-line    { border-top: 1px dashed rgba(255,255,255,0.15); margin: 4px 0; position: relative; }
.fc-plane-icon {
    display: inline-block;
    color: var(--accent); font-size: 1rem;
    animation: floatPlane 3s ease-in-out infinite;
}
.fc-footer  { display: flex; justify-content: space-between; align-items: flex-end; }
.fc-price   { font-family: 'Sora', sans-serif; font-size: 1.8rem; font-weight: 800; color: var(--gold); animation: goldShine 3s infinite; }
.fc-price-label { font-size: 0.72rem; color: var(--muted); margin-top: 2px; }
.fc-seats   { font-size: 0.8rem; color: var(--teal); font-weight: 500; }

/* ── Popular route card ── */
.route-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}
.route-card:hover {
    border-color: var(--gold-brd);
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(245,166,35,0.12);
}
.route-card::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--gold), var(--accent));
    opacity: 0;
    transition: opacity 0.3s;
}
.route-card:hover::before { opacity: 1; }
.route-flag  { font-size: 1.8rem; margin-bottom: 10px; }
.route-name  { font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 700; color: white; }
.route-price { font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 700; color: var(--gold); margin-top: 8px; }

/* ── Feature card ── */
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 28px 22px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}
.feature-card:hover {
    border-color: var(--teal-brd);
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,200,180,0.1);
}
.feature-icon { font-size: 2.6rem; margin-bottom: 14px; display: block; }
.feature-title { font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 700; color: white; margin-bottom: 10px; }
.feature-desc  { font-size: 0.85rem; color: var(--muted); line-height: 1.65; }

/* ── Alert boxes ── */
.success-box {
    background: var(--green-dim);
    border: 1px solid rgba(34,197,94,0.35);
    border-radius: 14px; padding: 16px 20px;
    color: #86efac; margin: 12px 0;
    animation: fadeUp 0.4s ease both;
    display: flex; align-items: flex-start; gap: 10px;
}
.error-box {
    background: var(--red-dim);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 14px; padding: 16px 20px;
    color: #fca5a5; margin: 12px 0;
    animation: fadeUp 0.4s ease both;
}
.info-box {
    background: var(--accent-dim);
    border: 1px solid var(--accent-brd);
    border-radius: 14px; padding: 16px 20px;
    color: #93c5fd; margin: 12px 0;
    animation: fadeUp 0.4s ease both;
}
.warning-box {
    background: var(--gold-dim);
    border: 1px solid var(--gold-brd);
    border-radius: 14px; padding: 16px 20px;
    color: #fcd34d; margin: 12px 0;
    animation: fadeUp 0.4s ease both;
}

/* ── Status pills ── */
.pill {
    display: inline-block;
    padding: 4px 13px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 700;
    font-family: 'Sora', sans-serif;
    text-transform: uppercase; letter-spacing: 0.8px;
}
.pill-confirmed { background: var(--green-dim); color: #86efac; border: 1px solid rgba(34,197,94,0.3); }
.pill-cancelled { background: var(--red-dim);   color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.pill-pending   { background: var(--gold-dim);  color: #fcd34d; border: 1px solid var(--gold-brd); }

/* ── Booking detail card ── */
.booking-detail-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 28px;
    margin-top: 20px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}
.booking-detail-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--teal), transparent);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}
.booking-ref {
    font-family: 'Sora', sans-serif;
    font-size: 1.2rem; font-weight: 800; color: white;
}
.booking-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 18px;
}
.meta-item { font-size: 0.87rem; color: var(--muted); }
.meta-item strong { color: white; }

/* ── Ticket / E-ticket card ── */
.ticket-wrap {
    background: linear-gradient(135deg, var(--bg-panel), #0a2860);
    border: 1px solid var(--accent-brd);
    border-radius: 20px;
    padding: 32px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
    animation: borderFlow 3s infinite;
}
.ticket-wrap::before {
    content: '✈ GRAND HORIZON AIRLINE ✈';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}
.ticket-notch-left, .ticket-notch-right {
    position: absolute;
    width: 26px; height: 26px;
    background: var(--bg-deep);
    border-radius: 50%;
    top: 50%; transform: translateY(-50%);
}
.ticket-notch-left  { left: -13px; }
.ticket-notch-right { right: -13px; }
.ticket-divider-dash {
    border: none;
    border-top: 2px dashed rgba(26,108,245,0.3);
    margin: 20px 0;
    position: relative;
}

/* ── Passenger form card ── */
.pax-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}
.pax-card::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--gold), var(--accent));
    border-radius: 3px 0 0 3px;
}
.pax-title {
    font-family: 'Sora', sans-serif;
    font-size: 0.92rem; font-weight: 700;
    color: var(--gold); margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
}

/* ── Price summary box ── */
.price-summary {
    background: linear-gradient(135deg, rgba(245,166,35,0.08), rgba(26,108,245,0.08));
    border: 1px solid var(--gold-brd);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 18px;
    animation: fadeUp 0.5s ease both;
}
.price-total {
    font-family: 'Sora', sans-serif;
    font-size: 1.8rem; font-weight: 800;
    color: var(--gold);
    animation: goldShine 3s infinite;
}
.price-breakdown { font-size: 0.82rem; color: var(--muted); margin-top: 5px; }

/* ── Admin stat card (5-col) ── */
.admin-stat {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    transition: all 0.3s;
    animation: fadeUp 0.5s ease both;
}
.admin-stat:hover {
    border-color: var(--accent-brd);
    transform: translateY(-3px);
}
.admin-stat-val {
    font-family: 'Sora', sans-serif;
    font-size: 1.9rem; font-weight: 800; color: var(--gold);
    animation: countUp 0.7s ease both;
}
.admin-stat-lbl {
    font-size: 0.7rem; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1.1px;
    margin-top: 5px; font-weight: 600;
}

/* ── Admin access card ── */
.admin-access-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 40px;
    max-width: 440px;
    margin: 0 auto;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}
.admin-access-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--teal), transparent);
    background-size: 300% 100%;
    animation: shimmer 4s linear infinite;
}

/* ── Confirmation screen ── */
.confirm-screen {
    background: linear-gradient(135deg, var(--bg-card), #0a2860);
    border: 1px solid var(--green-dim);
    border-radius: 24px;
    padding: 48px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.6s ease both;
}
.confirm-screen::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--green), transparent);
    background-size: 300% 100%;
    animation: shimmer 3s linear infinite;
}
.confirm-ref {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem; font-weight: 800;
    color: var(--green);
    letter-spacing: -1px;
    display: block;
    margin: 10px 0;
    animation: goldShine 3s infinite;
}

/* ── Divider ── */
.sky-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 28px 0;
}

/* ── Sidebar footer ── */
.sidebar-footer {
    font-size: 0.68rem;
    color: var(--faint);
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.05);
    line-height: 1.7;
}
.sidebar-version { color: var(--accent); font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ── App Initialization ─────────────────────────────────────────────────────────
@st.cache_resource
def initialize():
    db.init_db()
    db.seed_flights()

initialize()

# ── Session State Defaults ─────────────────────────────────────────────────────
defaults = {
    "page":             "Home",
    "search_results":   [],
    "selected_flight":  None,
    "booking_confirmed":False,
    "last_booking_ref": None,
    "search_params":    {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <span class="brand-plane">✈️</span>
        <div class="brand-name">Grand Horizon Airline</div>
        <div class="brand-sub">Fly Higher. Fly Smarter.</div>
        <div class="brand-tag">🌍 Global Network</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠  Home", "🔍  Search Flights", "📋  My Booking", "🛡️  Admin Panel"],
        label_visibility="collapsed",
    )
    st.session_state.page = page.split("  ", 1)[1] if "  " in page else page

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-footer">
        © 2025 Grand Horizon Airline Ltd.<br>
        All rights reserved.<br><br>
        <span class="sidebar-version">Version 1.0.0</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def section_title(icon, text):
    st.markdown(f'<div class="section-heading">{icon}&nbsp; {text}</div>', unsafe_allow_html=True)

def pill(label):
    if label == "Confirmed":
        return f'<span class="pill pill-confirmed">{label}</span>'
    elif label == "Cancelled":
        return f'<span class="pill pill-cancelled">{label}</span>'
    return f'<span class="pill pill-pending">{label}</span>'


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-scan"></div>
        <div class="hero-grid"></div>
        <div class="hero-eyebrow">✦ Grand Horizon Airline</div>
        <h1 class="hero-title">Your Journey<br>Begins Here</h1>
        <p class="hero-subtitle">
            Premium flights to 50+ destinations worldwide.<br>
            Search, book, and fly — all in one place.
        </p>
        <span class="hero-tagline">🌍 GLOBAL NETWORK &nbsp;·&nbsp; 24/7 SUPPORT &nbsp;·&nbsp; BEST PRICE GUARANTEE</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick stats ────────────────────────────────────────────────────────────
    stats = db.get_statistics()
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, delay in [
        (c1, "50+",               "Destinations",   "0s"),
        (c2, stats["confirmed"],  "Bookings Made",  "0.08s"),
        (c3, "15+",               "Airlines",       "0.16s"),
        (c4, "24/7",              "Support",        "0.24s"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card" style="animation-delay:{delay}">
                <div class="stat-value">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Popular routes ─────────────────────────────────────────────────────────
    section_title("🔥", "Popular Routes")
    popular_routes = [
        ("Lagos",    "London",    "from $310", "🇳🇬→🇬🇧"),
        ("Lagos",    "Dubai",     "from $280", "🇳🇬→🇦🇪"),
        ("Nairobi",  "London",    "from $360", "🇰🇪→🇬🇧"),
        ("Abuja",    "Frankfurt", "from $340", "🇳🇬→🇩🇪"),
        ("Lagos",    "Paris",     "from $305", "🇳🇬→🇫🇷"),
        ("New York", "London",    "from $380", "🇺🇸→🇬🇧"),
    ]
    cols = st.columns(3)
    for i, (org, dst, price, flag) in enumerate(popular_routes):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="route-card" style="animation-delay:{i*0.07}s">
                <div class="route-flag">{flag}</div>
                <div class="route-name">{org} → {dst}</div>
                <div class="route-price">{price}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Why choose us ──────────────────────────────────────────────────────────
    section_title("💎", "Why Grand Horizon Airline?")
    features = [
        ("🛡️", "Safe & Reliable",  "All flights operated by IATA-certified airlines with top-tier safety records.", "0s"),
        ("💸", "Best Price Guarantee", "Our price match guarantee ensures you never overpay for your seat.", "0.08s"),
        ("⚡", "Instant Booking",  "Confirm your seat in under 2 minutes with our streamlined checkout.", "0.16s"),
    ]
    f1, f2, f3 = st.columns(3)
    for col, (icon, title, desc, delay) in zip([f1, f2, f3], features):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="animation-delay:{delay}">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats bar ─────────────────────────────────────────────────────────────
    section_title("📊", "Live Stats")
    s1, s2, s3 = st.columns(3)
    s1.metric("Total Bookings",  stats["total_bookings"], f"+{stats['confirmed']} confirmed")
    s2.metric("Total Revenue",   f"${stats['total_revenue']:,.0f}", "USD collected")
    s3.metric("Top Route",       stats["popular_route"],  "Most booked")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SEARCH FLIGHTS
# ══════════════════════════════════════════════════════════════════════════════
def page_search():
    section_title("🔍", "Search Available Flights")

    cities = db.get_available_cities()

    # ── Search form ────────────────────────────────────────────────────────────
    with st.form("search_form"):
        c1, c2 = st.columns(2)
        with c1:
            origin      = st.selectbox("🛫  Departure City",  cities, index=0)
        with c2:
            destination = st.selectbox("🛬  Destination City", cities, index=min(1, len(cities)-1))

        c3, c4, c5 = st.columns(3)
        with c3:
            travel_date = st.date_input(
                "📅  Travel Date",
                value=date.today() + timedelta(days=7),
                min_value=date.today(),
                max_value=date.today() + timedelta(days=365),
            )
        with c4:
            passengers = st.number_input("👥  Passengers", min_value=1, max_value=9, value=1)
        with c5:
            flight_class = st.selectbox("✈️  Class", ["Economy", "Business", "First Class"])

        submitted = st.form_submit_button("🔍  Search Flights", use_container_width=True)

    if submitted:
        if origin == destination:
            st.markdown('<div class="error-box">⚠️ Departure and destination cities cannot be the same.</div>',
                        unsafe_allow_html=True)
        else:
            results = db.search_flights(origin, destination)
            st.session_state.search_results  = results
            st.session_state.search_params   = {
                "origin": origin, "destination": destination,
                "travel_date": str(travel_date),
                "passengers": passengers, "flight_class": flight_class,
            }

    # ── Results ────────────────────────────────────────────────────────────────
    if st.session_state.search_results:
        params  = st.session_state.search_params
        flights = st.session_state.search_results
        cls     = params["flight_class"]
        pax     = params["passengers"]

        st.markdown(f"""
        <div class="info-box">
            ✈️ Found <strong>{len(flights)}</strong> flight(s) from
            <strong>{params['origin']}</strong> to <strong>{params['destination']}</strong>
            on <strong>{params['travel_date']}</strong> ·
            {pax} passenger(s) · {cls}
        </div>
        """, unsafe_allow_html=True)

        price_key = {"Economy": "economy_price", "Business": "business_price", "First Class": "first_price"}[cls]

        for i, flight in enumerate(flights):
            base_price = flight[price_key]
            logo       = utils.get_airline_logo_emoji(flight["airline"])
            total      = utils.calculate_total_price(base_price, pax, date.fromisoformat(params["travel_date"]))
            surcharge  = (date.fromisoformat(params["travel_date"]) - date.today()).days <= 7

            col_info, col_btn = st.columns([5, 1])
            with col_info:
                st.markdown(f"""
                <div class="flight-card" style="animation-delay:{i*0.06}s">
                    <div class="fc-header">
                        <div class="fc-airline-wrap">
                            <span class="fc-logo">{logo}</span>
                            <div>
                                <div class="fc-airline">{flight['airline']}</div>
                                <div class="fc-number">{flight['flight_number']} · {flight['aircraft']}</div>
                            </div>
                        </div>
                        <div>
                            <span class="fc-badge">{cls}</span>
                            {"&nbsp;<span class='fc-badge' style='border-color:rgba(245,166,35,0.4);color:#fcd34d;background:rgba(245,166,35,0.1)'>⚡ Last Min</span>" if surcharge else ""}
                        </div>
                    </div>
                    <div class="fc-route">
                        <div>
                            <div class="fc-time">{flight['departure_time']}</div>
                            <div class="fc-city">{flight['origin']}</div>
                        </div>
                        <div class="fc-mid">
                            <div class="fc-duration">{flight['duration']}</div>
                            <div class="fc-line"></div>
                            <div class="fc-plane-icon">✈</div>
                        </div>
                        <div style="text-align:right">
                            <div class="fc-time">{flight['arrival_time']}</div>
                            <div class="fc-city">{flight['destination']}</div>
                        </div>
                    </div>
                    <div class="fc-footer">
                        <div>
                            <div class="fc-price">${total:,.2f}</div>
                            <div class="fc-price-label">total for {pax} pax · {cls}</div>
                        </div>
                        <div class="fc-seats">🪑 {flight['available_seats']} seats left</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='margin-top:96px'></div>", unsafe_allow_html=True)
                if st.button("Select ✈️", key=f"sel_{flight['flight_number']}", use_container_width=True):
                    st.session_state.selected_flight = flight
                    st.session_state.search_params["base_price"]  = base_price
                    st.session_state.search_params["total_price"] = total
                    st.rerun()

    elif st.session_state.search_params:
        st.markdown('<div class="error-box">😔 No flights found for this route. Try different cities or dates.</div>',
                    unsafe_allow_html=True)

    # ── Booking form (appears after selecting a flight) ──────────────────────
    if st.session_state.selected_flight:
        flight = st.session_state.selected_flight
        params = st.session_state.search_params
        pax    = params["passengers"]
        cls    = params["flight_class"]

        st.markdown("<hr class='sky-divider'>", unsafe_allow_html=True)
        section_title("📝", f"Passenger Details — {flight['flight_number']}")

        st.markdown(f"""
        <div class="info-box">
            You selected: <strong>{flight['airline']}</strong> {flight['flight_number']} ·
            {flight['origin']} → {flight['destination']} ·
            Departs <strong>{flight['departure_time']}</strong> · <strong>{cls}</strong>
        </div>
        """, unsafe_allow_html=True)

        seat_options   = utils.generate_seat_map(cls)
        passengers_data = []

        with st.form("booking_form"):
            for i in range(pax):
                st.markdown(f"""
                <div class="pax-card">
                    <div class="pax-title">👤 Passenger {i+1}</div>
                </div>
                """, unsafe_allow_html=True)

                bc1, bc2 = st.columns(2)
                with bc1:
                    fname      = st.text_input("First Name *",      key=f"fn_{i}",  placeholder="e.g. Amara")
                    passport   = st.text_input("Passport Number *", key=f"pp_{i}",  placeholder="e.g. A12345678")
                    nationality= st.text_input("Nationality *",     key=f"nat_{i}", placeholder="e.g. Nigerian")
                with bc2:
                    lname = st.text_input("Last Name *",     key=f"ln_{i}", placeholder="e.g. Okafor")
                    dob   = st.date_input(
                        "Date of Birth *", key=f"dob_{i}",
                        value=date(1990,1,1),
                        min_value=date(1920,1,1),
                        max_value=date.today() - timedelta(days=1),
                    )
                    used_seats     = [p.get("seat_number","") for p in passengers_data]
                    remaining      = [s for s in seat_options if s not in used_seats]
                    seat = st.selectbox("Seat Number *", remaining or ["N/A"], key=f"seat_{i}")

                passengers_data.append({
                    "booking_ref":    "",
                    "first_name":     fname,
                    "last_name":      lname,
                    "passport_number":passport,
                    "date_of_birth":  str(dob),
                    "nationality":    nationality,
                    "seat_number":    seat,
                })
                if i < pax - 1:
                    st.markdown("<hr class='sky-divider'>", unsafe_allow_html=True)

            # Price summary
            surcharge_note = "· ⚡ Last-minute surcharge applied" if (
                date.fromisoformat(params["travel_date"]) - date.today()
            ).days <= 7 else ""
            st.markdown(f"""
            <div class="price-summary">
                <div class="price-total">💳 ${params['total_price']:,.2f} USD</div>
                <div class="price-breakdown">
                    {pax} passenger(s) · {cls} · {params['origin']} → {params['destination']} {surcharge_note}
                </div>
            </div>
            """, unsafe_allow_html=True)

            confirm = st.form_submit_button("✅ Confirm Booking", use_container_width=True)

        if confirm:
            errors = []
            for i, p in enumerate(passengers_data):
                ok, msg = utils.validate_passenger_data(p)
                if not ok:
                    errors.append(f"Passenger {i+1}: {msg}")

            if errors:
                for err in errors:
                    st.markdown(f'<div class="error-box">⚠️ {err}</div>', unsafe_allow_html=True)
            else:
                ref = utils.generate_booking_ref()
                for p in passengers_data:
                    p["booking_ref"] = ref

                booking_record = {
                    "booking_ref":      ref,
                    "flight_id":        flight["id"],
                    "flight_number":    flight["flight_number"],
                    "booking_date":     datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "travel_date":      params["travel_date"],
                    "flight_class":     cls,
                    "total_passengers": pax,
                    "total_price":      params["total_price"],
                    "status":           "Confirmed",
                }
                success = db.create_booking(booking_record, passengers_data)
                if success:
                    st.session_state.booking_confirmed  = True
                    st.session_state.last_booking_ref   = ref
                    st.session_state.selected_flight    = None
                    st.session_state.search_results     = []
                    st.rerun()
                else:
                    st.markdown('<div class="error-box">❌ Booking failed. Please try again.</div>',
                                unsafe_allow_html=True)

    # ── Success screen ─────────────────────────────────────────────────────────
    if st.session_state.booking_confirmed:
        ref = st.session_state.last_booking_ref
        st.markdown(f"""
        <div class="confirm-screen">
            <div style="font-size:3rem;margin-bottom:8px;">🎉</div>
            <div style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:800;
                        color:white;margin-bottom:8px;">Booking Confirmed!</div>
            <div style="color:var(--muted);font-size:0.9rem;margin-bottom:12px;">
                Your reference number is:
            </div>
            <span class="confirm-ref">{ref}</span>
            <div style="color:var(--muted);font-size:0.85rem;margin-top:14px;">
                Go to <strong style="color:white;">My Booking</strong> in the sidebar
                to view and download your e-ticket.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Search Another Flight"):
            st.session_state.booking_confirmed = False
            st.session_state.last_booking_ref  = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: MY BOOKING
# ══════════════════════════════════════════════════════════════════════════════
def page_my_booking():
    section_title("📋", "Retrieve My Booking")

    st.markdown("""
    <div class="info-box">
        Enter your booking reference below to view your itinerary, passenger details,
        and download your e-ticket.
    </div>
    """, unsafe_allow_html=True)

    col_in, col_btn = st.columns([3, 1])
    with col_in:
        ref_input = st.text_input(
            "Booking Reference",
            placeholder="e.g. SKY-A3F9-X2",
            help="Your reference was shown on the confirmation screen.",
            label_visibility="collapsed",
        ).strip().upper()
    with col_btn:
        find = st.button("🔍 Find Booking", use_container_width=True)

    if find:
        if not ref_input:
            st.markdown('<div class="error-box">⚠️ Please enter your booking reference.</div>',
                        unsafe_allow_html=True)
        else:
            booking = db.get_booking(ref_input)
            if not booking:
                st.markdown('<div class="error-box">❌ No booking found with that reference. Check and try again.</div>',
                            unsafe_allow_html=True)
            else:
                passengers  = db.get_booking_passengers(ref_input)
                all_flights = db.get_all_flights()
                flight      = next((f for f in all_flights if f["id"] == booking["flight_id"]), {})

                # ── Booking card ───────────────────────────────────────────────
                st.markdown(f"""
                <div class="booking-detail-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                margin-bottom:20px;padding-bottom:16px;
                                border-bottom:1px dashed rgba(255,255,255,0.08)">
                        <div class="booking-ref">📄 {booking['booking_ref']}</div>
                        {pill(booking['status'])}
                    </div>
                    <div class="booking-meta">
                        <div class="meta-item">✈️ Flight <strong>{booking['flight_number']}</strong></div>
                        <div class="meta-item">🗓️ Travel Date <strong>{booking['travel_date']}</strong></div>
                        <div class="meta-item">🛫 Route <strong>{flight.get('origin','?')} → {flight.get('destination','?')}</strong></div>
                        <div class="meta-item">💺 Class <strong>{booking['flight_class']}</strong></div>
                        <div class="meta-item">👥 Passengers <strong>{booking['total_passengers']}</strong></div>
                        <div class="meta-item">💳 Total Paid <strong style="color:var(--gold)">${booking['total_price']:,.2f}</strong></div>
                        <div class="meta-item">📅 Booked On <strong>{booking['booking_date']}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Passengers ────────────────────────────────────────────────
                section_title("🧳", "Passenger Details")
                for i, p in enumerate(passengers, 1):
                    st.markdown(f"""
                    <div class="flight-card" style="animation-delay:{i*0.06}s">
                        <div class="pax-title">👤 Passenger {i}: {p['first_name']} {p['last_name']}</div>
                        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
                                    gap:10px;color:var(--muted);font-size:0.86rem;">
                            <div>🪪 Passport: <span style="color:white">{p['passport_number']}</span></div>
                            <div>🌍 Nationality: <span style="color:white">{p['nationality']}</span></div>
                            <div>🪑 Seat: <strong style="color:var(--gold);font-size:1rem">{p['seat_number']}</strong></div>
                            <div>🎂 DOB: <span style="color:white">{p['date_of_birth']}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── E-ticket ──────────────────────────────────────────────────
                section_title("🎫", "Your E-Ticket")
                ticket_text = utils.generate_ticket_text(booking, passengers, flight)

                st.markdown("""
                <div class="ticket-wrap">
                    <div class="ticket-notch-left"></div>
                    <div class="ticket-notch-right"></div>
                """, unsafe_allow_html=True)
                st.code(ticket_text, language=None)
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Ticket (.txt)",
                    data=ticket_text,
                    file_name=f"ticket_{ref_input}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════════════════════════════
def page_admin():
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    # ── PIN gate ───────────────────────────────────────────────────────────────
    if not st.session_state.admin_authenticated:
        st.markdown("""
        <div class="admin-access-card">
            <div style="text-align:center;margin-bottom:24px">
                <div style="font-size:2.8rem;margin-bottom:8px">🛡️</div>
                <div style="font-family:'Sora',sans-serif;font-size:1.3rem;
                            font-weight:800;color:white;margin-bottom:4px">Admin Access</div>
                <div style="font-size:0.85rem;color:var(--muted)">
                    Restricted to Grand Horizon Airline staff only.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        pin = st.text_input("Enter Admin PIN", type="password", placeholder="••••")
        if st.button("🔑 Login", use_container_width=True):
            if pin == "1234":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.markdown('<div class="error-box">❌ Incorrect PIN. Please try again.</div>',
                            unsafe_allow_html=True)
        st.caption("Demo PIN: 1234")
        return

    # ── Logout ─────────────────────────────────────────────────────────────────
    col_title, col_out = st.columns([5, 1])
    with col_title:
        section_title("🛡️", "Admin Dashboard")
    with col_out:
        if st.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

    # ── Statistics ─────────────────────────────────────────────────────────────
    stats = db.get_statistics()
    s1, s2, s3, s4, s5 = st.columns(5)
    stat_data = [
        (stats["total_bookings"],           "Total Bookings",  "0s"),
        (stats["confirmed"],                "Confirmed",       "0.06s"),
        (stats["cancelled"],                "Cancelled",       "0.12s"),
        (f"${stats['total_revenue']:,.0f}", "Revenue (USD)",   "0.18s"),
        (stats["popular_route"],            "Top Route",       "0.24s"),
    ]
    for col, (val, label, delay) in zip([s1, s2, s3, s4, s5], stat_data):
        with col:
            st.markdown(f"""
            <div class="admin-stat" style="animation-delay:{delay}">
                <div class="admin-stat-val">{val}</div>
                <div class="admin-stat-lbl">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋 All Bookings", "✈️ All Flights", "❌ Cancel Booking"])

    # Tab 1: All Bookings
    with tab1:
        bookings = db.get_all_bookings()
        if not bookings:
            st.markdown('<div class="info-box">No bookings found yet.</div>', unsafe_allow_html=True)
        else:
            df = pd.DataFrame(bookings)
            display_cols = ["booking_ref","flight_number","travel_date",
                            "flight_class","total_passengers","total_price","status","booking_date"]
            df_display = df[display_cols].rename(columns={
                "booking_ref":"Ref","flight_number":"Flight",
                "travel_date":"Travel Date","flight_class":"Class",
                "total_passengers":"Pax","total_price":"Price (USD)",
                "status":"Status","booking_date":"Booked On",
            })
            st.dataframe(df_display, use_container_width=True, height=400)
            st.caption(f"Showing {len(bookings)} booking(s)")

    # Tab 2: All Flights
    with tab2:
        flights  = db.get_all_flights()
        df_f     = pd.DataFrame(flights)
        display_f = ["flight_number","airline","origin","destination",
                     "departure_time","arrival_time","duration",
                     "economy_price","business_price","first_price",
                     "available_seats","total_seats","aircraft"]
        df_f_display = df_f[display_f].rename(columns={
            "flight_number":"Flight","airline":"Airline",
            "origin":"From","destination":"To",
            "departure_time":"Departs","arrival_time":"Arrives",
            "duration":"Duration","economy_price":"Economy $",
            "business_price":"Business $","first_price":"First $",
            "available_seats":"Avail.","total_seats":"Total","aircraft":"Aircraft",
        })
        st.dataframe(df_f_display, use_container_width=True, height=500)
        st.caption(f"Showing {len(flights)} flight(s)")

    # Tab 3: Cancel Booking
    with tab3:
        st.markdown("""
        <div class="info-box">
            Enter a booking reference below to cancel it. This action cannot be undone.
        </div>
        """, unsafe_allow_html=True)

        cancel_ref = st.text_input(
            "Booking Reference to Cancel",
            placeholder="e.g. SKY-A3F9-X2",
            label_visibility="collapsed",
        ).strip().upper()

        if cancel_ref:
            b = db.get_booking(cancel_ref)
            if b:
                st.markdown(f"""
                <div class="booking-detail-card">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div class="booking-ref">{cancel_ref}</div>
                        {pill(b['status'])}
                    </div>
                    <div class="booking-meta" style="margin-top:14px">
                        <div class="meta-item">✈️ <strong>{b['flight_number']}</strong></div>
                        <div class="meta-item">🗓️ <strong>{b['travel_date']}</strong></div>
                        <div class="meta-item">💺 <strong>{b['flight_class']}</strong></div>
                        <div class="meta-item">💳 <strong style="color:var(--gold)">${b['total_price']:,.2f}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if b["status"] == "Confirmed":
                    if st.button("❌ Cancel This Booking", type="primary"):
                        if db.cancel_booking(cancel_ref):
                            st.markdown('<div class="success-box">✅ Booking cancelled successfully.</div>',
                                        unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown('<div class="error-box">❌ Could not cancel booking.</div>',
                                        unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-box">⚠️ This booking is already cancelled.</div>',
                                unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ Booking not found.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page_map = {
    "Home":           page_home,
    "Search Flights": page_search,
    "My Booking":     page_my_booking,
    "Admin Panel":    page_admin,
}

current_page = st.session_state.page
page_map.get(current_page, page_home)()