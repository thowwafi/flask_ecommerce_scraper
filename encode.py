import base64
import hashlib

encoded = base64.b64encode('thawwafi@gmail.com'.encode('utf-8'))
dec = encoded.decode() + "9AJv"
print(dec)

mypass = "Alpiphysics_27"
string = base64.b64encode(mypass.encode('utf-8'))
password = hashlib.md5(string).hexdigest()
print(password)
pas_sha1 = hashlib.sha1(string).hexdigest()
pas_sha224 = hashlib.sha224(string).hexdigest()
pas_sha256 = hashlib.sha256(string).hexdigest()
pas_sha384 = hashlib.sha384(string).hexdigest()
pas_sha512 = hashlib.sha512(string).hexdigest()
pas_blake2b = hashlib.blake2b(string).hexdigest()
pas_blake2s = hashlib.blake2s(string).hexdigest()
pas_md5 = hashlib.md5(string).hexdigest()

print("pas_sha1", pas_sha1)
print("pas_sha224", pas_sha224)
print("pas_sha256", pas_sha256)
print("pas_sha384", pas_sha384)
print("pas_sha512", pas_sha512)
print("pas_blake2b", pas_blake2b)
print("pas_blake2s", pas_blake2s)
print("pas_md5", pas_md5)

# text = 'Hello'
hashObject = hashlib.new('md4', string)
digest = hashObject.hexdigest()
 
print("pas_md4", digest)