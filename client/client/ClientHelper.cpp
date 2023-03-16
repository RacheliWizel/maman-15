#include "ClientHelper.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <cstdlib>


clientHelper::clientHelper() {
	std::ifstream myfile("C:\\Users\\1\\PycharmProjects\\maman15\\client\\x64\\Debug\\transfer.info");

	std::string conectionInfo;
	if (myfile.is_open()) { // always check whether the file is open
		getline(myfile, conectionInfo);
		int index = conectionInfo.find(":");
		this->clientIp = conectionInfo.substr(0, index);
		this->clientPort = conectionInfo.substr(index + 1);
		getline(myfile, this->clientName);
		getline(myfile, this->clientFilePath);
		myfile.close();
	}
	else {
		std::cerr << "cannot open file";
	}
	this->countSendFile = 0;
	this->clientID = "net_set";
	this->clientAES = "net_set";
}

std::string clientHelper::getClientFilePath() {
	return this->clientFilePath;
}

std::string clientHelper::getClientIp() {
	return this->clientIp;
}

std::string clientHelper::getClientName() {
	return this->clientName;
}

std::string clientHelper::getClientPort() {
	return this->clientPort;
}

int clientHelper::getCountSendFile() {
	return this->countSendFile;
}

long clientHelper::getCrcSum() {
	return this->crcSum;
}

void clientHelper::updateCountSendFile() {
	this->countSendFile++;
}

void clientHelper::updateClientID(std::string clientID) {
	std::copy(clientID[0], clientID[CLIENT_ID_SIZE -1], this->clientID);
}

void clientHelper::updateClientAES(std::string clientAES, int keyLength) {
	std::copy(clientID[0], clientID[keyLength - 1], this->clientAES);
}

void clientHelper::updateCrcSum(long crcSum) {
	this->crcSum = crcSum;
}


bool checkIfReconnect() {
	std::ifstream myfile("C:\\Users\\1\\PycharmProjects\\maman15\\client\\x64\\Debug\\me.info");
	if (myfile.is_open()) { 
		myfile.close();
		return false;
	}
	return true;
}

void clientHelper::getExistingClientData() {
	std::string ClientName;
	std::ifstream myfile("C:\\Users\\1\\PycharmProjects\\maman15\\client\\x64\\Debug\\me.info");
	if (myfile.is_open()) { // check whether the file is open
		getline(myfile, ClientName);
		getline(myfile, this->clientID);
		getline(myfile, this->clientAES);
		myfile.close();
	}
	else {
		std::cerr << "cannot open file";
	}
}