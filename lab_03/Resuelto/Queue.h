#ifndef __QUEUE_H
#define __QUEUE_H

#include <omnetpp.h>

using namespace omnetpp;

class Queue : public cSimpleModule
{
  private:
    int bufferSize;
    cQueue queue;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

#endif