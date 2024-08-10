# TP-Generator

<p align="center">
    <a href="https://github.com/truocphan/TP-Generator/releases/"><img src="https://img.shields.io/github/release/truocphan/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/downloads/truocphan/TP-Generator/total" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/stars/truocphan/TP-Generator" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/forks/truocphan/TP-Generator" height=30></a>
	<a href="https://github.com/truocphan/TP-Generator/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/truocphan/TP-Generator" height=30></a>
	<a href="https://github.com/truocphan/TP-Generator/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/truocphan/TP-Generator" height=30></a>
	<a href="https://pypi.org/project/TP-Generator/" target="_blank"><img src="https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white" height=30></a>
	<a href="https://www.facebook.com/61550595106970" target="_blank"><img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" height=30></a>
	<a href="https://twitter.com/TPCyberSec" target="_blank"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" height=30></a>
	<a href="https://github.com/truocphan" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" height=30></a>
	<a href="mailto:tpcybersec2023@gmail.com" target="_blank"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" height=30></a>
	<a href="https://www.buymeacoffee.com/truocphan" target="_blank"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" height=30></a>
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

# {'RequestBody||id': "' AND '1'='1"}
# {'RequestBody||id': "' AND '1'='0"}
# {'RequestBody||name': "' AND '1'='1"}
# {'RequestBody||name': "' AND '1'='0"}
```

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

# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' AND '1'='1"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' AND '1'='0"}
```

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

# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' OR '1'='0"}
```

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

# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' AND '1'='1", 'RequestBody||name': "' OR '1'='0"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' AND '1'='0", 'RequestBody||name': "' OR '1'='0"}
# {'RequestBody||id': "' && '1'='1", 'RequestBody||name': "' OR '1'='1"}
# {'RequestBody||id': "' && '1'='1", 'RequestBody||name': "' OR '1'='0"}
```

```
from TP_Generator import MFA_Generator

print(MFA_Generator.TOTP("JBSWY3DPEHPK3PXP"))
print(MFA_Generator.HOTP("JBSWY3DPEHPK3PXP", 1))
```

```
from TP_Generator import Nonce_Generator

print(Nonce_Generator.WordPress_Nonce("rest"))
```

## CHANGELOG
#### [TP-Generator v2024.6.13](https://github.com/truocphan/TP-Generator/tree/2024.6.13)
- **Updated**: _MFA_Generator_: Fixed error generating **TOTP**, **HOTP** from jython

#### [TP-Generator v2024.4.5](https://github.com/truocphan/TP-Generator/tree/2024.4.5)
- **New**: _Bruteforcer_List_: **UUID1**

#### [TP-Generator v2024.3.3](https://github.com/truocphan/TP-Generator/tree/2024.3.3)
- **New**: _MFA_Generator_: **TOTP** (Time-based One-Time Password) and **HOTP** (HMAC-based One-Time Password)

#### [TP-Generator v2024.3.1](https://github.com/truocphan/TP-Generator/tree/2024.3.1)
- **New**: Generate test cases for attack types: **_Sniper_**, **_Battering Ram_**, **_Pitchfork_**, **_Cluster Bomb_**