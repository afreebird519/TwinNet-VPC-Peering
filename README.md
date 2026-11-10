TwinNet – Private AWS VPC Peering Simulator

A Python-based simulation of private network connectivity between two AWS Virtual Private Clouds.

Project Overview

TwinNet is a student project that demonstrates the fundamental concepts of AWS VPC Peering through a local Python simulation.

The project models two separate Virtual Private Clouds (VPCs), their private subnets, route tables and security group rules. It evaluates whether communication between two private application hosts should be allowed or blocked based on the network configuration.

No actual AWS cloud resources are required.

Objectives

- Understand AWS VPC architecture and private IP addressing.
- Study VPC peering and routing between separate networks.
- Understand inbound security group rules.
- Simulate forward and reverse network connectivity.
- Demonstrate connectivity failure and recovery scenarios.

Architecture

Component| IPv4 CIDR / Address
VPC A| 10.10.0.0/16
VPC B| 10.20.0.0/16
Public subnet A| 10.10.1.0/24
Private subnet A| 10.10.2.0/24
Private subnet B| 10.20.1.0/24
Bastion host| 10.10.1.10
App-A| 10.10.2.10
App-B| 10.20.1.10

Technologies Used

- Python 3
- AWS VPC networking concepts
- IPv4 and CIDR addressing
- Routing tables
- Security group rules

Features

1. Baseline connectivity test before peering routes.
2. Forward connectivity simulation from App-A to App-B.
3. Reverse connectivity simulation from App-B to App-A.
4. Controlled ICMP security rule failure.
5. Connectivity recovery after restoring the security rule.
6. Logical route and inbound security rule validation.

How to Run

1. Install Python 3 on your computer.
2. Download "TwinNet_VPC_Peering_Simulator.py".
3. Open a terminal in the downloaded file's folder.
4. Run:

python TwinNet_VPC_Peering_Simulator.py

On Windows, you can also use:

py TwinNet_VPC_Peering_Simulator.py

Expected Results

- Connectivity is blocked before the peering routes are configured.
- Forward and reverse logical connectivity checks pass after routes are added.
- Removing the inbound ICMP rule blocks the simulated traffic.
- Restoring the rule allows the simulated traffic again.

Project Scope and Limitations

This is a local logic simulation based on an AWS VPC peering design. It does not create actual AWS resources or transmit real network packets. The PASS and BLOCKED results represent simulated configuration checks, not live AWS ping tests.

Author

Vaishnavi Subash Pillai
Batch: 1
Register Number: 2114242440228

Learning Outcome

This project demonstrates that successful private communication between two VPCs requires non-overlapping CIDR ranges, appropriate forward and return routes, and correctly configured security group rules.