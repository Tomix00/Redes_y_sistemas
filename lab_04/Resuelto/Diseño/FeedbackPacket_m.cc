//
// Generated file, do not edit! Created by opp_msgtool 6.0 from FeedbackPacket.msg.
//

// Disable warnings about unused variables, empty switch stmts, etc:
#ifdef _MSC_VER
#  pragma warning(disable:4101)
#  pragma warning(disable:4065)
#endif

#if defined(__clang__)
#  pragma clang diagnostic ignored "-Wshadow"
#  pragma clang diagnostic ignored "-Wconversion"
#  pragma clang diagnostic ignored "-Wunused-parameter"
#  pragma clang diagnostic ignored "-Wc++98-compat"
#  pragma clang diagnostic ignored "-Wunreachable-code-break"
#  pragma clang diagnostic ignored "-Wold-style-cast"
#elif defined(__GNUC__)
#  pragma GCC diagnostic ignored "-Wshadow"
#  pragma GCC diagnostic ignored "-Wconversion"
#  pragma GCC diagnostic ignored "-Wunused-parameter"
#  pragma GCC diagnostic ignored "-Wold-style-cast"
#  pragma GCC diagnostic ignored "-Wsuggest-attribute=noreturn"
#  pragma GCC diagnostic ignored "-Wfloat-conversion"
#endif

#include <iostream>
#include <sstream>
#include <memory>
#include <type_traits>
#include "FeedbackPacket_m.h"

namespace omnetpp {

// Template pack/unpack rules. They are declared *after* a1l type-specific pack functions for multiple reasons.
// They are in the omnetpp namespace, to allow them to be found by argument-dependent lookup via the cCommBuffer argument

// Packing/unpacking an std::vector
template<typename T, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::vector<T,A>& v)
{
    int n = v.size();
    doParsimPacking(buffer, n);
    for (int i = 0; i < n; i++)
        doParsimPacking(buffer, v[i]);
}

template<typename T, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::vector<T,A>& v)
{
    int n;
    doParsimUnpacking(buffer, n);
    v.resize(n);
    for (int i = 0; i < n; i++)
        doParsimUnpacking(buffer, v[i]);
}

// Packing/unpacking an std::list
template<typename T, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::list<T,A>& l)
{
    doParsimPacking(buffer, (int)l.size());
    for (typename std::list<T,A>::const_iterator it = l.begin(); it != l.end(); ++it)
        doParsimPacking(buffer, (T&)*it);
}

template<typename T, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::list<T,A>& l)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        l.push_back(T());
        doParsimUnpacking(buffer, l.back());
    }
}

// Packing/unpacking an std::set
template<typename T, typename Tr, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::set<T,Tr,A>& s)
{
    doParsimPacking(buffer, (int)s.size());
    for (typename std::set<T,Tr,A>::const_iterator it = s.begin(); it != s.end(); ++it)
        doParsimPacking(buffer, *it);
}

template<typename T, typename Tr, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::set<T,Tr,A>& s)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        T x;
        doParsimUnpacking(buffer, x);
        s.insert(x);
    }
}

// Packing/unpacking an std::map
template<typename K, typename V, typename Tr, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::map<K,V,Tr,A>& m)
{
    doParsimPacking(buffer, (int)m.size());
    for (typename std::map<K,V,Tr,A>::const_iterator it = m.begin(); it != m.end(); ++it) {
        doParsimPacking(buffer, it->first);
        doParsimPacking(buffer, it->second);
    }
}

template<typename K, typename V, typename Tr, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::map<K,V,Tr,A>& m)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        K k; V v;
        doParsimUnpacking(buffer, k);
        doParsimUnpacking(buffer, v);
        m[k] = v;
    }
}

// Default pack/unpack function for arrays
template<typename T>
void doParsimArrayPacking(omnetpp::cCommBuffer *b, const T *t, int n)
{
    for (int i = 0; i < n; i++)
        doParsimPacking(b, t[i]);
}

template<typename T>
void doParsimArrayUnpacking(omnetpp::cCommBuffer *b, T *t, int n)
{
    for (int i = 0; i < n; i++)
        doParsimUnpacking(b, t[i]);
}

// Default rule to prevent compiler from choosing base class' doParsimPacking() function
template<typename T>
void doParsimPacking(omnetpp::cCommBuffer *, const T& t)
{
    throw omnetpp::cRuntimeError("Parsim error: No doParsimPacking() function for type %s", omnetpp::opp_typename(typeid(t)));
}

template<typename T>
void doParsimUnpacking(omnetpp::cCommBuffer *, T& t)
{
    throw omnetpp::cRuntimeError("Parsim error: No doParsimUnpacking() function for type %s", omnetpp::opp_typename(typeid(t)));
}

}  // namespace omnetpp

