import pylab as pb
import numpy as np
import GPy

data = GPy.util.datasets.crescent_data(seed=1000)
Y = data['Y']
Y[Y.flatten()==-1] = 0

m = GPy.models.GPClassification(data['X'], Y)
m.ensure_default_constraints()
m.update_likelihood_approximation()
m.optimize()
m.plot()
m1 = m.copy()

m = GPy.models.FITCClassification(data['X'], Y,num_inducing=10)
m.constrain_bounded('.*len',1.,1e3)
m.ensure_default_constraints()
m['.*len'] = 3.
m.update_likelihood_approximation()
m.optimize()
m.plot()
m2 = m.copy()

m = GPy.models.SparseGPClassification(data['X'], Y,num_inducing=10)
m['.*len']= 4.
m.ensure_default_constraints()
m.update_likelihood_approximation()
m.optimize()
m.plot()

fig1 = pb.figure(figsize=(15,5))
ax1 = fig1.add_subplot(131)
ax1.grid(True)
ax1.set_title('EP',fontsize=22)
m1.plot(ax=ax1)

ax2 = fig1.add_subplot(132)
ax2.grid(True)
ax2.set_title('EP-FITC',fontsize=22)
m2.plot(ax=ax2)

ax3 = fig1.add_subplot(133)
ax3.grid(True)
ax3.set_title('EP-DTC',fontsize=22)
m.plot(ax=ax3)


# Plot

#fig, axes = pb.subplots(2,1)
#m.plot_f(ax=axes[0])
#m.plot(ax=axes[1])
