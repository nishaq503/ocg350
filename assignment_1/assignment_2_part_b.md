# Najib Ishaq

## Assignment 1, Part b.

### Due Oct 13$^{th}$ 2020

#### 8

**a.**

```stripers``` is a list.
```stripers.append(item)``` adds ```item``` as a new element at the end of the list.
```stripers.remove(i)``` removes the item at index $i$ from the list.

**b.**

```random.uniform(low, high)``` produces a uniformly sampled random number in the half-open interval $[low, \ high)$.

**c.**

```math.floor(number)``` truncates the decimal portion of ```number``` and returns an integer.
This effectively rounds down ```number``` to the nearest integer.

**d.**

```for i in range(0, len(pogies))``` starts a ```for-loop``` which finds the number of items, call it $n$, in the list ```pogies``` and then iterates over the integers in the half open interval $[0, n)$, substituting the integer for ```i``` for each pass through the body of the loop.

**e.**

The ```if-elif-else``` statements form a “control-flow” sequence.
It is used in the following manner:
```python
if condition_1:
    # do stuff
elif condition_2:
    # do other stuff
else:
    # do yet other stuff
```
If ```condition_1``` is true, the code in the first indented block is executed.
Otherwise, the control-flow moves on the ```elif``` block (short of “else if”) and checks ```condition_2```.
If ```condition_2``` is true, the code in the second indented block is executed.
Otherwise, the control-flow moves on to the ```else``` block
and the code in the final indented block is executed.

\newpage


#### 9

There are some minor differences between the physical game and what is done in code.

* The reproduction rate of the menhaden is set to $0.5$ in code and was assumed to be $1$ in the physical game.
* The fish are represented as squares in both cases. However, in code, the squares cannot tilt as they can in the physical game.


#### 10

The results with the default values are presented in the following two plots.

![Default population plot](images/population-vs-time/plot::0.png)
![Default phase plot](images/phase-plots/plot::0.png)

\newpage

**a.**

Increasing the size of the bay would allow all fish more space in which to roam.
This would mean that the stripers have a smaller chance of catching the pogies.
Therefore, in the steady state, the pogies would be more abundant and the stripers would be less so.

This prediction is confirmed in the following two plots, when the dimensions of the bay were increaed from $(17, 11)$ to $(25.5, 16.5)$.

![Default population plot](images/population-vs-time/plot::1.png)
![Default phase plot](images/phase-plots/plot::1.png)

\newpage

**b.**

If the stripers are made larger, they will overlap with more of the pogies and will thus eat more of the pogies.
However, the stripers will also have more competition among themselves.
We would expect the maximum population of pogies to decrease, the maximum population of stripers to increase and the population of stripers to fluctuate more heavily between the maximum and minimum values.
The more pronounced fluctuations in the population of stripers will also result in more pronounced fluctiations in the population of pogies.

This prediction is confirmed in the following two plots, when the size of the stripers was increased from $(2.5, 2.5)$ to $(4, 4)$.

![Default population plot](images/population-vs-time/plot::2.png)
![Default phase plot](images/phase-plots/plot::2.png)

\newpage

**c.**

If the menhaden were larger, they would become easier for the stripers to catch.
The prediction remains the same as in part **b**.

The following two plots show what happens when the size of the pogies is increased from $(1, 1)$ to $(1.5, 1.5)$.
This time, however, the maximum population of pogies did not fall noticably in comparison to the default settings.

![Default population plot](images/population-vs-time/plot::3.png)
![Default phase plot](images/phase-plots/plot::3.png)

\newpage

**d.**

If the carrying capacity of the pogies is increased, the maximum population of pogies will increase.
This will allow the stripers to catch pogies more often, and so their maximum population will go up in accordance.

The following two plots show what happens when the carrying capacity of pogies is increased from $75$ to $100$.
These plots confirm the prediction.

![Default population plot](images/population-vs-time/plot::4.png)
![Default phase plot](images/phase-plots/plot::4.png)

\newpage

**e.**

Decreasing the reproduction rate of pogies will not have an effect on the maximum populations of either species.
Instead, the cyclic trend we saw with the default settings will be stretched out in time.

The following two plots show what happens when the reproduction rate of pogies is decreased from $0.5$ to $0.25$.
These plots confirm the prediction.
We see only $7$ peaks as compared to the $9$ peaks with the default settings.

![Default population plot](images/population-vs-time/plot::5.png)
![Default phase plot](images/phase-plots/plot::5.png)

\newpage

**f.**

If we decrease the number of pogies that the stripers need to eat in order to survive, the stripers will find it easier to survive and their population will increase.
The stripers will also reproduce faster so their population will cycle faster.
The higher maximum population of stripers will, in turn, cause more dramatic fluctuations in the population of pogies.

The following two plots show what happens when the stripers need to eat $2$ pogies instead of $3$ to survive and $4$ instead of $6$ in order to reproduce.
These plots confirm the prediction.

![Default population plot](images/population-vs-time/plot::6.png)
![Default phase plot](images/phase-plots/plot::6.png)

\newpage

**g.**

The observed “population-change” vs “population” trends for the pogies and stripers are shown in the following two plots.
These were generated with the default settings.

We see that both populations tend towards a steady state with some stable non-zero population and no net change.

![Default population plot](images/pogies-delta/plot::0.png)
![Default phase plot](images/stripers-delta/plot::0.png)

\newpage

These trends become more stable when the area of the bay and the carrying capacity of the pogies are each increased by a large factor, in this case by a factor of $25$.
This is because the correspondingly larger populations largely mute the effects of random chance.

![Default population plot](images/pogies-delta/plot::1.png)
![Default phase plot](images/stripers-delta/plot::1.png)

\newpage


#### 11

I reimplemented the code in python scripts and uploaded it to brightspace.
The code saves the population measurements as needed and the plots as shown in question **10**.
