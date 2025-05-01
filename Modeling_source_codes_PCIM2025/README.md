# Information
SiC MOSFET Device Modeling Tools; Ver 1.0

Date : 2025/03/21

Author : Kazuki MATSUMOTO, Hajime Takayama (Kyoto Institute Technology)

Contact information (replace <%%> with @):
- Hajime Takayama (hajime-takayama <%%> kit.ac.jp)

**Important Note:**
When you use this program, please refer to the paper as shown below and cite it in your work. The program is provided as is, and the authors are not responsible for any damages or issues that may arise from its use.

The paper can be found at [IEEE Xplore](URL not available at this moment).

The bibliographic information is as follows:
(not available at this moment.)

# Features

The program source codes and sample data for SiC power MOSFET modeling are provided as the supplemental materials for our paper presented at PCIM2025, entitled "Accurate Power MOSFET Modeling using Off-the-shelf Instruments."

The device model is composed of 4 elements; the three internal capacitance models (gate-source, gate-drain, drain-source) and two current models (drain current, body diode current). 

To use them, You need to perform four kinds of different experiments using two switching test circuits, namely the Double pulse circuit and Drain-pulsed circuit.
The sample data is provided, located in ./data/ .


Device under test is [SCT2160KE, ROHM Co., Ltd.](https://www.rohm.co.jp/products/sic-power-devices/sic-mosfet/sct2160ke-product). 


# Requirment
## Python version
Python 3.12.1
## Python libraries
```bash
pandas: 2.2.2
numpy: 1.26.4
matplotlib: 3.8.4
scipy: 1.13.0

os: built-in
random: built-in
time: built-in
sys: built-in
re: built-in
csv: built-in
datetime: built-in
```

# Installtion
To install this libraries, enter below code at your console.
```bash
pip install pandas numpy matplotlib scipy
```

Open .\Sample_PCIM in the working space.

Change file pathes of programs in function main();
```bash
Qgs_and_Qgd.py
Qds.py
Id-Vds
│  meas_vs_model.py
│  process_and_save_rms.py
│  sa.py
Idiode-Vds
│  meas_vs_model.py
│  process_and_save_rms.py
│  sa.py
```

"Qgs_and_Qgd.py" and "Qds.py" execute to read csv file and fit capacitance parameters.

Parameters are written to output file; "Qgs_and_Qgd_results.txt" or "Qds_results.txt".


<br>

Directory; "Id-Vds" and "Idiode-Vds" include programs which first reads the csv files and then perform fitting of the current-model parameters.

"current.py" include current caluclation function and cost function.

"data_loader.py" include function that read csv file.

You need setting "Vgs_list" in "data_loader.py" following the csv file name. NOT auto reading.

"RMS.py" caluclate RMS.

[Run Python] "process_and_save_rms.py" change experimental csv file to format csv file.

[Run Python] "sa.py" fit current parameters.

[Run Python] "meas_vs_model.py" make graph; measurment vs model.



# Tree of Directory and File
```bash
Sample_PCIM
├─program
│  │  Qgs_and_Qgd.py
│  │  Qds.py
│  │
│  ├─Idiode-Vds
│  │  │  current.py
│  │  │  meas_vs_model.py
│  │  │  data_loader.py
│  │  │  sa.py
│  │  │  process_and_save_rms.py
│  │  │  RMS.py
│  │  │
│  │  └─__pycache__
│  │          data_loader.cpython-310.pyc
│  │          current.cpython-310.pyc
│  │          RMS.cpython-310.pyc
│  │
│  └─Id-Vds
│      │  sa.py
│      │  RMS.py
│      │  process_and_save_rms.py
│      │  meas_vs_model.py
│      │  current.py
│      │  data_loader.py
│      │
│      └─__pycache__
│              current.cpython-310.pyc
│              data_loader.cpython-310.pyc
│              RMS.cpython-310.pyc
│
└─data
    │  Qg_Vgs=20_Vdd=100_000_ALL.csv
    │  Qds_results.txt
    │  Qds_Vgs=20_Vdd=100_000_ALL.csv
    │  Qgs_and_Qgd_results.txt
    │
    ├─Id-Vds
    │  │  Id_results.txt
    │  │  rms_results.csv
    │  │
    │  ├─Vgs=6.00
    │  │      Vdd=90.00_ALL.csv
    │  │      Vdd=18.00_ALL.csv
    │  │      Vdd=98.00_ALL.csv
    │  │      Vdd=32.00_ALL.csv
    │  │      Vdd=94.00_ALL.csv
    │  │      Vdd=16.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=50.00_ALL.csv
    │  │      Vdd=52.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=68.00_ALL.csv
    │  │      Vdd=70.00_ALL.csv
    │  │      Vdd=100.00_ALL.csv
    │  │      Vdd=82.00_ALL.csv
    │  │      Vdd=34.00_ALL.csv
    │  │      Vdd=42.00_ALL.csv
    │  │      Vdd=74.00_ALL.csv
    │  │      Vdd=80.00_ALL.csv
    │  │      Vdd=20.00_ALL.csv
    │  │      Vdd=24.00_ALL.csv
    │  │      Vdd=46.00_ALL.csv
    │  │      Vdd=26.00_ALL.csv
    │  │      Vdd=14.00_ALL.csv
    │  │      Vdd=36.00_ALL.csv
    │  │      Vdd=30.00_ALL.csv
    │  │      Vdd=76.00_ALL.csv
    │  │      Vdd=92.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=60.00_ALL.csv
    │  │      Vdd=48.00_ALL.csv
    │  │      Vdd=78.00_ALL.csv
    │  │      Vdd=88.00_ALL.csv
    │  │      Vdd=38.00_ALL.csv
    │  │      Vdd=12.00_ALL.csv
    │  │      Vdd=28.00_ALL.csv
    │  │      Vdd=54.00_ALL.csv
    │  │      Vdd=44.00_ALL.csv
    │  │      Vdd=66.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │      Vdd=40.00_ALL.csv
    │  │      Vdd=84.00_ALL.csv
    │  │      Vdd=58.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=96.00_ALL.csv
    │  │      Vdd=56.00_ALL.csv
    │  │      Vdd=22.00_ALL.csv
    │  │      Vdd=86.00_ALL.csv
    │  │      Vdd=72.00_ALL.csv
    │  │      Vdd=62.00_ALL.csv
    │  │      Vdd=64.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │
    │  ├─Vgs=10.00
    │  │      Vdd=64.00_ALL.csv
    │  │      Vdd=84.00_ALL.csv
    │  │      Vdd=52.00_ALL.csv
    │  │      Vdd=66.00_ALL.csv
    │  │      Vdd=80.00_ALL.csv
    │  │      Vdd=78.00_ALL.csv
    │  │      Vdd=92.00_ALL.csv
    │  │      Vdd=98.00_ALL.csv
    │  │      Vdd=60.00_ALL.csv
    │  │      Vdd=36.00_ALL.csv
    │  │      Vdd=56.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=46.00_ALL.csv
    │  │      Vdd=26.00_ALL.csv
    │  │      Vdd=12.00_ALL.csv
    │  │      Vdd=30.00_ALL.csv
    │  │      Vdd=50.00_ALL.csv
    │  │      Vdd=44.00_ALL.csv
    │  │      Vdd=16.00_ALL.csv
    │  │      Vdd=90.00_ALL.csv
    │  │      Vdd=48.00_ALL.csv
    │  │      Vdd=94.00_ALL.csv
    │  │      Vdd=68.00_ALL.csv
    │  │      Vdd=28.00_ALL.csv
    │  │      Vdd=38.00_ALL.csv
    │  │      Vdd=72.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=70.00_ALL.csv
    │  │      Vdd=34.00_ALL.csv
    │  │      Vdd=58.00_ALL.csv
    │  │      Vdd=82.00_ALL.csv
    │  │      Vdd=42.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=32.00_ALL.csv
    │  │      Vdd=76.00_ALL.csv
    │  │      Vdd=54.00_ALL.csv
    │  │      Vdd=62.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=22.00_ALL.csv
    │  │      Vdd=74.00_ALL.csv
    │  │      Vdd=86.00_ALL.csv
    │  │      Vdd=24.00_ALL.csv
    │  │      Vdd=20.00_ALL.csv
    │  │      Vdd=96.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=14.00_ALL.csv
    │  │      Vdd=100.00_ALL.csv
    │  │      Vdd=18.00_ALL.csv
    │  │      Vdd=88.00_ALL.csv
    │  │      Vdd=40.00_ALL.csv
    │  │
    │  ├─Vgs=12.00
    │  │      Vdd=60.00_ALL.csv
    │  │      Vdd=16.00_ALL.csv
    │  │      Vdd=34.00_ALL.csv
    │  │      Vdd=26.00_ALL.csv
    │  │      Vdd=64.00_ALL.csv
    │  │      Vdd=58.00_ALL.csv
    │  │      Vdd=94.00_ALL.csv
    │  │      Vdd=98.00_ALL.csv
    │  │      Vdd=28.00_ALL.csv
    │  │      Vdd=22.00_ALL.csv
    │  │      Vdd=100.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │      Vdd=74.00_ALL.csv
    │  │      Vdd=18.00_ALL.csv
    │  │      Vdd=92.00_ALL.csv
    │  │      Vdd=72.00_ALL.csv
    │  │      Vdd=38.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=36.00_ALL.csv
    │  │      Vdd=80.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=54.00_ALL.csv
    │  │      Vdd=48.00_ALL.csv
    │  │      Vdd=42.00_ALL.csv
    │  │      Vdd=40.00_ALL.csv
    │  │      Vdd=70.00_ALL.csv
    │  │      Vdd=78.00_ALL.csv
    │  │      Vdd=90.00_ALL.csv
    │  │      Vdd=52.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=46.00_ALL.csv
    │  │      Vdd=24.00_ALL.csv
    │  │      Vdd=62.00_ALL.csv
    │  │      Vdd=96.00_ALL.csv
    │  │      Vdd=76.00_ALL.csv
    │  │      Vdd=84.00_ALL.csv
    │  │      Vdd=50.00_ALL.csv
    │  │      Vdd=88.00_ALL.csv
    │  │      Vdd=32.00_ALL.csv
    │  │      Vdd=68.00_ALL.csv
    │  │      Vdd=86.00_ALL.csv
    │  │      Vdd=56.00_ALL.csv
    │  │      Vdd=20.00_ALL.csv
    │  │      Vdd=30.00_ALL.csv
    │  │      Vdd=66.00_ALL.csv
    │  │      Vdd=12.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=14.00_ALL.csv
    │  │      Vdd=44.00_ALL.csv
    │  │      Vdd=82.00_ALL.csv
    │  │
    │  ├─Vgs=20.00
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │
    │  ├─Vgs=16.00
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │
    │  ├─Vgs=8.00
    │  │      Vdd=70.00_ALL.csv
    │  │      Vdd=78.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=18.00_ALL.csv
    │  │      Vdd=26.00_ALL.csv
    │  │      Vdd=38.00_ALL.csv
    │  │      Vdd=72.00_ALL.csv
    │  │      Vdd=84.00_ALL.csv
    │  │      Vdd=22.00_ALL.csv
    │  │      Vdd=50.00_ALL.csv
    │  │      Vdd=20.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=32.00_ALL.csv
    │  │      Vdd=46.00_ALL.csv
    │  │      Vdd=68.00_ALL.csv
    │  │      Vdd=86.00_ALL.csv
    │  │      Vdd=82.00_ALL.csv
    │  │      Vdd=60.00_ALL.csv
    │  │      Vdd=92.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=14.00_ALL.csv
    │  │      Vdd=40.00_ALL.csv
    │  │      Vdd=16.00_ALL.csv
    │  │      Vdd=66.00_ALL.csv
    │  │      Vdd=34.00_ALL.csv
    │  │      Vdd=30.00_ALL.csv
    │  │      Vdd=42.00_ALL.csv
    │  │      Vdd=54.00_ALL.csv
    │  │      Vdd=98.00_ALL.csv
    │  │      Vdd=52.00_ALL.csv
    │  │      Vdd=28.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=80.00_ALL.csv
    │  │      Vdd=64.00_ALL.csv
    │  │      Vdd=88.00_ALL.csv
    │  │      Vdd=36.00_ALL.csv
    │  │      Vdd=58.00_ALL.csv
    │  │      Vdd=56.00_ALL.csv
    │  │      Vdd=74.00_ALL.csv
    │  │      Vdd=100.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=48.00_ALL.csv
    │  │      Vdd=62.00_ALL.csv
    │  │      Vdd=90.00_ALL.csv
    │  │      Vdd=76.00_ALL.csv
    │  │      Vdd=12.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │      Vdd=44.00_ALL.csv
    │  │      Vdd=24.00_ALL.csv
    │  │      Vdd=94.00_ALL.csv
    │  │      Vdd=96.00_ALL.csv
    │  │
    │  ├─Vgs=14.00
    │  │      Vdd=48.00_ALL.csv
    │  │      Vdd=98.00_ALL.csv
    │  │      Vdd=80.00_ALL.csv
    │  │      Vdd=30.00_ALL.csv
    │  │      Vdd=68.00_ALL.csv
    │  │      Vdd=84.00_ALL.csv
    │  │      Vdd=78.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=12.00_ALL.csv
    │  │      Vdd=60.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │      Vdd=36.00_ALL.csv
    │  │      Vdd=66.00_ALL.csv
    │  │      Vdd=54.00_ALL.csv
    │  │      Vdd=44.00_ALL.csv
    │  │      Vdd=82.00_ALL.csv
    │  │      Vdd=42.00_ALL.csv
    │  │      Vdd=92.00_ALL.csv
    │  │      Vdd=26.00_ALL.csv
    │  │      Vdd=76.00_ALL.csv
    │  │      Vdd=90.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=50.00_ALL.csv
    │  │      Vdd=18.00_ALL.csv
    │  │      Vdd=64.00_ALL.csv
    │  │      Vdd=38.00_ALL.csv
    │  │      Vdd=72.00_ALL.csv
    │  │      Vdd=32.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=34.00_ALL.csv
    │  │      Vdd=74.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=46.00_ALL.csv
    │  │      Vdd=58.00_ALL.csv
    │  │      Vdd=96.00_ALL.csv
    │  │      Vdd=62.00_ALL.csv
    │  │      Vdd=56.00_ALL.csv
    │  │      Vdd=52.00_ALL.csv
    │  │      Vdd=70.00_ALL.csv
    │  │      Vdd=16.00_ALL.csv
    │  │      Vdd=28.00_ALL.csv
    │  │      Vdd=88.00_ALL.csv
    │  │      Vdd=40.00_ALL.csv
    │  │      Vdd=86.00_ALL.csv
    │  │      Vdd=94.00_ALL.csv
    │  │      Vdd=22.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=14.00_ALL.csv
    │  │      Vdd=100.00_ALL.csv
    │  │      Vdd=20.00_ALL.csv
    │  │      Vdd=24.00_ALL.csv
    │  │
    │  ├─Vgs=4.00
    │  │      Vdd=20.00_ALL.csv
    │  │      Vdd=92.00_ALL.csv
    │  │      Vdd=16.00_ALL.csv
    │  │      Vdd=60.00_ALL.csv
    │  │      Vdd=58.00_ALL.csv
    │  │      Vdd=74.00_ALL.csv
    │  │      Vdd=42.00_ALL.csv
    │  │      Vdd=38.00_ALL.csv
    │  │      Vdd=8.00_ALL.csv
    │  │      Vdd=36.00_ALL.csv
    │  │      Vdd=14.00_ALL.csv
    │  │      Vdd=56.00_ALL.csv
    │  │      Vdd=34.00_ALL.csv
    │  │      Vdd=52.00_ALL.csv
    │  │      Vdd=0.00_ALL.csv
    │  │      Vdd=46.00_ALL.csv
    │  │      Vdd=28.00_ALL.csv
    │  │      Vdd=84.00_ALL.csv
    │  │      Vdd=30.00_ALL.csv
    │  │      Vdd=70.00_ALL.csv
    │  │      Vdd=6.00_ALL.csv
    │  │      Vdd=66.00_ALL.csv
    │  │      Vdd=72.00_ALL.csv
    │  │      Vdd=48.00_ALL.csv
    │  │      Vdd=26.00_ALL.csv
    │  │      Vdd=76.00_ALL.csv
    │  │      Vdd=98.00_ALL.csv
    │  │      Vdd=4.00_ALL.csv
    │  │      Vdd=82.00_ALL.csv
    │  │      Vdd=24.00_ALL.csv
    │  │      Vdd=40.00_ALL.csv
    │  │      Vdd=100.00_ALL.csv
    │  │      Vdd=10.00_ALL.csv
    │  │      Vdd=54.00_ALL.csv
    │  │      Vdd=12.00_ALL.csv
    │  │      Vdd=90.00_ALL.csv
    │  │      Vdd=64.00_ALL.csv
    │  │      Vdd=86.00_ALL.csv
    │  │      Vdd=78.00_ALL.csv
    │  │      Vdd=18.00_ALL.csv
    │  │      Vdd=88.00_ALL.csv
    │  │      Vdd=94.00_ALL.csv
    │  │      Vdd=68.00_ALL.csv
    │  │      Vdd=32.00_ALL.csv
    │  │      Vdd=80.00_ALL.csv
    │  │      Vdd=50.00_ALL.csv
    │  │      Vdd=62.00_ALL.csv
    │  │      Vdd=22.00_ALL.csv
    │  │      Vdd=44.00_ALL.csv
    │  │      Vdd=96.00_ALL.csv
    │  │      Vdd=2.00_ALL.csv
    │  │
    │  └─Vgs=18.00
    │          Vdd=8.00_ALL.csv
    │          Vdd=6.00_ALL.csv
    │          Vdd=0.00_ALL.csv
    │          Vdd=4.00_ALL.csv
    │          Vdd=2.00_ALL.csv
    │          Vdd=10.00_ALL.csv
    │
    └─Idiode-Vds
        │  rms_results.csv
        │  Idiode_results.txt
        │  Idiode_meas_vs_model.pdf
        │
        └─Vgs=0.00
                Vdd=10.00_ALL.csv
                Vdd=5.50_ALL.csv
                Vdd=0.00_ALL.csv
                Vdd=3.50_ALL.csv
                Vdd=13.00_ALL.csv
                Vdd=12.00_ALL.csv
                Vdd=0.50_ALL.csv
                Vdd=10.50_ALL.csv
                Vdd=8.50_ALL.csv
                Vdd=4.50_ALL.csv
                Vdd=3.00_ALL.csv
                Vdd=2.00_ALL.csv
                Vdd=6.00_ALL.csv
                Vdd=5.00_ALL.csv
                Vdd=7.50_ALL.csv
                Vdd=7.00_ALL.csv
                Vdd=12.50_ALL.csv
                Vdd=4.00_ALL.csv
                Vdd=8.00_ALL.csv
                Vdd=1.50_ALL.csv
                Vdd=11.50_ALL.csv
                Vdd=11.00_ALL.csv
                Vdd=9.00_ALL.csv
                Vdd=6.50_ALL.csv
                Vdd=1.00_ALL.csv
                Vdd=2.50_ALL.csv
                Vdd=9.50_ALL.csv
```