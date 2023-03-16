#pragma once

#include <string>
//#include "..\cryptopp870\base64.h"
#include <base64.h>


class Base64Wrapper
{
public:
	static std::string encode(const std::string& str);
	static std::string decode(const std::string& str);
};


