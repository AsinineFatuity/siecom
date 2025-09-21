### Siecom Deployment 
This microservice is deployed on kubernetes node
To deploy run these commands
1. Create secrets from your `.env` file by running `kubectl create secret generic siecom-secrets --from-env-file=.env`
* Note that for `DATABASE_URL` and the other db variables, you'll need to use a hosted db (rds)
2. `kubectl apply -f k8s/deployment.yml`
3. `kubectl apply -f k8s/service.yml`
Check the status of the pods by running `kubectl get pods`
* You may optionally modify the replicas value in `k8s/deployment.yml` to spin as many instance as desired

You can debug any failures by running 
* `kubectl get pods -o wide` to see the status of all pods
* `kubectl logs <pod_name> -c <container_name>`. 

Pod name is gotten from previous command and container name from the `k8s/deployment.yml` file

4. You may restart your pods by running `kubectl rollout restart deployment siecom-deployment`
5. Incase you update your `.env`, run the command 
`kubectl create secret generic siecom-secrets   --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -`
6. Get the external IP for your pod by running `kubectl get svc siecom-service`. Then go the browser and navigate to
`http:<your_external_ip>`