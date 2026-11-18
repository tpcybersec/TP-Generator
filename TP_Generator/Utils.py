try:
	unicode # Python 2
except NameError:
	unicode = str # Python 3

import platform, struct
import time
import uuid as _uuid
import base64
import random
import string
import binascii
from collections import OrderedDict
import json_duplicate_keys as jdks

if platform.python_version_tuple()[0] == "3":
	from urllib.parse import quote as urlencode, unquote as urldecode
else:
	from urllib import quote as urlencode, unquote as urldecode



def timestamp(length):
	if length <= 0:
		return 0
	elif length < 10:
		return int(time.time() / 10**(10-length))
	elif length == 10:
		return int(time.time())
	else:
		return int(time.time() * 10**(length-10))


def uuid(version):
	if version == 1:
		return str(_uuid.uuid1())
	elif version == 4:
		return str(_uuid.uuid4())


def RandomNumber(min, max):
	return random.randint(min, max)


def RandomString(length, charsets=None):
	if type(charsets) not in [str, unicode]:
		charsets = string.ascii_letters+string.digits+string.punctuation

	return "".join(random.choice(charsets) for i in range(length))


def toUTF8_Overlong(message, numBytes=2):
	retval = b""

	for c in message:
		if numBytes == 2:
			# 2 byte: 110xxxxx 10xxxxxx
			codepoint = bin(ord(c))[2:].zfill(11)[-11:]
			retval += binascii.unhexlify(hex(int("110"+codepoint[0:5],2))[2:]) + binascii.unhexlify(hex(int("10"+codepoint[5:11],2))[2:])
		elif numBytes == 3:
			# 3 byte: 1110xxxx 10xxxxxx 10xxxxxx
			codepoint = bin(ord(c))[2:].zfill(16)[-16:]
			retval += binascii.unhexlify(hex(int("1110"+codepoint[0:4],2))[2:]) + binascii.unhexlify(hex(int("10"+codepoint[4:10],2))[2:]) + binascii.unhexlify(hex(int("10"+codepoint[10:16],2))[2:])
		elif numBytes == 4:
			# 4 byte: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
			codepoint = bin(ord(c))[2:].zfill(21)[-21:]
			retval += binascii.unhexlify(hex(int("11110"+codepoint[0:3],2))[2:]) + binascii.unhexlify(hex(int("10"+codepoint[3:9],2))[2:]) + binascii.unhexlify(hex(int("10"+codepoint[9:15],2))[2:]) + binascii.unhexlify(hex(int("10"+codepoint[15:21],2))[2:])
		else:
			retval += binascii.unhexlify(hex(ord(c))[2:])

	return retval


def toUTF16(message, type="LE"):
	retval = b""

	for c in message:
		if type == "LE":
			retval += binascii.unhexlify(hex(ord(c))[2:].rjust(2, "0").ljust(4, "0"))
		elif type == "BE":
			retval += binascii.unhexlify(hex(ord(c))[2:].rjust(4, "0"))

	return retval


def toUTF32(message, type="LE"):
	retval = b""

	for c in message:
		if type == "LE":
			retval += binascii.unhexlify(hex(ord(c))[2:].rjust(2, "0").ljust(8, "0"))
		elif type == "BE":
			retval += binascii.unhexlify(hex(ord(c))[2:].rjust(8, "0"))

	return retval


def Str2Hex(message):
	return "".join(["%02x"%ord(c) for c in message])


def Hex2Str(message):
	return "".join([chr(int(message[i:i+2], 16)) for i in range(0, len(message), 2)])


def base64Encode(message):
	retval = base64.b64encode(message)

	return retval


def base64Decode(message):
	retval = base64.b64decode(message)

	return retval


def base64UrlEncode(message):
	retval = base64.urlsafe_b64encode(message).rstrip(b"=")

	return retval


def base64UrlDecode(message):
	padding = b"=" * (4-(len(message)%4))
	retval = base64.urlsafe_b64decode(message+padding)

	return retval


def UrlEncode(message):
	return urlencode(message)


def UrlDecode(message):
	return urldecode(message)


def HTMLEncode(message, type="hex", padding=0):
	if type == "dec":
		return "".join(["&#"+"0"*padding+str(ord(i))+";" for i in message])
	else:
		return "".join(["&#x"+"0"*padding+"%02x"%ord(i)+";" for i in message])


