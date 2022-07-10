# CommsSDR
This repository contains the files for using GNU Radio. Note: recordings are on [the drive](https://drive.google.com/drive/u/0/folders/1DGIPAhoZ6jmICI5QIeB0iDCdUGhm7tkY) due to large file sizes.

## Setup
### GNU Radio
[Install GNU Radio on Linux](https://wiki.gnuradio.org/index.php/InstallingGR)

### GR Satellites
[Install gr-satellites](https://github.com/daniestevez/gr-satellites). Using their [documentation](https://gr-satellites.readthedocs.io/en/latest/).

If built from source and you are having issues with gr satellites blocks after updating, run the building and installing section of the documentation again.
### Osmocom
[Install Osmocom](https://osmocom.org/) for getting the data from the HackRF to GNURadio.

### Python 3
Python 3 is required to run the GNURadio programs.
If you have an issue with modules not found, execute the lines in the terminal in addPythonPaths.txt with the correct file locations for gr-satellites.

## Folders:
### Rx
This folder contains GNURadio files for receiving radio messages. Currently it is set to receive at 145 MHz. It saves recordings and output files to /output. It will show the waterfall/frequency spectrum in a window.

### WavProcessing
This folder contains files for reading Wav files.

### Examples
Examples that Iris did not create are put here.

## Test1SDR.grc
Test1SDR.grc is the current working GNU Radio Companion file. 
It relies on the [satellite decoder from GR Satellites](https://github.com/daniestevez/gr-satellites/tree/main/examples/satellite_decoder). 

