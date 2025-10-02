## Monitoring And Observability 
1. We have a `healthz` endpoint that is used to check for the health of:
 - application's ability to receive traffic
 - database readiness 
 - cache readiness 
This is quickly accomplished using `curl` tool `curl -i http://174.138.123.164/healthz/` typical response is as below:
![curl command results](../assets/monitoring1.png)
