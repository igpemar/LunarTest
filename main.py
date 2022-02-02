import requests
import numpy as np
import datetime
import time
import pandas

# <editor-fold desc="Functions">


def findwaittime(current_time, hdsf, ldsf):
    wait = ldsf
    h = current_time.hour

    if 5 <= h < 11 or 13 <= h < 19:
        wait = hdsf
    return wait
# </editor-fold>


# <editor-fold desc="Input">

Home = (55.688519, 12.528168)   # GPS Coordinates in decimal degrees DDD.DDDDD
Work = (55.78210, 12.521248)    # GPS Coordinates in decimal degrees DDD.DDDDD (DTU)
Work = (55.6798552, 12.5823892)    # GPS Coordinates in decimal degrees DDD.DDDDD (Lunar)


API_KEY = 'AIzaSyC2FhCdJDamyyjhTxRS0qKJfN220C0rB-w'     # Google Api Key

DataDumpFrequency = 3  # In seconds (integer)

HighDataSamplingFrequency = 2          # In seconds Integer
Low_DataSamplingFrequency = 4     # In Seconds Integer

# </editor-fold>

# <editor-fold desc="Main">

#Intro message
print('------------------------------------------------------------------------------')
print('  Welcome to Google Maps Commute Analyzer')
print('------------------------------------------------------------------------------')
print(' Fetching driving time from ' + str(Home[0]) + ' N ; ' + str(Home[1]) + ' E to ' + str(Work[0]) + ' N ; ' + str(Work[1]) + ' E.')
print('------------------------------------------------------------------------------')
print('--------------------------------  Starting  ----------------------------------')
print(' ')

while True:
    #s = input('Would you like to start from scratch and erase the existing data? Y/N ')
    s = "y"
    if s == "y" or s == "Y":
        Restart_Flag = 1
        break

    if s == "n" or s == "N":
        Restart_Flag = 0
        Output_1 = pandas.read_csv('Output_1.csv', sep=';')
        Output_2 = pandas.read_csv('Output_2.csv', sep=';')
        req_n_1, req_n_2, dt_str, d_i_t_1, d_i_t_2, d_avg_1, d_avg_2, dist_1, dist_2 = [], [], [], [], [], [], [], [], []
        for i in range(Output_1.shape[0]):
            req_n_1.append(Output_1.values[i][0])
            dt_str.append(Output_1.values[i][1].strip())
            dist_1.append(Output_1.values[i][2])
            d_avg_1.append(Output_1.values[i][3])
            d_i_t_1.append(Output_1.values[i][4])

        for i in range(Output_2.shape[0]):
            req_n_2.append(Output_2.values[i][0])
            dist_2.append(Output_2.values[i][2])
            d_avg_2.append(Output_2.values[i][3])
            d_i_t_2.append(Output_2.values[i][4])
        break

# Building request
outputFormat = 'json'
RequestStart = 'https://maps.googleapis.com/maps/api/distancematrix/'
Origin = str(Home[0]) + '%2C' + str(Home[1])
Destination = str(Work[0]) + '%2C' + str(Work[1])
Req_car_Home_To_work = RequestStart + outputFormat + '?destinations=' + Destination + '&origins=' + Origin \
                       + '&mode=driving' + '&departure_time=now' + '&key=' + API_KEY
Req_car_Work_To_Home = RequestStart + outputFormat + '?destinations=' + Origin + '&origins=' + Destination \
                       + '&mode=driving' + '&departure_time=now' + '&key=' + API_KEY
# Initializing Variables

if Restart_Flag == 1:
    req_n_1, req_n_2, dt_str, d_i_t_1, d_i_t_2, d_avg_1, d_avg_2, dist_1, dist_2 = [], [], [], [], [], [], [], [], []

t0, dt_data_dump = datetime.datetime.now(), datetime.datetime.now()
dt = []


print("Start time: ", t0)

