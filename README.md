## Programming 5 Lab 3 [![Online Demo](Images/Button.png)](https://wokwi.com/projects/475960292905546753)

## Table of Contents
[1.0 Introduction](#10-introduction)  
>[1.1 Purpose](#11-purpose)  
>[1.2 Overview](#12-overview)

[2.0 Initial Functionality Test](#20-initial-functionality-test)  
[3.0 Maintenance Instructions](#30-maintenance-instructions)  
[4.0 Final Functionality Test](#40-final-functionality-test)  
[5.0 Assessment](#50-assessment)  
[6.0 Recommendations](#60-recommendations)  
[7.0 Test/Maintenance Report Approval](#70-testmaintenance-report-approval)  

# 1.0 INTRODUCTION

## 1.1 Purpose
This document contains the testing procedures, results, and operational verification performed on an ESP32-S3 based IoT orientation monitoring system using an MPU6050 6-axis IMU and a 16x2 I2C LCD display. It records the names of all individuals involved in the design, implementation, and testing of the system and, if modified, should be reviewed and approved by the individuals identified in the sections below.

## 1.2 OVERVIEW
An initial test was conducted to verify communication between the ESP32-S3, IMU, and LCD display. Additional testing was performed to validate the acquisition of acceleration and rotational data, the calculation of pitch, roll, and yaw values, and the display of sensor information on the LCD. Once development and verification activities were completed, a final evaluation was performed to determine the operational status of the UUT. The results of these tests were determined to be Successful.

Additional comments are included for future reference, and the document lists all individuals involved, and is sealed with the signature of the author 

# 2.0 Initial Functionality Test


# 3.0 Maintenance Instructions
<sub>Table 2: Maintenance Instructions<sub/>
| Step | Instructions | Comments |
| :--- | :--- | :--- |
| 3.1 | Attach an ESD wrist strap and connect it to a properly grounded point. | Prevent electrostatic damage to the ESP32-S3 and sensors. |
| 3.2 | Disconnect power from the ESP32-S3 before making any wiring changes. | Never modify connections while powered. |
| 3.3 | Inspect the ESP32-S3, MPU6050, and LCD modules for visible signs of damage. | Check for bent pins, loose wires, and damaged connectors. |
| 3.4 | Verify all I2C wiring connections between the ESP32-S3, MPU6050 and LCD. | Ensure SDA and SCL are connected to the correct GPIO pins. |
| 3.5 | Confirm all power and ground connections are secure. | A loose power connection may cause communication errors. |
| 3.6 | Connect the ESP32-S3 to a computer using a USB cable. | Use a known-good data cable. |
| 3.7 | Upload the latest project files<br>(main.py, mpu6050.py, and i2c_lcd.py) to the ESP32-S3. | Verify files are transferred successfully. |
| 3.8 | Power on the system and observe the LCD initialization message. | The LCD should display the startup message without errors. |
| 3.9 | Verify that accelerometer, gyroscope, and orientation data are displayed correctly. | Compare LCD readings with serial monitor output. |
| 3.10 | Record any faults, corrective actions, and observations. | Document issues for future maintenance. |


# 4.0 Final Functionality Test

# 5.0 Assessment
The testing effort documented in this report was determined to be Successful. The ESP32-S3, MPU6050 IMU, and I2C LCD display operated as intended, successfully acquiring, processing, and displaying sensor data.

A challenge encountered during the project was the development of custom MicroPython libraries for the MPU6050 and I2C LCD modules. Additional testing and debugging were required to ensure reliable communication between the devices and the ESP32-S3.

The final system met all stated functional requirements and demonstrated reliable operation throughout testing.

# 6.0 Recommendations
The system successfully met all project requirements and operated as intended during testing. Several improvements could be considered for future versions of the project, including the addition of a larger display to present more sensor data at once, improving the physical mounting of the MPU6050 to reduce unwanted movement and measurement errors, and adding wireless connectivity features to allow sensor data to be monitored remotely. Additional long-term testing could also be performed to further evaluate system reliability and performance.

# 7.0 Test/Maintenance Report Approval

# APPENDIX: KEY TERMS
The following table provides definitions for terms relevant to this document.
| Term | Definition |
| --------------- | --------------- |
| UUT | Unit Under Test |
| I2C | Inter-Integrated Circuit |
| LCD | Liquid Crystal Display |
| MPU | Motion Processing Unit |
