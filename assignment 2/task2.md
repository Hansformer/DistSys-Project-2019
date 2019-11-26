# Assignment 2

## Task 1

### Lecture 5

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

- ĺive = at least one transition is enabled
- actually also checked if every transaction is possibly enabled at some point
- how did I do this ? followed every possible path of every token and looked if one transaction is not included

### bounded
