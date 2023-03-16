#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <vector>

constexpr size_t    CLIENT_ID_SIZE = 16;

class clientHelper {
public:
	clientHelper();
	std::string getClientIp();
	std::string getClientName();
	std::string getClientFilePath();
	std::string getClientPort();
	void getExistingClientData();
	int getCountSendFile();
	long getCrcSum();
	void updateCountSendFile();
	void updateClientID(std::string clientID);
	void updateClientAES(std::string clientAES, int keyLength);
	void updateCrcSum(long crcSum);

private:
	std::string clientIp;
	std::string clientPort;
	std::string clientName;
	std::string clientFilePath;
	std::string clientID;
	std::string clientAES;
	long crcSum;
	int countSendFile;
};

