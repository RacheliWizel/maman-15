#pragma once
#include <string>
#include <cstdint>
#include <ostream>
#include <boost/asio/ip/tcp.hpp>

using boost::asio::ip::tcp;
using boost::asio::io_context;

constexpr size_t PACKET_SIZE = 1024;   // Better be the same on server side.

class HandleSocket
{
public:
	HandleSocket();
	virtual ~HandleSocket();

	// validations
	static bool validateIP(const std::string& address);
	static bool validatePort(const std::string& port);

	// logic
	bool setSocketInfo(const std::string& address, const std::string& port);
	bool connect();
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