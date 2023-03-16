#pragma once
#include <string>
#include <cstdint>
#include <ostream>
#include <boost/asio/ip/tcp.hpp>

using boost::asio::ip::tcp;
using boost::asio::io_context;
tcp::resolver resolver(io_context);



class HandleSocket
{
public:
	HandleSocket();
	virtual ~HandleSocket();

	// validations
	static bool validateIP(const std::string& address);
	static bool validatePort(const std::string& port);

	// logic
	bool connect(char* ip, char* address);
	void close();
	bool receive(uint8_t* const buffer, const size_t size) const;
	bool send(const uint8_t* const buffer, const size_t size) const;
	bool sendReceive(const uint8_t* const toSend, const size_t size, uint8_t* const response, const size_t resSize);


private:
	std::string    _address;
	std::string    _port;
	io_context* _ioContext;
	tcp::resolver* _resolver;
	tcp::socket* _socket;
	bool           _bigEndian;
	bool           _connected;  // indicates that socket has been open and connected.

	void swapBytes(uint8_t* const buffer, size_t size) const;

};