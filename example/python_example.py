import matplotlib.pyplot as plt
from spectrometer import Spectrometer


if __name__ == '__main__':
    wrapper = Spectrometer()
    num_open = wrapper.openAllSpectrometers()

    spectrometerIndex = 0
    channelIndex = 0
    integrationTime = 1
    wrapper.setIntegrationTime(spectrometerIndex, channelIndex, integrationTime)

    pixels = list(wrapper.getSpectrum(spectrometerIndex, channelIndex))
    wavelengths = list(wrapper.getWavelengths(spectrometerIndex, channelIndex))

    plt.plot(wavelengths, pixels)

    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (pixels)')
    plt.savefig("test.png")
    plt.show()


