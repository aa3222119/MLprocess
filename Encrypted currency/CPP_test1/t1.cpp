#include "ecc_encryption_algorithm.h"
#include <iostream>

//#include <openssl/ec.h>
//#include <openssl/ecdsa.h>
//#include <openssl/objects.h>
//#include <openssl/err.h>

#include <crypto/eccrypto.h>
#include "crypto/osrng.h"
#include "crypto/oids.h"
#include "crypto/hex.h"
#include "crypto/filters.h"

void EccEncryption::GenerateEccKeys(unsigned int uiKeySize, std::string& sPrivateKey, std::string& sPublicKey)
{
    using namespace CryptoPP;
    // Random pool, the second parameter is the length of key
    // 随机数池，第二个参数是生成密钥的长
    AutoSeededRandomPool rnd(false, 1024);

    ECIES<ECP>::PrivateKey  privateKey;
    ECIES<ECP>::PublicKey   publicKey;
    // Generate private key
    // 生成私钥
    privateKey.Initialize(rnd, ASN1::secp521r1());
    // Generate public key using private key
    // 用私钥生成密钥
    privateKey.MakePublicKey(publicKey);

    ECIES<ECP>::Encryptor encryptor(publicKey);
    HexEncoder pubEncoder(new StringSink(sPublicKey));
    encryptor.DEREncode(pubEncoder);
    pubEncoder.MessageEnd();

    ECIES<ECP>::Decryptor decryptor(privateKey);
    HexEncoder prvEncoder(new StringSink(sPrivateKey));
    decryptor.DEREncode(prvEncoder);
    prvEncoder.MessageEnd();
}

std::string EccEncryption::Encrypt(const std::string& sPublicKey, const std::string& sMsgToEncrypt)
{
    using namespace CryptoPP;
    // If to save the keys into a file, FileSource should be replace StringSource
    // 如果需要把密钥保存到文件里，可以用 FileSource
    StringSource pubString(sPublicKey, true, new HexDecoder);
    ECIES<ECP>::Encryptor encryptor(pubString);

    // Calculate the length of cipher text
    // 计算加密后密文的长度
    size_t uiCipherTextSize = encryptor.CiphertextLength(sMsgToEncrypt.size());
    std::string sCipherText;
    sCipherText.resize(uiCipherTextSize);
    RandomPool rnd;
    encryptor.Encrypt(rnd, (byte*)(sMsgToEncrypt.c_str()), sMsgToEncrypt.size(), (byte*)(sCipherText.data()));
    return sCipherText;
}

std::string EccEncryption::Decrypt(const std::string& sPrivateKey, const std::string& sMsgToDecrytp)
{
    using namespace CryptoPP;
    StringSource privString(sPrivateKey, true, new HexDecoder);
    ECIES<ECP>::Decryptor decryptor(privString);

    auto sPlainTextLen = decryptor.MaxPlaintextLength(sMsgToDecrytp.size());
    std::string sDecryText;
    sDecryText.resize(sPlainTextLen);
    RandomPool rnd;
    decryptor.Decrypt(rnd, (byte*)sMsgToDecrytp.c_str(), sMsgToDecrytp.size(), (byte*)sDecryText.data());
    return sDecryText;
}


//using namespace std;
int main(){
    cout<<"这是antony的C++test"<<endl;
    std::string sStrToTest = std::string("Hello world. This is an example of Ecc\
 encryption algorithm of Crypto++ open source library.");
    EccEncryption ecc;
    std::string sPrivateKey, sPublicKey;
    ecc.GenerateEccKeys(1024, sPrivateKey, sPublicKey);
      
    std::cout << "Generated private key is : "<< std::endl;
    std::cout << sPrivateKey << std::endl;
    std::cout << "***********************************************************" << std::endl;

    std::cout << "Generated public key is : "<< std::endl;
    std::cout << sPublicKey << std::endl;
    std::cout << "***********************************************************" << std::endl;

    std::cout << "The message to be encrypted is : " << std::endl;
    std::cout << sStrToTest << std::endl;
    std::cout << "***********************************************************" << std::endl;

    std::string sEncryptResult = ecc.Encrypt(sPublicKey, sStrToTest);
    std::cout << "The result of encrypt is : " << std::endl;
    std::cout << sEncryptResult << std::endl;
    std::cout << "***********************************************************" << std::endl;

    std::string sDecryptResult = ecc.Decrypt(sPrivateKey, sEncryptResult);
    std::cout << "The result of decrypt is : " << std::endl;
    std::cout << sDecryptResult << std::endl;
    std::cout << "***********************************************************" << std::endl;
    return 0;
}
