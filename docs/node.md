# Node

Node refers to a program. 

Each node must be hinerit from the node class.

Node can be configured with a node.config file --> detail this

On the topic hyearchy, nodes are detailed in :

<pre> {robot_name}/node/{name} </pre>

Each node must contain the following topics:
 - Version (version): string representation of the version of the node (X.Y.Z)
 - Node Status (node_status): One of the following value : Unknown, Connected, Disconnected, Working.

 Each node can have:
  - [parameters](parameters.md)
  - [topics](topic.md)
  - [services](service.md)
  - [actions](action.md)

## Example
Example for a node called drive on a robot called rollingbot, it would be represented as:
 - rollingbot
 - rollingbot/node/drive (*) --> do we need this ?
 - rollingbot/node/drive/version : 0.1
 - rollingbot/node/drive/node_status : Connected
 - rollingbot/node/drive/service : { move }