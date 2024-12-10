import os
import xml.etree.ElementTree as ET
import pandas as pd
from OtherFunctions.logdefine import MyLogging

mlogger = MyLogging(file=f"./log.log")


class MyXml:
    def __init__(self, input_file, save_path):
        """
        :param input_file: 输入路径,列表
        :param save_path:
        """
        self.input_file = input_file
        self.save_path = save_path
        self.res = pd.DataFrame()

    def xml2excel(self):
        for xml in self.input_file:
            if xml.endswith('.xml'):
                document = ET.parse(xml)
                root = document.getroot()
                dic = {}
                n = [i for i in root[1][2][0].attrib.keys()]
                for i in root[1][1]:
                    a = {i.text: int(list(i.attrib.values())[0]) - 1}
                    dic.update(a)
                    n.append(i.text)
                print(n)

                df = pd.DataFrame(columns=n)
                num = 0

                for i in root[1][2]:
                    v = [x for x in i.attrib.values()]
                    for j in dic.values():
                        # print(i[j].text)
                        v.append(i[j].text)
                    df.loc[num, :] = v
                    num += 1
                    mlogger.info(f"{num},{v[0]}")
                    v.clear()
                save = os.path.join(self.save_path, os.path.basename(xml).rsplit('.', 1)[0] + '.xlsx')
                self.res = df
                df.to_excel(save)
                mlogger.info(f'suss:{save}')


if __name__ == "__main__":

    a = MyXml(input_file=[r'E:\Desktop\CM-GNB-SA-CELLSELECTION-A001-ALLV1.6.0-20231113010000.xml'], save_path='E:\Desktop')
    a.xml2excel()