def XML2JSON(message, ordered_dict=False):
	if type(ordered_dict) is not bool: ordered_dict = False

	if platform.python_version_tuple()[0] == "3":
		try:
			# ===== Fallback Python (ElementTree) =====
			import xml.etree.ElementTree as ET
			try:
				from io import StringIO
			except:
				from StringIO import StringIO

			if not isinstance(message, str):
				message = message.decode("utf-8")

			uri2prefix = OrderedDict() if ordered_dict else {}
			prefix2uri = OrderedDict() if ordered_dict else {}

			for event, elem in ET.iterparse(StringIO(message), events=('start-ns',)):
				prefix, uri = elem
				uri2prefix[uri] = prefix
				prefix2uri[prefix] = uri

			root = ET.fromstring(message)

			def qname(tag):
				if tag.startswith("{"):
					uri, local = tag[1:].split("}")
					prefix = uri2prefix.get(uri)
					return "%s:%s" % (prefix, local) if prefix else local
				return tag

			def parse_node(elem):
				tag = qname(elem.tag)
				node_obj = OrderedDict() if ordered_dict else {}

				# ---- attributes ----
				attrs = OrderedDict() if ordered_dict else {}

				# normal attributes
				for k, v in elem.attrib.items():
					if k.startswith("{"):
						uri, local = k[1:].split("}")
						prefix = uri2prefix.get(uri)
						if prefix:
							attrs["%s:%s" % (prefix, local)] = v
						else:
							attrs[local] = v
					else:
						attrs[k] = v

				# ---- xmlns extraction from RAW STRING ----
				# locate exact opening tag text
				start = message.find("<" + tag)
				if start != -1:
					end = message.find(">", start)
					raw_tag = message[start:end]

					parts = raw_tag.split()
					for p in parts:
						if p.startswith("xmlns"):
							if "=" in p:
								k, v = p.split("=", 1)
								v = v.strip('"').strip("'")
								attrs[k] = v

				# inject xmlns:xsi ONLY when xsi:* exists
				if any(k.startswith("xsi:") for k in attrs):
					if "xmlns:xsi" not in attrs and "xsi" in prefix2uri:
						attrs["xmlns:xsi"] = prefix2uri["xsi"]

				if attrs:
					node_obj["@attributes"] = attrs

				# ---- children ----
				children = OrderedDict() if ordered_dict else {}
				has_child = False

				for child in elem:
					has_child = True
					child_tag = qname(child.tag)
					child_obj = parse_node(child)[child_tag]

					if child_tag in children:
						if not isinstance(children[child_tag], list):
							children[child_tag] = [children[child_tag]]
						children[child_tag].append(child_obj)
					else:
						children[child_tag] = child_obj

				if children:
					node_obj.update(children)

				# ---- text ----
				if not has_child:
					text = elem.text
					if text is None:
						node_obj["#text"] = ""
					else:
						node_obj["#text"] = text.strip() if text.strip() else ""

				return {tag: node_obj}

			return parse_node(root)
		except Exception as e:
			return False
	else:
		try:
			# ===== Try Jython (Java DOM) =====
			from java.lang import Exception as JavaException
			from javax.xml.parsers import DocumentBuilderFactory
			from java.io import ByteArrayInputStream

			if isinstance(message, unicode):
				data = message.encode("utf-8")
			else:
				data = message

			factory = DocumentBuilderFactory.newInstance()
			factory.setNamespaceAware(True)
			builder = factory.newDocumentBuilder()
			doc = builder.parse(ByteArrayInputStream(data))

			def get_tag(node):
				prefix = node.getPrefix()
				local = node.getLocalName()
				return "%s:%s" % (prefix, local) if prefix else local

			def parse_node(node):
				tag = get_tag(node)
				node_obj = OrderedDict() if ordered_dict else {}

				# attributes
				attrs = OrderedDict() if ordered_dict else {}
				attr_map = node.getAttributes()
				if attr_map:
					for i in range(attr_map.getLength()):
						attr = attr_map.item(i)
						name = attr.getNodeName()
						value = attr.getNodeValue()

						# keep xmlns only at root or Response level
						if name.startswith("xmlns"):
							if node.getParentNode() and node.getParentNode().getNodeType() == node.DOCUMENT_NODE:
								attrs[name] = value
							elif tag.endswith("Response"):
								attrs[name] = value
						else:
							attrs[name] = value

				if len(attrs) > 0:
					node_obj["@attributes"] = attrs

				# children
				children = OrderedDict() if ordered_dict else {}
				has_child = False

				child_nodes = node.getChildNodes()
				for i in range(child_nodes.getLength()):
					child = child_nodes.item(i)

					if child.getNodeType() == child.ELEMENT_NODE:
						has_child = True

						child_tag = get_tag(child)
						child_data = parse_node(child)[child_tag]

						if child_tag in children:
							if not isinstance(children[child_tag], list):
								children[child_tag] = [children[child_tag]]
							children[child_tag].append(child_data)
						else:
							children[child_tag] = child_data

				if children:
					node_obj.update(children)

				# text
				if not has_child:
					text = node.getTextContent()
					node_obj["#text"] = text.strip() if text else ""

				return {tag: node_obj}

			root = doc.getDocumentElement()
			return parse_node(root)
		except (Exception, JavaException) as e:
			return False


