# -*- coding: utf-8 -*-
"""11 - Approximation Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rb-OYJUnfgylO9u2ZChgekrdV5zTAV4U
"""

import matplotlib.pyplot as plt
import GridWorld
import numpy as np
import pandas as pd

robot=GridWorld.grid_world()

def print_values(V, rows,columns):
    for i in range(rows):
        print("---------------------------")
        for j in range(columns):
            v = V.get((i,j), 0)
            if v >= 0:
                print(" %.2f|" % v, end="")
            else:
                print("%.2f|" % v, end="") # -ve sign takes up an extra space
        print("")
def print_policy(policy,rows,columns):
    for i in range(rows):
        print("---------------------------")
        for j in range(columns):
            a = policy.get((i,j), ' ')
            print("  %s  |" % a, end="")
        print("")

### fixed policy ###
policy={(0, 0): 'R',
 (0, 1): 'R',
 (0, 2): 'R',
 (1, 0): 'U',
 (1, 2): 'U',
 (2, 0): 'U',
 (2, 1): 'L',
 (2, 2): 'U',
 (2, 3): 'L'
       }

X = [[0, 0], [1, 1], [2, 0], [0, 2]]
from sklearn.preprocessing import PolynomialFeatures
poly_features = PolynomialFeatures(degree=1)
poly_features.fit_transform(X)

poly_features.fit_transform(robot.States)

poly_features.n_output_features_

def predictV(s,w,featurizer):
    if featurizer=='poly':
        x = poly_features.fit_transform([s])[0]
    elif featurizer=='nystroem':
        x=Nystroem_featurizer.transform([s])[0]
    else:
        x=rbf_featurizer.transform([s])[0]
    return np.dot(x,w)

def gradientV(s,featurizer):
    if featurizer=='poly':
        x = poly_features.fit_transform([s])[0]
    elif featurizer=='nystroem':
        x=Nystroem_featurizer.transform([s])[0]
    else:
        x=rbf_featurizer.transform([s])[0]
    return x

def epsilon_greedy(greedy, s, eps=0.1):
  # we'll use epsilon-soft to ensure all states are visited
  # what happens if you don't do this? i.e. eps=0
    p = np.random.random()
    if p < (1 - eps):
        return greedy[s]
    else:
        return np.random.choice(robot.ACTION_SPACE)

GAMMA=0.9
ALPHA = 0.01
#Initialize weights as zero
poly_features = PolynomialFeatures(degree=1)
poly_features.fit_transform(robot.States)
w = np.zeros(poly_features.n_output_features_) 
n_episodes = 20000
for it in range(n_episodes):
    # begin a new episode
    s=robot.initial_state()
    Vs=predictV(s,w,featurizer='poly')
    done=False
    while not done:
        a = epsilon_greedy(policy, s, eps=0.1)
        next_s, r, done=robot.step(a)
        if done:
            target = r
        else:
            Vnext_s = predictV(next_s,w,featurizer='poly')
            target = r + GAMMA * Vnext_s
        # update the weights
        g = gradientV(s,featurizer='poly')
        err = target - predictV(s,w,featurizer='poly')
        w += ALPHA * err * g
        # update state
        s = next_s

w

V = {}
for s in robot.States:
    if s not in robot.actions.keys():
        V[s] = 0
    else:
        V[s] = predictV(s,w,featurizer='poly')

print_policy(policy,3,4)

print_values(V,3,4)

from sklearn.kernel_approximation import Nystroem
X = [[0, 0], [1, 1], [1, 0], [0, 1]]
featurizer = Nystroem(gamma=1,random_state=1,n_components=2)
X_features = featurizer.fit_transform(X)
X_features

featurizer.components_

def gather_samples(n_episodes=10000):
    samples = []
    for i in range(n_episodes):
        s=robot.initial_state()
        samples.append(s)
        done=False
        while not done:
            a = np.random.choice(robot.ACTION_SPACE)
            s, r, done=robot.step(a)
            samples.append(s)
    return samples

samples=gather_samples(n_episodes=10000)
Nystroem_featurizer = Nystroem(gamma=1,random_state=1,n_components=100)
Nystroem_featurizer.fit(samples)

Nystroem_featurizer.components_

s=[0,0]
Nystroem_featurizer.transform([s])

GAMMA=0.9
ALPHA = 0.01
#Initialize weights as zero
w = np.zeros(100) 
n_episodes = 20000
for it in range(n_episodes):
    # begin a new episode
    s=robot.initial_state()
    Vs=predictV(s,w,featurizer='nystroem')
    done=False
    while not done:
        a = epsilon_greedy(policy, s, eps=0.1)
        next_s, r, done=robot.step(a)
        if done:
            target = r
        else:
            Vnext_s = predictV(next_s,w,featurizer='nystroem')
            target = r + GAMMA * Vnext_s
        # update the weights
        g = gradientV(s,featurizer='nystroem')
        err = target - predictV(s,w,featurizer='nystroem')
        w += ALPHA * err * g
        # update state
        s = next_s

w

V = {}
for s in robot.States:
    if s not in robot.actions.keys():
        V[s] = 0
    else:
        V[s] = predictV(s,w,featurizer='nystroem')

print_values(V,3,4)

from sklearn.kernel_approximation import RBFSampler
X = [[0, 0], [1, 1], [1, 0], [0, 1]]
featurizer = RBFSampler(n_components=3)
featurizer.fit(X)
X_features = featurizer.transform(X)
X_features

RBFSampler()

rbf_featurizer = RBFSampler(n_components=100)
rbf_featurizer.fit(samples)

GAMMA=0.9
ALPHA = 0.01
#Initialize weights as zero
w = np.zeros(100) 
n_episodes = 100000
for it in range(n_episodes):
    # begin a new episode
    s=robot.initial_state()
    Vs=predictV(s,w,featurizer='rbf')
    done=False
    while not done:
        a = epsilon_greedy(policy, s, eps=0.1)
        next_s, r, done=robot.step(a)
        if done:
            target = r
        else:
            Vnext_s = predictV(next_s,w,featurizer='rbf')
            target = r + GAMMA * Vnext_s
        # update the weights
        g = gradientV(s,featurizer='rbf')
        err = target -  predictV(s,w,featurizer='rbf')
        w += ALPHA * err * g
        # update state
        s = next_s

V = {}
for s in robot.States:
    if s not in robot.actions.keys():
        V[s] = 0
    else:
        V[s] = predictV(s,w,featurizer='rbf')

print_values(V,3,4)

