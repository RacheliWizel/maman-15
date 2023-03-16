#include <boost/asio.hpp>
#include "protocol.h"
#include "ClientHelper.h"

using namespace boost::asio::ip;
using boost::asio::ip::tcp;
const int message_length = 1024;

int main(int argc, char* argv[])
{
    char* path;
    _get_pgmptr(&path);
// get client data
    clientHelper client = clientHelper();
// check if a new client
    bool newClient = checkNewClient();
//create first request
    //if (newClient) {
    //   request req = newClientRequest()
    //   convert to byte
    //}
    //else {
    //    request req = recoonectRequest()
    //   convert to byte
    //}

//open socket
    boost::asio::io_context io_context;
    tcp::socket s(io_context);
    tcp::resolver resolver(io_context);
//connect to server
    boost::asio::connect(s, resolver.resolve(client.getClientIp(), client.getClientPort()));
//send request
    //boost::asio::write(s, boost::asio::buffer(bytereq, max_length));
    while (true) {
        char reply[message_length];
        boost::asio::read(s, boost::asio::buffer(reply, message_length));
        Response response = Response(reply);
        short responseCode = response.getResponseCode();
        if (responseCode == ResponseCodeEnum::ERROR_RESPONSE || responseCode == ResponseCodeEnum::RECEIVED_MESSAGE || responseCode == ResponseCodeEnum::REGISTRATION_FAILED) {
            s.close();
        }
        else {
            Request request = response.handleRequest(client);
            std::string requestToSend = request.convertToByts();
            boost::asio::write(s, boost::asio::buffer(requestToSend, message_length));
        }
    }

}