Register_Class(FeedbackPacket)

FeedbackPacket::FeedbackPacket(const char *name, short kind) : ::omnetpp::cPacket(name, kind)
{
}

FeedbackPacket::FeedbackPacket(const FeedbackPacket& other) : ::omnetpp::cPacket(other)
{
    copy(other);
}

FeedbackPacket::~FeedbackPacket()
{
}

FeedbackPacket& FeedbackPacket::operator=(const FeedbackPacket& other)
{
    if (this == &other) return *this;
    ::omnetpp::cPacket::operator=(other);
    copy(other);
    return *this;
}

void FeedbackPacket::copy(const FeedbackPacket& other)
{
    this->delay = other.delay;
    this->lastDestination = other.lastDestination;
    this->source = other.source;
    this->destination = other.destination;
    this->hopCount = other.hopCount;
    this->clockWay = other.clockWay;
    this->needFeedback = other.needFeedback;
    this->isFeedback_ = other.isFeedback_;
}

void FeedbackPacket::parsimPack(omnetpp::cCommBuffer *b) const
{
    ::omnetpp::cPacket::parsimPack(b);
    doParsimPacking(b,this->delay);
    doParsimPacking(b,this->lastDestination);
    doParsimPacking(b,this->source);
    doParsimPacking(b,this->destination);
    doParsimPacking(b,this->hopCount);
    doParsimPacking(b,this->clockWay);
    doParsimPacking(b,this->needFeedback);
    doParsimPacking(b,this->isFeedback_);
}

void FeedbackPacket::parsimUnpack(omnetpp::cCommBuffer *b)
{
    ::omnetpp::cPacket::parsimUnpack(b);
    doParsimUnpacking(b,this->delay);
    doParsimUnpacking(b,this->lastDestination);
    doParsimUnpacking(b,this->source);
    doParsimUnpacking(b,this->destination);
    doParsimUnpacking(b,this->hopCount);
    doParsimUnpacking(b,this->clockWay);
    doParsimUnpacking(b,this->needFeedback);
    doParsimUnpacking(b,this->isFeedback_);
}

omnetpp::simtime_t FeedbackPacket::getDelay() const
{
    return this->delay;
}

void FeedbackPacket::setDelay(omnetpp::simtime_t delay)
{
    this->delay = delay;
}

int FeedbackPacket::getLastDestination() const
{
    return this->lastDestination;
}

void FeedbackPacket::setLastDestination(int lastDestination)
{
    this->lastDestination = lastDestination;
}

int FeedbackPacket::getSource() const
{
    return this->source;
}

void FeedbackPacket::setSource(int source)
{
    this->source = source;
}

int FeedbackPacket::getDestination() const
{
    return this->destination;
}

void FeedbackPacket::setDestination(int destination)
{
    this->destination = destination;
}

int FeedbackPacket::getHopCount() const
{
    return this->hopCount;
}

void FeedbackPacket::setHopCount(int hopCount)
{
    this->hopCount = hopCount;
}

int FeedbackPacket::getClockWay() const
{
    return this->clockWay;
}

void FeedbackPacket::setClockWay(int clockWay)
{
    this->clockWay = clockWay;
}

bool FeedbackPacket::getNeedFeedback() const
{
    return this->needFeedback;
}

void FeedbackPacket::setNeedFeedback(bool needFeedback)
{
    this->needFeedback = needFeedback;
}

bool FeedbackPacket::isFeedback() const
{
    return this->isFeedback_;
}

void FeedbackPacket::setIsFeedback(bool isFeedback)
{
    this->isFeedback_ = isFeedback;
}

class FeedbackPacketDescriptor : public omnetpp::cClassDescriptor
{
  private:
    mutable const char **propertyNames;
    enum FieldConstants {
        FIELD_delay,
        FIELD_lastDestination,
        FIELD_source,
        FIELD_destination,
        FIELD_hopCount,
        FIELD_clockWay,
        FIELD_needFeedback,
        FIELD_isFeedback,
    };
  public:
    FeedbackPacketDescriptor();
    virtual ~FeedbackPacketDescriptor();

    virtual bool doesSupport(omnetpp::cObject *obj) const override;
    virtual const char **getPropertyNames() const override;
    virtual const char *getProperty(const char *propertyName) const override;
    virtual int getFieldCount() const override;
    virtual const char *getFieldName(int field) const override;
    virtual int findField(const char *fieldName) const override;
    virtual unsigned int getFieldTypeFlags(int field) const override;
    virtual const char *getFieldTypeString(int field) const override;
    virtual const char **getFieldPropertyNames(int field) const override;
    virtual const char *getFieldProperty(int field, const char *propertyName) const override;
    virtual int getFieldArraySize(omnetpp::any_ptr object, int field) const override;
    virtual void setFieldArraySize(omnetpp::any_ptr object, int field, int size) const override;

