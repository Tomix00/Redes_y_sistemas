// FeedbackPacket.msg
message FeedbackPacket extends cPacket
{
    bool sendable = false;    
    bool trySend = false;
}