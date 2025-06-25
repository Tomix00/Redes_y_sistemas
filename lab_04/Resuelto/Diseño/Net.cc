#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <array>
#include <packet_m.h>
#include "FeedbackPacket_m.h"

static const int researchCounter = 3;
static const int maxNodes = 200;

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    cOutVector resendPacketsVector;
    cOutVector feedbacksVector;
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    std::array<std::array<simtime_t, 2>, maxNodes> costTable;
    std::array<int, maxNodes> researchTable;
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    resendPacketsVector.setName("ResendedPackets");
    feedbacksVector.setName("Feedbacks");

    /*Incializamos los valores de costo en saltos de transporte a cada nodo*/
    for (int row=0; row<2; row++) {
        for (int col=0; col<maxNodes; col++) {
            costTable[row][col] = -1;
        }
    }
    costTable[0][this->getParentModule()->getIndex()] = 0;
    costTable[1][this->getParentModule()->getIndex()] = 0;
    for (int col=0; col<maxNodes; col++) {
        researchTable[col] = researchCounter;
    }
}

void Net::finish() {
}

void Net::handleMessage(cMessage *msg) {
    
    Packet *pkt = (Packet *) msg;
    if(pkt->isFeedback()){
        FeedbackPacket *fkt = (FeedbackPacket *) pkt;
        if (fkt->getDestination() == this->getParentModule()->getIndex()){
            costTable[fkt->getClockWay()][fkt->getLastDestination()] = fkt->getDelay();
            delete(fkt);
        }
        else{
            send(fkt, "toLnk$o", 1);
        }
    }
    else{
        // If this node is the final destination, send to App
        if (pkt->getDestination() == this->getParentModule()->getIndex()) {
            send(msg, "toApp$o");
            if(pkt->getNeedFeedback()){
                FeedbackPacket *fkt = new FeedbackPacket();
                fkt->setDestination(pkt->getSource());
                fkt->setDelay(simTime() - pkt->getCreationTime());
                fkt->setClockWay(1);
                fkt->setLastDestination(pkt->getDestination());
                fkt->setIsFeedback(true);
                send(fkt, "toLnk$o", 1);
                feedbacksVector.record(1);
            }
        }
        // If not, forward the packet to some else... to who?
        else {
            pkt->setHopCount(pkt->getHopCount()+1);
            if(pkt->getSource() == this->getParentModule()->getIndex()){   
                if(researchTable[pkt->getDestination()]<=0){
                    costTable[0][pkt->getDestination()] = -1;
                    costTable[1][pkt->getDestination()] = -1;
                    researchTable[pkt->getDestination()] = researchCounter;
                } else {
                    researchTable[pkt->getDestination()]--;
                }
                
                if(costTable[1][pkt->getDestination()]<0){
                    pkt->setNeedFeedback(true);
                    pkt->setClockWay(1);
                    send(pkt, "toLnk$o", 1);
                } 
                else if(costTable[0][pkt->getDestination()]<0){
                    pkt->setNeedFeedback(true);
                    pkt->setClockWay(0);
                    send(pkt, "toLnk$o", 0);
                } 
                else  if(costTable[0][pkt->getDestination()]<0 && costTable[1][pkt->getDestination()]<0){
                    pkt->setNeedFeedback(false);
                    int clockWay = costTable[0][pkt->getDestination()] > costTable[1][pkt->getDestination()];
                    pkt->setClockWay(clockWay);
                    send(pkt, "toLnk$o", clockWay);
                }
            }
            else{
                send(msg, "toLnk$o", pkt->getClockWay());
                resendPacketsVector.record(1);
            }
        }
    }
}

