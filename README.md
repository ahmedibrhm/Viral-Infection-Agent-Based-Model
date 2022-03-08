# Viral-Infection-Model
<font color = "brown"><h3>Agent-Based Model</h3></font>
<p>Agent based model that simulates the virus propagation in a community. The model has the following assumptions:<br>
    1- Humans live in a world that has a length and width. <br>
    2- Humans can only be susceptibles, infected, or removed.<br>
    3- Each human occupy a space of coordinates (x,y) in the world.<br>
    4- People who get recover won't be susceptible again.<br>
    6- People can move randomly in 8 directions: East, West, North, South, NorthEast, NorthWest, SouthEast, and SouthWest.<br>
    7- Susceptibles can only be infected if they existed in a coordinate of (x,y) that an infected person existed in at the same time.<br>
    8- If a susceptible person existed at the same position as an infected person, there is a probability of getting infected according to the infection rate of the virus.<br>
    9- People who get the vaccine change from susceptibles to recovered.<br>
</p>
<font color = "brown"><h3>Model's graph</h3></font>
<p>The model is producing both visual representation of the three populations and a map. This map is for representing the model's world (simulated area). The map has four colors:<br>
<font color = "black">Black: </font>means no humans are in this place<br>
<font color = "red">Red: </font>Means there is infected person in this place<br>
    <font color = "orange">Yellow: </font>Means there is susceptible person in this place and there is no infected. <br>
    <font color = "green">Green: </font>Means there is only recovered persons in this place <br>
</p>
<img src="https://i.ibb.co/WH65Rwm/Agentbased-modelling.gif"/>
<font color = "brown"><h2>Model's Phase Space</h2></font>
<img src="https://i.ibb.co/dJY3bBy/Phase-Space.gif"/>
<p>
The model also produce a 3D phase Space that plots the susceptible, Infected, and Recovered population with regard to each others.
</p>
