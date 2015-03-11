#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>

int main(){
    int sock, bytes_recieved;  
    char send_data[1024],recv_data[1024];
    struct hostent *host;
    struct sockaddr_in server_addr;  
    srand(time(NULL)); 

    host = gethostbyname("127.0.0.1");

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Socket");
        exit(1);
    }

    server_addr.sin_family = AF_INET;     
    server_addr.sin_port = htons(5001);   
    server_addr.sin_addr = *((struct in_addr *)host->h_addr);
    bzero(&(server_addr.sin_zero),8); 

    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1){
        perror("Connect: could not connect to socket");
        exit(1);
    }

    while(1){
        bytes_recieved=recv(sock,recv_data,1024,0);
        recv_data[bytes_recieved] = '\0';

        if (strcmp(recv_data , "q") == 0 || strcmp(recv_data , "Q") == 0){
            close(sock);
            //break;
        }
        else{
            printf("\nRecieved data = %s " , recv_data);
            //printf("\nSEND (q or Q to quit) : ");
            //gets(send_data);
            int numSensors = atoi(recv_data);
            strcpy(send_data,"[");

            int x=0;
            for (x;x<numSensors;x++){
                //int l = strlen(send_data);
                char str[5];

                sprintf(str,"%d",19+rand()%4);
                strcat(send_data,"\"");
                strcat(send_data,str);                
                strcat(send_data,"\",");

            }
        }
        int l = strlen(send_data)-1;
        send_data[l]=']';
//        strcat(send_data,"
        send(sock,send_data,strlen(send_data), 0); 
        sleep(6);
    }
return 0;
}
