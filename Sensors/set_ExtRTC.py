# Setting DS3231 RTC from rshell

# 1. Connect, then without starting the sampling codes:

# 2. Initialize RTC, which will have been set to curent host time
from machine import RTC
rtc=RTC()
rtc_datetime = rtc.datetime()
print('Current onboard RTC datatime = ',rtc_datetime)

# 3. Initialize I2C and DS3231 instance
from machine import I2C
from ExtTime.urtc import DS3231, DateTimeTuple
i2c = I2C(1)
sensor = DS3231(i2c)
ds3231_datetime = sensor.datetime()
print('Current external (DS3231) RTC datatime = ',ds3231_datetime)

# 4. Confirm choice to reset DS3231 from onboard RTC
q = 'n'
q = input('Reset external (DS3231) RTC from onboard RTC? (y/n): ')
if q in ['y','Y']:
    # update the onboard rtc time;
    rtc_datetime = rtc.datetime()
    year = rtc_datetime[0]
    month = rtc_datetime[1]
    day = rtc_datetime[2]
    weekday = rtc_datetime[3]
    hour = rtc_datetime[4]
    minute = rtc_datetime[5]
    second = rtc_datetime[6]
    millisecond = rtc_datetime[7] # not used

    print('setting to (year, month, day, weekday, hour, minute, second): (',year, month, day, weekday, hour, minute, second,')')
    new_ds3231_datetime = DateTimeTuple(year=year, month=month, day=day, weekday=weekday, hour=hour, minute=minute, second=second, millisecond=None)
    sensor.datetime(new_ds3231_datetime)
    print('current ds3231 datetime = ',sensor.datetime())

else:
    print('cancelled reset')



