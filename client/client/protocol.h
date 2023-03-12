#pragma once
#include <cstdint>
#include <sstream>
#include <string>
#include <vector>

 // create header params
typedef uint8_t  version_t;
typedef uint16_t code_t;
typedef uint32_t payloadsize_t;

// param's sizes
constexpr version_t CLIENT_VERSION = 3;
constexpr size_t    CLIENT_ID_SIZE = 16;
constexpr size_t    CLIENT_NAME_SIZE = 255;
constexpr size_t    PUBLIC_KEY_SIZE = 160; 
constexpr size_t	CONTENT_SIZE_SIZE = 4;

int DEF_VAL = 0;

enum RequestCodeEnum
{
	REGISTRATION = 1100,
	SEND_PUBLIC_KEY = 1101,
	RE_CONNECT = 1102,
	SEND_FILE = 1103,
	CORRECT_CRC = 1104,
	INCORRECT_CRC = 1105,
	INCORRECT_CRC_FOURTH = 1106
};

enum ResponseCodeEnum
{
	REGISTRATION_SUCCESS = 2100,
	REGISTRATION_FAILED = 2101,
	AES_CREATED = 2102,
	CORRECT_AND_SEND_CRC = 2103,
	RECEIVED_MESSAGE = 2104,
	RE_CONNECT = 2105,
	RE_CONNECT_REFUSED = 2106,
	ERROR = 2107
};

struct ClientID
{
	uint8_t uuid[CLIENT_ID_SIZE];
	ClientID() : uuid{ DEF_VAL } {}

	bool operator==(const ClientID& otherID) const {
		for (size_t i = 0; i < CLIENT_ID_SIZE; ++i)
			if (uuid[i] != otherID.uuid[i])
				return false;
		return true;
	}

	bool operator!=(const ClientID& otherID) const {
		return !(*this == otherID);
	}

};

struct RequestHeader
{
	ClientID       clientId;
	const version_t version;
	const code_t    code;
	payloadsize_t     payloadSize;

	RequestHeader(const ClientID& id, const code_t reqCode) : clientId(id), version(CLIENT_VERSION), code(reqCode), payloadSize(0) {}
};

struct ResponsHeader
{
	version_t version;
	code_t    code;
	payloadsize_t   payloadSize;
};

class request
{
public:

};

