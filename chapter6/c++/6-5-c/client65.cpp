#include <iostream>
#include "TCPPacket.h"

using namespace std;

int main(int argc, char **argv) {
    int c;
    string ip;
    int port;
    ip = string(argv[1]);
    port = atoi(argv[2]);
    cout << "target IP: " << ip << " , port: " << port << endl;
    TCPPacket packet(9999);
    packet.conn(ip, port);

    return 0;
}