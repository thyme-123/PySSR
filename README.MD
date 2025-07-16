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
git clone https://github.com/
cd PySSR
./install.bat
```
### **Linux**
```shell
git clone https://github.com/
cd PySSR
chmod +x install.sh
bash ./install.sh
```
## **Usage Instructions**
### **SSR Merge**
This feature is implemented in the **"ssr repair"** window, the input and output are shown below:

#### **Path input area**
- nav path: Navigation data path input box
- ssr path: SSR data path input box
- sp3 path: out SP3 file path input box
- clk path: out Clock file path input box
- atx path: ATX antenna data path input box

#### **Option area**
- no ssr​​: Disable SSR data option checkbox
- pco: Phase center offset correction option checkbox

#### **Control button**
- start: Start processing button
- end: End processing button

#### **Instructions for use**
- Users can enter broadcast ephemeris data in the **"nav path"** and SSR corrections in BNC format in the **"ssr path"** (if “no ssr” is not selected).
- Users specify the output sp3 file and clk file via **"sp3 path"** and **"clk path"**.
- If the user selects **"no ssr"** mode, the software will only read the broadcast ephemeris to calculate the satellite's orbit and clock offset.
- If the user selects **"pco"** mode, the software will use the antenna file entered by the user in **"atx path"** to correct the antenna phase center of the SSR.

### **SSR Merge**