try:
	unicode # Python 2
except NameError:
	unicode = str # Python 3

import platform
import time
import uuid as _uuid
import base64
import random
import string
import binascii

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


def XML2JSON(message):
	if platform.python_version_tuple()[0] == "3":
		# ===== Fallback Python (ElementTree) =====
		import xml.etree.ElementTree as ET
		try:
			from io import StringIO
		except:
			from StringIO import StringIO

		if not isinstance(message, str):
			message = message.decode("utf-8")

		uri2prefix = {}
		prefix2uri = {}

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

		def parse(elem):
			tag = qname(elem.tag)
			node = {}

			# ---- attributes ----
			attrs = {}

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
				node["@attributes"] = attrs

			# ---- children ----
			children = {}
			has_child = False

			for child in elem:
				has_child = True
				child_tag = qname(child.tag)
				child_obj = parse(child)[child_tag]

				if child_tag in children:
					if not isinstance(children[child_tag], list):
						children[child_tag] = [children[child_tag]]
					children[child_tag].append(child_obj)
				else:
					children[child_tag] = child_obj

			if children:
				node.update(children)

			# ---- text ----
			if not has_child:
				text = elem.text
				if text is None:
					node["#text"] = ""
				else:
					node["#text"] = text.strip() if text.strip() else ""

			return {tag: node}

		return parse(root)
	else:
		# ===== Try Jython (Java DOM) =====
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
			node_obj = {}

			# attributes
			attrs = {}
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
			children = {}
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