# Entering request loop
while 1:
    #Incrementing request number
    if not req_n_1:
        req_n_1 = [1]
        req_n_2 = [2]
    else:
        req_n_1.append(req_n_1[-1] + 2)
        req_n_2.append(req_n_2[-1] + 2)

    #Dealing with timestamps
    MonthStr, DayStr, HourStr, MinuteStr, SecondStr = '0', '0', '0', '0', '0'
    dt_req = datetime.datetime.now()   
    dt.append(dt_req)
    if dt[-1].month >= 10:
        MonthStr=''
    if dt[-1].day >= 10:
        DayStr = ''
    if dt[-1].hour >= 10:
        HourStr = ''
    if dt[-1].minute >= 10:
        MinuteStr = ''
    if dt[-1].second >= 10:
        SecondStr = ''

    dt_str.append(str(dt[-1].year) + '-' + MonthStr + str(dt[-1].month) + '-' + DayStr + str(dt[-1].day) + ' '
                  + HourStr + str(dt[-1].hour) + ':' + MinuteStr + str(dt[-1].minute) + ':' + SecondStr + str(dt[-1].second))
    print(dt_str[-1])

    #Sending Requests
    try:
        payload = {}
        headers = {}
        print(str(dt_req)[0:-7] + ' ; Sending request #' + str(req_n_1[-1]))

        response_1 = requests.request("GET", Req_car_Home_To_work, headers=headers, data=payload)

        print(str(dt_req)[0:-7] + ' ; Request response successfully received')
        print(str(dt_req)[0:-7] + ' ; Sending request #' + str(req_n_2[-1]))

        response_2 = requests.request("GET", Req_car_Work_To_Home, headers=headers, data=payload)

        print(str(dt_req)[0:-7] + ' ; Request response successfully received')
        print(str(dt_req)[0:-7] + ' ; Storing data')
    except:
        req_n_1[-1] = req_n_1[-1] - 2
        req_n_2[-1] = req_n_2[-1] - 2
        print('ERROR: An error occurred while performing the API requests, check your internet connection')
        print('waiting 60 seconds before trying again')
        time.sleep(60)
        continue

    #Storing Data
    A = response_1.json()
    d_i_t_1.append(round(A['rows'][0]['elements'][0]['duration_in_traffic']['value']/60., 2))
    d_avg_1.append(round(A['rows'][0]['elements'][0]['duration']['value']/60., 2))
    dist_1.append(round(A['rows'][0]['elements'][0]['distance']['value']/1000., 2))
    MyList1 = np.column_stack((req_n_1, dt_str, dist_1, d_avg_1, d_i_t_1))


    B = response_2.json()
    d_i_t_2.append(round(B['rows'][0]['elements'][0]['duration_in_traffic']['value']/60., 2))
    d_avg_2.append(round(B['rows'][0]['elements'][0]['duration']['value']/60., 2))
    dist_2.append(round(B['rows'][0]['elements'][0]['distance']['value']/1000.0, 2))
    MyList2 = np.column_stack((req_n_2, dt_str, dist_2, d_avg_2, d_i_t_2))

    Elapsed_Time_Since_Last_Data_Dump = dt_req - dt_data_dump
    if req_n_1[-1] == 1 or Elapsed_Time_Since_Last_Data_Dump >= datetime.timedelta(seconds=DataDumpFrequency, microseconds=10):
        print(str(dt_req)[0:-7] + ' ; Writing request data to output file')
        np.savetxt('Output_1.csv', MyList1, fmt='%s', delimiter=' ; ', comments='',
                   header='Req nbr. ; Timestamp ; Distance [km] ; Duration (incl.traffic) [min] ; Duration (excl.traffic) [min]')
        np.savetxt('Output_2.csv', MyList2, fmt='%s', delimiter=' ; ', comments='',
                   header='Req nbr. ; Timestamp ; Distance [km] ; Duration (incl.traffic) [min] ; Duration (excl.traffic) [min]')
        dt_data_dump = datetime.datetime.now()

    print(str(dt_req)[0:-7] + ' ; ---> DONE')
    print(str(dt_req)[0:-7] + ' ; ----------------------------------------------')
    wait_time = findwaittime(dt_req, HighDataSamplingFrequency, Low_DataSamplingFrequency)
    print(str(dt_req)[0:-7] + ' ; ----- Waiting ' + str(wait_time) + ' seconds.-----')#
    print(str(dt_req)[0:-7] + ' ; ----------------------------------------------')
    time.sleep(wait_time)
# </editor-fold>


