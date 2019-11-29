# Assignment 2

## Task 1

- doctors hansformer
- vendor machine hansformer
- light niels
- car assembly niels
- insurance claims niels (see below)
- chair whichever niels

### Lecture 6

#### Exercise 1

It is not possible to model this as a Petri net, because you would have to add or remove your parts in the middle of your model in a really flexible way.
While the beginning, the initialization and the end the report are static and only happen ones, the middle part could be anything between 0 and infinity (not included).
If you would use an upper bound, like all humans on this Planet, it wouldn't make any sense, because then you would have to concact people not included in this Claim.  

#### Exercise 2

(Switch 1 Down ,Switch 2 Down,Switch 1 Up,Switch 2 Up,Light on)
(1,1,0,0,0) - (0,1,1,0,1)  
    |              |  
(1,0,0,1,1) - (0,0,1,1,2) -> (1,1,0,0,0) (diagonal to the beginning)

## Task 2

### Liveness (1)

[reference](https://en.wikipedia.org/wiki/Petri_net#Liveness)

- ĺive = not dead
- dead = can never fire, only input arcs no output arcs
- how did I do this ? check if any transaction had only input arcs
- is not the case in any of the given nets

### Boundedness (2)

[reference](https://en.wikipedia.org/wiki/Petri_net#Boundedness)

- Not bounded, because Reachibality Graph is not finite
- graph is not finite, eg. t3:
  -  in 1) it is giving the token from s1 to s2 and s4 -> increases number of tokens by 1 and creates new states, endless repeatable
  -  in 2) and 3) it is giving the token to s1, s4 and s5 -> increases number of tokens by 2 and creates new states, endless repeatable

### shortest path (3)

1) (1,1,0,0) ->  (1,0,1,1) -> (2,0,1,0)
   - t2 , t1
2) (1,1,0,0,1,1,0,0) -> (1,1,0,0,1,0,1,1) -> (1,1,0,1,2,0,1,0) -> (1,0,1,2,2,0,1,0) -> (2,0,1,1,2,0,1,0) -> (3,0,1,0,2,0,1,0)
   - t4 ,t3 ,t2 , t1, t1
3) (1,1,0,0,1,1,0,0,1,1,0,0) -> (1,1,0,0,1,1,0,0,1,0,1,1) -> (1,1,0,0,1,1,0,1,2,0,1,0) -> (1,1,0,0,1,0,1,2,2,0,1,0) -> (1,1,0,1,2,0,1,1,2,0,1,0) -> (1,1,0,2,3,0,1,0,2,0,1,0) -> (1,0,1,3,3,0,1,0,2,0,1,0) -> (2,0,1,2,3,0,1,0,2,0,1,0) -> (3,0,1,1,3,0,1,0,2,0,1,0) -> (3,0,1,0,3,0,1,0,2,0,1,0)
    - t6, t5 ,t4 ,t3, t3 ,t2 , t1, t1, t1

### shortest path for n (4)

- shortest path(n) = if n=1 -> 2, else -> shortest path(n-1) + (n-1) + 2

## Task 3

### Assumptions:

- We don't consider pedestrians in the assignment.


### Solution

We have divided the traffic lights in to three different components, which only one can be active at a time:
1. Main road lights forward (1 in the notation of the petrinet)  
2. Turning from the main road from the central to Kumpula. (2)
3. Turning from Kumpula to left towards Viikki and turning right from the mainroad to Kumpula (3).  

The mutex is responsible for deciding which one of these is going to be active after the last one turns from orange to red.

We tried multiple ways to cover the restrains for flow, as for (1) it should be max 10 cars and max 5 cars for (2),(3). One consideration was that, for example for (1), we use multiple tokens to the transition go1 (green->orange) with either timeout or car capacity, this however was really tedious and there were problems handling the tokens later. This was only one of the methods we tried, all of our concepts turned out not working, so we left those out.

But the idea is that for every one of these parts (1),(2) and (3), we have some kind of logic to activate green to orange transition, either when maximum amount of cars is passed or the timeout has activated.
