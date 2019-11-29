from scipy import exp
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import optimize, integrate


def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / ( 2 * stddev ) )**2)

def gaussian_and_linear(x, amplitude, mean, stddev, a, b):
    return amplitude * np.exp(-((x - mean) / ( 2 * stddev ) )**2) + a + b * x

def double_gaussian_and_linear(x, amplitude1, mean1, stddev1, amplitude2, mean2, stddev2, a, b):
    return amplitude1 * np.exp(-((x - mean1) / ( 2 * stddev1 ) )**2) + amplitude2 * np.exp(-((x - mean2) / ( 2 * stddev2 ) )**2) + a + b * x

def smoothWithReturn(a):
    arr = a.copy()
    for i in range(1, len(arr) - 1):
        arr[i] = (arr[i] + arr[i + 1] + arr[i - 1]) / 3
    return arr

def smoothInstance(arr):
    for i in range(1, len(arr) - 1):
        arr[i] = (arr[i] + arr[i + 1] + arr[i - 1]) / 3


def differentiate(arr):
    a = [0]
    for i in range(0, len(arr) - 1):
        a.append(arr[i + 1] - arr[i])
    return np.array(a)

def build(spectrum, mode):
    spectrum = np.array(spectrum)
    x = np.arange(len(spectrum))
    if mode == 1:
        plt.plot(x, spectrum, '.', label='Clear')
    if mode == 2:
        plt.plot(x, spectrum, '.', color='orange', label='1-st smooth')
    if mode == 3:
        plt.plot(x, spectrum, 'g.', label='2nd smooth')
    if mode == 4:
        plt.plot(x, spectrum, 'r.', label='derivative')
    if mode == 5:
        plt.plot(x, spectrum, 'b.', label='2nd derivative')

def peakSearchDerivative(derivative, h1, h2, epsilon):
    peaks_list = []
    for i in range(1, len(derivative) - 1):
       if ( derivative[i - 1] > h1 and np.abs(derivative[i]) < epsilon and derivative[i + 1] < -h2 ):
           peaks_list.append(i)
    return np.array(peaks_list)

def peakSearchDerivative2(derivative2, h1, h2, h3):
    peaks_list = []
    for i in range(1, len(derivative2) - 1):
        # if i == 300:
        #     print(str(derivative2[i - 1]) + ' ' + str(derivative2[i]) + ' ' + str(derivative2[i + 1]))
        if (derivative2[i - 1] >= derivative2[i] <= derivative2[i + 1]):
            for p in range(25):
                if ( derivative2[i - p] > h1 and derivative2[i] < -h2 and derivative2[i + p] > h3 ):
                    peaks_list.append(i)
                    break
    return np.array(peaks_list)

def sigmaSearch(derivative2, peaks, epsilon):
    sigmas = []
    sigma = []
    for peak in peaks: 
        left_bound, right_bound = 0, 0
		
        i = peak
        while( derivative2[i - 1] > derivative2[i] ):
			# Searching left bound
            if abs(derivative2[i]) < epsilon:
                left_bound = i
                break
            i -= 1

        i = peak
        while( derivative2[i + 1] > derivative2[i] ):
            # Right bound 
            if abs(derivative2[i]) < epsilon:
                right_bound = i
                break
            i += 1

        sigmas.append([left_bound, right_bound])

    for i in sigmas:
        if (i[0] == 0 or i[1] == 0 or i[0] - i[1] == 0):
            sigma.append(1)
        else:
            sigma.append(i[1] - i[0])
    return sigma

def fitGauss():
    pass


# def peakSearchDerivative(derivative_second, h1, h2, h3):
#   peaks_list = []
#   for i in range(1, len(derivative_second) - 1):
#       if ( derivative_second[i - 1] > h1 and  )

data = pd.read_csv('spectr_b.txt', delimiter='\t')
begining_intensity = np.array(data.Intensity.copy())
build(data.Intensity, 1)
smoothInstance(data.Intensity)
smoothInstance(data.Intensity)
build(data.Intensity, 2)    
smoothInstance(data.Intensity)
smoothInstance(data.Intensity)


build(data.Intensity, 3)
derivative = differentiate(data.Intensity)
build(derivative, 4)
derivative2 = differentiate(derivative)
build(derivative2, 5)

plt.legend()
plt.show()

derivative = differentiate(data.Intensity)
build(derivative, 4)
smoothInstance(derivative)

derivative2 = differentiate(derivative)
smoothInstance(derivative2)

build(derivative2, 5)
# smoothInstance(derivative2)
# build(derivative, 2)
# build(derivative2, 3)

plt.legend()
# plt.show()

peaks = peakSearchDerivative(derivative, 40, 40, 400)
print(peaks)
peaks2 = peakSearchDerivative2(derivative2, 50, 200, 50)
print(peaks2)
sigma = sigmaSearch(derivative2, peaks2, 100)
print(sigma)
plt.show()