    virtual const char *getFieldDynamicTypeString(omnetpp::any_ptr object, int field, int i) const override;
    virtual std::string getFieldValueAsString(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldValueAsString(omnetpp::any_ptr object, int field, int i, const char *value) const override;
    virtual omnetpp::cValue getFieldValue(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldValue(omnetpp::any_ptr object, int field, int i, const omnetpp::cValue& value) const override;

    virtual const char *getFieldStructName(int field) const override;
    virtual omnetpp::any_ptr getFieldStructValuePointer(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldStructValuePointer(omnetpp::any_ptr object, int field, int i, omnetpp::any_ptr ptr) const override;
};

Register_ClassDescriptor(FeedbackPacketDescriptor)

FeedbackPacketDescriptor::FeedbackPacketDescriptor() : omnetpp::cClassDescriptor(omnetpp::opp_typename(typeid(FeedbackPacket)), "omnetpp::cPacket")
{
    propertyNames = nullptr;
}

FeedbackPacketDescriptor::~FeedbackPacketDescriptor()
{
    delete[] propertyNames;
}

bool FeedbackPacketDescriptor::doesSupport(omnetpp::cObject *obj) const
{
    return dynamic_cast<FeedbackPacket *>(obj)!=nullptr;
}

const char **FeedbackPacketDescriptor::getPropertyNames() const
{
    if (!propertyNames) {
        static const char *names[] = {  nullptr };
        omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
        const char **baseNames = base ? base->getPropertyNames() : nullptr;
        propertyNames = mergeLists(baseNames, names);
    }
    return propertyNames;
}

const char *FeedbackPacketDescriptor::getProperty(const char *propertyName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    return base ? base->getProperty(propertyName) : nullptr;
}

int FeedbackPacketDescriptor::getFieldCount() const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    return base ? 8+base->getFieldCount() : 8;
}

unsigned int FeedbackPacketDescriptor::getFieldTypeFlags(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldTypeFlags(field);
        field -= base->getFieldCount();
    }
    static unsigned int fieldTypeFlags[] = {
        FD_ISEDITABLE,    // FIELD_delay
        FD_ISEDITABLE,    // FIELD_lastDestination
        FD_ISEDITABLE,    // FIELD_source
        FD_ISEDITABLE,    // FIELD_destination
        FD_ISEDITABLE,    // FIELD_hopCount
        FD_ISEDITABLE,    // FIELD_clockWay
        FD_ISEDITABLE,    // FIELD_needFeedback
        FD_ISEDITABLE,    // FIELD_isFeedback
    };
    return (field >= 0 && field < 8) ? fieldTypeFlags[field] : 0;
}

const char *FeedbackPacketDescriptor::getFieldName(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldName(field);
        field -= base->getFieldCount();
    }
    static const char *fieldNames[] = {
        "delay",
        "lastDestination",
        "source",
        "destination",
        "hopCount",
        "clockWay",
        "needFeedback",
        "isFeedback",
    };
    return (field >= 0 && field < 8) ? fieldNames[field] : nullptr;
}

int FeedbackPacketDescriptor::findField(const char *fieldName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    int baseIndex = base ? base->getFieldCount() : 0;
    if (strcmp(fieldName, "delay") == 0) return baseIndex + 0;
    if (strcmp(fieldName, "lastDestination") == 0) return baseIndex + 1;
    if (strcmp(fieldName, "source") == 0) return baseIndex + 2;
    if (strcmp(fieldName, "destination") == 0) return baseIndex + 3;
    if (strcmp(fieldName, "hopCount") == 0) return baseIndex + 4;
    if (strcmp(fieldName, "clockWay") == 0) return baseIndex + 5;
    if (strcmp(fieldName, "needFeedback") == 0) return baseIndex + 6;
    if (strcmp(fieldName, "isFeedback") == 0) return baseIndex + 7;
    return base ? base->findField(fieldName) : -1;
}

const char *FeedbackPacketDescriptor::getFieldTypeString(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldTypeString(field);
        field -= base->getFieldCount();
    }
    static const char *fieldTypeStrings[] = {
        "omnetpp::simtime_t",    // FIELD_delay
        "int",    // FIELD_lastDestination
        "int",    // FIELD_source
        "int",    // FIELD_destination
        "int",    // FIELD_hopCount
        "int",    // FIELD_clockWay
        "bool",    // FIELD_needFeedback
        "bool",    // FIELD_isFeedback
    };
    return (field >= 0 && field < 8) ? fieldTypeStrings[field] : nullptr;
}

