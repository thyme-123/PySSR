# **PySSR**
## **Introduction**
This Python toolbox is designed for broadcast ephemeris merging and SSR data integration. The key features of the software are as follows:

- Data merging capability that combines broadcast ephemeris with archived SSR data and outputs them as CLK files compliant with SP3 and RINEX3 formats.

- Orbit/clock comparison tools for analyzing accuracy differences between two SP3 files, with built-in integrity verification.

- Visualization support that automatically saves comparison results in multiple image formats.

- Real-time data integration based on pyrtcm for streaming SSR corrections
## **Install**
### **window**
```shell
git clone https://github.com/thyme-123/PySSR
cd PySSR
./install.bat
```
### **Linux**
```shell
git clone https://github.com/thyme-123/PySSR
cd PySSR
chmod +x install.sh
bash ./install.sh
```
## **Run**
### **window**
#### **Python script**
```shell
python ./main.py
```
### **Linux**
#### **Python script**
```shell
python ./main.py
```
#### **Executable file**
```shell
chmod +x ./PySSR
./PySSR
```

## **Usage Instructions**
### **SSR Merge**
This feature is implemented in the **"ssr repair"** window, the input and output are shown below:

#### **Path input area**
- nav path : Navigation data path input box
- ssr path : SSR data path input box
- sp3 path : out SP3 file path input box
- clk path : out Clock file path input box
- atx path : ATX antenna data path input box

#### **Option area**
- no ssr : Disable SSR data option checkbox
- pco : Phase center offset correction option checkbox

#### **Control button**
- start : Start processing button
- end : End processing button

#### **Instructions for use**
- Users can enter broadcast ephemeris data in the **"nav path"** and SSR corrections in BNC format in the **"ssr path"** (if **"no ssr"** is not selected).
- Users specify the output sp3 file and clk file via **"sp3 path"** and **"clk path"**.
- If the user selects **"no ssr"** mode, the software will only read the broadcast ephemeris to calculate the satellite's orbit and clock offset.
- If the user selects **"pco"** mode, the software will use the antenna file entered by the user in **"atx path"** to correct the antenna phase center of the SSR.

### **Precision Analysis**
This feature is implemented in the **"diff plot"** window, the input and output are shown below:

#### **Path input area**
- input sp3 path : Paths of SP3 files
- template sp3 path : Paths of SP3 files
- nav path : Navigation data path input box
- img path : The output path of the image

#### **Option area**
- X : Checkbox for the output in the X direction
- Y : Checkbox for the output in the Y direction
- Z : Checkbox for the output in the Z direction
- 3D : Checkbox for the output in the 3D direction
- R : Checkbox for the output in the R direction
- A : Checkbox for the output in the A direction
- C : Checkbox for the output in the X direction
- CLK : Checkbox for the output in the clock difference , default output clock difference STD
- GPS : The checkbox output from the GPS system
- GAL : The checkbox output from the Galileo system
- GLO : The checkbox output from the Glonass system
- DBS : The checkbox output from the BeiDou system

#### **Control button**
- start : Start processing button

#### **Instructions for use**
- Users can enter different SP3 file in **"input sp3 path"** and **"template sp3 path"**.
- Users can enter broadcast ephemeris data in the **"nav path"** used to calculate satellite speed.
- Users need to enter the path to export the picture in the **"img path"**
#### **Note**
We believe that when comparing the clock error of different analysis centers, it is necessary to eliminate the radial error, and there is a fixed system error for each satellite, and there is a system error between all satellites, so we use the following formula to analyze the clock error of different analysis centers.

$$ \Delta clk^{epoch,prn}=clk_{input}^{epoch,prn} - clk_{tempalte}^{epoch,prn} -\frac{diffRadial_{input,template}^{epoch,prn}}{c}\tag 1 $$

In Equation 1, **_input_** and **_template_** represent the two different broadcast ephemeris of the input, **_prn_** represents the satellite number, **_epoch_** represents the epoch, **_diffRadia_** represents the coordinate error in the direction of Radia, and **_c_** represents the speed of light.

Based on this, we use Equation 2 to calculate the average of the errors of a single satellite as the systematic error of the satellite.

$$ error_{prn}=\frac{\sum\limits_{epoch}^{epochs}clk^{peoch,prn}}{\sum\limits_{epoch}^{epochs}1}\tag 2 $$

Then, we calculate the average of the satellite system errors of different satellites for each epoch using Equation 3 as the systematic error of the epoch.

$$error_{epoch}=\frac{\sum\limits_{prn}^{prns}clk_{epoch,prn}-error_{prn}}{\sum\limits_{prn}^{prns}1} \tag 3$$

Finally, we calculate the satellite clock difference for the satellites of different analysis centers using Equation 4.

$$ \Delta clkPre^{epoch,prn}=clk^{epoch,prn}-error_{prn}-error_{epoch} \tag 4$$

### **Real Time Data**

This feature is implemented in the **"rt data"** window, the input and output are shown below:

#### **Path input area**

- url : Host on the ntrip server
- port : Port on the ntrip server
- username : Username on the ntrip server
- passwrod : Passwrod on the ntrip server
- out : The output path

#### **Control button**

- start : Start processing button
- end : End processing button

#### **Instructions for use**

- Frist, Users need to fill in the server connection information (URL, Port, username, and password)
- Second, select the mount point for the broadcast ephemeris (Only RTCM 1019, 1020, 1045, and 1042 are supported)
- Then, select the SSR correction mount point (only RTCM 1060, 1066, 1243, and 1261 are supported)
- Finally, click the start button to start receiving, and it will output sp3, clk, rnx, ssr files in the path specified in the **"out"** input box

### **Integrity Testing**

This feature is implemented in the **"integrity"** window, the input and output are shown below:

#### **Path input area**

- input sp3/ssr : SP3 or SSR files that need to be detected
- step : Port on the ntrip server
- img path : Username on the ntrip server

#### **Control button**

- start : Start processing button

#### **Instructions for use**

- Users need to enter the SP3 or SSR file, specify the time interval of the file, and the software will output the Gantt chart of the completeness rate and the completeness rate statistics to the folder specified in the **"img path"** input box.