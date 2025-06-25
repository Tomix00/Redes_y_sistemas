#ifndef TRANSPORTTX
#define TRANSPORTTX

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPacket_m.h"

using namespace omnetpp;

class TransportTx: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
public:
    TransportTx();
    virtual ~TransportTx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportTx);

TransportTx::TransportTx() {
    endServiceEvent = NULL;
}

TransportTx::~TransportTx() {
    cancelAndDelete(endServiceEvent);
}

void TransportTx::initialize() {
    buffer.setName("buffer");
    bufferSizeVector.setName("bufferSize");
    packetDropVector.setName("packetDrop");
    endServiceEvent = new cPacket("endService");
    endServiceEvent->setKind(1);  
}

void TransportTx::finish() {
}

void TransportTx::handleMessage(cMessage *msg) {
    
    // if msg is signaling an endServiceEvent
    if (msg == endServiceEvent) {
        FeedbackPacket *fb = new FeedbackPacket("Feedback");
        fb->setKind(2);  
        send(fb, "outFeedback");
    } 
    else if (msg->getKind() == 2) {
        FeedbackPacket *fbPacket = check_and_cast<FeedbackPacket *>(msg);
        if (fbPacket->getSendable()) {
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
        } else {
            FeedbackPacket *fb = new FeedbackPacket("Feedback");
            fb->setKind(2);  
            fb->setTrySend(true);
            send(fb, "outFeedback");
        }
        delete(fbPacket);
    }
    else { 
        // check buffer limit
            if (buffer.getLength() >= par("bufferSize").doubleValue()) {
                // drop the packet
                delete msg;
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

#endif /* TRANSPORTTX */
