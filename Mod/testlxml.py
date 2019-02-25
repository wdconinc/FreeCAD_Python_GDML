from lxml import etree
'''
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
'''
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i
mats = etree.Element("materials")
etree.SubElement(mats, "element", name='Nitrogen', formula='N')
gdml_str = etree.tostring(mats, pretty_print=True)
print gdml_str
indent(mats)
doc = etree.ElementTree(mats)
outfile = open('test.xml','w')
doc.write(outfile, xml_declaration=True, encoding='utf-8')
#gdml.write("test.xml",pretty_print=True)
