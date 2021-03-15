# Project 5: Traffic

Write an AI to identify which traffic sign appears in a photograph.

# Experimental Process

Things I have tried:

1. First Trial:
   1. MaxPooling2D: pool_size=(3,3)
   2. Dropout features for Densing Hidden layer
2. Second Trial:
   1. MaxPooling2D: pool_size=(2,2)
   2. Dropout features for Densing Hidden layer
3. Latter trials:
   1. different number of hidden layer doing densing and pooling ...
   2. different activation functions ...

# Things I found out

1. Pooling size will affect the accuracy.
   1. Where smaller pooling size will lead to longer commuting time, since more variables needs to be calculated.
   2. However, the accuracy can be improved due to extensive computation.
   3. If the pooling size getting too big, may lead to loss of accuracy
2. Hidden layer can increase the accuracy.
   1. Pooling layer
      1. An extra pooling layer can increase the computing time since more computation happens before densing, but reduce the computational time latter for BP algorithm. So it contributes to an overall shorter computational time.
      2. It also contributes to a better accuracy as well.
   2. Densing layer
      1. An extra densing layer can increase the commuting time since longer paths needed for BP algorithm, and it may or may-not increase the accuracy.
3. Activation method can affect the accuracy.
   1. The relationships are not clear yet since there are many activation functions can be used.
4. Time of training improve accuracy, but it may decrease the chance of utilizing it outside of traning-testing sets.
