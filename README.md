<div align="center">
	<h1>TP-Generator - PyPI</h1>
	<i></i>
	<br><br>
	<a href="https://github.com/TPCyberSec/TP-Generator/releases/"><img src="https://img.shields.io/github/release/TPCyberSec/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/downloads/TPCyberSec/TP-Generator/total" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/stars/TPCyberSec/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/forks/TPCyberSec/TP-Generator" height=30></a>
	<a href="https://github.com/TPCyberSec/TP-Generator/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/TPCyberSec/TP-Generator" height=30></a>
	<a href="https://github.com/TPCyberSec/TP-Generator/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/TPCyberSec/TP-Generator" height=30></a>
	<br>
	<a href="#"><img src="https://img.shields.io/pypi/v/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/pypi/pyversions/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/pypi/dm/TP-Generator" height=30></a>
</div>

---
# 🛠️ Installation
#### From PyPI:
```console
pip install TP-Generator
```
#### From Source:
```console
git clone https://github.com/TPCyberSec/TP-Generator.git --branch <Branch/Tag>
cd TP-Generator
python -m build
python -m pip install dist/tp_generator-<version>-py3-none-any.whl
```

---
# 📘 Basic Usage
### Utils
```
from TP_Generator import Utils

Utils.timestamp(10)
# OUTPUT: 1733597189

Utils.uuid(1)
# OUTPUT: '9daeab4b-b4cb-11ef-b79b-00a554ba203d'

Utils.RandomNumber(0, 1000)
# OUTPUT: 931

Utils.RandomString(10)
# OUTPUT: 'Wz<:1<.YSC'

Utils.toUTF8_Overlong('TPCyberSec', numBytes=2)
# OUTPUT: b'\xc1\x94\xc1\x90\xc1\x83\xc1\xb9\xc1\xa2\xc1\xa5\xc1\xb2\xc1\x93\xc1\xa5\xc1\xa3'

Utils.toUTF16('TPCyberSec')
# OUTPUT: b'T\x00P\x00C\x00y\x00b\x00e\x00r\x00S\x00e\x00c\x00'

Utils.toUTF32('TPCyberSec')
# OUTPUT: b'T\x00\x00\x00P\x00\x00\x00C\x00\x00\x00y\x00\x00\x00b\x00\x00\x00e\x00\x00\x00r\x00\x00\x00S\x00\x00\x00e\x00\x00\x00c\x00\x00\x00'

Utils.Str2Hex('TPCyberSec')
# OUTPUT: '54504379626572536563'

Utils.Hex2Str('54504379626572536563')
# OUTPUT: 'TPCyberSec'

Utils.base64Encode('TPCyberSec'.encode())
# OUTPUT: b'VFBDeWJlclNlYw=='

Utils.base64Decode('VFBDeWJlclNlYw==')
# OUTPUT: b'TPCyberSec'

Utils.base64UrlEncode('TPCyberSec'.encode())
# OUTPUT: b'VFBDeWJlclNlYw'

Utils.base64UrlDecode('VFBDeWJlclNlYw'.encode())
# OUTPUT: b'TPCyberSec'

Utils.UrlEncode('TP Cyber Security')
# OUTPUT: 'TP%20Cyber%20Security'

Utils.UrlDecode('TP%20Cyber%20Security')
# OUTPUT: 'TP Cyber Security'

Utils.HTMLEncode('TPCyberSec')
# OUTPUT: '&#x54;&#x50;&#x43;&#x79;&#x62;&#x65;&#x72;&#x53;&#x65;&#x63;'

Utils.HTMLEncode('TPCyberSec', type="dec")
# OUTPUT: '&#84;&#80;&#67;&#121;&#98;&#101;&#114;&#83;&#101;&#99;'

xml_string = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>'''

json_object = Utils.XML2JSON(xml_string)
print(json_object)
# OUTPUT: {'note': {'to': {'#text': 'Tove'}, 'from': {'#text': 'Jani'}, 'heading': {'#text': 'Reminder'}, 'body': {'#text': "Don't forget me this weekend!"}}}

xml_string = Utils.JSON2XML(json_object)
print(xml_string)
# OUTPUT: <?xml version="1.0" encoding="UTF-8"?><note><to>Tove</to><from>Jani</from><heading>Reminder</heading><body>Don&apos;t forget me this weekend!</body></note>

ProtoData = "AAAAAEwIz///////////ARI4SOG7hyB0aOG7kW5nIMSRYW5nIGPDsyBs4buXaSwgdnVpIGzDsm5nIHRo4butIGzhuqFpIHNhdSEwAVgGyAEB"
json_object = Utils.Protobuf2JSON(ProtoData, keyName_mapping={"1":{"name":"status"},"2":{"name":"message"}})
print(json_object.dumps())
# OUTPUT: {"status": -49, "message": "H\u1ec7 th\u1ed1ng \u0111ang c\u00f3 l\u1ed7i, vui l\u00f2ng th\u1eed l\u1ea1i sau!", "6": 1, "11": 6, "25": 1}
```

