import json
import traceback
from datetime import datetime

import requests

from common.log import logger

week_map = {
    '1': "一",
    '2': "二",
    '3': "三",
    '4': "四",
    '5': "五",
    '6': "六",
    '7': "日",
}

adcode_config = dict()
with open('./resources/weather/adcode.json', 'r') as pf:
    raw = pf.read()
    adcode_config = json.loads(raw)


class WeatherCast:
    def __init__(self, date: str, week: str, day_weather: str, night_weather: str, day_temp: str, night_temp: str,
                 day_wind: str, night_wind: str, day_power: str, night_power: str, day_temp_float: float,
                 night_temp_float: float):
        self.date = date
        self.week = week
        self.day_weather = day_weather
        self.night_weather = night_weather
        self.day_temp = day_temp
        self.night_temp = night_temp
        self.day_wind = day_wind
        self.night_wind = night_wind
        self.day_power = day_power
        self.night_power = night_power
        self.day_temp_float = day_temp_float
        self.night_temp_float = night_temp_float


class WeatherReport:
    def __init__(self, city: str, adcode: str, province: str, report_time: str, weather_casts: dict):
        self.city = city
        self.adcode = adcode
        self.province = province
        self.report_time = report_time
        self.weather_casts = weather_casts


def get_weather_from_gaode(key, city_code) -> (bool, WeatherReport):
    """
    https://lbs.amap.com/api/webservice/guide/api/weatherinfo/
    key: like 9f7626caa9d4382b1221f6fd3ad936ef gaode key
    city_code:https://lbs.amap.com/api/webservice/download
    """
    if key is None:
        key = '9f7626caa9d4382b1221f6fd3ad936ef'
    if city_code is None:
        # "北京市市辖区"
        city_code = '110100'
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key={}&city={}&extensions=all&output=JSON".format(key,
                                                                                                             city_code)
    response = requests.get(url)
    if response.status_code != 200:
        return False, None
    data = json.loads(response.text)
    forecasts = data['forecasts'][0]
    weather = WeatherReport(
        city=forecasts['city'],
        adcode=forecasts['adcode'],
        province=forecasts['province'],
        report_time=forecasts['reporttime'],
        weather_casts={item['date']: WeatherCast(
            date=item['date'],
            week=item['week'],
            day_weather=item['dayweather'],
            night_weather=item['nightweather'],
            day_temp=item['daytemp'],
            night_temp=item['nighttemp'],
            day_wind=item['daywind'],
            night_wind=item['nightwind'],
            day_power=item['daypower'],
            night_power=item['nightpower'],
            day_temp_float=item['daytemp_float'],
            night_temp_float=item['nighttemp_float']
        ) for item in forecasts['casts']}
    )
    return True, weather


def get_latest_weather() -> (bool, str):
    try:
        yes, weather = get_weather_from_gaode(None, None)
        # weather = WeatherReport(weather)
        cur_date = datetime.now().strftime("%Y-%m-%d")
        # latest = WeatherCast(weather.weather_casts[cur_date])
        latest = weather.weather_casts[cur_date]
        if not yes:
            return False, None
        report = "{} 发布\n今日星期{} {}\n".format(weather.report_time, week_map[latest.week], weather.city)
        report += "全天 {} 转 {} 气温 {}℃ ～ {}℃。\n/:sun{}风,{}级;/:moon{}风,{}级\n\n💗今天也是爱你的一天😍💗".format(
            latest.day_weather, latest.night_weather, latest.night_temp, latest.day_temp,
            latest.day_wind, latest.day_power, latest.night_wind, latest.night_power
        )
        return True, report
    except:
        logger.error("fail to get weather:{}".format(traceback.print_stack()))
        return False, "fail to get weahter"

