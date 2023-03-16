#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include <stdio.h>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <sys/stat.h>
#include <boost/crc.hpp>
#include "boost/filesystem.hpp"
#include "boost/filesystem/fstream.hpp"
#include "Base64Wrapper.h"
#include "RSAWrapper.h"
#include "AESWrapper.h"
#include "ClientHelper.h"


 // create header params
//typedef uint8_t  version_t;
//typedef uint16_t code_t;
//typedef uint32_t payloadsize_t;

char CLIENT_VERSION = '3';


// param's sizes
constexpr size_t    VERSION_SIZE = 1;
constexpr size_t    CLIENT_ID_SIZE = 16;
constexpr size_t    CLIENT_NAME_SIZE = 255;
constexpr size_t	PAYLOAD_SIZE_SIZE = 4;
constexpr size_t	CODE_SIZE = 2;
constexpr size_t	FILE_CONTENT_SIZE_SIZE = 4;
constexpr size_t	FILE_NAME_SIZE = 255;
constexpr size_t	CKSUM_SIZE = 4;


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
	SEND_CRC = 2103,
	RECEIVED_MESSAGE = 2104,
	SUCCESS_RE_CONNECT = 2105,
	REFUSED_RE_CONNECT = 2106,
	ERROR_RESPONSE = 2107
};

#pragma pack(push, 1)
struct Request
{	
private:
	char clientId[CLIENT_ID_SIZE];
	char clientVersion[VERSION_SIZE];
	short   requestCode;
	int  requestPayloadSize;
	std::string requestPayload;
public:
	Request(char id[CLIENT_ID_SIZE], short reqCode, std::string payload);
	char* getRequestClientId();
	char* getRequestVersion();
	short getRequestCode();
	int getRequestPayloadSize();
	std::string getPayload();
	std::string convertToByts();
	
};
#pragma pack(pop)


#pragma pack(push, 1)
struct Response
{
private:
	char serverVersion[VERSION_SIZE];
	short responseCode;
	long responsePayloadSize;
	std::string responsePayload;
public:
	Response(char* responsFromClient);
	long getResponsePayloadSize();
	short getResponseCode();
	char* getServerVersion();
	std::string getResponsePayload();
	Request handleRequest(clientHelper client);
};
#pragma pack(pop)

std::string genaratePublicKey();
void writeMeFile(std::string name, std::string ID, std::string privetKey);




