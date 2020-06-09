#include <iostream>
#include "TCPPacket.h"

using namespace std;

int main() {
    TCPPacket packet(8889);
    packet.lsn();
    return 0;
}