## Project Results
Here I provide annotated screenshots of the results of various project requirements

### Deployment Via Kubernetes
Successful deployment via kubectl from terminal
<img width="1869" height="310" alt="image" src="https://github.com/user-attachments/assets/5c236c16-5923-46f6-9e53-d9fd1b4ea463" />
Microservice available online via public ip [http://174.138.123.164]
<img width="2521" height="915" alt="image" src="https://github.com/user-attachments/assets/ded76f94-0939-4937-a238-e678fcb2be74" />
Services consumed for this were:
- [docker hub](https://hub.docker.com/r/asininefatuity/siecom) to host the docker container
- [digital ocean kubernetes](https://www.digitalocean.com/products/kubernetes) to provision the kubernetes cluster
- [digital ocean command line interface](https://github.com/digitalocean/doctl) to connect provisioned cluster with `kubectl`
### Unit & Integration Tests
The following screenshots are for a summary test runs and coverage report
<img width="2552" height="880" alt="image" src="https://github.com/user-attachments/assets/c458015e-0397-4631-a90f-9b82a66d312b" />
### Email & SMS Confirmation
Email Confirmation to admin when order is made 
<img width="1768" height="1024" alt="emailExample2" src="https://github.com/user-attachments/assets/cb4868c1-6456-4beb-a859-46ee18422330" />

This was executed asynchronously by `huey`
<img width="2539" height="1045" alt="image" src="https://github.com/user-attachments/assets/d202c971-a9ca-4f31-b7a5-6cfef69c25d7" />

Configured `Africa's Talking` successfully but upon sending messages, I got response that sender id was in blacklist (tried activating all promo messages), should have arrived otherwise
<img width="2541" height="1022" alt="smsResp" src="https://github.com/user-attachments/assets/de9c3f3d-6dd2-4d41-9f7c-4dbfd632b362" />
### Continuous Integration With Github Actions
<img width="1762" height="912" alt="image" src="https://github.com/user-attachments/assets/388e2b5d-5566-4ca0-aee0-fdf1e53fc893" />
### Continuous Delivery With Github Actions
Complete history for CI/CD can be viewed [in the actions tab](https://github.com/AsinineFatuity/siecom/actions)





