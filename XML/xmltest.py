import xml.etree.ElementTree as et
et = et.ElementTree(file="xmltest.xml")
print(et)
root = et.getroot()

print(root.tag)         # datas  标签
print(root.attrib)      # {'title': 'root'}   属性
print(root[0][1].text)  # 18    值

for tag in root:
    print(tag.tag, tag.attrib)