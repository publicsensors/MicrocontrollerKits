#
# Utilities to facilitate setting time on the onboard and external Real Time Clocks (RTCs).
#
try:
    from sys import print_exception, exit
except:
    print_exception = print

try:
    from machine import RTC
    onbrdRTC=RTC()
    onbrdRTC_datetime = onbrdRTC.datetime()
    print('Current onboard RTC datetime = ',onbrdRTC_datetime)
except Exception as e:
    print('Error in getting datetime from onboard RTC')
    print_exception(e)
    exit(1)

def setONBRD(year=None,month=None,day=None,weekday=None,hour=None,minute=None,second=None,
             millisecond=None,accept='n'):
    onbrdRTC_datetime = list(onbrdRTC.datetime())
    print('Onboard RTC datetime is: ',onbrdRTC_datetime)
    # Fill in unspecified fields with current values
    if year is not None:
        onbrdRTC_datetime[0] = year
    if month is not None:
        onbrdRTC_datetime[1] = month
    if day is not None:
        onbrdRTC_datetime[2] = day
    if weekday is not None:
        onbrdRTC_datetime[3] = weekday
    if hour is not None:
        onbrdRTC_datetime[4] = hour
    if minute is not None:
        onbrdRTC_datetime[5] = minute
    if second is not None:
        onbrdRTC_datetime[6] = second
    if millisecond is not None:
        onbrdRTC_datetime[7] = millisecond
    print('New datetime is: ',onbrdRTC_datetime)
    # Confirm choice to reset onboard RTC    
    if accept not in ['y','Y']:
        accept = input('Reset onboard RTC? (y/n): ')
    if accept in ['y','Y']:
        onbrdRTC.datetime(onbrdRTC_datetime)
        print('current onbrdRTC datetime = ',onbrdRTC.datetime())
    else:
        print('User cancelled reset')


# 3. Initialize I2C and DS3231 instances, using board-specific platform_defs
try:
    from Setup.platform_defs import i2c
    from ExtTime.urtc import DS3231, DateTimeTuple

    extRTC = DS3231(i2c)
    extRTC_datetime = extRTC.datetime()
    print('Current external (DS3231) RTC datetime = ',extRTC_datetime)
except Exception as e:
    print('External RTC not found for getting datetime...')
    #print_exception(e)
    #exit(1)

def setEXT(year=None,month=None,day=None,weekday=None,hour=None,minute=None,second=None,
             millisecond=0,accept='n'):
    extRTC_datetime=extRTC.datetime()
    print('External RTC datetime is: ',extRTC_datetime)
    # Fill in unspecified fields with current values
    if year is None:
        year = extRTC_datetime.year
    if month is None:
        month = extRTC_datetime.month
    if day is None:
        day = extRTC_datetime.day
    if weekday is None:
        weekday = extRTC_datetime.weekday
    if hour is None:
        hour = extRTC_datetime.hour
    if minute is None:
        minute = extRTC_datetime.minute
    if second is None:
        second = extRTC_datetime.second
    if millisecond is None:
        millisecond = extRTC_datetime.millisecond
    # Assemble datetime from arguments
    extRTC_datetime = DateTimeTuple(year=year, month=month, day=day, weekday=weekday,
                                        hour=hour, minute=minute, second=second,
                                        millisecond=millisecond)
    print('New datetime is: ',extRTC_datetime)
    # Confirm choice to reset external RTC    
    if accept not in ['y','Y']:
        accept = input('Reset external RTC? (y/n): ')
    if accept in ['y','Y']:
        extRTC.datetime(extRTC_datetime)
        print('current extRTC datetime = ',extRTC.datetime())
    else:
        print('User cancelled reset')


def ONBRDfromEXT(accept='n'):
    onbrdRTC_datetime = onbrdRTC.datetime()
    print('Initial onboard RTC datetime is: ',onbrdRTC_datetime)
    extRTC_datetime=extRTC.datetime()
    print('External RTC datetime is: ',extRTC_datetime)
    # Confirm choice to reset onboard RTC from external RTC    
    if accept not in ['y','Y']:
        accept = input('Reset onboard RTC from external RTC? (y/n): ')
    if accept in ['y','Y']:
        extRTC_datetime=extRTC.datetime()
        setONBRD(year=extRTC_datetime.year,month=extRTC_datetime.month,day=extRTC_datetime.day,
                 weekday=extRTC_datetime.weekday,hour=extRTC_datetime.hour,
                 minute=extRTC_datetime.minute,second=extRTC_datetime.second,
                 accept=accept)
        print('Onboard RTC set to: ',onbrdRTC.datetime())
    else:
        print('User cancelled reset...')
    
def EXTfromONBRD(accept='n'):
    extRTC_datetime=extRTC.datetime()
    print('Initial external RTC datetime is: ',extRTC_datetime)
    print('Onboard RTC datetime is: ',onbrdRTC.datetime())
    # Confirm choice to reset DS3231 from onboard RTC
    if accept not in ['y','Y']:
        accept = input('Reset external RTC from RTC? (y/n): ')
    if accept in ['y','Y']:
        # update the onboard rtc time;
        onbrdRTC_datetime = onbrdRTC.datetime()
        year = onbrdRTC_datetime[0]
        month = onbrdRTC_datetime[1]
        day = onbrdRTC_datetime[2]
        weekday = onbrdRTC_datetime[3]
        hour = onbrdRTC_datetime[4]
        minute = onbrdRTC_datetime[5]
        second = onbrdRTC_datetime[6]
        millisecond = onbrdRTC_datetime[7] # not used
        setEXT(year=year, month=month, day=day, weekday=weekday,
               hour=hour, minute=minute, second=second, millisecond=None,
               accept=accept)
        print('External RTC set to:',extRTC.datetime())
    else:
        print('User cancelled reset')




