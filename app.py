from flask import Flask, render_template_string, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'travel-secret-key-2024'

destinations = [
    {
        "id": 1,
        "name": "Tokyo",
        "country": "Japan",
        "continent": "Asia",
        "image": "https://picsum.photos/600/400?random=10",
        "flag": "🇯🇵",
        "price": 1200,
        "duration": "7-10 days",
        "best_season": "March - May",
        "rating": 4.9,
        "tags": ["Culture", "Food", "Technology"],
        "description": "A city where ancient temples meet neon-lit skyscrapers. Experience sushi, cherry blossoms, and Shibuya's iconic crossing.",
        "highlights": ["Mount Fuji", "Shibuya Crossing", "Senso-ji Temple", "Akihabara"]
    },
    {
        "id": 2,
        "name": "Paris",
        "country": "France",
        "continent": "Europe",
        "image": "https://picsum.photos/600/400?random=20",
        "flag": "🇫🇷",
        "price": 1500,
        "duration": "5-7 days",
        "best_season": "Apr - Jun, Sep - Oct",
        "rating": 4.8,
        "tags": ["Romance", "Art", "Food"],
        "description": "The city of light, love, and world-class cuisine. Stroll along the Seine and marvel at the Eiffel Tower.",
        "highlights": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Montmartre"]
    },
    {
        "id": 3,
        "name": "New York",
        "country": "USA",
        "continent": "Americas",
        "image": "https://picsum.photos/600/400?random=30",
        "flag": "🇺🇸",
        "price": 1100,
        "duration": "5-8 days",
        "best_season": "Sep - Nov",
        "rating": 4.7,
        "tags": ["Urban", "Culture", "Shopping"],
        "description": "The city that never sleeps. From Central Park to Times Square, NYC pulses with energy 24/7.",
        "highlights": ["Times Square", "Central Park", "Statue of Liberty", "Brooklyn Bridge"]
    },
    {
        "id": 4,
        "name": "Santorini",
        "country": "Greece",
        "continent": "Europe",
        "image": "https://picsum.photos/600/400?random=40",
        "flag": "🇬🇷",
        "price": 1800,
        "duration": "5-7 days",
        "best_season": "Jun - Sep",
        "rating": 4.9,
        "tags": ["Beach", "Romance", "Views"],
        "description": "White-washed buildings, volcanic caldera views, and legendary sunsets make Santorini utterly magical.",
        "highlights": ["Oia Sunset", "Caldera View", "Red Beach", "Akrotiri Ruins"]
    },
    {
        "id": 5,
        "name": "Bali",
        "country": "Indonesia",
        "continent": "Asia",
        "image": "https://picsum.photos/600/400?random=50",
        "flag": "🇮🇩",
        "price": 800,
        "duration": "8-12 days",
        "best_season": "May - Sep",
        "rating": 4.8,
        "tags": ["Nature", "Culture", "Wellness"],
        "description": "Island of the Gods. Lush rice terraces, spiritual temples, surf-ready beaches, and incredible food.",
        "highlights": ["Ubud Rice Terraces", "Tanah Lot", "Seminyak Beach", "Mount Batur"]
    },
    {
        "id": 6,
        "name": "Cape Town",
        "country": "South Africa",
        "continent": "Africa",
        "image": "https://picsum.photos/600/400?random=60",
        "flag": "🇿🇦",
        "price": 950,
        "duration": "7-10 days",
        "best_season": "Nov - Mar",
        "rating": 4.7,
        "tags": ["Nature", "Adventure", "Wildlife"],
        "description": "Where mountains meet the ocean. Table Mountain, Cape Point, and world-class wine await.",
        "highlights": ["Table Mountain", "Cape of Good Hope", "Robben Island", "Boulders Beach"]
    },
    {
        "id": 7,
        "name": "Dubai",
        "country": "UAE",
        "continent": "Asia",
        "image": "https://picsum.photos/600/400?random=70",
        "flag": "🇦🇪",
        "price": 1600,
        "duration": "4-6 days",
        "best_season": "Nov - Mar",
        "rating": 4.6,
        "tags": ["Luxury", "Shopping", "Modern"],
        "description": "A futuristic city rising from the desert. Record-breaking skyscrapers, indoor skiing, and gold souks.",
        "highlights": ["Burj Khalifa", "Palm Jumeirah", "Desert Safari", "Dubai Mall"]
    },
    {
        "id": 8,
        "name": "Machu Picchu",
        "country": "Peru",
        "continent": "Americas",
        "image": "https://picsum.photos/600/400?random=80",
        "flag": "🇵🇪",
        "price": 1300,
        "duration": "6-9 days",
        "best_season": "May - Oct",
        "rating": 4.9,
        "tags": ["History", "Adventure", "Nature"],
        "description": "The Lost City of the Incas perched high in the Andes. One of humanity's most breathtaking achievements.",
        "highlights": ["Inca Trail", "Sun Gate", "Aguas Calientes", "Sacred Valley"]
    },
    {
        "id": 9,
        "name": "Kyoto",
        "country": "Japan",
        "continent": "Asia",
        "image": "https://picsum.photos/600/400?random=90",
        "flag": "🇯🇵",
        "price": 1100,
        "duration": "4-6 days",
        "best_season": "Mar - May, Oct - Nov",
        "rating": 4.9,
        "tags": ["Culture", "History", "Nature"],
        "description": "Japan's ancient capital, home to thousands of shrines, geisha districts, and bamboo forests.",
        "highlights": ["Fushimi Inari", "Arashiyama Bamboo", "Gion District", "Kinkaku-ji"]
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WanderWorld — International Travel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --sand: #f5f0e8;
            --ink: #1a1410;
            --terra: #c8622a;
            --terra-light: #e8845a;
            --gold: #d4a843;
            --mist: #e8e2d9;
            --deep: #2d2420;
            --white: #fdfaf5;
        }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'DM Sans', sans-serif;
            background: var(--white);
            color: var(--ink);
            overflow-x: hidden;
        }

        /* NAV */
        nav {
            position: fixed; top: 0; width: 100%; z-index: 100;
            padding: 1.2rem 3rem;
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(253,250,245,0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(200,98,42,0.12);
            transition: box-shadow 0.3s;
        }
        nav.scrolled { box-shadow: 0 4px 30px rgba(26,20,16,0.08); }

        .nav-logo {
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem;
            color: var(--terra);
            letter-spacing: -0.5px;
            text-decoration: none;
        }
        .nav-logo span { color: var(--ink); }

        .nav-links { display: flex; gap: 2rem; list-style: none; }
        .nav-links a {
            text-decoration: none; color: var(--ink); font-size: 0.9rem;
            font-weight: 500; letter-spacing: 0.3px;
            position: relative; padding-bottom: 2px;
        }
        .nav-links a::after {
            content: ''; position: absolute; bottom: 0; left: 0;
            width: 0; height: 1.5px; background: var(--terra);
            transition: width 0.3s;
        }
        .nav-links a:hover::after { width: 100%; }

        .nav-right { display: flex; align-items: center; gap: 1rem; }

        .wishlist-btn {
            background: none; border: 1.5px solid var(--terra);
            color: var(--terra); padding: 0.5rem 1.2rem;
            border-radius: 2rem; cursor: pointer;
            font-size: 0.85rem; font-weight: 500;
            display: flex; align-items: center; gap: 0.4rem;
            transition: all 0.2s;
            font-family: 'DM Sans', sans-serif;
        }
        .wishlist-btn:hover { background: var(--terra); color: white; }
        .wishlist-count {
            background: var(--terra); color: white;
            border-radius: 50%; width: 18px; height: 18px;
            font-size: 11px; display: flex; align-items: center; justify-content: center;
        }

        /* HERO */
        .hero {
            min-height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: var(--ink);
            position: relative; overflow: hidden;
            padding: 6rem 2rem 4rem;
        }

        .hero-bg {
            position: absolute; inset: 0;
            background: url('https://picsum.photos/1600/900?random=99') center/cover no-repeat;
            opacity: 0.3;
            filter: saturate(0.6);
        }

        .hero-overlay {
            position: absolute; inset: 0;
            background: linear-gradient(160deg, rgba(26,20,16,0.7) 0%, rgba(200,98,42,0.2) 100%);
        }

        .hero-content { position: relative; z-index: 2; text-align: center; max-width: 800px; }

        .hero-eyebrow {
            font-size: 0.75rem; letter-spacing: 4px; text-transform: uppercase;
            color: var(--gold); margin-bottom: 1.5rem; font-weight: 500;
        }

        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(3rem, 8vw, 6rem);
            color: var(--white); line-height: 1.05;
            margin-bottom: 1.5rem;
        }

        .hero-title em { color: var(--terra-light); font-style: italic; }

        .hero-sub {
            color: rgba(253,250,245,0.7); font-size: 1.1rem;
            max-width: 500px; margin: 0 auto 2.5rem;
            font-weight: 300; line-height: 1.7;
        }

        .hero-cta {
            display: inline-flex; align-items: center; gap: 0.6rem;
            background: var(--terra); color: white;
            padding: 1rem 2.4rem; border-radius: 3rem;
            text-decoration: none; font-weight: 500;
            font-size: 1rem; transition: all 0.3s;
            border: none; cursor: pointer; font-family: 'DM Sans', sans-serif;
        }
        .hero-cta:hover { background: var(--terra-light); transform: translateY(-2px); box-shadow: 0 12px 30px rgba(200,98,42,0.35); }

        /* STATS BAR */
        .stats-bar {
            background: var(--terra);
            padding: 1.5rem 3rem;
            display: flex; justify-content: center; gap: 5rem;
        }
        .stat { text-align: center; color: white; }
        .stat-num { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; }
        .stat-label { font-size: 0.78rem; letter-spacing: 1.5px; text-transform: uppercase; opacity: 0.85; }

        /* SEARCH */
        .search-section {
            padding: 4rem 3rem;
            background: var(--sand);
        }
        .search-wrap { max-width: 900px; margin: 0 auto; }
        .search-label {
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem; margin-bottom: 1.5rem; text-align: center;
        }
        .search-bar {
            display: flex; gap: 1rem;
            background: white; border-radius: 1rem;
            padding: 0.6rem; box-shadow: 0 4px 20px rgba(26,20,16,0.08);
        }
        .search-bar input {
            flex: 1; border: none; outline: none;
            padding: 0.8rem 1rem; font-size: 0.95rem;
            font-family: 'DM Sans', sans-serif; background: transparent;
            color: var(--ink);
        }
        .search-bar select {
            border: none; outline: none; background: var(--sand);
            border-radius: 0.6rem; padding: 0.6rem 1rem;
            font-family: 'DM Sans', sans-serif; color: var(--ink);
            font-size: 0.9rem; cursor: pointer;
        }
        .search-bar button {
            background: var(--terra); color: white;
            border: none; border-radius: 0.7rem;
            padding: 0.8rem 1.8rem; cursor: pointer;
            font-size: 0.9rem; font-weight: 500;
            font-family: 'DM Sans', sans-serif;
            display: flex; align-items: center; gap: 0.5rem;
            transition: background 0.2s;
        }
        .search-bar button:hover { background: var(--terra-light); }

        /* FILTERS */
        .filters {
            display: flex; gap: 0.7rem; flex-wrap: wrap;
            justify-content: center; margin-top: 1.5rem;
        }
        .filter-btn {
            padding: 0.45rem 1.2rem; border-radius: 2rem;
            border: 1.5px solid var(--mist); background: white;
            color: var(--ink); font-size: 0.85rem; cursor: pointer;
            font-family: 'DM Sans', sans-serif; font-weight: 500;
            transition: all 0.2s;
        }
        .filter-btn:hover, .filter-btn.active {
            background: var(--terra); color: white; border-color: var(--terra);
        }

        /* DESTINATIONS */
        .destinations-section {
            padding: 5rem 3rem;
            max-width: 1300px; margin: 0 auto;
        }
        .section-header {
            display: flex; align-items: flex-end; justify-content: space-between;
            margin-bottom: 3rem;
        }
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.4rem; line-height: 1.2;
        }
        .section-title span { color: var(--terra); }
        .section-count { color: var(--terra); font-size: 0.9rem; font-weight: 500; }

        .dest-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 2rem;
        }

        .dest-card {
            background: white; border-radius: 1.2rem;
            overflow: hidden; box-shadow: 0 2px 12px rgba(26,20,16,0.06);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
            border: 1px solid var(--mist);
        }
        .dest-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 16px 40px rgba(26,20,16,0.12);
        }

        .card-img {
            position: relative; height: 220px; overflow: hidden;
        }
        .card-img img {
            width: 100%; height: 100%; object-fit: cover;
            transition: transform 0.5s;
        }
        .dest-card:hover .card-img img { transform: scale(1.06); }

        .card-badge {
            position: absolute; top: 1rem; left: 1rem;
            background: rgba(26,20,16,0.75); color: white;
            border-radius: 2rem; padding: 0.3rem 0.8rem;
            font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase;
            backdrop-filter: blur(6px);
        }

        .card-wish {
            position: absolute; top: 1rem; right: 1rem;
            background: rgba(253,250,245,0.9); border: none;
            width: 36px; height: 36px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: all 0.2s;
            color: var(--ink);
        }
        .card-wish:hover, .card-wish.active { background: var(--terra); color: white; }

        .card-price {
            position: absolute; bottom: 1rem; right: 1rem;
            background: var(--terra); color: white;
            border-radius: 0.5rem; padding: 0.3rem 0.7rem;
            font-size: 0.85rem; font-weight: 600;
        }

        .card-body { padding: 1.4rem; }

        .card-location {
            font-size: 0.8rem; color: var(--terra);
            letter-spacing: 1px; text-transform: uppercase;
            margin-bottom: 0.4rem; font-weight: 500;
        }

        .card-name {
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem; margin-bottom: 0.6rem; color: var(--ink);
        }

        .card-desc {
            font-size: 0.88rem; color: #5a5048;
            line-height: 1.6; margin-bottom: 1rem;
            display: -webkit-box; -webkit-line-clamp: 2;
            -webkit-box-orient: vertical; overflow: hidden;
        }

        .card-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1rem; }
        .tag {
            background: var(--sand); color: var(--deep);
            border-radius: 2rem; padding: 0.2rem 0.7rem;
            font-size: 0.75rem; font-weight: 500;
        }

        .card-meta {
            display: flex; gap: 1.2rem; font-size: 0.82rem;
            color: #7a6e65; padding-top: 1rem;
            border-top: 1px solid var(--mist);
        }
        .card-meta span { display: flex; align-items: center; gap: 0.3rem; }
        .card-meta i { color: var(--terra); }

        .card-footer {
            display: flex; justify-content: space-between; align-items: center;
            padding: 1rem 1.4rem;
            border-top: 1px solid var(--mist);
            background: var(--sand);
        }

        .rating { display: flex; align-items: center; gap: 0.3rem; font-size: 0.9rem; font-weight: 600; }
        .stars { color: var(--gold); font-size: 0.8rem; }

        .view-btn {
            background: var(--ink); color: white;
            border: none; border-radius: 2rem;
            padding: 0.5rem 1.3rem; font-size: 0.85rem;
            cursor: pointer; font-family: 'DM Sans', sans-serif;
            font-weight: 500; transition: background 0.2s;
        }
        .view-btn:hover { background: var(--terra); }

        /* MODAL */
        .modal-overlay {
            position: fixed; inset: 0; background: rgba(26,20,16,0.7);
            z-index: 200; display: none; align-items: center; justify-content: center;
            padding: 2rem;
        }
        .modal-overlay.open { display: flex; }

        .modal {
            background: var(--white); border-radius: 1.5rem;
            max-width: 750px; width: 100%; max-height: 90vh;
            overflow-y: auto;
            animation: modalIn 0.3s ease;
        }
        @keyframes modalIn {
            from { opacity: 0; transform: scale(0.95) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        .modal-img { width: 100%; height: 300px; object-fit: cover; border-radius: 1.5rem 1.5rem 0 0; }

        .modal-body { padding: 2rem; }

        .modal-flag { font-size: 2.5rem; margin-bottom: 0.5rem; }

        .modal-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem; margin-bottom: 0.3rem;
        }

        .modal-country { color: var(--terra); font-size: 1rem; margin-bottom: 1.2rem; font-weight: 500; }

        .modal-desc { font-size: 0.95rem; line-height: 1.8; color: #4a4038; margin-bottom: 1.5rem; }

        .modal-info {
            display: grid; grid-template-columns: repeat(3, 1fr);
            gap: 1rem; margin-bottom: 1.5rem;
        }
        .info-box {
            background: var(--sand); border-radius: 0.8rem;
            padding: 1rem; text-align: center;
        }
        .info-box i { color: var(--terra); font-size: 1.2rem; margin-bottom: 0.4rem; }
        .info-box .label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #7a6e65; }
        .info-box .value { font-weight: 600; font-size: 0.95rem; margin-top: 0.2rem; }

        .modal-highlights h4 {
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem; margin-bottom: 0.8rem;
        }
        .highlights-list { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; }
        .highlight-chip {
            background: var(--deep); color: white;
            border-radius: 2rem; padding: 0.35rem 0.9rem;
            font-size: 0.82rem;
        }

        .modal-actions { display: flex; gap: 1rem; }
        .btn-primary {
            flex: 1; background: var(--terra); color: white;
            border: none; border-radius: 2rem; padding: 1rem;
            font-size: 1rem; font-weight: 600; cursor: pointer;
            font-family: 'DM Sans', sans-serif; transition: background 0.2s;
        }
        .btn-primary:hover { background: var(--terra-light); }
        .btn-secondary {
            background: var(--sand); color: var(--ink);
            border: none; border-radius: 2rem; padding: 1rem 1.8rem;
            font-size: 1rem; cursor: pointer;
            font-family: 'DM Sans', sans-serif; transition: background 0.2s;
        }
        .btn-secondary:hover { background: var(--mist); }

        .modal-close {
            position: absolute; top: 1rem; right: 1rem;
            background: white; border: none; border-radius: 50%;
            width: 40px; height: 40px; cursor: pointer;
            font-size: 1.2rem; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .modal-wrap { position: relative; }

        /* WISHLIST PANEL */
        .wishlist-panel {
            position: fixed; right: 0; top: 0; height: 100vh; width: 380px;
            background: var(--white); z-index: 150;
            box-shadow: -4px 0 30px rgba(26,20,16,0.12);
            transform: translateX(100%); transition: transform 0.3s ease;
        }
        .wishlist-panel.open { transform: translateX(0); }

        .panel-header {
            padding: 2rem; border-bottom: 1px solid var(--mist);
            display: flex; justify-content: space-between; align-items: center;
        }
        .panel-title { font-family: 'Playfair Display', serif; font-size: 1.5rem; }
        .panel-close {
            background: none; border: 1.5px solid var(--mist);
            border-radius: 50%; width: 36px; height: 36px;
            cursor: pointer; font-size: 1rem;
            display: flex; align-items: center; justify-content: center;
        }

        .panel-body { padding: 1.5rem; overflow-y: auto; height: calc(100vh - 80px); }

        .wish-item {
            display: flex; gap: 1rem; padding: 1rem;
            border-radius: 0.8rem; background: var(--sand);
            margin-bottom: 1rem; align-items: center;
        }
        .wish-img { width: 60px; height: 60px; border-radius: 0.5rem; object-fit: cover; }
        .wish-info { flex: 1; }
        .wish-name { font-weight: 600; font-size: 0.95rem; }
        .wish-country { font-size: 0.8rem; color: var(--terra); }
        .wish-price { font-size: 0.85rem; color: #5a5048; margin-top: 0.2rem; }
        .wish-remove {
            background: none; border: none; color: #aaa;
            cursor: pointer; font-size: 1rem; transition: color 0.2s;
        }
        .wish-remove:hover { color: var(--terra); }

        .empty-wish {
            text-align: center; padding: 3rem 2rem; color: #9a8e85;
        }
        .empty-wish i { font-size: 3rem; color: var(--mist); margin-bottom: 1rem; display: block; }

        /* TOAST */
        .toast {
            position: fixed; bottom: 2rem; left: 50%;
            transform: translateX(-50%) translateY(20px);
            background: var(--deep); color: white;
            padding: 0.8rem 2rem; border-radius: 2rem;
            font-size: 0.9rem; opacity: 0;
            transition: all 0.3s; z-index: 300;
            pointer-events: none;
        }
        .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

        /* FOOTER */
        footer {
            background: var(--ink); color: rgba(253,250,245,0.7);
            padding: 4rem 3rem 2rem;
        }
        .footer-grid {
            max-width: 1200px; margin: 0 auto;
            display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 3rem; margin-bottom: 3rem;
        }
        .footer-brand .logo {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem; color: white; margin-bottom: 0.8rem;
        }
        .footer-brand p { font-size: 0.88rem; line-height: 1.7; max-width: 260px; }
        .footer-col h5 {
            color: white; font-size: 0.8rem; text-transform: uppercase;
            letter-spacing: 2px; margin-bottom: 1rem;
        }
        .footer-col ul { list-style: none; }
        .footer-col ul li { margin-bottom: 0.6rem; }
        .footer-col ul li a { color: rgba(253,250,245,0.6); text-decoration: none; font-size: 0.88rem; transition: color 0.2s; }
        .footer-col ul li a:hover { color: var(--terra-light); }
        .footer-bottom {
            max-width: 1200px; margin: 0 auto;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 1.5rem; text-align: center; font-size: 0.82rem;
        }

        /* NO RESULTS */
        .no-results {
            text-align: center; padding: 4rem; color: #9a8e85;
            display: none;
        }
        .no-results i { font-size: 3rem; color: var(--mist); margin-bottom: 1rem; display: block; }

        @media (max-width: 768px) {
            nav { padding: 1rem 1.5rem; }
            .nav-links { display: none; }
            .stats-bar { gap: 2rem; flex-wrap: wrap; }
            .search-section { padding: 2rem 1.5rem; }
            .search-bar { flex-direction: column; }
            .destinations-section { padding: 3rem 1.5rem; }
            .footer-grid { grid-template-columns: 1fr; gap: 2rem; }
            .modal-info { grid-template-columns: 1fr 1fr; }
        }
    </style>
</head>
<body>

<!-- NAV -->
<nav id="navbar">
    <a href="#" class="nav-logo">Wander<span>World</span></a>
    <ul class="nav-links">
        <li><a href="#destinations">Destinations</a></li>
        <li><a href="#about">Why Us</a></li>
        <li><a href="#contact">Contact</a></li>
    </ul>
    <div class="nav-right">
        <button class="wishlist-btn" onclick="toggleWishlist()">
            <i class="fas fa-heart"></i> Wishlist
            <span class="wishlist-count" id="wishCount">0</span>
        </button>
    </div>
</nav>

<!-- HERO -->
<section class="hero">
    <div class="hero-bg"></div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <p class="hero-eyebrow">✈ Your World Awaits</p>
        <h1 class="hero-title">Travel the World,<br><em>Your Way</em></h1>
        <p class="hero-sub">Discover handpicked international destinations. From ancient ruins to modern skylines — every journey starts here.</p>
        <button class="hero-cta" onclick="document.getElementById('search-sec').scrollIntoView({behavior:'smooth'})">
            Explore Destinations <i class="fas fa-arrow-right"></i>
        </button>
    </div>
</section>

<!-- STATS -->
<div class="stats-bar">
    <div class="stat"><div class="stat-num">9+</div><div class="stat-label">Destinations</div></div>
    <div class="stat"><div class="stat-num">50K+</div><div class="stat-label">Happy Travellers</div></div>
    <div class="stat"><div class="stat-num">4.8★</div><div class="stat-label">Average Rating</div></div>
    <div class="stat"><div class="stat-num">24/7</div><div class="stat-label">Support</div></div>
</div>

<!-- SEARCH -->
<section class="search-section" id="search-sec">
    <div class="search-wrap">
        <h2 class="search-label">Find your next <span style="color:var(--terra); font-style:italic">adventure</span></h2>
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Search destinations, countries..." oninput="applyFilters()">
            <select id="continentFilter" onchange="applyFilters()">
                <option value="all">All Continents</option>
                <option value="Asia">Asia</option>
                <option value="Europe">Europe</option>
                <option value="Americas">Americas</option>
                <option value="Africa">Africa</option>
            </select>
            <select id="budgetFilter" onchange="applyFilters()">
                <option value="all">Any Budget</option>
                <option value="budget">Under $1000</option>
                <option value="mid">$1000 - $1500</option>
                <option value="luxury">$1500+</option>
            </select>
            <button onclick="applyFilters()"><i class="fas fa-search"></i> Search</button>
        </div>
        <div class="filters">
            <button class="filter-btn active" onclick="filterTag('all', this)">All</button>
            <button class="filter-btn" onclick="filterTag('Culture', this)">Culture</button>
            <button class="filter-btn" onclick="filterTag('Beach', this)">Beach</button>
            <button class="filter-btn" onclick="filterTag('Adventure', this)">Adventure</button>
            <button class="filter-btn" onclick="filterTag('Romance', this)">Romance</button>
            <button class="filter-btn" onclick="filterTag('Food', this)">Food</button>
            <button class="filter-btn" onclick="filterTag('Nature', this)">Nature</button>
            <button class="filter-btn" onclick="filterTag('Luxury', this)">Luxury</button>
        </div>
    </div>
</section>

<!-- DESTINATIONS -->
<section class="destinations-section" id="destinations">
    <div class="section-header">
        <h2 class="section-title">Top <span>Destinations</span></h2>
        <span class="section-count" id="destCount">{{ products|length }} destinations found</span>
    </div>
    <div class="dest-grid" id="destGrid">
        {% for d in products %}
        <div class="dest-card"
             data-id="{{ d.id }}"
             data-name="{{ d.name|lower }}"
             data-country="{{ d.country|lower }}"
             data-continent="{{ d.continent }}"
             data-price="{{ d.price }}"
             data-tags="{{ d.tags|join(',') }}">
            <div class="card-img">
                <img src="{{ d.image }}" alt="{{ d.name }}" loading="lazy">
                <span class="card-badge">{{ d.continent }}</span>
                <button class="card-wish" data-id="{{ d.id }}" onclick="toggleWishItem(event, {{ d.id }})">
                    <i class="fas fa-heart"></i>
                </button>
                <span class="card-price">from ${{ d.price }}</span>
            </div>
            <div class="card-body">
                <p class="card-location">{{ d.flag }} {{ d.country }}</p>
                <h3 class="card-name">{{ d.name }}</h3>
                <p class="card-desc">{{ d.description }}</p>
                <div class="card-tags">
                    {% for tag in d.tags %}
                    <span class="tag">{{ tag }}</span>
                    {% endfor %}
                </div>
                <div class="card-meta">
                    <span><i class="fas fa-clock"></i> {{ d.duration }}</span>
                    <span><i class="fas fa-sun"></i> {{ d.best_season }}</span>
                </div>
            </div>
            <div class="card-footer">
                <div class="rating">
                    <span class="stars">★★★★★</span>
                    {{ d.rating }}
                </div>
                <button class="view-btn" onclick="openModal({{ d.id }})">View Trip →</button>
            </div>
        </div>
        {% endfor %}
    </div>
    <div class="no-results" id="noResults">
        <i class="fas fa-globe"></i>
        <p>No destinations found for your search.</p>
        <p style="font-size:0.85rem; margin-top:0.5rem">Try adjusting your filters.</p>
    </div>
</section>

<!-- MODAL -->
<div class="modal-overlay" id="modalOverlay" onclick="closeModalOutside(event)">
    <div class="modal-wrap">
        <button class="modal-close" onclick="closeModal()"><i class="fas fa-times"></i></button>
        <div class="modal" id="modalContent"></div>
    </div>
</div>

<!-- WISHLIST PANEL -->
<div class="wishlist-panel" id="wishlistPanel">
    <div class="panel-header">
        <span class="panel-title">My Wishlist</span>
        <button class="panel-close" onclick="toggleWishlist()"><i class="fas fa-times"></i></button>
    </div>
    <div class="panel-body" id="wishlistBody"></div>
</div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<!-- FOOTER -->
<footer id="contact">
    <div class="footer-grid">
        <div class="footer-brand">
            <div class="logo">WanderWorld</div>
            <p>Your trusted partner for international travel experiences. We curate the world's most unforgettable journeys.</p>
        </div>
        <div class="footer-col">
            <h5>Destinations</h5>
            <ul>
                <li><a href="#">Asia</a></li>
                <li><a href="#">Europe</a></li>
                <li><a href="#">Americas</a></li>
                <li><a href="#">Africa</a></li>
            </ul>
        </div>
        <div class="footer-col">
            <h5>Company</h5>
            <ul>
                <li><a href="#">About Us</a></li>
                <li><a href="#">Careers</a></li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Press</a></li>
            </ul>
        </div>
        <div class="footer-col">
            <h5>Support</h5>
            <ul>
                <li><a href="#">Help Center</a></li>
                <li><a href="#">Contact</a></li>
                <li><a href="#">Privacy</a></li>
                <li><a href="#">Terms</a></li>
            </ul>
        </div>
    </div>
    <div class="footer-bottom">
        <p>&copy; 2024 WanderWorld. Built with Flask & ❤</p>
    </div>
</footer>

<script>
    // Data from Flask
    const allDestinations = {{ products | tojson }};
    let wishlist = JSON.parse(localStorage.getItem('ww_wishlist') || '[]');
    let activeTag = 'all';

    // Init wishlist UI
    function initWishlist() {
        document.getElementById('wishCount').textContent = wishlist.length;
        document.querySelectorAll('.card-wish').forEach(btn => {
            const id = parseInt(btn.dataset.id);
            if (wishlist.find(w => w.id === id)) btn.classList.add('active');
        });
        renderWishlistPanel();
    }

    // Toggle wish item
    function toggleWishItem(e, id) {
        e.stopPropagation();
        const dest = allDestinations.find(d => d.id === id);
        const idx = wishlist.findIndex(w => w.id === id);
        const btn = document.querySelector(`.card-wish[data-id="${id}"]`);

        if (idx > -1) {
            wishlist.splice(idx, 1);
            btn && btn.classList.remove('active');
            showToast(`${dest.name} removed from wishlist`);
        } else {
            wishlist.push(dest);
            btn && btn.classList.add('active');
            showToast(`${dest.flag} ${dest.name} added to wishlist!`);
        }

        localStorage.setItem('ww_wishlist', JSON.stringify(wishlist));
        document.getElementById('wishCount').textContent = wishlist.length;
        renderWishlistPanel();
    }

    function renderWishlistPanel() {
        const body = document.getElementById('wishlistBody');
        if (wishlist.length === 0) {
            body.innerHTML = `<div class="empty-wish"><i class="fas fa-heart-broken"></i><p>Your wishlist is empty.</p><p style="font-size:0.82rem;margin-top:0.5rem">Save destinations you love!</p></div>`;
            return;
        }
        body.innerHTML = wishlist.map(d => `
            <div class="wish-item">
                <img src="${d.image}" alt="${d.name}" class="wish-img">
                <div class="wish-info">
                    <div class="wish-name">${d.flag} ${d.name}</div>
                    <div class="wish-country">${d.country}</div>
                    <div class="wish-price">from $${d.price} · ${d.duration}</div>
                </div>
                <button class="wish-remove" onclick="toggleWishItem(event, ${d.id})"><i class="fas fa-times"></i></button>
            </div>
        `).join('');
    }

    function toggleWishlist() {
        document.getElementById('wishlistPanel').classList.toggle('open');
    }

    // Filters
    function filterTag(tag, btn) {
        activeTag = tag;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyFilters();
    }

    function applyFilters() {
        const search = document.getElementById('searchInput').value.toLowerCase();
        const continent = document.getElementById('continentFilter').value;
        const budget = document.getElementById('budgetFilter').value;
        const cards = document.querySelectorAll('.dest-card');
        let visible = 0;

        cards.forEach(card => {
            const name = card.dataset.name;
            const country = card.dataset.country;
            const cont = card.dataset.continent;
            const price = parseInt(card.dataset.price);
            const tags = card.dataset.tags.split(',');

            const matchSearch = !search || name.includes(search) || country.includes(search);
            const matchContinent = continent === 'all' || cont === continent;
            const matchBudget = budget === 'all' ||
                (budget === 'budget' && price < 1000) ||
                (budget === 'mid' && price >= 1000 && price <= 1500) ||
                (budget === 'luxury' && price > 1500);
            const matchTag = activeTag === 'all' || tags.includes(activeTag);

            if (matchSearch && matchContinent && matchBudget && matchTag) {
                card.style.display = 'block'; visible++;
            } else {
                card.style.display = 'none';
            }
        });

        document.getElementById('destCount').textContent = `${visible} destination${visible !== 1 ? 's' : ''} found`;
        document.getElementById('noResults').style.display = visible === 0 ? 'block' : 'none';
    }

    // Modal
    function openModal(id) {
        const d = allDestinations.find(x => x.id === id);
        if (!d) return;
        const isWished = wishlist.find(w => w.id === id);
        const starsHtml = '★'.repeat(Math.floor(d.rating)) + (d.rating % 1 ? '½' : '');

        document.getElementById('modalContent').innerHTML = `
            <img src="${d.image}" alt="${d.name}" class="modal-img">
            <div class="modal-body">
                <div class="modal-flag">${d.flag}</div>
                <h2 class="modal-title">${d.name}</h2>
                <p class="modal-country"><i class="fas fa-map-marker-alt"></i> ${d.country} · ${d.continent} · ${starsHtml} ${d.rating}</p>
                <p class="modal-desc">${d.description}</p>
                <div class="modal-info">
                    <div class="info-box"><i class="fas fa-dollar-sign"></i><div class="label">Starting From</div><div class="value">$${d.price}</div></div>
                    <div class="info-box"><i class="fas fa-calendar"></i><div class="label">Best Season</div><div class="value">${d.best_season}</div></div>
                    <div class="info-box"><i class="fas fa-clock"></i><div class="label">Duration</div><div class="value">${d.duration}</div></div>
                </div>
                <div class="modal-highlights">
                    <h4>Must-See Highlights</h4>
                    <div class="highlights-list">
                        ${d.highlights.map(h => `<span class="highlight-chip"><i class="fas fa-star" style="font-size:0.65rem;margin-right:4px;color:var(--gold)"></i>${h}</span>`).join('')}
                    </div>
                </div>
                <div class="modal-actions">
                    <button class="btn-primary" onclick="showToast('✈ Booking coming soon for ${d.name}!')">Book This Trip</button>
                    <button class="btn-secondary" onclick="toggleWishItem(event, ${d.id})">${isWished ? '♥ Saved' : '♡ Save'}</button>
                </div>
            </div>
        `;
        document.getElementById('modalOverlay').classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        document.getElementById('modalOverlay').classList.remove('open');
        document.body.style.overflow = '';
    }

    function closeModalOutside(e) {
        if (e.target === document.getElementById('modalOverlay')) closeModal();
    }

    // Toast
    function showToast(msg) {
        const t = document.getElementById('toast');
        t.textContent = msg;
        t.classList.add('show');
        setTimeout(() => t.classList.remove('show'), 2800);
    }

    // Scroll nav
    window.addEventListener('scroll', () => {
        document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
    });

    // Init
    initWishlist();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, products=destinations)

@app.route("/api/destinations")
def get_destinations():
    continent = request.args.get('continent', 'all')
    search = request.args.get('search', '').lower()
    result = destinations
    if continent != 'all':
        result = [d for d in result if d['continent'] == continent]
    if search:
        result = [d for d in result if search in d['name'].lower() or search in d['country'].lower()]
    return jsonify(result)

@app.route("/api/destination/<int:dest_id>")
def get_destination(dest_id):
    dest = next((d for d in destinations if d['id'] == dest_id), None)
    if dest:
        return jsonify(dest)
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)