def getD1D2(p0, distance_for_1_sigma):
    if p0[2] == 1:
        d1 = (p0[1] - distance_for_1_sigma)
        d2 = (p0[1]  + distance_for_1_sigma)
    else:
        d1 = (p0[1] - 6 * p0[2])
        d2 = (p0[1]  + 6 * p0[2])
    return d1, d2

#### Fitting
distance_for_1_sigma = 30

for i in range(len(peaks2)):
    p0 = [np.abs(begining_intensity[peaks2[i]] - begining_intensity[-1]), peaks2[i], sigma[i], 1, 0.1] # begining_intensity[peaks2[i]]
    d1, d2 = getD1D2(p0, distance_for_1_sigma)
    if i != len(peaks2) - 1:
        if (np.abs(peaks2[i + 1] - peaks2[i]) <= 2):
            continue
        if p0[2] == 1:
            popt1, _ = optimize.curve_fit(gaussian_and_linear, data.Channel[d1:d2], begining_intensity[d1:d2], p0=p0)
            if (np.abs(peaks2[i + 1] - peaks2[i]) < distance_for_1_sigma):
                p0_2 = [np.abs(begining_intensity[peaks2[i + 1]] - begining_intensity[-1]), peaks2[i + 1], sigma[i + 1], 1, 0.1]
                d1_2, d2_2 = getD1D2(p0_2, distance_for_1_sigma)

                popt2, _ = optimize.curve_fit(gaussian, data.Channel[d1_2:d2_2], begining_intensity[d1_2:d2_2], p0=p0_2[0:3])
                plt.plot(data.Channel[d1_2:d2_2], gaussian(data.Channel[d1_2:d2_2], *popt2), 'b--')
                pSum = popt2.copy()
                pSum = np.concatenate((pSum, popt1), axis=None)
                print(pSum)

                popt, _ = optimize.curve_fit(double_gaussian_and_linear, data.Channel[d1:d2], begining_intensity[d1:d2], p0=pSum)
                plt.plot(data.Channel[d1:d2], double_gaussian_and_linear(data.Channel[d1:d2], *pSum), 'r-')
                print('Peak: ' + str(popt[0]) + ' E ' + str(popt[1]) + ' sigma ' + str(popt[2]) + '\n')
                print('Peak: ' + str(popt[3]) + ' E ' + str(popt[4]) + ' sigma ' + str(popt[5]) + '\n')
                i += 1
            else:
                plt.plot(data.Channel[d1:d2], gaussian_and_linear(data.Channel[d1:d2], *popt1), 'r-')
                print('Peak: ' + str(popt1[0]) + ' E ' + str(popt1[1]) + ' sigma ' + str(popt1[2]) + '\n')

        else:
            popt1, _ = optimize.curve_fit(gaussian_and_linear, data.Channel[d1:d2], begining_intensity[d1:d2], p0=p0)
            plt.plot(data.Channel[d1:d2], gaussian_and_linear(data.Channel[d1:d2], *popt1), 'g-')
            if (np.abs(peaks2[i + 1] - peaks2[i]) <= 6 * p0[2]):
                p0_2 = [np.abs(begining_intensity[peaks2[i + 1]] - begining_intensity[-1]), peaks2[i + 1], sigma[i + 1], 1, 0.1]
                d1_2, d2_2 = getD1D2(p0_2, distance_for_1_sigma)

                popt2, _ = optimize.curve_fit(gaussian, data.Channel[d1_2:d2_2], begining_intensity[d1_2:d2_2], p0=p0_2[0:3])
                plt.plot(data.Channel[d1_2:d2_2], gaussian(data.Channel[d1_2:d2_2], *popt2), 'b--')
                pSum = popt2.copy()
                pSum = np.concatenate((pSum, popt1), axis=None)

                popt, _ = optimize.curve_fit(double_gaussian_and_linear, data.Channel[d1:d2], begining_intensity[d1:d2], p0=pSum)
                plt.plot(data.Channel[d1:d2], double_gaussian_and_linear(data.Channel[d1:d2], *pSum), 'r-')
                i += 1
                print('Peak: ' + str(popt[0]) + ' E ' + str(popt[1]) + ' sigma ' + str(popt[2]) + '\n')
                print('Peak: ' + str(popt[3]) + ' E ' + str(popt[4]) + ' sigma ' + str(popt[5]) + '\n')
            else:
                plt.plot(data.Channel[d1:d2], gaussian_and_linear(data.Channel[d1:d2], *popt1), 'r-')
                print('Peak: ' + str(popt1[0]) + ' E ' + str(popt1[1]) + ' sigma ' + str(popt1[2]) + '\n')
    else:
        popt1, _ = optimize.curve_fit(gaussian_and_linear, data.Channel[d1:d2], begining_intensity[d1:d2], p0=p0)
        plt.plot(data.Channel[d1:d2], gaussian_and_linear(data.Channel[d1:d2], *popt1), 'r-')
        print('Peak: ' + str(popt1[0]) + ' E ' + str(popt1[1]) + ' sigma ' + str(popt1[2]) + '\n')


build(begining_intensity, 1)
plt.xlabel('E, keV')
plt.show()
