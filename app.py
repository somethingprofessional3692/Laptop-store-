import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ==============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="NEXUS TECH | Professional Laptop & Computing Hardware",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design & Color Palette (Emerald / Dark Slate - NO BLUE)
CUSTOM_CSS = """
<style>
    /* Global Theme & Typography */
    :root {
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --accent-emerald: #10b981;
        --accent-emerald-hover: #059669;
        --accent-amber: #f59e0b;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --border-color: #334155;
    }

    /* Main Container background overrides */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-main);
    }
    
    /* Header & Navigation Styling */
    .brand-header {
        background: linear-gradient(135deg, #022c22 0%, #0f172a 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        border: 1px solid var(--accent-emerald);
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.1);
    }
    .brand-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        margin: 0;
    }
    .brand-subtitle {
        color: var(--accent-emerald);
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 5px;
    }

    /* Cards & Product Layout */
    .product-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .product-card:hover {
        border-color: var(--accent-emerald);
        transform: translateY(-3px);
    }
    .badge-discount {
        background-color: #ef4444;
        color: white;
        font-size: 0.75rem;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .badge-gen {
        background-color: #374151;
        color: #e5e7eb;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-left: 5px;
    }
    .price-original {
        text-decoration: line-through;
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-right: 8px;
    }
    .price-discounted {
        color: var(--accent-emerald);
        font-size: 1.3rem;
        font-weight: 700;
    }
    .specs-text {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin: 8px 0;
        line-height: 1.4;
    }
    
    /* Buttons Override */
    .stButton > button {
        background-color: var(--accent-emerald) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: var(--accent-emerald-hover) !important;
    }
    
    /* Utility Banner */
    .promo-banner {
        background-color: #1e1b4b;
        border-left: 4px solid var(--accent-amber);
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 2rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session State
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []

# ==============================================================================
# DATASET GENERATION (50+ REALISTIC LAPTOP MODELS ACROSS 6 CATEGORIES & GENERATIONS)
# ==============================================================================
@st.cache_data
def load_laptop_catalog():
    laptops = [
        # --- CATEGORY 1: ULTRA-PORTABLE & ULTRABOOKS ---
        {"id": 101, "name": "Apple MacBook Air 13 M3", "brand": "Apple", "category": "Ultrabook", "gen": "Latest Gen (M3)", "cpu": "Apple M3 (8-Core)", "ram": "16GB Unified", "storage": "512GB SSD", "display": "13.6\" Liquid Retina", "price": 1299, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop"},
        {"id": 102, "name": "Dell XPS 13 9340", "brand": "Dell", "category": "Ultrabook", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 7 155H", "ram": "16GB LPDDR5x", "storage": "1TB NVMe SSD", "display": "13.4\" FHD+ InfinityEdge", "price": 1399, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 103, "name": "Lenovo Yoga Slim 7i", "brand": "Lenovo", "category": "Ultrabook", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 5 125H", "ram": "16GB LPDDR5x", "storage": "512GB SSD", "display": "14\" 2.8K OLED 120Hz", "price": 1049, "discount_pct": 8, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 104, "name": "ASUS Zenbook 14 OLED", "brand": "ASUS", "category": "Ultrabook", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 7 155H", "ram": "32GB LPDDR5x", "storage": "1TB Gen4 SSD", "display": "14\" 3K OLED Touch", "price": 1299, "discount_pct": 12, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 105, "name": "HP Spectre x360 14", "brand": "HP", "category": "Ultrabook", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 7 155H", "ram": "16GB LPDDR5x", "storage": "1TB NVMe SSD", "display": "14\" 2.8K OLED Touch", "price": 1499, "discount_pct": 5, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 106, "name": "Acer Swift Go 14", "brand": "Acer", "category": "Ultrabook", "gen": "13th Gen Intel", "cpu": "Intel Core i7-13700H", "ram": "16GB LPDDR5", "storage": "512GB SSD", "display": "14\" 2.8K OLED", "price": 899, "discount_pct": 20, "img": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=500&auto=format&fit=crop"},
        {"id": 107, "name": "LG Gram 14 SuperSlim", "brand": "LG", "category": "Ultrabook", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1360P", "ram": "16GB LPDDR5", "storage": "1TB SSD", "display": "15.6\" FHD OLED", "price": 1199, "discount_pct": 18, "img": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop"},
        {"id": 108, "name": "Samsung Galaxy Book4 Pro", "brand": "Samsung", "category": "Ultrabook", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 7 155H", "ram": "16GB LPDDR5x", "storage": "512GB SSD", "display": "14\" Dynamic AMOLED 2X", "price": 1449, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=500&auto=format&fit=crop"},
        {"id": 109, "name": "Microsoft Surface Laptop 6", "brand": "Microsoft", "category": "Ultrabook", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 5 135H", "ram": "16GB LPDDR5x", "storage": "256GB Gen4 SSD", "display": "13.5\" PixelSense Touch", "price": 1199, "discount_pct": 5, "img": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=500&auto=format&fit=crop"},

        # --- CATEGORY 2: HIGH-PERFORMANCE GAMING ---
        {"id": 201, "name": "ASUS ROG Strix SCAR 18", "brand": "ASUS", "category": "Gaming", "gen": "14th Gen Intel / RTX 40", "cpu": "Intel Core i9-14900HX", "ram": "32GB DDR5", "storage": "2TB NVMe Raid 0", "display": "18\" QHD+ 240Hz Mini-LED", "price": 2999, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&auto=format&fit=crop"},
        {"id": 202, "name": "Lenovo Legion Pro 7i", "brand": "Lenovo", "category": "Gaming", "gen": "14th Gen Intel / RTX 40", "cpu": "Intel Core i9-14900HX", "ram": "32GB DDR5", "storage": "1TB Gen4 SSD", "display": "16\" WQXGA 240Hz IPS", "price": 2499, "discount_pct": 12, "img": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=500&auto=format&fit=crop"},
        {"id": 203, "name": "Razer Blade 16", "brand": "Razer", "category": "Gaming", "gen": "14th Gen Intel / RTX 40", "cpu": "Intel Core i9-14900HX", "ram": "32GB DDR5", "storage": "1TB SSD", "display": "16\" Dual-Mode Mini-LED 4K/FHD+", "price": 3099, "discount_pct": 5, "img": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=500&auto=format&fit=crop"},
        {"id": 204, "name": "MSI Titan 18 HX", "brand": "MSI", "category": "Gaming", "gen": "14th Gen Intel / RTX 40", "cpu": "Intel Core i9-14900HX", "ram": "64GB DDR5", "storage": "4TB NVMe SSD", "display": "18\" 4K+ 120Hz Mini-LED", "price": 4999, "discount_pct": 8, "img": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop"},
        {"id": 205, "name": "Alienware m18 R2", "brand": "Dell", "category": "Gaming", "gen": "14th Gen Intel / RTX 40", "cpu": "Intel Core i9-14900HX", "ram": "32GB DDR5", "storage": "2TB NVMe SSD", "display": "18\" QHD+ 480Hz", "price": 2799, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 206, "name": "Acer Predator Helios 16", "brand": "Acer", "category": "Gaming", "gen": "13th Gen Intel / RTX 40", "cpu": "Intel Core i7-13700HX", "ram": "16GB DDR5", "storage": "1TB SSD", "display": "16\" WQXGA 240Hz", "price": 1699, "discount_pct": 22, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 207, "name": "HP OMEN 16", "brand": "HP", "category": "Gaming", "gen": "AMD Ryzen 7000 / RTX 40", "cpu": "AMD Ryzen 7 7840HS", "ram": "16GB DDR5", "storage": "512GB SSD", "display": "16.1\" FHD 165Hz", "price": 1299, "discount_pct": 18, "img": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&auto=format&fit=crop"},
        {"id": 208, "name": "ASUS TUF Gaming A15", "brand": "ASUS", "category": "Gaming", "gen": "AMD Ryzen 7000 / RTX 40", "cpu": "AMD Ryzen 7 7735HS", "ram": "16GB DDR5", "storage": "1TB SSD", "display": "15.6\" FHD 144Hz", "price": 999, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 209, "name": "Gigabyte AORUS 17H", "brand": "Gigabyte", "category": "Gaming", "gen": "13th Gen Intel / RTX 40", "cpu": "Intel Core i7-13700H", "ram": "16GB DDR5", "storage": "1TB SSD", "display": "17.3\" FHD 360Hz", "price": 1899, "discount_pct": 25, "img": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=500&auto=format&fit=crop"},

        # --- CATEGORY 3: PROFESSIONAL WORKSTATION & CREATOR ---
        {"id": 301, "name": "Apple MacBook Pro 16 M3 Max", "brand": "Apple", "category": "Workstation", "gen": "Latest Gen (M3)", "cpu": "Apple M3 Max (16-Core)", "ram": "48GB Unified", "storage": "1TB SSD", "display": "16.2\" Liquid Retina XDR", "price": 3499, "discount_pct": 7, "img": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop"},
        {"id": 302, "name": "Dell Precision 7680", "brand": "Dell", "category": "Workstation", "gen": "13th Gen Intel / RTX Ada", "cpu": "Intel Core i9-13950HX", "ram": "64GB CAMM2 DDR5", "storage": "2TB NVMe SSD", "display": "16\" OLED UHD+ Touch", "price": 3899, "discount_pct": 14, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 303, "name": "Lenovo ThinkPad P1 Gen 6", "brand": "Lenovo", "category": "Workstation", "gen": "13th Gen Intel / RTX Ada", "cpu": "Intel Core i7-13800H", "ram": "32GB DDR5", "storage": "1TB Gen4 SSD", "display": "16\" WQUXGA OLED Touch", "price": 2799, "discount_pct": 20, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 304, "name": "HP ZBook Studio G10", "brand": "HP", "category": "Workstation", "gen": "13th Gen Intel", "cpu": "Intel Core i9-13900H", "ram": "32GB DDR5", "storage": "1TB SSD", "display": "16\" HP DreamColor 120Hz", "price": 2999, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 305, "name": "ASUS ProArt Studiobook 16", "brand": "ASUS", "category": "Workstation", "gen": "13th Gen Intel / RTX 40", "cpu": "Intel Core i9-13980HX", "ram": "64GB DDR5", "storage": "2TB SSD", "display": "16\" 3.2K 120Hz OLED Touch", "price": 2599, "discount_pct": 12, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 306, "name": "Apple MacBook Pro 14 M3 Pro", "brand": "Apple", "category": "Workstation", "gen": "Latest Gen (M3)", "cpu": "Apple M3 Pro (12-Core)", "ram": "18GB Unified", "storage": "512GB SSD", "display": "14.2\" Liquid Retina XDR", "price": 1999, "discount_pct": 8, "img": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop"},
        {"id": 307, "name": "MSI Creator Z17 HX Studio", "brand": "MSI", "category": "Workstation", "gen": "13th Gen Intel / RTX 40", "cpu": "Intel Core i9-13950HX", "ram": "32GB DDR5", "storage": "2TB SSD", "display": "17\" QHD+ 165Hz Touch", "price": 2899, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop"},
        {"id": 308, "name": "Dell XPS 16 9640 Creator", "brand": "Dell", "category": "Workstation", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 9 185H", "ram": "32GB LPDDR5x", "storage": "1TB SSD", "display": "16.3\" 4K+ OLED Touch", "price": 2699, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},

        # --- CATEGORY 4: BUSINESS & ENTERPRISE ---
        {"id": 401, "name": "Lenovo ThinkPad X1 Carbon Gen 12", "brand": "Lenovo", "category": "Business", "gen": "14th Gen / Intel Core Ultra", "cpu": "Intel Core Ultra 7 165U", "ram": "32GB LPDDR5x", "storage": "1TB Gen4 SSD", "display": "14\" 2.8K OLED 120Hz", "price": 1849, "discount_pct": 20, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 402, "name": "HP EliteBook 840 G10", "brand": "HP", "category": "Business", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1360P", "ram": "16GB DDR5", "storage": "512GB SSD", "display": "14\" WUXGA IPS SureView", "price": 1399, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 403, "name": "Dell Latitude 7440", "brand": "Dell", "category": "Business", "gen": "13th Gen Intel", "cpu": "Intel Core i5-1345U", "ram": "16GB LPDDR5", "storage": "512GB SSD", "display": "14\" FHD+ Anti-Glare", "price": 1249, "discount_pct": 18, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 404, "name": "Lenovo ThinkPad T14s Gen 4", "brand": "Lenovo", "category": "Business", "gen": "AMD Ryzen 7000", "cpu": "AMD Ryzen 7 PRO 7840U", "ram": "32GB LPDDR5x", "storage": "1TB SSD", "display": "14\" Low Power WUXGA", "price": 1429, "discount_pct": 25, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 405, "name": "ASUS ExpertBook B9 OLED", "brand": "ASUS", "category": "Business", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1355U", "ram": "32GB LPDDR5", "storage": "1TB SSD", "display": "14\" 2.8K OLED 90Hz", "price": 1699, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 406, "name": "HP ProBook 450 G10", "brand": "HP", "category": "Business", "gen": "13th Gen Intel", "cpu": "Intel Core i5-1335U", "ram": "8GB DDR4", "storage": "512GB SSD", "display": "15.6\" FHD IPS", "price": 749, "discount_pct": 12, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 407, "name": "Dell Latitude 5540", "brand": "Dell", "category": "Business", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1355U", "ram": "16GB DDR5", "storage": "512GB SSD", "display": "15.6\" FHD IPS", "price": 1099, "discount_pct": 14, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 408, "name": "Fujitsu LifeBook U9311", "brand": "Fujitsu", "category": "Business", "gen": "11th Gen Intel", "cpu": "Intel Core i7-1165G7", "ram": "16GB LPDDR4x", "storage": "512GB SSD", "display": "13.3\" FHD Anti-Glare", "price": 999, "discount_pct": 30, "img": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop"},

        # --- CATEGORY 5: 2-IN-1 CONVERTIBLES & CONVERTIBLE TOUCH ---
        {"id": 501, "name": "Lenovo Yoga Book 9i Dual-Screen", "brand": "Lenovo", "category": "2-in-1 Touch", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1355U", "ram": "16GB LPDDR5x", "storage": "1TB SSD", "display": "Dual 13.3\" 2.8K OLED Touch", "price": 1999, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 502, "name": "Microsoft Surface Pro 9", "brand": "Microsoft", "category": "2-in-1 Touch", "gen": "12th Gen Intel", "cpu": "Intel Core i7-1255U", "ram": "16GB LPDDR5", "storage": "256GB SSD", "display": "13\" PixelSense 120Hz Touch", "price": 1099, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=500&auto=format&fit=crop"},
        {"id": 503, "name": "HP Envy x360 15", "brand": "HP", "category": "2-in-1 Touch", "gen": "AMD Ryzen 7000", "cpu": "AMD Ryzen 7 7730U", "ram": "16GB LPDDR4x", "storage": "1TB SSD", "display": "15.6\" FHD OLED Touch", "price": 849, "discount_pct": 18, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 504, "name": "Dell Inspiron 14 2-in-1", "brand": "Dell", "category": "2-in-1 Touch", "gen": "13th Gen Intel", "cpu": "Intel Core i5-1335U", "ram": "8GB LPDDR5", "storage": "512GB SSD", "display": "14\" FHD+ Touch", "price": 649, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 505, "name": "ASUS ROG Flow X16 2-in-1", "brand": "ASUS", "category": "2-in-1 Touch", "gen": "13th Gen Intel / RTX 40", "cpu": "Intel Core i9-13900H", "ram": "32GB DDR5", "storage": "1TB SSD", "display": "16\" Mini-LED QHD+ 240Hz Touch", "price": 2199, "discount_pct": 20, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 506, "name": "Lenovo IdeaPad Flex 5", "brand": "Lenovo", "category": "2-in-1 Touch", "gen": "AMD Ryzen 7000", "cpu": "AMD Ryzen 5 7530U", "ram": "16GB LPDDR4x", "storage": "512GB SSD", "display": "14\" WUXGA Touch", "price": 599, "discount_pct": 12, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 507, "name": "Samsung Galaxy Book3 Pro 360", "brand": "Samsung", "category": "2-in-1 Touch", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1360P", "ram": "16GB LPDDR5", "storage": "1TB SSD", "display": "16\" 3K AMOLED Touch", "price": 1499, "discount_pct": 22, "img": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=500&auto=format&fit=crop"},

        # --- CATEGORY 6: EVERYDAY VALUE & BUDGET COMPUTING ---
        {"id": 601, "name": "Acer Aspire 5 A515", "brand": "Acer", "category": "Budget", "gen": "13th Gen Intel", "cpu": "Intel Core i5-1335U", "ram": "8GB DDR4", "storage": "512GB SSD", "display": "15.6\" FHD IPS", "price": 499, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=500&auto=format&fit=crop"},
        {"id": 602, "name": "ASUS Vivobook 15", "brand": "ASUS", "category": "Budget", "gen": "12th Gen Intel", "cpu": "Intel Core i3-1215U", "ram": "8GB DDR4", "storage": "256GB SSD", "display": "15.6\" FHD Anti-Glare", "price": 379, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 603, "name": "HP Laptop 15t", "brand": "HP", "category": "Budget", "gen": "13th Gen Intel", "cpu": "Intel Core i7-1355U", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "15.6\" FHD IPS", "price": 549, "discount_pct": 25, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 604, "name": "Lenovo IdeaPad Slim 3", "brand": "Lenovo", "category": "Budget", "gen": "AMD Ryzen 7000", "cpu": "AMD Ryzen 3 7320U", "ram": "8GB LPDDR5", "storage": "256GB SSD", "display": "15.6\" FHD TN", "price": 329, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"},
        {"id": 605, "name": "Dell Inspiron 15 3530", "brand": "Dell", "category": "Budget", "gen": "13th Gen Intel", "cpu": "Intel Core i5-1335U", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "15.6\" FHD 120Hz", "price": 529, "discount_pct": 18, "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop"},
        {"id": 606, "name": "Acer Chromebook Plus 515", "brand": "Acer", "category": "Budget", "gen": "12th Gen Intel", "cpu": "Intel Core i3-1215U", "ram": "8GB LPDDR5", "storage": "128GB UFS", "display": "15.6\" FHD IPS", "price": 299, "discount_pct": 20, "img": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=500&auto=format&fit=crop"},
        {"id": 607, "name": "ASUS Chromebook CX34", "brand": "ASUS", "category": "Budget", "gen": "12th Gen Intel", "cpu": "Intel Core i3-1215U", "ram": "8GB LPDDR5", "storage": "128GB Storage", "display": "14\" FHD Touch", "price": 349, "discount_pct": 14, "img": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500&auto=format&fit=crop"},
        {"id": 608, "name": "HP Pavilion 15", "brand": "HP", "category": "Budget", "gen": "AMD Ryzen 7000", "cpu": "AMD Ryzen 5 7530U", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "15.6\" FHD IPS Micro-edge", "price": 599, "discount_pct": 15, "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop"},
        {"id": 609, "name": "MSI Modern 14", "brand": "MSI", "category": "Budget", "gen": "13th Gen Intel", "cpu": "Intel Core i5-1335U", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "14\" FHD IPS-Level", "price": 479, "discount_pct": 12, "img": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop"},
        {"id": 610, "name": "Lenovo V15 Gen 4", "brand": "Lenovo", "category": "Budget", "gen": "AMD Ryzen 7000", "cpu": "AMD Ryzen 5 7520U", "ram": "8GB LPDDR5", "storage": "256GB SSD", "display": "15.6\" FHD TN", "price": 389, "discount_pct": 10, "img": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop"}
    ]
    return pd.DataFrame(laptops)

df_catalog = load_laptop_catalog()

# Calculate Discounted Prices
df_catalog['discounted_price'] = (df_catalog['price'] * (1 - df_catalog['discount_pct'] / 100)).round(2)

# ==============================================================================
# HEADER & NAVIGATION BAR
# ==============================================================================
st.markdown("""
<div class="brand-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="brand-title">NEXUS TECH</h1>
            <div class="brand-subtitle">ENTERPRISE & CONSUMER COMPUTING STORE</div>
        </div>
        <div style="text-align: right; color: #cbd5e1; font-size: 0.9rem;">
            🟢 LIVE CATALOG | ⚡ 50+ MODELS IN STOCK<br>
            📍 <i>Flagship Center: Tech Quarter, San Francisco, CA</i>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Bar Navigation Tabs
