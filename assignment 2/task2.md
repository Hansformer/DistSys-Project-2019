# Assignment 2

## Task 1

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

### Are the nets living

[reference](https://en.wikipedia.org/wiki/Petri_net#Liveness)

- ĺive = not dead
- dead = can never fire, only input arcs no output arcs
- how did I do this ? check if any transaction had only input arcs
- is not the case in any of the given nets

### bounded
- 