EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L automated_modules:core_alu U?
U 1 1 60690127
P 6850 2450
F 0 "U?" H 7850 2737 60  0000 C CNN
F 1 "core_alu" H 7850 2631 60  0000 C CNN
F 2 "" H 7050 2500 60  0001 L CNN
F 3 "" H 7050 2300 60  0001 L CNN
	1    6850 2450
	1    0    0    -1  
$EndComp
$Comp
L automated_modules:core_bus_wrapper U?
U 1 1 60690717
P 2350 2000
F 0 "U?" H 3500 2287 60  0000 C CNN
F 1 "core_bus_wrapper" H 3500 2181 60  0000 C CNN
F 2 "" H 2550 2050 60  0001 L CNN
F 3 "" H 2550 1850 60  0001 L CNN
	1    2350 2000
	1    0    0    -1  
$EndComp
$Comp
L automated_modules:core_id_segreg U?
U 1 1 60690BD3
P 4850 3700
F 0 "U?" H 6200 3987 60  0000 C CNN
F 1 "core_id_segreg" H 6200 3881 60  0000 C CNN
F 2 "" H 5050 3750 60  0001 L CNN
F 3 "" H 5050 3550 60  0001 L CNN
	1    4850 3700
	1    0    0    -1  
$EndComp
$Comp
L automated_modules:core_id_stage U?
U 1 1 60691DAD
P 6350 5100
F 0 "U?" H 7250 5387 60  0000 C CNN
F 1 "core_id_stage" H 7250 5281 60  0000 C CNN
F 2 "" H 6550 5150 60  0001 L CNN
F 3 "" H 6550 4950 60  0001 L CNN
	1    6350 5100
	1    0    0    -1  
$EndComp
$Comp
L automated_modules:core_regfile U?
U 1 1 60692809
P 9450 3650
F 0 "U?" H 10200 3937 60  0000 C CNN
F 1 "core_regfile" H 10200 3831 60  0000 C CNN
F 2 "" H 9650 3700 60  0001 L CNN
F 3 "" H 9650 3500 60  0001 L CNN
	1    9450 3650
	1    0    0    -1  
$EndComp
$Comp
L automated_modules:core_top U?
U 1 1 606931B4
P 2400 6250
F 0 "U?" H 4128 6103 60  0000 L CNN
F 1 "core_top" H 4128 5997 60  0000 L CNN
F 2 "" H 2600 6300 60  0001 L CNN
F 3 "" H 2600 6100 60  0001 L CNN
	1    2400 6250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 3900 4150 3900
Wire Wire Line
	4850 4000 4150 4000
Wire Wire Line
	4850 4100 4150 4100
Wire Wire Line
	4850 4200 4150 4200
Wire Wire Line
	4850 4300 4150 4300
Wire Wire Line
	4850 4400 4150 4400
Wire Wire Line
	4850 4500 4150 4500
Text Label 4150 3900 0    50   ~ 0
i_boot_addr
Text Label 4150 4000 0    50   ~ 0
~id_stall
Text Label 4150 4100 0    50   ~ 0
~id_read_disable
Text Label 4150 4200 0    50   ~ 0
ex_branch_jalr
Text Label 4150 4400 0    50   ~ 0
ex_branch_jalr_target
Text Label 4150 4300 0    50   ~ 0
id_jal
$EndSCHEMATC
