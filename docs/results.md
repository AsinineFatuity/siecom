## Project Results
Here I provide annotated screenshots of the results of various project requirements

### Deployment Via Kubernetes
Successful deployment via kubectl from terminal
<img width="1869" height="310" alt="image" src="https://github.com/user-attachments/assets/5c236c16-5923-46f6-9e53-d9fd1b4ea463" />
Microservice available online via public ip [http://174.138.123.164/]
<img width="2535" height="1101" alt="image" src="https://github.com/user-attachments/assets/f01fb751-31c3-4771-bc89-830cfef30ee8" />

Services consumed for this were:
- [docker hub](https://hub.docker.com/r/asininefatuity/siecom) to host the docker container
- [digital ocean kubernetes](https://www.digitalocean.com/products/kubernetes) to provision the kubernetes cluster
- [digital ocean command line interface](https://github.com/digitalocean/doctl) to connect provisioned cluster with `kubectl`

Details on **monitoring and observability** can be found [here](./monitoring.md)
### Unit & Integration Tests
The following screenshots are for a summary test runs and coverage report
<img width="2545" height="903" alt="image" src="https://github.com/user-attachments/assets/4c3c4fce-f03e-4d73-be5c-47ebbeb7ef86" />

### Email & SMS Confirmation
Email Confirmation to admin when order is made 
<img width="1768" height="1024" alt="emailExample2" src="https://github.com/user-attachments/assets/cb4868c1-6456-4beb-a859-46ee18422330" />

This was executed asynchronously by `huey`
<img width="2539" height="1045" alt="image" src="https://github.com/user-attachments/assets/d202c971-a9ca-4f31-b7a5-6cfef69c25d7" />

Configured `Africa's Talking` successfully but upon sending messages, I got response that sender id was in blacklist (tried activating all promo messages), should have arrived otherwise
<img width="2541" height="1022" alt="smsResp" src="https://github.com/user-attachments/assets/de9c3f3d-6dd2-4d41-9f7c-4dbfd632b362" />
### Continuous Integration With Github Actions
![ci image with coveralls](../assets/ci.png)
### Continuous Deployment With Github Actions
<img width="1800" height="1087" alt="image" src="https://github.com/user-attachments/assets/bbfed527-12ca-4208-b488-f75efb3931f7" />

Complete history for CI/CD can be viewed [in the actions tab](https://github.com/AsinineFatuity/siecom/actions)