const char **FeedbackPacketDescriptor::getFieldPropertyNames(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldPropertyNames(field);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    }
}

const char *FeedbackPacketDescriptor::getFieldProperty(int field, const char *propertyName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldProperty(field, propertyName);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    }
}

int FeedbackPacketDescriptor::getFieldArraySize(omnetpp::any_ptr object, int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldArraySize(object, field);
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        default: return 0;
    }
}

void FeedbackPacketDescriptor::setFieldArraySize(omnetpp::any_ptr object, int field, int size) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldArraySize(object, field, size);
            return;
        }
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        default: throw omnetpp::cRuntimeError("Cannot set array size of field %d of class 'FeedbackPacket'", field);
    }
}

const char *FeedbackPacketDescriptor::getFieldDynamicTypeString(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldDynamicTypeString(object,field,i);
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        default: return nullptr;
    }
}

std::string FeedbackPacketDescriptor::getFieldValueAsString(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldValueAsString(object,field,i);
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        case FIELD_delay: return simtime2string(pp->getDelay());
        case FIELD_lastDestination: return long2string(pp->getLastDestination());
        case FIELD_source: return long2string(pp->getSource());
        case FIELD_destination: return long2string(pp->getDestination());
        case FIELD_hopCount: return long2string(pp->getHopCount());
        case FIELD_clockWay: return long2string(pp->getClockWay());
        case FIELD_needFeedback: return bool2string(pp->getNeedFeedback());
        case FIELD_isFeedback: return bool2string(pp->isFeedback());
        default: return "";
    }
}

void FeedbackPacketDescriptor::setFieldValueAsString(omnetpp::any_ptr object, int field, int i, const char *value) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldValueAsString(object, field, i, value);
            return;
        }
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        case FIELD_delay: pp->setDelay(string2simtime(value)); break;
        case FIELD_lastDestination: pp->setLastDestination(string2long(value)); break;
        case FIELD_source: pp->setSource(string2long(value)); break;
        case FIELD_destination: pp->setDestination(string2long(value)); break;
        case FIELD_hopCount: pp->setHopCount(string2long(value)); break;
        case FIELD_clockWay: pp->setClockWay(string2long(value)); break;
        case FIELD_needFeedback: pp->setNeedFeedback(string2bool(value)); break;
        case FIELD_isFeedback: pp->setIsFeedback(string2bool(value)); break;
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'FeedbackPacket'", field);
    }
}

omnetpp::cValue FeedbackPacketDescriptor::getFieldValue(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldValue(object,field,i);
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        case FIELD_delay: return pp->getDelay().dbl();
        case FIELD_lastDestination: return pp->getLastDestination();
        case FIELD_source: return pp->getSource();
        case FIELD_destination: return pp->getDestination();
        case FIELD_hopCount: return pp->getHopCount();
        case FIELD_clockWay: return pp->getClockWay();
        case FIELD_needFeedback: return pp->getNeedFeedback();
        case FIELD_isFeedback: return pp->isFeedback();
        default: throw omnetpp::cRuntimeError("Cannot return field %d of class 'FeedbackPacket' as cValue -- field index out of range?", field);
    }
}

void FeedbackPacketDescriptor::setFieldValue(omnetpp::any_ptr object, int field, int i, const omnetpp::cValue& value) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldValue(object, field, i, value);
            return;
        }
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        case FIELD_delay: pp->setDelay(value.doubleValue()); break;
        case FIELD_lastDestination: pp->setLastDestination(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_source: pp->setSource(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_destination: pp->setDestination(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_hopCount: pp->setHopCount(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_clockWay: pp->setClockWay(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_needFeedback: pp->setNeedFeedback(value.boolValue()); break;
        case FIELD_isFeedback: pp->setIsFeedback(value.boolValue()); break;
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'FeedbackPacket'", field);
    }
}

const char *FeedbackPacketDescriptor::getFieldStructName(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldStructName(field);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    };
}

omnetpp::any_ptr FeedbackPacketDescriptor::getFieldStructValuePointer(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldStructValuePointer(object, field, i);
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        default: return omnetpp::any_ptr(nullptr);
    }
}

void FeedbackPacketDescriptor::setFieldStructValuePointer(omnetpp::any_ptr object, int field, int i, omnetpp::any_ptr ptr) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldStructValuePointer(object, field, i, ptr);
            return;
        }
        field -= base->getFieldCount();
    }
    FeedbackPacket *pp = omnetpp::fromAnyPtr<FeedbackPacket>(object); (void)pp;
    switch (field) {
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'FeedbackPacket'", field);
    }
}

namespace omnetpp {

}  // namespace omnetpp

