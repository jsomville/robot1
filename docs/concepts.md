# Concepts

The SROSA (Simple ROS Alternative) is a set of libraries highly inspired by ROS (Robot Operating system) to integrate robot, sensors, motors, etc.

The key concepts are:
 - [Nodes](node.md) relates to individual programs
 - [Nodes](node.md) communicate using a communication protocol
 - [Nodes](node.md) can be configured using parameters
 - [Nodes](node.md) offers [services](service.md)  (request / reply)
 - [Nodes](node.md) can perform [actions](action.md)  (long lasting)
 - [Nodes](node.md) can subscribe and publish [topics](topic.md)  exchanged on the communication protocol

 INSERT SCHEMA

 The overall architecture is based on a tree with the following structure:
  - Robot Name
  -  |- node/{node1}
  -       |- version : X.Y.Z
  -       |- connexion_status : Unknown, Connected, Disconnected, Working
  -       |- services
  -             | - {service_name} : json service detail
  -       |- parameters : json parameters detail
  -             |- {name_of_parameter} : value (optional)



## Example : Rollingbot

The rollingbot is a simple real life example.

In its minimal state, it is composed of :
 - One Node called drive
 - One node called remote

 The drive node is responsible for controlling the movement of the bot (rolling the bot) and publish some status. The remote node is used to send actions to the drive from a keyboard.

 Optionnaly this example can be updated with: 
  - One sensor called proximity
