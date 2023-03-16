#include "protocol.h"

Request::Request(char id[CLIENT_ID_SIZE], short reqCode, std::string payload) {
	std::memcpy(clientId, id, CLIENT_ID_SIZE);
	this->requestCode = reqCode;
	clientVersion[0] = CLIENT_VERSION;
	this->requestPayload = payload;
	this->requestPayloadSize = sizeof(payload);
}

char* Request::getRequestClientId() {
	return this->clientId;
}

char* Request::getRequestVersion() {
	return this->clientVersion;
}

short Request::getRequestCode() {
	return this->requestCode;
}

int Request::getRequestPayloadSize() {
	return this->requestPayloadSize;
}

std::string Request::getPayload() {
	return this->requestPayload;
}

std::string Request::convertToByts()
{
    int size = this->getRequestPayloadSize();
    char* sendToServer = new char[VERSION_SIZE + CLIENT_ID_SIZE + PAYLOAD_SIZE_SIZE + CODE_SIZE + size];
    std::memcpy(sendToServer, this->getRequestClientId(), CLIENT_ID_SIZE);
    std::memcpy(sendToServer, this->getRequestVersion(), 1);
    char code[2];
    *(unsigned short*)code = this->getRequestCode();
    std::memcpy(sendToServer, code, 2);
    char payloadSize[4];
    *(unsigned int*)payloadSize = this->getRequestPayloadSize();
    std::memcpy(sendToServer, payloadSize, 4);
    std::memcpy(sendToServer, (this->getPayload()).c_str(), size);
    return sendToServer;
}

Response::Response(char* responsFromServer) {
	char code[CODE_SIZE];
	int responeIndex = 0;
	std::copy(responsFromServer + responeIndex, responsFromServer + responeIndex + VERSION_SIZE -1 , this->serverVersion);
	responeIndex += VERSION_SIZE;
	std::copy(responsFromServer + responeIndex, responsFromServer + responeIndex + CODE_SIZE -1, code);
	responeIndex += CODE_SIZE;
	this->responseCode = atoi(code);
	std::string PayloadSize;
	std::copy(responsFromServer + responeIndex, responsFromServer + responeIndex + PAYLOAD_SIZE_SIZE -1, PayloadSize);
	responeIndex += PAYLOAD_SIZE_SIZE;
	int paloadSizeInt = atoi(PayloadSize.c_str());
	this->responsePayloadSize = paloadSizeInt;
	std::copy(responsFromServer + PAYLOAD_SIZE_SIZE, responsFromServer + paloadSizeInt -1, this->responsePayload);
}

long Response::getResponsePayloadSize() {
	return this->responsePayloadSize;
}

short Response::getResponseCode() {
	return this->responseCode;
}

char* Response::getServerVersion() {
	return this->serverVersion;
}

std::string Response::getResponsePayload() {
	return this->responsePayload;
}

