
import sys
import pyowm
print "Welcome to Your Name's weather report system"

city = raw_input('Please input place information (format: city, country, such as Boston, us)\n')
myAPIKey = '44a799a158d8678084a0cb1184a85726'
owm = pyowm.OWM(myAPIKey)  # You MUST provide a valid API key

# Search for current weather in Boston (us) or any city you like
observation = owm.weather_at_place(str(city))
obs = owm.weather_at_place(str(city)) 
l = observation.get_location()
w = observation.get_weather()
city_id = l.get_ID()
city_name = l.get_name()

#registry = owm.city_id_registry()
#num_id = registry.id_for(str(city))

print '======================================================'
print 'City information:', city  # missing code
print '======================================================'
print 'City name:',   city_name
print 'City ID:',     city_id
print 'City Geolocation:',  l
print 'Genereal weather infor for now: ', w
# <Weather - reference time=2016-10-29 09:20, # status=Clouds>

# The following method can be found in pyOWM wiki webpage.
forecast = owm.daily_forecast(str(city))
tomorrow = pyowm.timeutils.tomorrow()

print '======================================================'
print 'Below is the brief for tomorrow:'
print 'Sunny?',  forecast.will_be_sunny_at(tomorrow)
print 'Rainy?',  forecast.will_be_rainy_at(tomorrow)
print 'Foggy?',  forecast.will_be_foggy_at(tomorrow)
print 'Cloudy?', forecast.will_be_cloudy_at(tomorrow)
print 'Snowy?',  forecast.will_be_snowy_at(tomorrow)
print '======================================================'

humi = w.get_humidity()
press = w.get_pressure()
temp = w.get_temperature()
current_time = w.get_reference_time(timeformat='iso')
w_s = w.get_wind()
weather_info = w.get_detailed_status()

# Weather details
print 'Weather details'
print '======================================================'
print 'Current time:',  current_time
print 'Wind speed and direction:', w_s   # missing code {'speed': 4.6, 'deg': 330}
print 'Humudity level:',     humi        # 87
print 'Pressure:', press    # missing code
print 'Weather information:', weather_info  # missing code # get detailed weather report
#print 'Detailed weather information:', w.get_detailed_status() 
print 'Temperature information:', temp # missing code # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
# you can change fahrenheit to celsinus by changing argument 
print '======================================================'
print 'The next 7 days of weather forcast in', city, 'are as follows:'
#fc = forecast.get_forecast()
# missing code
fc = owm.daily_forecast(str(city), limit=7)
fore = fc.get_forecast()
for weather in fore:
	print (weather.get_reference_time('iso'), weather.get_status())

# Search current weather observations in the surroundings of 
# lat=42.32, lon=-71.04 (42.314820, -71.037695) (UMASS Boston)
observation_list = owm.weather_around_coords(42.32, -71.04)
print '======================================================'
#print type(observation_list)

for i in enumerate(observation_list):
	print i

