
#############################################################
#    MIT License                                            #
#    Copyright (c) 2017 Yuta KItagami                       #
#############################################################
from PyMCP2221A import PyMCP2221A

import time
#print('-'*50)
#print('MCP2221(A) with MCP9808 ')
#print('-'*50)
#mcp2221 = PyMCP2221A.PyMCP2221A()
#mcp2221.Reset()
mcp2221 = PyMCP2221A.PyMCP2221A()

usbdata=[0] * 6
usbdata[0] = 0x05
#usbdata[1] = 0x05
addressdata=[0] * 2

mcp2221.I2C_Init()

print()

#Point to resolution register
#usbdata[0] = 0x08
#usbdata[0] = 0x03
#mcp2221.I2C_Write(0x18,usbdata)

#Setting resolution at 0.625 as per the datasheet page 29
usbdata[0] = 0x08
usbdata[1] = 0x03
mcp2221.I2C_Write(0x18,usbdata)
resolution = mcp2221.I2C_Read(0x18,1)
#print("Resolution Data: " + str(resolution))

#check that the chip has the right Manfucaturer data, MCP9804 should be 0x54 or 84 in DEC
addressdata[0] = 0x06
mcp2221.I2C_Write(0x18,addressdata)
mfgdata = mcp2221.I2C_Read(0x18,3)
#print("MFG Data: " + str(mfgdata))

# Point to temperature register and read temperature data
##addressdata[0] = 0x00
addressdata[0] = 0x05
mcp2221.I2C_Write(0x18,addressdata)

rdata = mcp2221.I2C_Read(0x18,2)

#Below is the dataconversion datasheet looks like C but i have "ported" it to Python

#print("Read Data: " + str(rdata))
uppertempbyte = rdata[0]
#Zeroing Alert Bits.
#print("Read Data Upper pre mask " + str(uppertempbyte))
uppertempbyte = uppertempbyte & 0x1f
#print("Read Data Upper post mask: " + str(uppertempbyte))
lowertempbyte = rdata[1]

if ((uppertempbyte & 0x10) == 0x10):
   uppertempbyte = uppertempbyte & 0x0f
   tempperatureminus = 256 - ( uppertempbyte * 16 + lowertempbyte /16)
   print("Temperature: " + str(tempperatureminus))
else:
   tempperatureplus = ( uppertempbyte * 16 + lowertempbyte /16)
  # alternatetemperatureplus = (lowertempbyte<<4)
  # alternatetemperatureplus = alternatetemperatureplus>>8

 #  print("Alternate Positive Temperature: " + str(alternatetemperatureplus))

   print("Temperature: " + str(tempperatureplus))

# At ~23c i get a positive temp of 6.375



#print("Read Data Upper: " + str(uppertempbyte))
#print("Read Data Lower: " + str(lowertempbyte))