### Generating testcases for the Sniper attack
```
from TP_Generator import AttackTypes

InjectionPoints = [
	"RequestBody||id",
	"RequestBody||name"
]

Payloads = [
	[
		"' AND '1'='1",
		"' AND '1'='0"
	]
]

for testcases in AttackTypes.Sniper(InjectionPoints, Payloads):
	print(testcases)

# OUTPUT:
# {'RequestBody||id': "' AND '1'='1"}
# {'RequestBody||id': "' AND '1'='0"}
# {'RequestBody||name': "' AND '1'='1"}
# {'RequestBody||name': "' AND '1'='0"}
```

### Generating testcases for the Batteringram attack
```
from TP_Generator import AttackTypes

InjectionPoints = [
	"RequestBody||id",
	"RequestBody||name"
]

Payloads = [
	[
		"' AND '1'='1",
		"' AND '1'='0"
	]
]

for testcases in AttackTypes.Batteringram(InjectionPoints, Payloads):
	print(testcases)

# OUTPUT:
# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' AND '1'='1"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' AND '1'='0"}
```

### Generating testcases for the Pitchfork attack
```
from TP_Generator import AttackTypes

InjectionPoints = [
	"RequestBody||id",
	"RequestBody||name"
]

Payloads = [
	[
		"' AND '1'='1",
		"' AND '1'='0"
	],
	[
		"' OR '1'='1",
		"' OR '1'='0"
	]
]

for testcases in AttackTypes.Pitchfork(InjectionPoints, Payloads):
	print(testcases)

# OUTPUT:
# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' OR '1'='0"}
```

### Generating testcases for the Clusterbomb attack
```
from TP_Generator import AttackTypes

InjectionPoints = [
	"RequestBody||id",
	"RequestBody||name"
]

Payloads = [
	[
		"' AND '1'='1",
		"' AND '1'='0",
		"' && '1'='1"
	],
	[
		"' OR '1'='1",
		"' OR '1'='0",
	]
]

for testcases in AttackTypes.Clusterbomb(InjectionPoints, Payloads):
	print(testcases)

# OUTPUT:
# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' OR '1'='0"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' OR '1'='0"}
# {'RequestBody||id': "' && '1'='1", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' && '1'='1", 'RequestBody||name': "' OR '1'='0"}
```

### Generating the TOTP, HOTP code
```
from TP_Generator import MFA_Generator

print(MFA_Generator.TOTP("JBSWY3DPEHPK3PXP"))
# OUTPUT: 862642

print(MFA_Generator.HOTP("JBSWY3DPEHPK3PXP", 1))
# OUTPUT: 996554
```

### Generating the WordPress Nonce for unauthenticated users with wp-rest action
```
from TP_Generator import Nonce_Generator

action = "wp-rest"
NONCE_KEY = "Y9(H0]_u8BA:^or^<^4>AM@EkgnAm`{Mpsq*H!Z-?8 OHe6ITmPY6kQSai)y3w{}"
NONCE_SALT = "xV&%-Ji<,`Clp+|bqt9<c%JrGpq!EiMy///`z0+<D1F<E%H14mha9Csm<TH;~TfH"

print(Nonce_Generator.WordPress_Nonce(nonce_action=action, WORDPRESS_NONCE_KEY=NONCE_KEY, WORDPRESS_NONCE_SALT=NONCE_SALT))
# OUTPUT: ac06630f78
```

### (Un)parsing QR Code: VietQR (`TAG 38`), MoMo (`TAG 38`), VNPAYQR (`TAG 26`), KHQR_Individual (`TAG 29`), KHQR_Corporate (`TAG 30`), ThaiQR_CREDIT_TRANSFER (`TAG 29`), ThaiQR_BILL_PAYMENT (`TAG 30`)
```
from TP_Generator import QR_Generator

QR_String = "00020101021230340009nbcb@devb01090000001230204DEVB520459995303840540115802KH5912Coffee Klang6010Phnom Penh62300314Coffe Klang0010708A60086679917001316418876882756304CE7C"

