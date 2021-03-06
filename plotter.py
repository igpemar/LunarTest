import numpy as np
import matplotlib.pyplot as plt
import pandas
import datetime
import seaborn as sns

chop = [0, 1480]

def initialize_plot_axes(range='', XLABEL='X label', XLABFS=15, YLABEL='Y label', YLABFS=15,  XTICKFS=10, YTICKFS=10):

    # Plotting the dataset
    #sns.set()
    if range != '':
        plt.axis(range)
    plt.xticks(fontsize=XTICKFS)
    plt.yticks(fontsize=YTICKFS)
    plt.xlabel(XLABEL, fontsize=XLABFS)
    plt.ylabel(YLABEL, fontsize=YLABFS)


def restart_check(DataFolderPath=''):
    req_n_1, req_n_2, dt_str, d_i_t_1, d_i_t_2, d_avg_1, d_avg_2, dist_1, dist_2 = [], [], [], [], [], [], [], [], []
    Output_1 = pandas.read_csv(DataFolderPath+ '/' + 'Output_1.csv', sep=';')
    Output_2 = pandas.read_csv(DataFolderPath+ '/' + 'Output_2.csv', sep=';')

    for i in range(Output_1.shape[0]):
        req_n_1.append(Output_1.values[i][0])
        dt_str.append(Output_1.values[i][1].strip())
        dist_1.append(Output_1.values[i][2])
        d_avg_1.append(Output_1.values[i][4])
        d_i_t_1.append(Output_1.values[i][3])

    for i in range(Output_2.shape[0]):
        req_n_2.append(Output_2.values[i][0])
        dist_2.append(Output_2.values[i][2])
        d_avg_2.append(Output_2.values[i][4])
        d_i_t_2.append(Output_2.values[i][3])

    reqs = np.column_stack((req_n_1, req_n_2))
    dist = np.column_stack((dist_1, dist_2))
    d_avg = np.column_stack((d_avg_1, d_avg_2))
    d_i_t = np.column_stack((d_i_t_1, d_i_t_2))

    datevec, elapsed_time = [], []
    [datevec.append(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')) for date in dt_str]
    datevec = np.array(datevec).reshape(-1, 1)

    [elapsed_time.append(t - datevec[0]) for t in datevec]

    elapsed_time = np.array(elapsed_time).reshape(-1, 1)
    elapsed_time_sec = np.array([elapsed_time[i][0].days * 24 * 3600 + elapsed_time[i][0].seconds for i in
                                 range(elapsed_time.shape[0])]).reshape(-1, 1)
    return reqs, dt_str, datevec, elapsed_time_sec, dist, d_avg, d_i_t

# Reading the data
reqs, dt_str, datevec, elapsed_time_sec, dist, d_avg, d_i_t = restart_check('Raw_Data')

# Plotting
#sns.set()
plt.figure(1, figsize=(20, 10))
Axis_Range = [elapsed_time_sec[0], elapsed_time_sec[-1]-elapsed_time_sec[chop[1]], 0, 25]
initialize_plot_axes(range=Axis_Range, XLABEL='Elapsed Time [s]', XLABFS=15, YLABEL='Comute Time  [min]',
                     YLABFS=15,  XTICKFS=10, YTICKFS=10)
X = elapsed_time_sec[chop[0]:chop[1]]-elapsed_time_sec[chop[0]]
Y = d_i_t[chop[0]:chop[1],0].reshape(-1,1)
plt.plot(X, Y, 'b.')

Y =  d_i_t[chop[0]:chop[1],1].reshape(-1,1)
plt.plot(X, Y, 'r.')

t0 = datevec[chop[0]][0]
labels = [str((t0 + datetime.timedelta(hours= int(i), minutes=-t0.minute, seconds= - t0.second)))[:-3] for i in range(0, 7*24+8, 8)]

plt.xticks(np.linspace(0, 86400 * 7, 3 * 7 + 1), labels=labels)
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()

plt.show()
pass