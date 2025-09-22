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
<img width="1929" height="1112" alt="image" src="https://github.com/user-attachments/assets/447377fa-4371-4a75-95b8-e1e7992953c6" />
This was executed asynchronously by `huey`
<img width="2547" height="1024" alt="image" src="https://github.com/user-attachments/assets/fc8271ec-c804-4a2c-9adc-9162a77fce64" />




