#!/usr/bin/env python
import roslib; roslib.load_manifest('guts')
import rospy
from guts.msg import sonar_data
from guts.msg import gp_prediction

import pylab as pb
pb.ion()
import numpy as np
import GPy

mean = np.array([[0,0]])
cov = np.array([[2,2]])

############################
#        gp training
############################

#####################################
# step1. read the relavent data from the files
#####################################

# y = 1

with open('./GUTS_sonar_data_v1.1/training_data_-0.5_1.txt', 'r') as f:
  data_m05_1 = []
  for line in f: # read lines
    data_m05_1.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0_1.txt', 'r') as f:
  data_0_1 = []
  for line in f: # read lines
    data_0_1.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0.5_1.txt', 'r') as f:
  data_05_1 = []
  for line in f: # read lines
    data_05_1.append([float(x) for x in line.split()])


# y = 1.5
with open('./GUTS_sonar_data_v1.1/training_data_-1_1.5.txt', 'r') as f:
  data_m1_15 = []
  for line in f: # read lines
    data_m1_15.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-0.5_1.5.txt', 'r') as f:
  data_m05_15 = []
  for line in f: # read lines
    data_m05_15.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0_1.5.txt', 'r') as f:
  data_0_15 = []
  for line in f: # read lines
    data_0_15.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0.5_1.5.txt', 'r') as f:
  data_05_15 = []
  for line in f: # read lines
    data_05_15.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1_1.5.txt', 'r') as f:
  data_1_15 = []
  for line in f: # read lines
    data_1_15.append([float(x) for x in line.split()])



# y = 2
with open('./GUTS_sonar_data_v1.1/training_data_-1.5_2.txt', 'r') as f:
  data_m15_2 = []
  for line in f: # read lines
    data_m15_2.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-1_2.txt', 'r') as f:
  data_m1_2 = []
  for line in f: # read lines
    data_m1_2.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-0.5_2.txt', 'r') as f:
  data_m05_2 = []
  for line in f: # read lines
    data_m05_2.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0_2.txt', 'r') as f:
  data_0_2 = []
  for line in f: # read lines
    data_0_2.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0.5_2.txt', 'r') as f:
  data_05_2 = []
  for line in f: # read lines
    data_05_2.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1_2.txt', 'r') as f:
  data_1_2 = []
  for line in f: # read lines
    data_1_2.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1.5_2.txt', 'r') as f:
  data_15_2 = []
  for line in f: # read lines
    data_15_2.append([float(x) for x in line.split()])



# y = 2.5
with open('./GUTS_sonar_data_v1.1/training_data_-1.5_2.5.txt', 'r') as f:
  data_m15_25 = []
  for line in f: # read lines
    data_m15_25.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-1_2.5.txt', 'r') as f:
  data_m1_25 = []
  for line in f: # read lines
    data_m1_25.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-0.5_2.5.txt', 'r') as f:
  data_m05_25 = []
  for line in f: # read lines
    data_m05_25.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0_2.5.txt', 'r') as f:
  data_0_25 = []
  for line in f: # read lines
    data_0_25.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0.5_2.5.txt', 'r') as f:
  data_05_25 = []
  for line in f: # read lines
    data_05_25.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1_2.5.txt', 'r') as f:
  data_1_25 = []
  for line in f: # read lines
    data_1_25.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1.5_2.5.txt', 'r') as f:
  data_15_25 = []
  for line in f: # read lines
    data_15_25.append([float(x) for x in line.split()])



# y = 3
with open('./GUTS_sonar_data_v1.1/training_data_-1.5_3.txt', 'r') as f:
  data_m15_3 = []
  for line in f: # read lines
    data_m15_3.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-1_3.txt', 'r') as f:
  data_m1_3 = []
  for line in f: # read lines
    data_m1_3.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_-0.5_3.txt', 'r') as f:
  data_m05_3 = []
  for line in f: # read lines
    data_m05_3.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0_3.txt', 'r') as f:
  data_0_3 = []
  for line in f: # read lines
    data_0_3.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_0.5_3.txt', 'r') as f:
  data_05_3 = []
  for line in f: # read lines
    data_05_3.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1_3.txt', 'r') as f:
  data_1_3 = []
  for line in f: # read lines
    data_1_3.append([float(x) for x in line.split()])

with open('./GUTS_sonar_data_v1.1/training_data_1.5_3.txt', 'r') as f:
  data_15_3 = []
  for line in f: # read lines
    data_15_3.append([float(x) for x in line.split()])

#####################################
# step2. input and output data
#####################################

