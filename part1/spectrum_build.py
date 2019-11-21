from scipy import exp
from parse import ParseThings
import numpy as np
from matplotlib import pyplot as plt

# Maybe better to use maps (no problems with ranges) ???
        # Define arguments

class SpectrumBuild:

    def __init__(self, args):
        self.lines = args.lines
        self.background = args.background
        self.e_max = args.e_max
        self.number_of_chanels = args.chanels_num
        self.e0 = args.E0
        self.time = args.time
        self.background_intensity = args.background_intensity

    def build(spectrum):
        spectrum = np.array(spectrum)
        x = np.arange(len(spectrum))
        plt.plot(x, spectrum, 'ro')
        plt.show()


    def FwhmToSigma(fwhm):
        return fwhm / 2.355

    def gaussian(x, A, mean, sigma):
              return A * np.exp(- np.power((x - mean), 2.) / (2 * np.power(sigma, 2)) )

    def getChanelFromEnergy(number_of_chanels, E, E_max, delta_E):
        if (E + delta_E >= E_max):
            return -999
        return int( ( (E + delta_E) * number_of_chanels ) // E_max )

    def getEnergyFromChanel(number_of_chanels, chanel_num, E_max, delta_E):
        return float(chanel_num * E_max / number_of_chanels - delta_E)

    def backgroundFunction(x, par):
        return par[0] * exp( - par[1] * x) + par[2] + par[3] * x

    args = ParseThings().parse()

    width_and_statistics = [0] * args.chanels_num

    print(args)

    # Clear (physical) spectrum
    def clearPeaks():
        clear = [0] * args.chanels_num
        for line in args.lines:
            chanel_num = getChanelFromEnergy(args.chanels_num, line[0], args.e_max, args.E0)
            if chanel_num != -999:
                clear[chanel_num] = line[1] * args.time
        return clear

    # Spectrum + background
    def clearBackground():
        clear_background = [0] * args.chanels_num
        for chanel_num in range(args.chanels_num):
            energy = getEnergyFromChanel(args.chanels_num, chanel_num, args.e_max, args.E0)
            clear_background[chanel_num] = backgroundFunction(energy, args.background) * args.time * args.background_intensity
        return clear_background

    # Spectrum need to be an ineteger numbers ??!!!
    # OPTIMIZE???!!!
    def widthPeaks():
        width = [0] * args.chanels_num
        for line in args.lines:
            for chanel in range(args.chanels_num):
                x_0 = line[0]
                energy = getEnergyFromChanel(args.chanels_num, chanel, args.e_max, args.E0)
                # Calculate amplitude of Gauss function asuming that intensity should be the same as before
                # That's mean integrals should be same
                amplitude = line[1] * args.time / ( np.sqrt(2 * np.pi) * FwhmToSigma(line[2]) )
                width[chanel] += gaussian( energy, amplitude, x_0, FwhmToSigma(line[2]) )
        return width

    def widthPeaks2():
        a0 = 0.1
        a1 = 0.1
        width = [0] * args.chanels_num
        for line in args.lines:
            for chanel in range(args.chanels_num):
                x_0 = line[0]
                energy = getEnergyFromChanel(args.chanels_num, chanel, args.e_max, args.E0)
                # Calculate amplitude of Gauss function asuming that intensity should be the same as before
                # That's mean integrals should be same
                amplitude = line[1] * args.time / ( np.sqrt(2 * np.pi) * FwhmToSigma(line[2]) )
                width[chanel] += gaussian( energy, amplitude, x_0, a0 + a1 * np.sqrt(line[0]) )
        return width

    def statisticDistribution(ar):
        for i in range(len(ar)):
            if (ar[i] > 10):
                ar[i] = np.random.poisson(ar[i], 1)
            else:
                ar[i] = np.random.normal(ar[i], np.sqrt(ar[i], 1))
        return ar

args = ParseThings().parse()
builder = SpectrumBuild(args)

clear = builder.clearPeaks()
clear_bck = builder.clearBackground()
width = builder.widthPeaks()
width2 = builder.widthPeaks2()
# build(clear)
builder.build(clear_bck)
result = np.array(width2) + np.array(clear_bck)
builder.build(result)
builder.build(builder.statisticDistribution(result))