tab_store, tab_cart, tab_checkout, tab_about = st.tabs([
    "💻 Storefront & Products", 
    f"🛒 Shopping Cart ({len(st.session_state.cart)})", 
    "💳 Checkout & Order Summary", 
    "🏢 About & Location"
])

# ==============================================================================
# TAB 1: STOREFRONT & PRODUCTS
# ==============================================================================
with tab_store:
    st.markdown("""
    <div class="promo-banner">
        <strong>🔥 SEASONAL HARDWARE CLEARANCE:</strong> Up to 30% instant market discount applied on select 13th/14th Gen & Apple M3 Series Laptops. Free global express shipping on orders over $1,000.
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("🔍 Catalog Filters")
    
    search_query = st.sidebar.text_input("Search Model / CPU / Spec:", placeholder="e.g. M3, RTX 40, i9, OLED")

    all_categories = ["All Categories"] + list(df_catalog['category'].unique())
    selected_category = st.sidebar.selectbox("Category:", all_categories)

    all_generations = ["All Generations"] + list(df_catalog['gen'].unique())
    selected_gen = st.sidebar.selectbox("Processor Generation:", all_generations)

    all_brands = ["All Brands"] + list(df_catalog['brand'].unique())
    selected_brand = st.sidebar.selectbox("Manufacturer / Brand:", all_brands)

    min_price, max_price = int(df_catalog['discounted_price'].min()), int(df_catalog['discounted_price'].max())
    price_range = st.sidebar.slider("Discounted Price Range ($):", min_price, max_price, (min_price, max_price))

    filtered_df = df_catalog.copy()

    if search_query:
        query_lower = search_query.lower()
        filtered_df = filtered_df[
            filtered_df['name'].str.lower().str.contains(query_lower) |
            filtered_df['cpu'].str.lower().str.contains(query_lower) |
            filtered_df['category'].str.lower().str.contains(query_lower)
        ]
    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_gen != "All Generations":
        filtered_df = filtered_df[filtered_df['gen'] == selected_gen]
    if selected_brand != "All Brands":
        filtered_df = filtered_df[filtered_df['brand'] == selected_brand]
    
    filtered_df = filtered_df[
        (filtered_df['discounted_price'] >= price_range[0]) & 
        (filtered_df['discounted_price'] <= price_range[1])
    ]

    st.write(f"Showing **{len(filtered_df)}** of **{len(df_catalog)}** available laptop models matching your criteria.")
    st.markdown("---")

    cols_per_row = 3
    rows = [filtered_df.iloc[i:i+cols_per_row] for i in range(0, len(filtered_df), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, (_, item) in enumerate(row.iterrows()):
            with cols[idx]:
                st.markdown(f"""
                <div class="product-card">
                    <div>
                        <span class="badge-discount">{item['discount_pct']}% OFF</span>
                        <span class="badge-gen">{item['gen']}</span>
                        <img src="{item['img']}" style="width:100%; height:180px; object-fit:cover; border-radius:6px; margin: 8px 0;">
                        <h4 style="margin: 5px 0; color: #f8fafc; font-size: 1.1rem;">{item['name']}</h4>
                        <p class="specs-text">
                            ⚙️ <b>CPU:</b> {item['cpu']}<br>
                            🧠 <b>RAM:</b> {item['ram']} | 💾 <b>Storage:</b> {item['storage']}<br>
                            🖥️ <b>Screen:</b> {item['display']}
                        </p>
                    </div>
                    <div>
                        <div style="margin: 10px 0;">
                            <span class="price-original">${item['price']:,.2f}</span>
                            <span class="price-discounted">${item['discounted_price']:,.2f}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🛒 Add to Cart", key=f"add_{item['id']}"):
                    st.session_state.cart.append(item.to_dict())
                    st.toast(f"Added {item['name']} to cart!", icon="✅")
                    st.rerun()

# ==============================================================================
# TAB 2: SHOPPING CART MANAGEMENT
# ==============================================================================
with tab_cart:
    st.header("🛒 Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your shopping cart is currently empty. Browse the Storefront tab to select high-performance laptops.")
    else:
        cart_df = pd.DataFrame(st.session_state.cart)
        
        st.dataframe(
            cart_df[['name', 'category', 'gen', 'price', 'discount_pct', 'discounted_price']],
            column_config={
                "name": "Model Name",
                "category": "Category",
                "gen": "Generation",
                "price": st.column_config.NumberColumn("MSRP ($)", format="$%.2f"),
                "discount_pct": st.column_config.NumberColumn("Discount (%)", format="%d%%"),
                "discounted_price": st.column_config.NumberColumn("Final Price ($)", format="$%.2f")
            },
            hide_index=True,
            use_container_width=True
        )

        subtotal = cart_df['discounted_price'].sum()
        total_savings = (cart_df['price'].sum() - subtotal)

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🗑️ Clear Entire Cart"):
                st.session_state.cart = []
                st.rerun()
        with col2:
            st.markdown(f"### Subtotal: **${subtotal:,.2f}**")
            st.markdown(f"<span style='color:#10b981;'>Total Market Savings: ${total_savings:,.2f}</span>", unsafe_allow_html=True)

# ==============================================================================
# TAB 3: CHECKOUT & DEMO ORDER WORKFLOW
# ==============================================================================
with tab_checkout:
    st.header("💳 Demo Order Checkout")

    if not st.session_state.cart:
        st.warning("Please add items to your cart before proceeding with checkout.")
    else:
        st.markdown("> **Note:** This is a live demonstration order processing workflow. Orders will generate downloadable receipts and save session state records.")

        cart_df = pd.DataFrame(st.session_state.cart)
        subtotal = cart_df['discounted_price'].sum()
        tax = subtotal * 0.08
        grand_total = subtotal + tax

        st.subheader("Order Items Summary")
        for idx, item in cart_df.iterrows():
            st.text(f"• {item['name']} — ${item['discounted_price']:,.2f}")
        
        st.markdown(f"**Subtotal:** ${subtotal:,.2f} | **Tax (8%):** ${tax:,.2f} | **Grand Total:** `${grand_total:,.2f}`")
        st.markdown("---")

        st.subheader("Customer & Delivery Details")
        with st.form("checkout_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                cust_name = st.text_input("Full Name *", value="Alex Morgan")
                cust_email = st.text_input("Email Address *", value="alex.morgan@example.com")
            with col_b:
                cust_phone = st.text_input("Phone Number *", value="+1 (555) 019-2834")
                cust_address = st.text_area("Delivery Address *", value="Market Street, Suite 400, San Francisco, CA 94103")

            payment_method = st.selectbox("Payment Gateway (Demo Integration)", ["Credit Card (Visa/Mastercard)", "Corporate Purchase Order", "PayPal Express"])

            submit_order = st.form_submit_button("🚀 Place Demo Order & Generate Receipt")

            if submit_order:
                if not cust_name or not cust_email or not cust_address:
                    st.error("Please fill in all required customer details.")
                else:
                    order_ref = f"NEXUS-ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    order_data = {
                        "order_ref": order_ref,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "customer_name": cust_name,
                        "email": cust_email,
                        "address": cust_address,
                        "total_amount": grand_total,
                        "items_count": len(st.session_state.cart),
                        "items": cart_df['name'].tolist()
                    }
                    st.session_state.orders.append(order_data)

                    st.success(f"🎉 Order Successfully Placed! Reference ID: **{order_ref}**")
                    
                    receipt_json = json.dumps(order_data, indent=4)
                    st.download_button(
                        label="📥 Download Order Receipt (JSON)",
                        data=receipt_json,
                        file_name=f"{order_ref}_Receipt.json",
                        mime="application/json"
                    )
                    
                    st.session_state.cart = []

# ==============================================================================
# TAB 4: ABOUT BUSINESS & PHYSICAL LOCATION
# ==============================================================================
with tab_about:
    st.header("🏢 About NEXUS TECH")
    
    col_x, col_y = st.columns([1, 1])
    with col_x:
        st.markdown("""
        **NEXUS TECH** is a leading global supplier of high-performance laptop systems, enterprise workstations, ultrabooks, and gaming hardware.
        
        ### Business Address & Contact Info
        - 🏢 **Flagship Store & HQ:** 500 Technology Way, San Francisco, CA 94105
        - 📞 **Corporate Hotline:** +1 (800) 555-NEXUS
        - ✉️ **Enterprise Inquiries:** sales@nexustech-computing.com
        - ⏰ **Operating Hours:** Mon – Sat: 9:00 AM – 8:00 PM PST
        """)
    
    with col_y:
        st.markdown("### 📍 Location Map (San Francisco Tech District)")
        map_df = pd.DataFrame({
            'lat': [37.7886],
            'lon': [-122.3970]
        })
        st.map(map_df, zoom=13)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>© 2026 NEXUS TECH Computing Inc. All rights reserved. | Production Demonstration Platform</div>", unsafe_allow_html=True)