# input:
X = np.vstack((np.array(data_m05_1),np.array(data_0_1),np.array(data_05_1),np.array(data_m1_15),np.array(data_m05_15),np.array(data_0_15),np.array(data_05_15),np.array(data_1_15),np.array(data_m15_2),np.array(data_m1_2),np.array(data_m05_2),np.array(data_0_2),np.array(data_05_2),np.array(data_1_2),np.array(data_15_2),np.array(data_m15_25),np.array(data_m1_25),np.array(data_m05_25),np.array(data_0_25),np.array(data_05_25),np.array(data_1_25),np.array(data_15_25),np.array(data_m15_3),np.array(data_m1_3),np.array(data_m05_3),np.array(data_0_3),np.array(data_05_3),np.array(data_1_3),np.array(data_15_3)))

# filter invalid data
for x1 in range(np.size(X[:,0])):
  for x2 in range(np.size(X[0,:])):
    if X[x1,x2] > 15000:
      X[x1,x2] = 15000

X_4 = X[:,1:5]

X_3_1 = X[:,2:5]
X_3_2 = np.hstack((X[:,1:2],X[:,3:4],X[:,4:5]))
X_3_3 = np.hstack((X[:,1:2],X[:,2:3],X[:,4:5]))
X_3_4 = X[:,1:4]

X_2_1_2 = np.hstack((X[:,1:2],X[:,2:3]))
X_2_1_3 = np.hstack((X[:,1:2],X[:,3:4]))
X_2_1_4 = np.hstack((X[:,1:2],X[:,4:5]))
X_2_2_3 = np.hstack((X[:,2:3],X[:,3:4]))
X_2_2_4 = np.hstack((X[:,2:3],X[:,4:5]))
X_2_3_4 = np.hstack((X[:,3:4],X[:,4:5]))



# output x coordinate:
Y_x = np.vstack(((-0.5)*np.ones([20,1]),0*np.ones([20,1]),0.5*np.ones([20,1]),(-1)*np.ones([20,1]),(-0.5)*np.ones([20,1]),0*np.ones([20,1]),0.5*np.ones([20,1]),1*np.ones([20,1]),(-1.5)*np.ones([20,1]),(-1)*np.ones([20,1]),(-0.5)*np.ones([20,1]),0*np.ones([20,1]),0.5*np.ones([20,1]),1*np.ones([20,1]),1.5*np.ones([20,1]),(-1.5)*np.ones([20,1]),(-1)*np.ones([20,1]),(-0.5)*np.ones([20,1]),0*np.ones([20,1]),0.5*np.ones([20,1]),1*np.ones([20,1]),1.5*np.ones([20,1]),(-1.5)*np.ones([20,1]),(-1)*np.ones([20,1]),(-0.5)*np.ones([20,1]),0*np.ones([20,1]),0.5*np.ones([20,1]),1*np.ones([20,1]),1.5*np.ones([20,1])))

# output y coordinate:
Y_y = np.vstack((1*np.ones([20,1]),1*np.ones([20,1]),1*np.ones([20,1]),1.5*np.ones([20,1]),1.5*np.ones([20,1]),1.5*np.ones([20,1]),1.5*np.ones([20,1]),1.5*np.ones([20,1]),2*np.ones([20,1]),2*np.ones([20,1]),2*np.ones([20,1]),2*np.ones([20,1]),2*np.ones([20,1]),2*np.ones([20,1]),2*np.ones([20,1]),2.5*np.ones([20,1]),2.5*np.ones([20,1]),2.5*np.ones([20,1]),2.5*np.ones([20,1]),2.5*np.ones([20,1]),2.5*np.ones([20,1]),2.5*np.ones([20,1]),3*np.ones([20,1]),3*np.ones([20,1]),3*np.ones([20,1]),3*np.ones([20,1]),3*np.ones([20,1]),3*np.ones([20,1]),3*np.ones([20,1])))

# combine x,y coordinate:
Y = np.hstack((Y_x,Y_y))

with open('./GUTS_sonar_data_v1.1/overall_training_data.txt', 'w') as f:
  for i in range(20*(3+5+7+7+7)):
    f.write('%f %f %f %f          %f %f\n' % (float(X[i,0]),float(X[i,1]),float(X[i,2]),float(X[i,3]), float(Y_x[i]),float(Y_y[i])))

del X
del data_m05_1, data_0_1, data_05_1, data_m1_15, data_m05_15, data_0_15, data_05_15, data_1_15, data_m15_2, data_m1_2, data_m05_2, data_0_2, data_05_2, data_1_2, data_15_2, data_m15_25, data_m1_25, data_m05_25, data_0_25, data_05_25, data_1_25, data_15_25, data_m15_3, data_m1_3, data_m05_3, data_0_3, data_05_3, data_1_3, data_15_3
#####################################
# step3. train GP
#####################################

