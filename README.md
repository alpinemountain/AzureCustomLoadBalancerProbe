# AzureCustomLoadBalancerProbe

This is a custom load balancer probe written in Python for the following scenario:

You have two VMs with one "primary" and the second "backup."  Only the "primary" is allowed to receive traffic.  When you execute LoadBalancerCustomProbeForPrimaryBackup_MakePrimary.py, it will change the primary to the current machine.

The state is maintained in an Azure Block Block "currentPrimary.dat"
