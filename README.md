# TP-Generator

<p align="center">
	<a href="https://github.com/truocphan/TP-Generator/releases/"><img src="https://img.shields.io/github/release/truocphan/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/downloads/truocphan/TP-Generator/total" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/stars/truocphan/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/forks/truocphan/TP-Generator" height=30></a>
	<a href="https://github.com/truocphan/TP-Generator/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/truocphan/TP-Generator" height=30></a>
	<a href="https://github.com/truocphan/TP-Generator/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/truocphan/TP-Generator" height=30></a>
	<br>
	<a href="#"><img src="https://img.shields.io/pypi/v/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/pypi/dm/TP-Generator" height=30></a>
</p>

## Installation
#### From PyPI:
```console
pip install TP-Generator
```
#### From Source:
```console
git clone https://github.com/truocphan/TP-Generator.git --branch <Branch/Tag>
cd TP-Generator
python setup.py build
python setup.py install
```

## Basic Usage
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

Utils.Str2Hex('TPCyberSec')
# OUTPUT: '54504379626572536563'

Utils.Hex2Str('54504379626572536563')
# OUTPUT: 'TPCyberSec'

Utils.base64Encode('TPCyberSec')
# OUTPUT: 'VFBDeWJlclNlYw=='

Utils.base64Decode('VFBDeWJlclNlYw==')
# OUTPUT: 'TPCyberSec'

Utils.base64UrlEncode('TPCyberSec')
# OUTPUT: 'VFBDeWJlclNlYw'

Utils.base64UrlDecode('VFBDeWJlclNlYw')
# OUTPUT: 'TPCyberSec'

Utils.UrlEncode('TP Cyber Security')
# OUTPUT: 'TP%20Cyber%20Security'

Utils.UrlDecode('TP%20Cyber%20Security')
# OUTPUT: 'TP Cyber Security'

```

#### Generating testcases for the Sniper attack
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

#### Generating testcases for the Batteringram attack
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

#### Generating testcases for the Pitchfork attack
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

#### Generating testcases for the Clusterbomb attack
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

#### Generating the TOTP, HOTP code
```
from TP_Generator import MFA_Generator

print(MFA_Generator.TOTP("JBSWY3DPEHPK3PXP"))
# OUTPUT: 862642

print(MFA_Generator.HOTP("JBSWY3DPEHPK3PXP", 1))
# OUTPUT: 996554
```

#### Generating the WordPress Nonce for unauthenticated users with wp-rest action
```
from TP_Generator import Nonce_Generator

action = "wp-rest"
NONCE_KEY = "Y9(H0]_u8BA:^or^<^4>AM@EkgnAm`{Mpsq*H!Z-?8 OHe6ITmPY6kQSai)y3w{}"
NONCE_SALT = "xV&%-Ji<,`Clp+|bqt9<c%JrGpq!EiMy///`z0+<D1F<E%H14mha9Csm<TH;~TfH"

print(Nonce_Generator.WordPress_Nonce(nonce_action=action, WORDPRESS_NONCE_KEY=NONCE_KEY, WORDPRESS_NONCE_SALT=NONCE_SALT))
# OUTPUT: ac06630f78
```

#### (Un)parsing QR Code
```
from TP_Generator import QR_Generator

QR_String = "00020101021230340009nbcb@devb01090000001230204DEVB520459995303840540115802KH5912Coffee Klang6010Phnom Penh62300314Coffe Klang0010708A60086679917001316418876882756304CE7C"

QRObj = QR_Generator.intQR("KHQR_Corporate").parse(QR_String)
print(QRObj.dumps())
# OUTPUT: {"PayloadFormatIndicator": "01", "PointOfInitiationMethod": "12", "MerchantAccountInformation": {"BakongAccountID": "nbcb@devb", "MerchantID": "000000123", "AcquiringBank": "DEVB"}, "MerchantCategoryCode": "5999", "TransactionCurrency": "840", "TransactionAmount": "1", "CountryCode": "KH", "MerchantName": "Coffee Klang", "MerchantCity": "Phnom Penh", "AdditionalDataFieldTemplate": {"StoreLabel": "Coffe Klang001", "TerminalLabel": "A6008667"}, "CRC": "CE7C", "Timestamp": {"timestamp": "1641887688275"}}

QRObj.update("TransactionAmount", "1000")
print(QR_Generator.intQR("KHQR_Corporate").unparse(QRObj))
# OUTPUT: 00020101021230340009nbcb@devb01090000001230204DEVB520459995303840540410005802KH5912Coffee Klang6010Phnom Penh62300314Coffe Klang0010708A600866799170013164188768827563043ECD
```


## CHANGELOG
#### [TP-Generator v2024.12.12](https://github.com/truocphan/TP-Generator/tree/2024.12.12)
- **New**: _Utils_ module
- **New**: _QR_Generator_: Parse/Unparse QR code types: **VietQR**, **MoMo**, **KHQR_Individual**, **KHQR_Corporate**

#### [TP-Generator v2024.8.10](https://github.com/truocphan/TP-Generator/tree/2024.8.10)
- **Updated**: _AttackTypes_: **Sniper**, **Batteringram**, **Pitchfork**, **Pitchfork**
- **New**: _Nonce_Generator_: Generate the WordPress Nonce

#### [TP-Generator v2024.6.13](https://github.com/truocphan/TP-Generator/tree/2024.6.13)
- **Updated**: _MFA_Generator_: Fixed error generating **TOTP**, **HOTP** from jython

#### [TP-Generator v2024.4.5](https://github.com/truocphan/TP-Generator/tree/2024.4.5)
- **New**: _Bruteforcer_List_: **UUID1**

#### [TP-Generator v2024.3.3](https://github.com/truocphan/TP-Generator/tree/2024.3.3)
- **New**: _MFA_Generator_: **TOTP** (Time-based One-Time Password) and **HOTP** (HMAC-based One-Time Password)

#### [TP-Generator v2024.3.1](https://github.com/truocphan/TP-Generator/tree/2024.3.1)
- **New**: Generate test cases for attack types: **_Sniper_**, **_Battering Ram_**, **_Pitchfork_**, **_Cluster Bomb_**