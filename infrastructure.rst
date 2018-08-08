Ideal infrastructure
====================

1 Public load balancer

Multiple EC2 instances in different avaiability zones in an AWS region

RDS as Database instance

All instances except load balancer will be in private subnet, load balancer will be in Public subnet.

Nginx and uwsgi has been used as web server and application server respectively.
