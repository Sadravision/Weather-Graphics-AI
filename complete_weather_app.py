import requests
import flet as ft
from datetime import datetime , timedelta
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import asyncio
from timezonefinder import TimezoneFinder
import pytz

# ================== تابع در حال بارگذاری ==================

async def splash_screen(page: ft.Page):
    page.bgcolor = "#f2fcfd"
    progress = ft.ProgressBar(width=400, color="green", bgcolor="#444444", value=0)
    label = ft.Text("در حال بارگذاری...", size=20, color="white")
    logo = ft.Image(src="logo.jpg", width=50, height=50)

    page.add(
        ft.Column(
            [
                ft.Container(height=60),
                ft.Text("!خوش آمدید", size=40, weight="bold", color="black"),
                ft.Container(height=40),
                ft.Row(
                    [
                        ft.Container(width=20),
                        ft.Text("Sadra Shahbandari طراحی شده توسط", size=32, weight="bold", color="black"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=40),
                progress,
                ft.Container(height=10),
                label
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    steps = 50
    delay = 2.5 / steps
    for i in range(steps + 1):
        progress.value = i / steps
        label.value = f"%در حال بارگذاری... {int((i / steps) * 100)}"
        label.color = "black"
        page.update()
        await asyncio.sleep(delay)

    await main_page(page)

async def main_page(page: ft.Page):
    page.controls.clear()
    page.bgcolor = "white"
    page.update()

# ================== تابع گرفتن داده از سایت همراه برای گرفتن ساعت دقیق ==================

def get_local_time(lat, lon):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    if timezone_str is None:
        return None
    timezone = pytz.timezone(timezone_str)
    return datetime.now(timezone)

# ================== تابع گرفتن داده از سایت همراه با مدیریت خطا ==================
def get_weather_data(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

# ================== مدل‌سازی و پیش‌بینی با هوش مصنوعی ==================
def build_model(data):
    return "Sadra Shahbandari طراحی شده توسط"

def predict_tomorrow(model, data):
    tmax = data["daily"]["temperature_2m_max"]
    tmin = data["daily"]["temperature_2m_min"]
    precip = data["daily"]["precipitation_sum"]
    temp_diff = tmax[0] - tmin[0]
    temp_mean = (tmax[0] + tmin[0]) / 2
    return model.predict([[tmin[0], tmax[0], precip[0], temp_diff, temp_mean]])[0]



ICON_TOP_MARGIN = -700
ICON_RIGHT_MARGIN = -500

def is_daytime(hour):
    return 6 <= hour < 18

def weather_code_info_day_night(code, rain_amount, hour):
    if is_daytime(hour):
        return weather_code_info_day(code, rain_amount)
    else:
        return weather_code_info_night(code, rain_amount)

# آیکون‌های روز

def weather_code_info_day(code, rain_amount):
    if code == 0:
        return ("#b3eafc", "☀️", "آفتابی", "images/sun1.png", "images/sun2.png")
    elif code == 1:
        return ("#ccf2ff", "☀️", "آفتابی", "images/sun11.png", "images/sun2.png")
    elif code in [2, 3, 61, 60, 63, 65]:
        if rain_amount > 0.5:
            return ("#467eb6", "☔️", "بارانی", "images/rain1.png", "images/sun2.png")
        return ("#d9d9d9", "☁️", "ابری", "images/cloud1.png", "images/sun2.png")
    elif 45 <= code <= 48:
        return ("#999999", "🌫️", "مه‌آلود", "images/fog1.png", "images/sun2.png")
    elif 71 <= code <= 77 or 85 <= code <= 86:
        return ("#e6f7ff", "❄️", "برفی", "images/snow0.png", "images/sun2.png")
    elif 95 == code or code == 96 or 99:
        return ("#27779C", "🌩️", "رعد و برق", "images/cloud4.png", "images/sun2.png")
    else:
        return ("#cccccc", "❓", "نامشخص", "images/unknown.png", "images/sun2.png")

# آیکون‌های شب

def weather_code_info_night(code, rain_amount):
    if code == 0 :
        return ("#1E1E6E", "🌕", "صاف (شب)", "images/moon0.png", "images/moon22.png")
    elif code in [1, 2, 3, 61, 60, 63, 65]:
        if rain_amount > 0.5:
            return ("#2a4056", "🌧️", "بارانی (شب)", "images/moon3.png", "images/moon22.png")
        return ("#34495e", "☁️", "ابری (شب)", "images/moon2.png", "images/moon22.png")
    elif 45 <= code <= 48:
        return ("#4b4b4b", "🌫️", "مه‌آلود (شب)", "images/fog1.png", "images/moon22.png")
    elif 71 <= code <= 77 or 85 <= code <= 86:
        return ("#e6f7ff", "❄️", "برفی", "images/snow11.png", "images/moon22.png")
    elif 95 == code or code == 96 or 99:
        return ("#e6f7ff", "🌩️", "رعد و برق", "images/moon3.png", "images/moon22.png")
    else:
        return ("#cccccc", "❓", "نامشخص", "images/unknown.png", "images/moon22.png")

# تابع محاسبه ساعت محلی بر اساس طول جغرافیایی

#"#dfffe0"
#"#080043"
def main(page: ft.Page):
    page.title = "پیش‌بینی آب‌وهوایی"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#fff8e1"
    page.window_height = 700
    page.window_width = 500
    asyncio.run(splash_screen(page))
    
    lat_field = ft.TextField(label="عرض جغرافیایی", width=300, text_align=ft.TextAlign.CENTER, color="black")
    lon_field = ft.TextField(label="طول جغرافیایی", width=300, text_align=ft.TextAlign.CENTER, color="black")
    result_text = ft.Text(color="blue", text_align=ft.TextAlign.CENTER)
    label_text = ft.Text("🌍 :لطفاً مختصات را وارد کنید", size=20, weight=ft.FontWeight.BOLD, color="black")
    weather_info = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    loading_spinner = ft.ProgressRing(color= 'green', visible=False)

    def on_show_weather(e):
        try:
            lat = float(lat_field.value)
            lon = float(lon_field.value)
        except:
            result_text.value = "خطا: لطفاً مقادیر معتبر وارد کنید."
            result_text.color = "red"
            page.update()
            return

        loading_spinner.visible = True
        page.update()

        local_time = get_local_time(lat, lon)

        data = get_weather_data(lat, lon)
        if not data:
            result_text.value = "خطا در دریافت داده! لطفاً اتصال اینترنت را بررسی کنید."
            result_text.color = "red"
            page.update()
            return

        lat_field.color = 'black'
        lon_field.color = 'black'
        label_text.color = 'black'

        daily = data["daily"]
        dates = daily["time"]
        precip = daily["precipitation_sum"]
        tmax = daily["temperature_2m_max"]
        tmin = daily["temperature_2m_min"]
        current_weather = data.get("current_weather", {})
        weather_code = current_weather.get("weathercode", 3)

        bg_color, emoji, weather_text, icon_small, icon_big = weather_code_info_day_night(weather_code, precip[0], current_hour)
        page.bgcolor = bg_color


        try:
            date_obj = datetime.strptime(dates[0], "%Y-%m-%d")
            date_str = date_obj.strftime("%Y/%m/%d")
        except:
            date_str = dates[0]

        weather_info.controls.clear()

        weather_info.controls.append(
            ft.Row([ft.Image(src=icon_small, width=100, height=100)], alignment=ft.MainAxisAlignment.CENTER)
        )

        loading_spinner.visible = False
        page.update()

        info_row = ft.Row([
            ft.Column([
                ft.Text(f"📍 مختصات جغرافیایی= {lat} , {lon}", size=15, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f"📅 تاریخ: {date_str}", size=18, weight=ft.FontWeight.BOLD, color=  font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f"وضعیت فعلی: {emoji} {weather_text} (کد: {weather_code})", size=18, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f"🌡️ دمای بیشینه امروز: {tmax[0]:.1f} °C", size=18, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f"🌡️ دمای کمینه امروز: {tmin[0]:.1f} °C", size=18, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f"🌧️ میزان بارش امروز: {precip[0]:.1f} mm", size=18, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text('________________________________________________', color =  font_color),
                ft.Text(f"🌡️ sadrashahbandari3@gmail.com: {0:.1f} °C", size=22, weight=ft.FontWeight.BOLD, color= font_color_for_ai, text_align=ft.TextAlign.CENTER),
                ft.Text(f"🌧️ 09915439774: {0:.1f} mm", size=22, weight=ft.FontWeight.BOLD, color= font_color_for_ai, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Sadra Shahbandari طراحی شده توسط: {0:.2f}", size=14, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Sadra Shahbandari طراحی شده توسط: {0:.2f}", size=14, color= font_color, text_align=ft.TextAlign.CENTER),
                ft.Text(f'ساعت دقیق مختصات : {local_time.strftime('%H:%M')}', size=20, weight=ft.FontWeight.BOLD, color= font_color, text_align=ft.TextAlign.LEFT),
            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Container(
                content=ft.Image(src=icon_big, width=400),
                margin=ft.margin.only(top=ICON_TOP_MARGIN, right=ICON_RIGHT_MARGIN)
            )
        ], alignment=ft.MainAxisAlignment.CENTER)

        weather_info.controls.append(info_row)
        result_text.value = ""
        page.update()

    show_button = ft.ElevatedButton(text="نمایش آب‌وهوا", on_click=on_show_weather)

    page.add(
        ft.Column([
            label_text,
            ft.Row([lat_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([lon_field], alignment=ft.MainAxisAlignment.CENTER),
            show_button,
            ft.Row([result_text], alignment=ft.MainAxisAlignment.CENTER),
            weather_info,
            loading_spinner
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
