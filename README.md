# Shunsheng Integration Tool User Manual

The tool currently includes six functional modules: planning tools, power verification, interoperability verification, Excel processing, PDF processing and XML processing, and mainly integrates tools that are more in demand for on-site use.

Computer version requirements: Win7 or above 64-bit system


## 一、Login and registration module

You need to register before logging in. You can change the codes to set the authentication, i just use a db to recoed the email for the tools.
![image](https://github.com/user-attachments/assets/b68d38f9-d7b6-4e8a-9096-621246bd23c4)
![image](https://github.com/user-attachments/assets/d99694df-02b7-4cf7-88de-2e62ebc1cf26)







If you encounter the following error, it may be that the company email account has not been entered into the tool. 
You can change the codes to set the authentication

![image](https://github.com/user-attachments/assets/be2c8f03-cdf5-4423-8803-4a437609419a)



## 二、 Planning Module

### 2.1 PCI|TAC Planning

![image](https://github.com/user-attachments/assets/baa867fd-6c66-4e62-b0d2-295874df10c2)


1. Select the table to be planned: the table must be in .xlsx format, and the content format template is as follows:

![image](https://github.com/user-attachments/assets/649b5433-7c31-4a9f-9ee7-bbb30ff94539)


**PCINeeded: 0 means no PCI is planned; 1 means PCI is planned; **

CurrentPCI: PCI used by the cell at that time, **PCI used by the cell to be planned, just fill in a number, it cannot be left blank. **

TAC: TAC used by the cell at that time, TAC used by the cell to be planned, it can be left blank.

**Azimuth: The selection of the cell PCI mode is determined by the azimuth, so the azimuth must be filled in accurately. Indoor division is generally an omnidirectional antenna with an azimuth of 0. When multiple indoor division cells are planned for PCI at the same physical point, in order to avoid mode 3 interference, please manually adjust the indoor division azimuth**, such as: 3 cells are opened at one physical point, when planning PCI, the azimuth can be set to 0, 120, 240 respectively.

The file selection steps are as follows:

![image](https://github.com/user-attachments/assets/605a1731-eff7-4098-90c6-91ba8dbd1bd1)


2. Output result path:

 ![image](https://github.com/user-attachments/assets/bb159f92-2f6b-4cb5-92ec-1ede8a8ffc9c)


3. Output result table name: default value PCI planning table, can be modified.

4. PCI reuse distance: unit (meter), default value 3000, can be modified

5. PCI use start value and PCI use end value: LTE PCI 0~503, a total of 504, NR PCI 0~1007, a total of 1008, default value 0, 1007. Since some PCIs may be reserved for indoor distribution or special scenarios on site, the PCI use range is set to be modifiable during tool development, which is conducive to on-site adjustment according to actual conditions.

6. M0, M1, M2 azimuth starting value: To avoid mode 3 conflict, the PCI mode selection is determined according to the cell azimuth. Under normal circumstances (default value): 30060 degrees is mode 0, 60180 degrees is mode 1, and 180~300 degrees is mode 2. This value can also be adjusted. When adjusting, you only need to modify the starting value of the M0 azimuth. M1 and M2 will be automatically adjusted according to the value of M0, with an adjustment range of 120 degrees.

7. Prach reuse distance: unit (meter), default value 5000, can be modified.

8. Leading format: 839 (long format)/139 (short format), default value 839, can be modified.

9. Ncs: No need to fill in, this value is calculated based on the Prach reuse distance and leading format, and it can be automatically presented after execution.

10. Recipient email: optional. Fill in the format: [13866159657@139.com](mailto:13866159657@139.com)

11. Both formats can be used, and the two mailboxes are separated by **English commas**. (Currently, the company mailbox has not been sent successfully. When using it, please give priority to using 139 or 163 mailboxes)

#### 2.1.1 template

in the excel file 

### 2.2 Neighborhood Planning

![image](https://github.com/user-attachments/assets/8abd5776-8e82-46c6-bb5a-94ea0e25105a)


1. Select the table to be planned and the whole network engineering parameters: the table must be in .xlsx format, and the content format template is as follows: (the yellow columns are required, and the other columns are optional)

Select the table to be planned, content format:

![image](https://github.com/user-attachments/assets/caff88fc-3dc5-4556-8667-1ae92e83e3d3)


Select the whole network engineering parameters, content format:

![image](https://github.com/user-attachments/assets/e1ce1aa9-fca7-4acf-8a5d-1d748aa0551b)


Be sure to ensure the accuracy of latitude, longitude, azimuth, and TA. TA unit (meter), fill in the estimated cell coverage distance for TA in the planning table, and fill in the network management TA average for TA in the engineering parameter table.

The file selection steps are as follows:

![image](https://github.com/user-attachments/assets/51489ecc-2c25-428e-8054-f66391cb2888)
![image](https://github.com/user-attachments/assets/e4117279-3ba7-4bc0-9874-ebc979af126e)



2. Output result path:

![image](https://github.com/user-attachments/assets/98e5529f-fc67-4cd5-85fa-6ddfeed74a48)


   

3. Output result table name: default value Neighborhood planning table, which can be modified.

4. Planning cell coverage radius: It is the same concept as TA in the table to be planned. It is subject to the table and can be ignored here.

5. Strong correlation radius: unit (meter), default value 1000, neighboring cells within this range must be added, and this parameter can be modified according to actual conditions. For example: in dense urban areas, when there are too many surrounding sites, the priority of adding neighboring cells can be arranged according to the distance. The closer the distance, the higher the priority.

6. Discard radius: unit (meter), default value 5000, this parameter is opposite to the strong correlation radius. When the distance between two cells is greater than the parameter value, the neighboring cells are discarded.

7. Plannable overlap ratio: This parameter determines the position based on longitude and latitude, the direction based on azimuth, the coverage width based on half-power angle, and the coverage distance based on TA, and calculates the overlapping coverage area between the two cells. Overlap ratio = overlapping coverage area/neighborhood coverage area, the default value is 0.1, that is, when the overlapping coverage is lower than the parameter value, the neighboring cells are discarded.

8. Half-power angle correction parameter, TA correction parameter: Due to the complex wireless environment, the sector radiation range may be biased, so the correction parameter adjustment is set to make the planning result as accurate as possible. The default value is 1.5 and can be modified.

9. Recipient email: The description is the same as the PCI|TAC planning section.

#### 2.2.2 template



##  三、Power check

Select file: You can select multiple excel files;

Remove file: After selecting the file, you can use the button to remove it if you don’t need it;

Execute and save: After clicking, you will first select the save file path, and then directly execute the power check.

![image](https://github.com/user-attachments/assets/76d3bc70-3817-49fa-b51b-db1133f974df)


###  3.1 Power verification involves MOC table

| network management | System  | MOC                  | network management | System | MOC                       |
| ------------------ | ------- | -------------------- | ------------------ | ------ | ------------------------- |
| UME                | MIMO    | DUEUtranCellTDDLTE   | U31                | FDD    | ECellEquipmentFunction    |
| UME                | MIMO    | DUEUtranCellFDDLTE   | U31                | FDD    | EUtranCellFDD             |
| UME                | MIMO    | CUEUtranCellFDDLTE   | U31                | TDD    | ECellEquipmentFunctionTDD |
| UME                | MIMO    | CUEUtranCellTDDLTE   | U31                | TDD    | EUtranCellTDD             |
| UME                | MIMO    | ECellEquipFuncFDDLTE | U31                | FDD    | ECellEquipFuncFDDLTE      |
| UME                | MIMO    | ECellEquipFuncTDDLTE | U31                | TDD    | ECellEquipFuncTDDLTE      |
| UME                | MIMO/NR | SectorFunction       | U31                | FDD    | EUtranCellFDDLTE          |
| UME                | MIMO/NR | AauTxRxGroup         | U31                | TDD    | EUtranCellTDDLTE          |
| UME                | MIMO/NR | PrruTxRxGroup        | U31                | SDR    | RfDevice                  |
| UME                | MIMO/NR | IrRruTxRxGroup       | U31                | SDR    | BpDevice                  |
| UME                | NR      | NRSectorCarrier      | U31                | NB     | ECellEquipmentFunctionNB  |
| UME                | NR      | PowerControlDL       | U31                | NB     | CarrierNB                 |
| UME                | NR      | CPList               | U31                | GSM    | GCellEquipmentFunction    |
| UME                | NR      | NRCarrier            | U31                | GSM    | GCell                     |
| UME                | MIMO/NR | BpPoolFunction       | UME                | NR     | NRCellDU                  |
| UME                | MIMO/NR | ReplaceableUnit      | UME                | NR     | CarrierDL                 |
| UME                | MIMO/NR | RfLink               |                    |        |                           |

###  3.2 Equipment rated power and verification standards

The contents of rated power.xlsx and standard.xlsx in the **MyRS** file under the tool path can be modified according to the format in the template.

Rated power is the rated power of RRU or AAU; standard is the power verification standard (currently only the 5G verification standard of Jiangsu Province is used for judgment based on equipment power. If other judgment conditions are required on site, feedback is required to adjust the tool)

![image](https://github.com/user-attachments/assets/d31a2816-ae27-4e3d-af3a-133adbb53d86)




### 3.3 Equipment power calculation method

1. RRU power calculation of FDD common mode:

Take the 4-channel * 40W RRU of FDD1800 as an example:

The RRU power of FDD is evenly distributed. Without considering 2G: open a few channels and the maximum transmit power can be configured to the maximum value, that is, 40W for 1 channel, 80W for 2 channels, and 160W for 4 channels;

Considering 2G:

Use (40W-2G maximum channel transmit power) * 4 to get the maximum transmit power that can be configured for FDD1800, such as:

2G is configured as 2 channels, 1 channel is 10W, 4 channels are 20W, then the maximum power that can be configured for FDD1800 when 4 channels are configured is:

(40W-20W) * 4 = 80W;

2. Summarize LTE power calculation based on common mode RRU power calculation, **Calculate RRU power margin in units of RRU channels**:

1) Calculate the number of channels referenced by baseband resources

Use the location of the number 1 in the baseband resource table—TDD (uplink activation antenna bitmap); FDD (downlink antenna configuration mapping bitmap) to determine the RRU transmission channel

2) Calculate the maximum power that can be transmitted by the RRU channel referenced by the baseband resources

(single channel rated power - gsm & NB usage power) * number of channels (or cumulative sum). Generally, the rated power of a channel under a baseband resource is consistent. To avoid inconsistency, the calculation formula is optimized to **min(channel 1-** **gsm&NB**** power usage, channel 2-** **gsm&NB**** power usage...)\*number of channels

3) Calculate the total 4G power usage of each RRU channel and add them up (mainly for multi-carrier scenarios)

4) Calculate the power margin W

Baseband resources refer to the maximum power that can be sent by the RRU channel-sum(channel 1_4G power usage, channel 2_4G power usage...) --- This calculation method is not reflected in the tool

5) Calculate the power margin W that can be increased

**Baseband resources refer to the maximum power that can be sent by the RRU channel-max(channel 1_4G total power usage, channel 2_4G total power usage...) \*number of channels**

————————————————————————————————————

3、The difference is illustrated by an example: assuming a 4-channel RRU 4*20W, 2 cells are opened, and cell A quotes the 1st and 4th channel transmit power network management configuration of 20W (channel power is average, that is, network management power/number of channels used) and cell B quotes 10W of transmit power network management configuration. According to the above configuration, 10W of power is available in channel 4 of cell A, but channel 1 is fully configured. In this case, the network management quotes the remaining power of the RRU channel as 10W, and the power of cell A cannot be increased. The actual power margin of the RRU device is 50W (channels 2 and 3 are not used).

![image](https://github.com/user-attachments/assets/08f579d5-958e-4f88-b488-fcd97de8721f)


 

##  四、Interoperability Verification

The interoperability verification interface is the same as the power verification interface. Currently, only data exported by the 4G network management ICM is supported.

### 4.1 Related parameters

| MOC                                                          | parameter                          |
| ------------------------------------------------------------ | ---------------------------------- |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | MOI                                |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | SubNetwork                         |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | MEID                               |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | ENBFunctionTDD/ENBFunctionFDD      |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | userLabel                          |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | cellLocalId                        |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | pci                                |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | tac                                |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | bandIndicator/freqBandInd          |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | earfcn/earfcnDl                    |
| EUtranCellTDD/EUtranCellFDD/EUtranCellFDDLTE/EUtranCellTDDLTE | bandWidth/bandWidthDl              |
| EUtranCellMeasurementTDD/EUtranCellMeasurement/EUtranCellMeasFDDLTE/EUtranCellMeasTDDLTE | MOI                                |
| EUtranCellMeasurementTDD/EUtranCellMeasurement/EUtranCellMeasFDDLTE/EUtranCellMeasTDDLTE | eutranMeasParas_interCarriFreq     |
| EUtranCellMeasurementTDD/EUtranCellMeasurement/EUtranCellMeasFDDLTE/EUtranCellMeasTDDLTE | refCellMeasGroup                   |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | MOI                                |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | selQrxLevMin                       |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | qrxLevMinOfst                      |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | qhyst                              |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | snonintrasearch                    |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | threshSvrLow                       |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | cellReselectionPriority            |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | intraQrxLevMin                     |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslPara_interReselPrio       |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslPara_interThrdXLow        |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslPara_interThrdXHigh       |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslPara_interQrxLevMin       |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslPara_interCarriFreq       |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslParaExt_interReselPrioExt |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslParaExt_interThrdXLowExt  |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslParaExt_interThrdXHighExt |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslParaExt_interQrxLevMinExt |
| EUtranReselectionTDD/EUtranReselection/EUtranReselectionTDDLTE/EUtranReselectionFDDLTE | eutranRslParaExt_interCarriFreqExt |
| UeEUtranMeasurementTDD/UeEUtranMeasurement/UeEUtranMeasurementLTE | MOI                                |
| UeEUtranMeasurementTDD/UeEUtranMeasurement/UeEUtranMeasurementLTE | measCfgIdx                         |
| UeEUtranMeasurementTDD/UeEUtranMeasurement/UeEUtranMeasurementLTE | eventId                            |
| UeEUtranMeasurementTDD/UeEUtranMeasurement/UeEUtranMeasurementLTE | thresholdOfRSRP                    |
| UeEUtranMeasurementTDD/UeEUtranMeasurement/UeEUtranMeasurementLTE | a5Threshold2OfRSRP                 |
| CellMeasGroupTDD/CellMeasGroup/CellMeasGroupLTE              | MOI                                |
| CellMeasGroupTDD/CellMeasGroup/CellMeasGroupLTE              | closedInterFMeasCfg                |
| CellMeasGroupTDD/CellMeasGroup/CellMeasGroupLTE              | openInterFMeasCfg                  |
| CellMeasGroupTDD/CellMeasGroup/CellMeasGroupLTE              | interFHOMeasCfg                    |

### 4.2 ICM creates templates for easy daily export

Note: You can import only the 41 parameters you need to reduce the amount of data and improve tool operation efficiency.

## 五、Excel Processing

### 5.1 Excel Split

The split function is divided into split by content and split by number.

Split by content: After selecting a column, split it by the value of the column, and each value is an Excel table

Split by number: Split the Excel table into Excel tables with a fixed number of rows

![image](https://github.com/user-attachments/assets/d5375b31-900f-4425-b68f-2744f31d2700)


### 5.2 excel Merge

Merge the selected excel sheets. Note: If you want to merge sheets with the same name, you need to select the button (merge the sheets with the same worksheet name in each file into one sheet)

![image](https://github.com/user-attachments/assets/db6bcb08-4ca5-41dd-8b01-19bc4fe43e85)


### 5.3 row-column conversion

After selecting the Excel table, all the columns in the Excel table will be automatically displayed, and the columns that do not need to be transferred will be removed:

![image](https://github.com/user-attachments/assets/81058186-a283-4192-bd30-cb3a0912f007)


Left side: Select the column to be used as index

Right side: Select the column to be converted from row to column or column to row (**When converting from row to column, only one column can be selected on the right side, when converting from column to row, multiple columns can be selected on the right side**)




##  六、PDF Processing
![image](https://github.com/user-attachments/assets/eb5e2df8-868f-4b0c-bf39-5d3884394d27)



###  6.1 PDF Merge

Reference excel merge.

### 6.2 PDF Split

The default split step is 10, which means every 10 pages are split into 1 PDF file. It can be modified.

### 6.3 PDF to Word

PDF to Word sets three conversion modes: default (split all), split according to the starting page, and split on fixed pages.

1. Split all: default, that is, the conversion start page number and conversion end page number are not set, and conversion by fixed number of pages is not selected (hollow point)

2. Split by starting page: set the conversion start page number and conversion end page number, and conversion by fixed number of pages is not selected (hollow point)

3. Split on fixed pages: select conversion by fixed number of pages (solid), and set the page number to be converted, and the page numbers are separated by commas in English

## 七、xml Processing

###  7.1 xml to excel

Since the format of each XML content is not fixed, currently only the XML in the northbound configuration data format reported by ZTE network management is supported. All parameters in the XML can be converted to Excel for storage.

![image](https://github.com/user-attachments/assets/3055d470-bfe5-490e-8218-f8709213aa2a)


The xml content format is as follows:

![image](https://github.com/user-attachments/assets/9346de88-79eb-4c05-b10a-389db40cda96)


## 八、Conclusion

Later, relevant functions can be added according to the needs of the site to solve the actual needs of the site and improve office efficiency. If you encounter related problems or areas that need improvement during use, please contact us in time for optimization and adjustment. Contact information: zhangdaye@shunscom.com