Request Response::handleRequest(clientHelper client)
{
	if (this->responseCode == REGISTRATION_SUCCESS) {
		std::string clintID;
		std::copy(this->getResponsePayload()[0], this->getResponsePayload()[CLIENT_ID_SIZE - 1], clintID);
		//update client
		client.updateClientID(clintID);
		//creat rsa key
		std::string rsaPrivetKey = genaratePublicKey();
		// create me.info
		writeMeFile(client.getClientName(), this->getResponsePayload(), rsaPrivetKey);
		// creat request
		char id[CLIENT_ID_SIZE];
		std::memcpy(id, (this->getResponsePayload()).c_str(), CLIENT_ID_SIZE);
		Request request = Request(id, RequestCodeEnum::SEND_PUBLIC_KEY, rsaPrivetKey);
		return request;
	}
	else {
		if (this->responseCode == AES_CREATED) {
			// get payload
			std::string clintID;
			std::string AESkey;
			std::string RSAkey;
			std::copy(this->getResponsePayload()[0], this->getResponsePayload()[CLIENT_ID_SIZE - 1], clintID);
			std::copy(this->getResponsePayload()[CLIENT_ID_SIZE], this->getResponsePayload()[this->getResponsePayloadSize()], AESkey);
			// update client
			client.updateClientAES(AESkey, this->getResponsePayloadSize() - CLIENT_ID_SIZE);
			//decrypt RSA key
			std::ifstream infile("me.info");
			for (size_t i = 0; i < 3; i++)
			{
				std::getline(infile, RSAkey);
			}
			infile.close();
			std::string rsa_decrypted_key = DecryptAESKey(AESkey, RSAkey);
			//read file data
			std::string fileData = readFileData(client.getClientFilePath());
			//check file CRC
			int crc = calculate_crc(fileData);
			// update Client
			client.updateCrcSum(crc);
			//encrypt file
			std::string encryptFile = EncryptFileUsingAES(rsa_decrypted_key, fileData);
			// get payload data
			long contentSize = encryptFile.length();
			char fileName[FILE_NAME_SIZE];
			std::memcpy(fileName, (client.getClientFilePath()).c_str(), CLIENT_NAME_SIZE);
			//send request
			char* payload;
			int index = 0;
			std::memcpy(payload + index, (std::to_string(contentSize)).c_str(), FILE_CONTENT_SIZE_SIZE);
			int index = FILE_CONTENT_SIZE_SIZE;
			std::memcpy(payload + index, fileName, FILE_NAME_SIZE);
			int index = FILE_NAME_SIZE;
			std::memcpy(payload + index, encryptFile.c_str(), contentSize);
			Request request = Request(client.getClientIp(), RequestCodeEnum::SEND_FILE, payload);
			return request;
		}
		else {
			if (this->responseCode == SEND_CRC) {
				//get data from payload
				int index = CLIENT_ID_SIZE + FILE_CONTENT_SIZE_SIZE + FILE_NAME_SIZE;
				std::string ckSum;
				std::copy(this->getResponsePayload()[index], this->getResponsePayload()[index + CKSUM_SIZE], ckSum);
				if () {

				}
				
			}
			else {
				if (this->responseCode == SUCCESS_RE_CONNECT) {

				}
				else {
					if (this->responseCode == REFUSED_RE_CONNECT) {

					}
				}

			}
		}
	}
}

std::string genaratePublicKey() {
	RSAPrivateWrapper rsa;
	char pubkeybuff[RSAPublicWrapper::KEYSIZE];
	rsa.getPublicKey(pubkeybuff, RSAPublicWrapper::KEYSIZE);
	std::string base64key = Base64Wrapper::encode(rsa.getPrivateKey());
	return base64key;
}

void writeMeFile(std::string name, std::string ID, std::string privetKey) {
	std::ofstream MeFile("me.info");
	MeFile << name + "\n";
	MeFile << ID + "\n";
	MeFile << privetKey + "\n";
	MeFile.close();
}

std::string DecryptAESKey(std::string aes_key, std::string rsa_key)
{
	RSAPrivateWrapper rsaWrapper(rsa_key);
	std::string decrypted_key = rsaWrapper.decrypt(aes_key);
	return decrypted_key;
}

uint32_t calculate_crc(std::string& text)
{
	boost::crc_32_type result;
	result.process_bytes(text.data(), text.length());
	return result.checksum();
}

std::string readFileData(std::string file_path)
{
	std::string fileData;
	std::string lineData;
	std::ifstream inFile;
	inFile.open(file_path);
	while (inFile >> lineData) {
		fileData += lineData;
	}
	inFile.close();
	return fileData;
}

std::string EncryptFileUsingAES(std::string aes_key, std::string file_data)
{
	//convert key from string to char
	unsigned char* key = new unsigned char[AESWrapper::DEFAULT_KEYLENGTH];
	std::memcpy(key, aes_key.c_str(), AESWrapper::DEFAULT_KEYLENGTH);
	// creat AESWrapper
	AESWrapper aes(key, AESWrapper::DEFAULT_KEYLENGTH);
	// encrypt the file content
	//the key maybe in hex//
	std::string encryptedText = aes.encrypt(file_data.c_str(), file_data.length());
	return encryptedText;
}







