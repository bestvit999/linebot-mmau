from graphviz import Digraph
import pydotplus as pydot
from urllib.request import urlretrieve
import dbmgr
import os
from location import get_location

def setLabel(hench,formular,level,pic_src,drop):
	location = get_location(hench)
	if os.path.isfile('graph/srcImage/'+pic_src):
		label = '<<table border="0"><tr><td border="0"><img src="srcImage/'+ pic_src +'"/></td></tr><tr><td>'+ hench + ' ' + level + '</td></tr><tr><td>' + drop + '</td></tr><tr><td>地圖: ' + str(location) + '</td></tr>' + formular +'</table>>'
		return label
	else:
		urlretrieve("https://mixmasteronline.com.au/resources/uploads/common/formular/" + pic_src, 'graph/srcImage/'+pic_src)
		label = '<<table border="0"><tr><td border="0"><img src="srcImage/'+ pic_src +'"/></td></tr><tr><td>'+ hench + ' ' + level + '</td></tr><tr><td>' + drop + '</td></tr><tr><td>地圖: ' + str(location) + '</td></tr>' + formular +'</table>>'
		return label

def createGraph(hench):
	if os.path.isfile('graph/' + hench.lower().replace(' ','') + '.png'):
		return 'graph/' + hench.lower().replace(' ','') + '.png'
	else:
		hench = hench.lower().replace(' ','')
		formulars = dbmgr.selectMonsterinFormular(hench)
		formular = setFormularToHtml(str(dbmgr.selectFormular(hench)))
		level = dbmgr.selectLevel(hench)
		pic_src = swapDeadImg(dbmgr.selectPic(hench))
		drop = dbmgr.selectDropped(hench)
		label = setLabel(hench,formular,level,pic_src,drop)

		dot = Digraph(comment='mix graph',format='png')
		dot.node(hench,label=label,fontname="Microsoft YaHei",shape='box',style='rounded')	
		
		for _hench in formulars:
			_formulars = dbmgr.selectMonsterinFormular(_hench)
			formular = setFormularToHtml(str(dbmgr.selectFormular(_hench)))
			level = dbmgr.selectLevel(_hench)
			pic_src = swapDeadImg(dbmgr.selectPic(_hench))
			drop = dbmgr.selectDropped(_hench)
			label = setLabel(_hench,formular,level,pic_src,drop)

			dot.node(_hench,label=label,fontname="Microsoft YaHei",shape='box',style='rounded')
			dot.edge(hench,_hench)

			for __hench in _formulars:
				formular = setFormularToHtml(str(dbmgr.selectFormular(__hench)))
				level = dbmgr.selectLevel(__hench)
				pic_src = swapDeadImg(dbmgr.selectPic(__hench))
				drop = dbmgr.selectDropped(__hench)
				label = setLabel(__hench,formular,level,pic_src,drop)

				dot.node(__hench,label=label,fontname="Microsoft YaHei",shape='box',style='rounded')
				dot.edge(_hench,__hench)
		dot.render(hench,'graph')

		return 'graph/' + hench.lower().replace(' ','') + '.png'

def setFormularToHtml(formular):
	formulars = formular.split(', ')
	html = ''

	for each in formulars:
		each.replace('\'','')
		html += '<tr><td>' + each  +'</td></tr>'
	return html

def swapDeadImg(img_src):
	src = {
        '1996.png' : '1807.png',
        '1865.png' : "1.png",
        '1907.png' : "4.png",
        '457.png' : '389.png'
    }
	return src.get(img_src,img_src)