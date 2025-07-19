# Topic Conventions

MQTT has a hierachy of topics here are the conventions for it to work with this robot.

## Robot Name

The root node is the robot name, this way multiple robots can be present on the same mqtt network.

<pre> my-robot/ </pre>

### Nodes

Under the root node, there is a node topic that contains the details of each individual node.

<pre> my-robot/node/{name} </pre>

On this node, the date time in isoformat when the node was last initialized.

The node detail must contain:
 - Version : string representation of the version of the node
 - Status : One of the following value : Unknown, Connected, Disconnected, Working.

 Optionally nodes can publish its own detail about:
  - Services : json list of services it provides
  - Topics : json list of topics its provides

### Services

<pre> my-robot/service/{service_name} </pre>

Each node would subscribe on the services it implements.

