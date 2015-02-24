# Filename: CannyBot.py
# Authors: Tommy Lin, TJ Maynes

import os, sys, math, time
import cv2.cv as cv

"""
cv.NamedWindow('RoboVision', 1)
cv.NamedWindow('HumanVision', 2)
cap = cv.CaptureFromCAM(-1)
cv.SetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
cv.SetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
"""

# helper functions and values

rows = 4
columns = 4
ELBOW_OFFSET_Y = 15
UPPER_ARM_LENGTH = 105
SHOULDER_OFFSET_Y = 98
SHOULDER_OFFSET_Z = 100
LOWER_ARM_LENGTH = 55.95

def pretty_print(name, matrix):
    print "\nThis is matrix = " + name
    for row in matrix:
        print row

# main functions

def robo_vision():
    while True:
        frame = cv.QueryFrame(cap)
        cv.ShowImage('HumanVision', frame)
        
        # Convert to greyscale
        grey = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
        cv.CvtColor(frame, grey, cv.CV_RGB2GRAY)
  
        # Gaussian blur to remove noise
        blur = cv.CreateImage(cv.GetSize(grey), cv.IPL_DEPTH_8U, grey.channels)
        cv.Smooth(grey, blur, cv.CV_GAUSSIAN, 5, 5)
 
        # And do Canny edge detection
        canny = cv.CreateImage(cv.GetSize(blur), blur.depth, blur.channels)
        cv.Canny(blur, canny, 10, 100, 3)
        cv.ShowImage('RoboVision', canny)

        contours,h = cv.findContours(canny,1,2)

        # only return value when you find a circle or square
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            print len(approx)
            if len(approx)==5:
                print "pentagon"
                cv.drawContours(img,[cnt],0,255,-1)
            elif len(approx)==3:
                print "triangle"
                cv.drawContours(img,[cnt],0,(0,255,0),-1)
            elif len(approx)==4:
                return "square"
                cv.drawContours(img,[cnt],0,(0,0,255),-1)
            elif len(approx) == 9:
                print "half-circle"
                cv.drawContours(img,[cnt],0,(255,255,0),-1)
            elif len(approx) > 15:
                return "circle"
                cv.drawContours(img,[cnt],0,(0,255,255),-1)

        c = cv.WaitKey(50)
        if c == 27:
            exit(0)

def transformation_matrix(name_of_matrix, matrix, rows, columns, a, alpha, distance, theta):
    temp = 0.0
    for i in range(rows):
        for j in range(columns):
            if i == 0 and j == 0:
                temp = math.cos(theta*math.pi/180.0)
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 0 and j == 1:
                temp = (-(math.sin(theta*math.pi/180.0))*math.cos(alpha*math.pi/180.0))
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 0 and j == 2:
                temp = (math.sin(theta*math.pi/ 180.0) * math.sin(alpha*math.pi/ 180.0))
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 0 and j == 3:
                temp = (a * math.cos(theta*math.pi/180.0))
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 1 and j == 0:
                temp = math.sin(theta*math.pi/180.0)
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 1 and j == 1:
                temp = (math.cos(theta*math.pi/180.0)*math.cos(alpha*math.pi/180.0))
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 1 and j == 2:
                temp = (-(math.cos(theta*math.pi/180.0))*math.sin(alpha*math.pi/180.0))
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 1 and j == 3:
                temp = a*math.sin(theta*math.pi/180.0)
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 2 and j == 0:
                matrix[i][j] = 0.0
            if i == 2 and j == 1:
                temp = math.sin(alpha * math.pi/180.0)
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 2 and j == 2:
                temp = math.cos(alpha * math.pi/180.0)
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 2 and j == 3:
                temp = distance
                if temp == -0:
                    temp = 0.0
                matrix[i][j] = round(temp)
            if i == 3 and j == 0:
                matrix[i][j] = 0.0
            if i == 3 and j == 1:
                matrix[i][j] = 0.0
            if i == 3 and j == 2:
                matrix[i][j] = 0.0
            if i == 3 and j == 3:
                matrix[i][j] = 1.0

    pretty_print(name_of_matrix, matrix)
    return matrix

def  multiply_matrices(RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristRoll):

    # initialize temp matrices
    m0 = [[0 for x in range(4)] for x in range(4)]
    m1 = [[0 for x in range(4)] for x in range(4)]
    m2 = [[0 for x in range(4)] for x in range(4)]
    m3 = [[0 for x in range(4)] for x in range(4)]

    for i in range(rows):
        for j in range(columns):
            for inner in range(4):
                m0[i][j] = round(m0[i][j]+RShoulderPitch[i][inner]*RShoulderRoll[inner][j])

    for i in range(rows):
        for j in range(columns):
            for inner in range(4):
                m1[i][j] = round(m1[i][j]+m0[i][inner]*RElbowYaw[inner][j])

    for i in range(rows):
        for j in range(columns):
            for inner in range(4):
                m2[i][j] = round(m2[i][j]+m1[i][inner]*RElbowRoll[inner][j])

    for i in range(rows):
        for j in range(columns):
            for inner in range(4):
                m3[i][j] = round(m3[i][j]+m2[i][inner]*RWristRoll[inner][j])

    return m3
    
if __name__ == '__main__':
    print("Welcome to the CannyBot Program!")
    #shape = roboVision()
    #print("The shape found on the workspace was a %d", shape)

    # initialize matrices
    RShoulderPitch = [[0 for x in range(4)] for x in range(4)]
    RShoulderRoll = [[0 for x in range(4)] for x in range(4)]
    RElbowYaw = [[0 for x in range(4)] for x in range(4)]
    RElbowRoll = [[0 for x in range(4)] for x in range(4)]
    RWristRoll = [[0 for x in range(4)] for x in range(4)] 
    base_to_start = [[0 for x in range(4)] for x in range(4)]

    # process file
    print("Processing files in input.txt")
    f = open('input.txt', 'r')
    theta0 = f.readline()
    theta1 = f.readline()
    theta2 = f.readline()
    theta3 = f.readline()
    theta4 = f.readline()
    f.close()
    print("Finished processing file.")
    print "Thetas are %d %d %d %d %d" % (float(theta0), float(theta1), float(theta2), float(theta3), float(theta4))

    # transformation matrices
    RShoulderPitch = transformation_matrix("RShoulderPitch",RShoulderPitch,rows,columns,0,-(math.pi/2.0), 0, float(theta0))
    RShoulderRoll = transformation_matrix("RShoulderRoll",RShoulderRoll,rows,columns,0,math.pi/2.0, 0, float(theta1) + (math.pi/2.0))
    
    RElbowYaw = transformation_matrix("RElbowYaw",RElbowYaw,rows,columns,-ELBOW_OFFSET_Y, (math.pi / 2.0), UPPER_ARM_LENGTH, float(theta2))
    
    RElbowRoll = transformation_matrix("RElbowRoll",RElbowRoll,rows,columns,0, -(math.pi / 2.0), 0, float(theta3))
    RWristRoll = transformation_matrix("RWristRoll",RWristRoll,rows,columns,LOWER_ARM_LENGTH, (math.pi/ 2.0), 0, float(theta4))

    base_to_start = multiply_matrices(RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristRoll)
    pretty_print("base_to_start", base_to_start)
    
    print("End of Program.")