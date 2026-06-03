# 这是一个简单的Python程序，用于打印"Hello World!"
#1定义字典存5个城市温度
city_temp = {"北京":25,"上海":20,"广州":28,"深圳":22,"成都":26}
print(city_temp)
#2列表推导shi筛选温度>20
hot_cities = [(city, temp) for city, temp in city_temp.items() if temp > 20]
print(hot_cities)
print(f"温度高于20°C的城市共 {len(hot_cities)} 个：")
for city, temp in hot_cities:
    print(f"      {city} 温度为 {temp}℃")
hotcitcitsorted = sorted(hot_cities, key=lambda x: x[1], reverse=True)
print(hotcitcitsorted)
print(f"温度从高到低排序后的城市温度为：")
for city, temp in hotcitcitsorted:
    print(f"      {city} 温度为 {temp}℃")