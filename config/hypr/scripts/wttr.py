#!/usr/bin/env python

import json
import requests
from datetime import datetime

WEATHER_CODES = {
    '113': '☀️',
    '116': '⛅️',
    '119': '☁️',
    '122': '☁️',
    '143': '🌫',
    '176': '🌦',
    '179': '🌧',
    '182': '🌧',
    '185': '🌧',
    '200': '⛈',
    '227': '🌨',
    '230': '❄️',
    '248': '🌫',
    '260': '🌫',
    '263': '🌦',
    '266': '🌦',
    '281': '🌧',
    '284': '🌧',
    '293': '🌦',
    '296': '🌦',
    '299': '🌧',
    '302': '🌧',
    '305': '🌧',
    '308': '🌧',
    '311': '🌧',
    '314': '🌧',
    '317': '🌧',
    '320': '🌨',
    '323': '🌨',
    '326': '🌨',
    '329': '❄️',
    '332': '❄️',
    '335': '❄️',
    '338': '❄️',
    '350': '🌧',
    '353': '🌦',
    '356': '🌧',
    '359': '🌧',
    '362': '🌧',
    '365': '🌧',
    '368': '🌨',
    '371': '❄️',
    '374': '🌧',
    '377': '🌧',
    '386': '⛈',
    '389': '🌩',
    '392': '⛈',
    '395': '❄️'
}

CHANCE = {
    "chanceoffog": "起霧",
    "chanceoffrost": "結霜",
    "chanceofovercast": "陰天",
    "chanceofrain": "降雨",
    "chanceofsnow": "降雪",
    "chanceofsunshine": "晴天",
    "chanceofthunder": "打雷",
    "chanceofwindy": "大風"
}


def format_date_by_count(count: int):
    if count == 0:
        return '今天'
    elif count == 1:
        return '明天'
    return '後天'


def format_time(time: str):
    return time.replace("00", "").zfill(2)


def format_temp(temp: str):
    return f"{temp}°C".ljust(3)


def format_chances(hour_weather: str):
    result = []
    for event in CHANCE.keys():
        if int(hour_weather[event]) > 0:
            result.append(f'{CHANCE[event]} {hour_weather[event]}%')

    return ", ".join(result)


def format_current_condition_weather(current_condition) -> str:
    result = ""
    result += f"<b>{current_condition['lang_zh-tw'][0]['value']} {current_condition['temp_C']}°C</b>\n"
    result += f"體感溫度: {current_condition['FeelsLikeC']}°C\n"
    result += f"風速: {current_condition['windspeedKmph']}Km/h\n"
    result += f"濕度: {current_condition['humidity']}%\n"
    return result


def format_day_weather(count: int, day_weather) -> str:
    result = ""
    result += f"\n<b>{format_date_by_count(count)}, {day_weather['date']}</b>\n"
    result += f"⬆️ {day_weather['maxtempC']}°C ⬇️ {day_weather['mintempC']}°C "
    result += f"🌅 {day_weather['astronomy'][0]['sunrise']} 🌇 {day_weather['astronomy'][0]['sunset']}\n"
    for hour in day_weather['hourly']:
        if count == 0:
            if int(format_time(hour['time'])) < datetime.now().hour - 2:
                continue
        result += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])}, {format_chances(hour)}, {hour['lang_zh-tw'][0]['value']}\n"

    return result


if __name__ == '__main__':
    result = {
        'text': "",
        'tooltip': ""
    }
    try:
        weather_data_json = requests.get(
            "https://wttr.in/Taichung?format=j1&lang=zh-tw").json()

        current_condition = weather_data_json["current_condition"][0]
        weather = weather_data_json["weather"]

        result["text"] = f" {WEATHER_CODES[current_condition['weatherCode']]} {current_condition['FeelsLikeC']}°C"
        result['tooltip'] = format_current_condition_weather(current_condition)

        for i, day_weather in enumerate(weather):
            result['tooltip'] += format_day_weather(i, day_weather)
    except:
        result['text'] = 'Wttr: Error'
        result['tooltip'] = ""
    print(json.dumps(result, ensure_ascii=False))
