#ifndef TRANSPORTRX
#define TRANSPORTRX

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPacket_m.h"

using namespace omnetpp;

class TransportRx: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
public:
    TransportRx();
    virtual ~TransportRx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportRx);

TransportRx::TransportRx() {
    endServiceEvent = NULL;
}

TransportRx::~TransportRx() {
    cancelAndDelete(endServiceEvent);
}

void TransportRx::initialize() {
    buffer.setName("buffer");
    bufferSizeVector.setName("bufferSize");
    packetDropVector.setName("packetDrop");
    endServiceEvent = new cPacket("endService");
    endServiceEvent->setKind(1);  
}

void TransportRx::finish() {
}

void TransportRx::handleMessage(cMessage *msg) {
    
    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        // if packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // dequeue packet
            cPacket *pkt = (cPacket*) buffer.pop();
            pkt->setKind(1);  
            // send packet
            send(pkt, "outPackage");
            // start new service
            serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    }
    else if (msg->getKind() == 2) {
        delete msg;
        FeedbackPacket *fb = new FeedbackPacket("Feedback");
        fb->setKind(2);  
        fb->setSendable(buffer.getLength() < par("bufferSize").doubleValue());
        send(fb, "outFeedback");
    } 
    else { 
        // check buffer limit
            if (buffer.getLength() >= par("bufferSize").doubleValue()) {
                // drop the packet
                delete msg;
                this->bubble("packet dropped");
                packetDropVector.record(1);
            } else {
                // enqueue the packet
                buffer.insert(msg);
                bufferSizeVector.record(buffer.getLength());
                // if the server is idle
                if (!endServiceEvent->isScheduled()) {
                    // start the service now
                    scheduleAt(simTime() + 0, endServiceEvent);
                    }
                }
            }
}

#endif /* TRANSPORTRX */