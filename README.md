# .CAT Platform
Small platform for IoT applications

### How to clone
This repository uses git submodules. To clone it properly, use `git clone --recursive` instead of simple `git clone`. Additional information is available here: 
* StackOverflow: https://stackoverflow.com/questions/3796927/how-to-git-clone-including-submodules
* Git docs (en): [git-scm/book/en](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
* Git docs (ru): [git-scm/book/ru](https://git-scm.com/book/ru/v1/%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B-Git-%D0%9F%D0%BE%D0%B4%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B8)

### Goals:
* provide an authomous software platform for various IoT systems
* collection of information from different sources, including physical sensors
* controlling of actuators
* creation of the abstraction layer for different protocols and categories of devices
* providing of the API for client devices (RESTfull approach chosen)
* integration with existing services
* automation scenarios: if _this_ than _that_

### Components:
* `Thing` classes and subclasses; abstractions of real-world objects;
* all things are connected via various `Connection`s;
* REST API interface;
* debug CLI interface;
* `MessageHub`: message routing subsystem;
* `Handler`s: scripts that starts on specified events.

### UML diagram:
[to be filled]

### Compatibility
Core platform can be runned on any computer with Linux-based OS and Python 3 installed.

Additional dependencies: [requirements.txt](requirements.txt)

### In the next release (v0.4):
* upgraded `Things` subsystem;
* caching of `Thing`'s state, dynamic state updating;
* support of dynamic connection, reconnection and disconnection of Things;
* filtering of Things by placement (room, for example) in REST API;
* basic support of `Sensor`s and `MQTTSensor`s;
* authorization of clients;
* proper documentation.

### In future releases:
* data/history logger;
* support of the command-line parameters;
* users and permissions;
* more things and connections.

### Outdated description of the system (v0.2):
Подробное опиcание и документация данного проекта (**устаревшие**) размещены на [ Google Docs ]( https://docs.google.com/document/d/1ZmPlSTxpE9TxT5H26R77BYhkNbkK-HwpbFaOIhWRylA/edit# )
