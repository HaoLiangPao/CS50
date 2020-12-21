# Docker Learning

##### Step 1: Virtual Machine

1. Ubuntu
2. Guest Addition -> Resolution auto switching



##### Step 2: Intall Docker

1. Update / Install curl

   `suto apt-get curl`

2. Download and Install Docker through https request

   `curl -fsSL https://get.docker.com -o get-docker.sh`

3. Get demo docker image
   `docker run docker/whalesay cowsay Hello World`
   *However, the docker command may needs root permission, we can choose to add the user to docker group*

   ```bash
   sudo groupadd docker
   # Add your user to the docker group.
   sudo usermod -aG docker ${USER}
   # You would need to loog out and log back in so that your group membership is re-evaluated or type the following command:
   su -s ${USER}
   # Verify that you can run docker commands without sudo.
   docker run hello-world
   ```

4. 

5. 

6. 

7. 

8. 

9. 

10. 

##### Step 3: Docker Command

1. Run & Start
