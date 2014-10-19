pySimians
=========

pySimians is a suite of Python tools for testing the fault-tolerance of your cloud.
It consists of services (lovingly called monkeys) that introduce random failures on your machines, detect security faults and test your infrastructure's ability to survive them.
While inspired by Netflix's SimianArmy (https://github.com/Netflix/SimianArmy), it aims to introduce a lot more freedom for the user: with more configurable options, plug-ins, scripts and supporting all cloud providers.

The current services include:

Chaos monkey
------------
Selects a random machine from your infrastructure and tries to break it (either brings it down entirely or fills the disk, burns cpu, introduces network latency, etc).

Security monkey
---------------
Crawls your servers and checks for bad practices and known flaws (expired SSL certificates, vulnerable package versions, etc). It then creates a report with all the anomalies that were detected and the faulty servers.

Janitor monkey
--------------
Should ensure that your cloud environment is running free of clutter and waste. It searches for unused resources and disposes of them.
This is WIP.


Any contributions are welcome.
