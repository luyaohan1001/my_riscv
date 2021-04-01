####################################################################################################
## A python script for parsing SystemVerilog Files
####################################################################################################
## Author: Luyao Han
## I read a lot of RTL design files and one of the challenges to look at a set of HDL files is
## that there are too much port names parameters involves. Thus I have constructed this parsing 
## struct that allows to convert all HDL files in a directory to dictionary structure.
## Thus allows the designer to extract out the macro parameters and understand a design more easily. 
## 
## Each SystemVerilog module declares with two sections: parameters and ports
## This script deals with each separately 
##  
## To run this program 
## $ cd <project_folder>/<RTL>
## $ ./parse_SystemVeriog.py | tee <output_log> 

import os
import re
import sys

# Constants
print_separator = "======================================================================="
print_separator_02 = "---------------------------------------------------\n"

# Current directory
curr_dir = os.getcwd() 
# Stores a dictionary modules_dict[<module>] = {<input_type>,<logic_type>,<width>,<port_name>}
modules_dict = dict()

#iterate all SystemVerilog (*.sv) files in current folder
for filename in os.listdir(curr_dir):
    if filename.endswith('.sv'):  #if filename.endswith('.v'):
        with open(os.path.join(curr_dir, filename)) as f:
            # sv_souce: contains all source code in each .sv file
            sv_source= f.read()


            ##### Step 1a. Get module definition: <string>
            regex_module_def = r"module(.*?);" # regex: <module ... ;>
            module_def_list = re.findall(regex_module_def, sv_source, re.DOTALL)
            if(len(module_def_list)>0):
                # Convert list to string
                module_def = str(module_def_list[0])
                # Remove all comments
                module_def = re.sub(re.compile("//.*?\n"),"", module_def)
                #print(module_def)

            '''
            module_def print example:
            
            "isp_uart #(
                parameter  UART_RX_CLK_DIV = 108,   // 50MHz/4/115200Hz=108
                parameter  UART_TX_CLK_DIV = 434    // 50MHz/1/115200Hz=434
            )(
                input  logic        clk,
                input  logic        i_uart_rx,
                output logic        o_uart_tx,
                output logic        o_rst_n,
                output logic [31:0] o_boot_addr,
                naive_bus.master    bus,
                naive_bus.slave     user_uart_bus
            )"
            '''





            ##### Step 1b. Get module name: <string>
            module_name = ""
            regex_module_name = r"module(.*?)\(" # regex: <module ... (>   
            module_name_list = re.findall(regex_module_name,sv_source, re.DOTALL)
            if(len(module_name_list)>0):
                # Convert list to string
                module_name = str(module_name_list[0])
                module_name = module_name.replace("#","")
                module_name = module_name.replace(" ","")
                #print("printing module name.....")
                #print(module_name)
    
            '''
            module_name print example:
                "isp_uart"
            '''




            ##### Step 1c. Get parameters snippet: <string>
            #print("printing parameters: ")
            regex_params = r"\#\((.*?)\)" # regex: <# ... )> 
            module_params = ""
            module_params_list = re.findall(regex_params, module_def, re.DOTALL)
            if(len(module_params_list)>0):
                module_params = str(module_params_list[0])
                module_params = module_params.replace("(","")
                module_params = module_params.replace("\)","")
                module_params = module_params.replace("\n","")
                module_params = module_params.replace("\t","")
            #split each parameter clause into an array
            module_params_arr = module_params.split(",")
            #print(module_params)
            #print(module_params_arr)
            '''
            module_params print example:
                "parameter  UART_RX_CLK_DIV = 108,parameter  UART_TX_CLK_DIV = 434"
            '''




            ##### Step 1d. Get ports definition snippet: <string>
            
            #print("printing ports: ")
            if(len(module_params) == 0):
                regex_ports = r"\(.*?\)"
            else:
                regex_ports = r"\)\(.*?\)"
            module_ports_list = re.findall(regex_ports, module_def, re.DOTALL)
            if(len(module_ports_list)>0):
                module_ports = str(module_ports_list[0])
                module_ports = module_ports.replace("(","")
                module_ports = module_ports.replace(")","")
                module_ports = module_ports.replace("\n","")
                module_ports = module_ports.replace("\t","")
                #print(module_ports)
            module_ports_arr = module_ports.split(",")
            #print(module_ports_arr)
            '''
            module_ports print example:
                "input logic clk,input logic i_uart_rx, output logic o_uart_tx, output logic o_rst_n,output logic [31:0] o_boot_addr,naive_bus.master bus, naive_bus.slave user_uart_bus"
            '''
            

            



            ################################################################################################
            ### Step 2. Parse each individual parameter attributes (name,width,value) of current module to an array 
            ################################################################################################
            param_attributes_arr = []
            param_width = ""
            for i,param in enumerate(module_params_arr):
                if(param != ""):

                    ### Get parameter name
                    regex_param_name = r"parameter(.*?)=" # regex: <parameter ... =)> 
                    param_name_list = re.findall(regex_param_name, str(param), re.DOTALL)
                    if(len(param_name_list) > 0):
                        # Collect param_attr = [<parameter/port>,<width>,<input_type>,<logic_type>,<param_name=value>]

                        param_attr = [] #an array for storing individual parameter declaration
                                        # for example, the result of "parameter  UART_RX_CLK_DIV = 108"

                        
                        param_attr.append("parameter")

                        # Step 2a. Get parameter name
                        param_name = str(param_name_list[0])
                        param_name = param_name.replace(" ","")
                        param = param.replace("parameter","")
                        #print(param_name)
                        
                        '''
                        param_name print example:
                            "UART_TX_CLK_DIV"
                        '''
                        
                        # Step 2b. Get and append width                 
                        # Width exists between "[", "]"
                        if "[" in param:
                            param_width = "" # if found then jettison the one from last param
                            regex_param_width = r"\[.*?\]" # regex: <[ ... ]>  
                            matches = re.findall(regex_param_width, param, re.DOTALL)
                            
                            # For 2D array there might be several matches, for example "[0:INSTR_CNT-1] [31:0]"" 
                            for match in matches:
                                param_width += str(match) 
                                param = param.replace(str(match),"") # deleted from the original string
                        else:
                            #if true, then not using width from the previously declared parameter
                            if("parameter" in param):
                                param_width = 1 # not specified, then automatically assuming 1
                        param_attr.append(param_width) #param_attr = [<input_type>,<logic_type>,<width>]



                        # Step 2c. Parameters should have no inout type
                        # param_attr = [<input_type>]
                        param_attr.append("NA") 

                        # Step 2d. Parameters should have neither be variable nor logic                   
                        # param_attr = [<input_type>,<logic_type>]
                        param_attr.append("NA") 
                                                 
                       

                        # Step 2e. Append name     
                        param_attr.append(param_name)
                        
                        # Step 2f. Append to the array that contains ALL other parameters for this module.
                        param_attributes_arr.append(param_attr)
                
















            ########################################################################
            ### Step 2b. Parse ports attributes (inout, logic type, width, name)into an array
            ########################################################################
            port_attributes_arr = []
            port_inout_type = "input"
            port_logic_type = "logic"
            port_width = ""
            
            for i,port in enumerate(module_ports_arr):
                if(port != ""):
                    #collect port_attributes = [<parameter/port>,<width>,<input_type>,<logic_type>,<port_name>]
                    port_attr = []

                    port_attr.append("port")

                    # Step 3a. Get and append width                 
                    # Width exists between "[" and "]"
                    if "[" in port:
                        port_width = "" #found then jettison the one from last port 
                        regex_port_width = r"\[.*?\]"
                        matches = re.findall(regex_port_width,port, re.DOTALL)
                        # For 2D array there might be several matches
                        for match in matches:
                            port_width += str(match)
                            port = port.replace(str(match),"")
                    else:
                        #if any exists then current port using attributes from last declared port
                        if ( ("input" in port) or ("output" in port) or ("inout" in port)):
                            port_width = 1
                    port_attr.append(port_width) # param_attr = [<input_type>,<logic_type>,<width>]


                    # Step 3b. Get input/output type
                    # param_attr = [<input_type>]
                    if "output" in port:
                        port_inout_type = "output"
                        port = port.replace("output","")
                    elif "input" in port:
                        port_inout_type = "input"
                        port = port.replace("input","")
                    elif "inout" in port:
                        port_inout_type = "inout"
                        port = port.replace("inout","")
                    #else: will use port_inout_type for the one specified for the previous
                    port_attr.append(port_inout_type) #param_attr = [<input_type>]


                    # Step 3c. Get logic/variable type                   
                    # param_attr = [<input_type>,<logic_type>]
                    if "logic" in port:
                        port_logic_type = "logic"
                        port = port.replace("logic","")
                    elif "variable" in port:
                        port_logic_type = "variable"
                        port = port.replace("variable","")                    
                    port_attr.append(port_logic_type)   #param_attr = [<input_type>,<logic_type>]

                 

                    # Step 3d. Append port name (what's left in the variable "port" after removing other attributes is the name)
                    # Get rid of space in the actual port name
                    port = port.replace(" ","")
                    port_attr.append(port) # param_attr = [<input_type>,<logic_type>,<width>,<name=value>]
                    
                    # Step 2e. Append to the array that contains ALL other ports for this module.
                    port_attributes_arr.append(port_attr)
                



            # Append to the dictionary that contains all modules and each modules' parameter and ports
            modules_dict[module_name] = param_attributes_arr +  port_attributes_arr

            #print(print_separator)
               

#make a folder for storing all the csv files for creating kicad library
if not os.path.exists("modules_csv"):
    os.mkdir("modules_csv")
os.chdir("modules_csv")


print("\n\n\n-----print all ports in all modules-----") 
for module_name,module_def in modules_dict.items():
    #write file name format <module_xxx>
    if(module_name != ""):
        write_file = "module_" + module_name + ".csv"
        os.system("touch " + write_file)
        print(module_name)

        with open(write_file, 'w') as f:

            #write module name on the first line
            f.write(module_name+"\n")
            f.write("Pin,Type,Name,Side" + "\n")
            
            
            #write entity (port or parameter) on each iterated lines
            for i,entity in enumerate(module_def):
                print(entity)

                if(entity[0] == "port"): #only ports are built into the symbol
                    if(entity[2] == "input"):
                        side = "left"
                    elif(entity[2] == "output"):
                        side = "right"

                    f.write(str(i+1) +","+ str(entity[2]) +"," +str(entity[4]) + "," + side + "\n" )
            print("\n")
            



for filename in os.listdir(curr_dir+"/modules_csv"):
    if filename.endswith(".csv"):
        print("generating symbol for module " + str(filename))
        os.system("kipart " + filename + " -a -o " + "sv_modules.lib")

