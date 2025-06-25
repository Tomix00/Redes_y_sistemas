simple Generator
{
    parameters:
        volatile double generationInterval; // sec
        volatile double packetByteSize;     // bytes
        @display("i=block/source");
    gates:
        output out;
}

simple Sink
{
    parameters:
        @display("i=block/sink");
    gates:
        input in;
}

simple Queue
{
    parameters:
        volatile double bufferSize;  // bytes
        volatile double serviceTime; // sec
        @display("i=block/queue;q=buffer");
    gates:
        input inFeedback;
        input inPackage;
        output outFeedback;
        output outPackage;
} 

simple TransportTx
{
    parameters:
        double bufferSize;
        volatile double serviceTime; // sec
        @display("i=block/queue;q=buffer");
    gates:
        input inFeedback;
        input inPackage;
        input skip;
        output outFeedback;
        output outPackage;
}

simple TransportRx
{
    parameters:
        double bufferSize;
        volatile double serviceTime; // sec
        @display("i=block/queue;q=buffer");
    gates:
        input inFeedback;
        input inPackage;
        output outFeedback;
        output outPackage;
        output skip;
}

module NodeTx
{
    parameters:
        @display("i=block/routing");
    gates:
        input inFeedback;
        input inPackage;
        output outFeedback;
        output outPackage;
    submodules:
        gen: Generator {
            parameters:
                @display("p=75,50");
        }
        transport: TransportTx {
            parameters:
                @display("p=75,190");
        }
    connections:
        gen.out --> transport.inPackage;
        transport.outPackage --> outPackage;
        transport.outFeedback --> outFeedback;
        inFeedback --> transport.inFeedback;
        inPackage --> transport.skip;
}

module NodeRx
{
    parameters:
        @display("i=block/routing");
    gates:
        input inFeedback;
        input inPackage;
        output outFeedback;
        output outPackage;
    submodules:
        sink: Sink {
            parameters:
                @display("p=75,50");
        }
        transport: TransportRx {
            parameters:
                @display("p=75,190");
        }
    connections:
        inPackage --> transport.inPackage;
        inFeedback --> transport.inFeedback;
        transport.outPackage --> { datarate = 0.5Mbps; } --> sink.in;
        transport.outFeedback --> outFeedback;
        transport.skip --> outPackage;
}

network Network
{
    @display("bgl=2");
    submodules:
        nodeTx: NodeTx {
            @display("p=30,30");
        }
        nodeRx: NodeRx {
            @display("p=230,30");
        }
        queueTx: Queue {
            @display("p=130,30");
        }
        queueRx: Queue {
            @display("p=130,90");
        }
        
    connections:
        nodeTx.outPackage --> {datarate = 1Mbps; delay = 100us; } --> queueTx.inPackage;
        queueTx.outPackage --> {datarate = 1Mbps; delay = 100us; } --> nodeRx.inPackage;

        nodeTx.outFeedback --> queueTx.inFeedback;
        queueTx.outFeedback --> nodeRx.inFeedback;

        nodeRx.outFeedback --> queueRx.inFeedback;
        queueRx.outFeedback --> nodeTx.inFeedback;  

        nodeRx.outPackage --> queueRx.inPackage;
        queueRx.outPackage --> nodeTx.inPackage;  
}



