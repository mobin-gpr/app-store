from google_play_scraper import app


def get_app_data(app_id):
    return app(app_id, lang="en", country="us")


def en_genre_to_fa(genre):
    data = {
        "WEATHER": "آب و هوا",
        "EDUCATION": "آموزش",
        "TOOLS": "ابزار",
        "SOCIAL": "شبکه اجتماعی",
        "NEWS_AND_MAGAZINES": "اخبار و مجله",
        "COMMUNICATION": "ارتباطات",
        "FINANCE": "امور مالی",
        "ANDROID_WEAR": "برنامه های ساعت",
        "HEALTH_AND_FITNESS": "بهداشت و تناسب اندام",
        "PRODUCTIVITY": "بهره وری",
        "SHOPPING": "فروشگاه",
        "DATING": "دوستیابی",
        "LIFESTYLE": "روش زندگی",
        "ENTERTAINMENT": "سرگرمی",
        "TRAVEL_AND_LOCAL": "سفر",
        "PERSONALIZATION": "شخصی سازی",
        "WATCH_FACE": "صفحه های ساعت",
        "COMICS": "طنز",
        "PHOTOGRAPHY": "عکاسی",
        "FOOD_AND_DRINK": "غذا و نوشیدنی",
        "MUSIC_AND_AUDIO": "موسیقی و صدا",
        "ART_AND_DESIGN": "هنر و طراحی",
        "SPORTS": "ورزشی",
        "MEDICAL": "پزشکی",
        "LIBRARIES_AND_DEMO": "کتابخانه",
        "BOOKS_AND_REFERENCE": "کتاب و منابع",
        "BUSINESS": "کسب و کار",
        "BEAUTY": "آرایش و زیبایی",
        "VIDEO_PLAYERS": "ویدیو پلیر",
        "HOUSE_AND_HOME": "خانه و مسکن",
        "EVENTS": "رویداد و بلیت",
        "PARENTING": "فرزند داری",
        "MAPS_AND_NAVIGATION": "نقشه و راهبری",
        "AUTO_AND_VEHICLES": "وسیله نقلیه و خودرو",
        "GAME_ARCADE": "آرکید",
        "GAME_EDUCATIONAL": "آموزشی",
        "GAME_STRATEGY": "استراتژی",
        "GAME_TRIVIA": "اطلاعات عمومی",
        "GAME_ROLE_PLAYING": "ایفای نقش",
        "GAME_ACTION": "اکشن",
        "GAME_BOARD": "تخته ای",
        "GAME_SIMULATION": "شبیه سازی",
        "GAME_CARD": "کارتی",
        "GAME_CASINO": "کازینو",
        "GAME_WORD": "کلمه یابی",
        "GAME_ADVENTURE": "ماجراجویی",
        "GAME_RACING": "مسابقه",
        "GAME_PUZZLE": "معمایی",
        "GAME_CASUAL": "معمولی",
        "GAME_MUSIC": "موسیقی",
        "GAME_SPORTS": "ورزشی",
    }

    return data[genre]