def JSON2XML(message):
	def escape_xml(value):
		return (str(value)
			.replace("&", "&amp;")
			.replace("<", "&lt;")
			.replace(">", "&gt;")
			.replace('"', "&quot;")
			.replace("'", "&apos;"))

	def build(tag, content):
		if not isinstance(content, dict): return ""

		if not tag or len(tag.strip()) == 0: return ""

		has_attrs = "@attributes" in content and len(content["@attributes"]) > 0
		has_text = "#text" in content
		has_children = any(k not in ("@attributes", "#text") for k in content)

		if not (has_attrs or has_text or has_children): return ""

		attrs = ""
		children = ""
		text = ""

		if has_attrs:
			for k, v in content["@attributes"].items():
				attrs += ' {}="{}"'.format(k, escape_xml(v))

		if has_text:
			text = escape_xml(content["#text"])

		for k, v in content.items():
			if k in ("@attributes", "#text"):
				continue
			if isinstance(v, list):
				for item in v:
					children += build(k, item)
			else:
				children += build(k, v)

		return "<{tag}{attrs}>{text}{children}</{tag}>".format(tag=tag, attrs=attrs, text=text, children=children)

	root_tag = list(message.keys())[0]
	xml_body = build(root_tag, message[root_tag])

	return '<?xml version="1.0" encoding="UTF-8"?>' + xml_body


def Protobuf2JSON(message, Coding="utf-8", keyName_mapping={}, protoData=None):
	def read_varint(data):
		value = 0
		shift = 0

		while True:
			b = (data[0] if isinstance(data[0], int) else ord(data[0])); data = data[1:]
			value |= (b & 0x7F) << shift
			if not (b & 0x80):
				break
			shift += 7

		return value, data

	if protoData is None:
		protoData = base64.b64decode(message)
		flag = protoData[0]; protoData = protoData[1:]

		protoLen = struct.unpack(">I", protoData[:4])[0]; protoData = protoData[4:]
		if protoLen != len(protoData):
			return False

	if type(keyName_mapping) is not dict: keyName_mapping = {}
	retval = jdks.loads("{}", ordered_dict=True)

	while len(protoData) > 0:
		key, protoData = read_varint(protoData)
		fieldNum = str(key >> 3)
		fieldName = keyName_mapping.get(fieldNum,{}).get("name",fieldNum)
		wireType = key & 0x07

		if wireType == 0: # varint
			value, protoData = read_varint(protoData)

			value = struct.pack("<Q", value)
			value = struct.unpack("<q", value)[0]

			retval.set(fieldName, value)

		elif wireType == 2: # length-delimited
			length, protoData = read_varint(protoData)

			if length > len(protoData):
				return False

			value = protoData[:length]; protoData = protoData[length:]

			if retval.get(fieldName)["value"] == "JSON_DUPLICATE_KEYS_ERROR":
				sub_keyName_mapping = keyName_mapping.get(fieldNum,{}).get("subNames",{})
				if sub_keyName_mapping.get("$1$",False):
					sub_keyName_mapping = sub_keyName_mapping.get("$1$",{})
			elif type(retval.get(fieldName)["value"]) == list:
				sub_keyName_mapping = keyName_mapping.get(fieldNum,{}).get("subNames",{}).get("$"+str(len((retval.get(fieldName)["value"]))+1)+"$",{})
			else:
				sub_keyName_mapping = keyName_mapping.get(fieldNum,{}).get("subNames",{})
				if sub_keyName_mapping.get("$2$",False):
					sub_keyName_mapping = sub_keyName_mapping.get("$2$",{})

			nestedMessage = Protobuf2JSON(None, Coding=Coding, keyName_mapping=sub_keyName_mapping, protoData=value)
			if nestedMessage is False:
				value = value.decode(Coding)
			else:
				value = nestedMessage.getObject()

			if retval.get(fieldName)["value"] == "JSON_DUPLICATE_KEYS_ERROR":
				retval.set(fieldName, value)
			elif type(retval.get(fieldName)["value"]) == list:
				retval.insert(fieldName, value)
			else:
				prev_value = retval.get(fieldName)["value"]
				retval.update(fieldName, [prev_value, value])

		else:
			return False

	return retval