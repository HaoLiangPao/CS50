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

   `docker run ${image name}`

   1. Tag

      ```bash
      # Default to latest tag
      docker run redis
      # Tag to specific version
      docker run redis:4.0
      ```

   2. STDIN

      **by default a docker container is not going to read standard input, it works in an non-interactive way**

      ```bash
      # kodekloud/simple-prompt-docker is a simple application takes in a prompt and print out a standard message
      # Normal
      docker run kodekloud/simple-prompt-docker
      # Interactive mode
      docker run -i kodekloud/simple-prompt-docker
      # Interactive mode + prompt active (t stands for a standard terminal)
      docker run -it kodekloud/simple-prompt-docker
      ```

   3. PORT mapping

      ```bash
      # Running a web application on local host 5000, but map it to port 80 for clients
      docker run -p 80:5000 kodekcloud/simple-webapp
      ```

   4. Volumn mapping

      ```bash
      # Data will be destroied if we remove mysql container instance
      docker run mysql
      docker stop mysql
      docker rm mysql
      
      # Specify an external address for data
      docker run -v /opt/datadir:/var/lib/mysql mysql
      
      ```

      For the second run command: map an external directory `/opt/datadir` to container data storage address (`/var/lib/mysql`), so that after we stop and remove the container instance, the data will be kept in the data directory. 

   5. 

2. Run - Tag

   1. default tag is lattest

3. 
