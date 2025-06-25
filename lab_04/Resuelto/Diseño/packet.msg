packet Packet {
    int source;
    int destination;
    int hopCount;
    bool clockWay;      //Si es 1, el paquete esta siendo enviado y debe seguir siendo enviado en sentido horario y si es 0 en sentido antihorario.
    bool needFeedback;
    bool isFeedback;
}
