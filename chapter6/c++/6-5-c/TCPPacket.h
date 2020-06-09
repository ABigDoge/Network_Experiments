#include <iostream>
#include <fstream>
#include <cstdio>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>

using namespace std;

unsigned str2int(string ip) {
    int re = 0, tmp = 0;
    for (auto chr:ip) {
        if (chr == '.') {
            re = re * 256 + tmp;
            tmp = 0;
        } else {
            tmp = tmp * 10 + chr - '0';
        }
    }
    return re * 256 + tmp;
}

class TCPPacket {
    int socket_id;
    socklen_t last_src_addrlen;
    sockaddr_in last_src;

public:
    TCPPacket(int port=0) {
        socket_id = socket(AF_INET, SOCK_STREAM, 0);
        sockaddr_in serveraddr{};
        serveraddr.sin_family = AF_INET;
        serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
        serveraddr.sin_port = htons(port);
        auto re = bind(socket_id, (struct sockaddr *) &serveraddr, sizeof(serveraddr));
    }

    ~TCPPacket() {
        close(socket_id);
    }

    void conn(string ip, int port) {
        sockaddr_in dst{};
        dst.sin_family = AF_INET;
        dst.sin_addr.s_addr = htonl(str2int(ip));
        dst.sin_port = htons(port);
        cout << "request: syn(1), ack(0)" << endl;
        if (auto cnn = connect(socket_id, (sockaddr *) &dst, sizeof(dst)) < 0) {
            cout << "Fail" << endl;
        } else {
            cout << "reply: syn(1), ack(1)" << endl;
            shutdown(cnn, 2); 
        }
    }

    void lsn() {
        int rqst;
        while(true) 
        {
            while ((rqst = accept(socket_id,
              (struct sockaddr *) &last_src, &last_src_addrlen)) < 0) {
                if ((errno != ECHILD) && (errno != EINTR)) {
                    exit(1);
                }
            }
            cout << "get a connection" << endl;
            shutdown(rqst, 2);  
        }
    }
};