############# For X_4 #############
# define kernel
kernel_4 = GPy.kern.rbf(input_dim=4, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_4 = GPy.models.GPRegression(X_4,Y,kernel_4,True,True)

# add constraints
gp_4.unconstrain('')
gp_4.ensure_default_constraints()
gp_4.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_4.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_4
del X_4

############# For X_3_1 #############
# define kernel
kernel_3_1 = GPy.kern.rbf(input_dim=3, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_3_1 = GPy.models.GPRegression(X_3_1,Y,kernel_3_1,True,True)

# add constraints
gp_3_1.unconstrain('')
gp_3_1.ensure_default_constraints()
gp_3_1.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_3_1.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_3_1
del X_3_1
############# For X_3_2 #############
# define kernel
kernel_3_2 = GPy.kern.rbf(input_dim=3, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_3_2 = GPy.models.GPRegression(X_3_2,Y,kernel_3_2,True,True)

# add constraints
gp_3_2.unconstrain('')
gp_3_2.ensure_default_constraints()
gp_3_2.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_3_2.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_3_2
del X_3_2
############# For X_3_3 #############
# define kernel
kernel_3_3 = GPy.kern.rbf(input_dim=3, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_3_3 = GPy.models.GPRegression(X_3_3,Y,kernel_3_3,True,True)

# add constraints
gp_3_3.unconstrain('')
gp_3_3.ensure_default_constraints()
gp_3_3.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_3_3.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_3_3
del X_3_3
############# For X_3_4 #############
# define kernel
kernel_3_4 = GPy.kern.rbf(input_dim=3, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_3_4 = GPy.models.GPRegression(X_3_4,Y,kernel_3_4,True,True)

# add constraints
gp_3_4.unconstrain('')
gp_3_4.ensure_default_constraints()
gp_3_4.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_3_4.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_3_4
del X_3_4
############# For X_2_1_2 #############
# define kernel
kernel_2_1_2 = GPy.kern.rbf(input_dim=2, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_2_1_2 = GPy.models.GPRegression(X_2_1_2,Y,kernel_2_1_2,True,True)

# add constraints
gp_2_1_2.unconstrain('')
gp_2_1_2.ensure_default_constraints()
gp_2_1_2.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_2_1_2.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_2_1_2
del X_2_1_2
############# For X_2_1_3 #############
# define kernel
kernel_2_1_3 = GPy.kern.rbf(input_dim=2, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_2_1_3 = GPy.models.GPRegression(X_2_1_3,Y,kernel_2_1_3,True,True)

# add constraints
gp_2_1_3.unconstrain('')
gp_2_1_3.ensure_default_constraints()
gp_2_1_3.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_2_1_3.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_2_1_3
del X_2_1_3
############# For X_2_1_4 #############
# define kernel
kernel_2_1_4 = GPy.kern.rbf(input_dim=2, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_2_1_4 = GPy.models.GPRegression(X_2_1_4,Y,kernel_2_1_4,True,True)

# add constraints
gp_2_1_4.unconstrain('')
gp_2_1_4.ensure_default_constraints()
gp_2_1_4.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_2_1_4.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_2_1_4
del X_2_1_4
############# For X_2_2_3 #############
# define kernel
kernel_2_2_3 = GPy.kern.rbf(input_dim=2, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_2_2_3 = GPy.models.GPRegression(X_2_2_3,Y,kernel_2_2_3,True,True)

# add constraints
gp_2_2_3.unconstrain('')
gp_2_2_3.ensure_default_constraints()
gp_2_2_3.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_2_2_3.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_2_2_3
del X_2_2_3
############# For X_2_2_4 #############
# define kernel
kernel_2_2_4 = GPy.kern.rbf(input_dim=2, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_2_2_4 = GPy.models.GPRegression(X_2_2_4,Y,kernel_2_2_4,True,True)

# add constraints
gp_2_2_4.unconstrain('')
gp_2_2_4.ensure_default_constraints()
gp_2_2_4.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_2_2_4.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_2_2_4
del X_2_2_4
############# For X_2_3_4 #############
# define kernel
kernel_2_3_4 = GPy.kern.rbf(input_dim=2, variance=7.1126, lengthscale=0.6854)

# compute GP
gp_2_3_4 = GPy.models.GPRegression(X_2_3_4,Y,kernel_2_3_4,True,True)

# add constraints
gp_2_3_4.unconstrain('')
gp_2_3_4.ensure_default_constraints()
gp_2_3_4.constrain_fixed('.*noise',0.05)

# optimize GP
#gp_2_3_4.optimize()

# restart optimize to improve results
#gp_x.optimize_restarts(num_restarts = 10)
#gp_y.optimize_restarts(num_restarts = 10)

# print it
print gp_2_3_4
del X_2_3_4
#####################################
















# motor_cmd.left_motor_speed and motor_cmd.right_motor_speed has to be -63-63
def callback(sonar_data_msg):
    rospy.loginfo(rospy.get_name() + ": I heard %d %d %d %d %d %d " % (sonar_data_msg.sonar_data[0],sonar_data_msg.sonar_data[1],sonar_data_msg.sonar_data[2],sonar_data_msg.sonar_data[3],sonar_data_msg.sonar_data[4],sonar_data_msg.sonar_data[5]))

    ######################
    #  gp testing
    ######################
    test_data = np.array(sonar_data_msg.sonar_data)
    test_data = test_data[1:5]
    
 
    for x in range(4):
        if test_data[x]>15000:
            test_data[x] = 0
    
    print test_data

    if (test_data[0]!=0) and (test_data[1]!=0) and (test_data[2]!=0) and (test_data[3]!=0):
        mean,cov,high,low = gp_4.predict(test_data)
        print "gp_4"
    # gp_3
    elif (test_data[0]==0) and (test_data[1]!=0) and (test_data[2]!=0) and (test_data[3]!=0):
        test_data = np.hstack((test_data[1],test_data[2],test_data[3]))
        mean,cov,high,low = gp_3_1.predict(test_data)
        print "gp_3_1"
    elif (test_data[0]!=0) and (test_data[1]==0) and (test_data[2]!=0) and (test_data[3]!=0):
        test_data = np.hstack((test_data[0],test_data[2],test_data[3]))
        mean,cov,high,low = gp_3_2.predict(test_data)
        print "gp_3_2"
    elif (test_data[0]!=0) and (test_data[1]!=0) and (test_data[2]==0) and (test_data[3]!=0):
        test_data = np.hstack((test_data[0],test_data[1],test_data[3]))
        mean,cov,high,low = gp_3_3.predict(test_data)
        print "gp_3_3"
    elif (test_data[0]!=0) and (test_data[1]!=0) and (test_data[2]!=0) and (test_data[3]==0):
        test_data = np.hstack((test_data[0],test_data[1],test_data[2]))
        mean,cov,high,low = gp_3_4.predict(test_data)
        print "gp_3_4"
    # gp_2
    elif (test_data[0]!=0) and (test_data[1]!=0) and (test_data[2]==0) and (test_data[3]==0):
        test_data = np.hstack((test_data[0],test_data[1]))
        mean,cov,high,low = gp_2_1_2.predict(test_data)
        print "gp_2_1_2"
    elif (test_data[0]!=0) and (test_data[1]==0) and (test_data[2]!=0) and (test_data[3]==0):
        test_data = np.hstack((test_data[0],test_data[2]))
        mean,cov,high,low = gp_2_1_3.predict(test_data)
        print "gp_2_1_3"
    elif (test_data[0]!=0) and (test_data[1]==0) and (test_data[2]==0) and (test_data[3]!=0):
        test_data = np.hstack((test_data[0],test_data[3]))
        mean,cov,high,low = gp_2_1_4.predict(test_data)
        print "gp_2_1_4"
    elif (test_data[0]==0) and (test_data[1]!=0) and (test_data[2]!=0) and (test_data[3]==0):
        test_data = np.hstack((test_data[1],test_data[2]))
        mean,cov,high,low = gp_2_2_3.predict(test_data)
        print "gp_2_2_3"
    elif (test_data[0]==0) and (test_data[1]!=0) and (test_data[2]==0) and (test_data[3]!=0):
        test_data = np.hstack((test_data[1],test_data[3]))
        mean,cov,high,low = gp_2_2_4.predict(test_data)
        print "gp_2_2_4"
    elif (test_data[0]==0) and (test_data[1]==0) and (test_data[2]!=0) and (test_data[3]!=0):
        test_data = np.hstack((test_data[2],test_data[3]))
        mean,cov,high,low = gp_2_3_4.predict(test_data)
        print "gp_2_3_4"
    # else
    else:
        mean,cov,high,low = gp_4.predict(test_data)
        cov = cov*10;
        print "not enough data, previous prediction produced..."

    print mean
    print cov
    ################################################

    pub = rospy.Publisher('gp_prediction_msg', gp_prediction,queue_size=10)

    gp_prediction_msg = gp_prediction()
    gp_prediction_msg.mean_x = mean[0,0]
    gp_prediction_msg.mean_y = mean[0,1]
    gp_prediction_msg.cov_x = cov[0,0]
    gp_prediction_msg.cov_y = cov[0,1]
    pub.publish(gp_prediction_msg)    


def receive_motor_cmd_smg():
    rospy.Subscriber("guts_sonar_ir_data",sonar_data, callback)
    rospy.init_node('guts_sonar_gp_node', anonymous=True)
    
    rospy.spin()


if __name__ == '__main__':
    receive_motor_cmd_smg()
