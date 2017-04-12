# .CAT Platform
Small platform for IoT applications

Goals:
* provide an authomous software platform for various IoT systems
* collection of information from different sources, including physical sensors
* controlling of actuators
* creation of the abstraction layer for different protocols and categories of devices
* providing of the API for client devices (RESTfull approach chosen)
* integration with existing services
* automation scenarios: if _this_ than _that_

Components:
* `Thing` classes and subclasses; abstractions of real-world objects;
* all things are connected via various `Connection`s;
* REST API interface;
* debug CLI interface;
* `MessageHub`: message routing subsystem;
* `Handler`s: scripts that starts on specified events.

In the next release (v0.4):
* upgraded `Things` subsystem;
* caching of `Thing`'s state, dynamic state updating;
* filtering of Things by room in REST API;
* 

UML diagram:
[to be filled]

Подробное опиcание и документация данного проекта (**устаревшие**) размещены на [ Google Docs ]( https://docs.google.com/document/d/1ZmPlSTxpE9TxT5H26R77BYhkNbkK-HwpbFaOIhWRylA/edit# )