QRObj = QR_Generator.initQR("KHQR_Corporate").parse(QR_String)
print(QRObj.dumps())
# OUTPUT: {"PayloadFormatIndicator": "01", "PointOfInitiationMethod": "12", "MerchantAccountInformation": {"BakongAccountID": "nbcb@devb", "MerchantID": "000000123", "AcquiringBank": "DEVB"}, "MerchantCategoryCode": "5999", "TransactionCurrency": "840", "TransactionAmount": "1", "CountryCode": "KH", "MerchantName": "Coffee Klang", "MerchantCity": "Phnom Penh", "AdditionalDataFieldTemplate": {"StoreLabel": "Coffe Klang001", "TerminalLabel": "A6008667"}, "CRC": "CE7C", "Timestamp": {"timestamp": "1641887688275"}}

QRObj.update("TransactionAmount", "1000")
print(QR_Generator.initQR("KHQR_Corporate").unparse(QRObj))
# OUTPUT: 00020101021230340009nbcb@devb01090000001230204DEVB520459995303840540410005802KH5912Coffee Klang6010Phnom Penh62300314Coffe Klang0010708A600866799170013164188768827563043ECD
```

---
# 👥 Contributors

---
# 📝 CHANGELOG
### [TP-Generator v2026.11.18](https://github.com/TPCyberSec/TP-Generator/tree/2026.11.18)
- **New**: _Utils_: **Protobuf2JSON**
- **Fixed**: an unexpected keyword argument 'ordered_dict' when initializing the QR object in _QR_Generator_ module

### [TP-Generator v2026.5.18](https://github.com/TPCyberSec/TP-Generator/tree/2026.5.18)
- **New**: _Utils_: **HTMLEncode**, **toUTF8_Overlong**
- **Updated**: Preserve the order of keys when parsing from XML to JSON by setting the `ordered_dict` parameter to `True`

### [TP-Generator v2026.4.30](https://github.com/TPCyberSec/TP-Generator/tree/2026.4.30)
- **New**: _Utils_: **XML2JSON**, **JSON2XML**

### [TP-Generator v2026.3.29](https://github.com/TPCyberSec/TP-Generator/tree/2026.3.29)
- **Updated**: **toUTF16**, **toUTF32**, **base64Encode**, **base64Decode**, **base64UrlEncode**, **base64UrlDecode** functions in _Utils_ module

### [TP-Generator v2025.10.7](https://github.com/TPCyberSec/TP-Generator/tree/2025.10.7)
- **New**: _QR_Generator_: **ThaiQR_CREDIT_TRANSFER** (`TAG 29`), **ThaiQR_BILL_PAYMENT** (`TAG 30`)

### [TP-Generator v2025.9.10](https://github.com/TPCyberSec/TP-Generator/tree/2025.9.10)
- **Fixed**:  _base64Encode_, _base64Decode_, _base64UrlEncode_, _base64UrlDecode_

### [TP-Generator v2025.1.1](https://github.com/TPCyberSec/TP-Generator/tree/2025.1.1)
- **New**: _Utils_: **toUTF16**, **toUTF32**
- **New**: _QR_Generator_: **VNPAYQR** (`TAG 26`)

### [TP-Generator v2024.12.12](https://github.com/TPCyberSec/TP-Generator/tree/2024.12.12)
- **New**: _Utils_ module
- **New**: _QR_Generator_: Parse/Unparse QR code types: **VietQR** (`TAG 38`), **MoMo** (`TAG 38`), **KHQR_Individual** (`TAG 29`), **KHQR_Corporate** (`TAG 30`)

### [TP-Generator v2024.8.10](https://github.com/TPCyberSec/TP-Generator/tree/2024.8.10)
- **Updated**: _AttackTypes_: **Sniper**, **Batteringram**, **Pitchfork**, **Pitchfork**
- **New**: _Nonce_Generator_: Generate the WordPress Nonce

### [TP-Generator v2024.6.13](https://github.com/TPCyberSec/TP-Generator/tree/2024.6.13)
- **Updated**: _MFA_Generator_: Fixed error generating **TOTP**, **HOTP** from jython

### [TP-Generator v2024.4.5](https://github.com/TPCyberSec/TP-Generator/tree/2024.4.5)
- **New**: _Bruteforcer_List_: **UUID1**

### [TP-Generator v2024.3.3](https://github.com/TPCyberSec/TP-Generator/tree/2024.3.3)
- **New**: _MFA_Generator_: **TOTP** (Time-based One-Time Password) and **HOTP** (HMAC-based One-Time Password)

### [TP-Generator v2024.3.1](https://github.com/TPCyberSec/TP-Generator/tree/2024.3.1)
- **New**: Generate test cases for attack types: **_Sniper_**, **_Battering Ram_**, **_Pitchfork_**, **_Cluster Bomb_**

---