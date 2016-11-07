# -*- coding: utf-8 -*-

# NaitoTakaya
# pontyasan★Gmail.com

#起動コマンド
"""
import sys
sys.path.insert(0,r'お好みのパス')
import CreateStrechIK
reload(CreateStrechIK)
"""
import math
import functools
import maya.cmds as cmds

def main(*args):
    curve = cmds.textField('inputTextField', q=True, text=True)

    if cmds.checkBox('ScaleX', q=True, value=True) == True:
        axis = 'X'
    elif cmds.checkBox('ScaleY', q=True, value=True) == True:
        axis = 'Y'
    elif cmds.checkBox('ScaleZ', q=True, value=True) == True:
        axis = 'Z'
    else:
        pass

    curveNode = cmds.listRelatives(curve,s=True)
    ik = cmds.listConnections(curveNode,d=True)
    effector = cmds.listConnections(ik, s=True, type='ikEffector')
    jt = cmds.listConnections(ik, s=True, type='joint')[0]
    jtList = cmds.listRelatives(jt, ad=True,type='joint')
    jtList.reverse()
    jtList.insert(0,jt)

    # rc = cmds.createNode('rebuildCurve')
    # cmds.connectAttr(curveNode[0] + '.worldSpace[0]',rc + '.inputCurve')
    # cmds.setAttr(rc + '.keepRange', 0)
    # curveNode.insert(0,rc)



    #Create Locater
    n = 0
    pociList = []
    locList = []
    locTopNode = cmds.createNode('transform', n=jt + '_locGroup')
    for i in xrange(len(jtList)):
        n = n + 1
        loc = cmds.spaceLocator(n=jt + '_loc' + str(n))
        locList.append(loc[0])
        cmds.setAttr(loc[0]+'.translateX', cmds.xform(jt, q=True, ws=True ,t=True)[0])
        cmds.setAttr(loc[0]+'.translateY', cmds.xform(jt, q=True, ws=True ,t=True)[1])
        cmds.setAttr(loc[0]+'.translateZ', cmds.xform(jt, q=True, ws=True ,t=True)[2])
        cmds.parent(loc[0], locTopNode)
        
        poci = cmds.createNode('pointOnCurveInfo', n=jt + '_poci' + str(n))
        pociList.append(poci)
        cmds.setAttr(jt + '_poci' + str(n) + '.turnOnPercentage', 1)
        cmds.connectAttr(curveNode[0] + '.worldSpace[0]',poci + '.inputCurve')
        cmds.connectAttr(jt + '_poci' + str(n) + '.result.position', jt + '_loc' + str(n) + '.translate')

    #get jt all range
    AllLength = 0
    for i in xrange(len(jtList)-1):
        #print jtList[i] + '|' + jtList[i+1]
        x1 = cmds.xform(jtList[i], q=True, ws=True ,t=True)[0]
        y1 = cmds.xform(jtList[i], q=True, ws=True ,t=True)[1]
        z1 = cmds.xform(jtList[i], q=True, ws=True ,t=True)[2]
        x2 = cmds.xform(jtList[i+1], q=True, ws=True ,t=True)[0]
        y2 = cmds.xform(jtList[i+1], q=True, ws=True ,t=True)[1]
        z2 = cmds.xform(jtList[i+1], q=True, ws=True ,t=True)[2]
        
        AllLength = AllLength + math.pow( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1), 0.5 )
        

    #それぞれのパラメーターを設定
    tempLength = 0
    for i in xrange(len(jtList)-1):
        x1 = cmds.xform(jtList[i], q=True, ws=True ,t=True)[0]
        y1 = cmds.xform(jtList[i], q=True, ws=True ,t=True)[1]
        z1 = cmds.xform(jtList[i], q=True, ws=True ,t=True)[2]
        x2 = cmds.xform(jtList[i+1], q=True, ws=True ,t=True)[0]
        y2 = cmds.xform(jtList[i+1], q=True, ws=True ,t=True)[1]
        z2 = cmds.xform(jtList[i+1], q=True, ws=True ,t=True)[2]
        
        length = math.pow( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1), 0.5 )
        tempLength = tempLength + (length/AllLength)
        cmds.setAttr(pociList[i + 1] + '.parameter', tempLength)
        
    #DistanceBeetWeen
    for i in xrange(len(jtList)-1):
        db = cmds.createNode('distanceBetween', name=locList[i] + '_db_' + str(i))
        cmds.connectAttr(locList[i] + '.translate',db + '.point1')
        cmds.connectAttr(locList[i+1] + '.translate',db + '.point2')
        md = cmds.createNode('multiplyDivide', name=locList[i] + '_md' + str(i))
        cmds.setAttr(md + '.operation', 2)
        cmds.connectAttr(db + '.distance', md + '.input1X')
        cmds.setAttr(md + '.input2X',cmds.getAttr(db+'.distance'))
        cmds.connectAttr(md + '.outputX',jtList[i+1] + '.scale%s'%axis)

def getTextField(TF, *args):
    TFtext = cmds.ls(sl=True)[0]
    print str(TFtext)
    cmds.textField('%s'%TF,e=True,text=str(TFtext))


def editCheckBox(checkBoxType, *args):
    cmds.checkBox('ScaleX', e=True, value=False)
    cmds.checkBox('ScaleY', e=True, value=False)
    cmds.checkBox('ScaleZ', e=True, value=False)
    cmds.checkBox('%s'%checkBoxType, e=True, value=True)  


def mainWindow():
    windowName = u'StrechIKMaker'
    windowTitle = u'StrechIKMaker'
    
    if cmds.window(windowName,exists = True):
        cmds.deleteUI(windowName, window = True)

    cmds.window(windowName,title=windowTitle,menuBar=True)
    cmds.setParent( windowName )

    CL = cmds.columnLayout(adjustableColumn=True)
    cmds.text(label=u'SplinIKカーブ', p=CL)
    cmds.textField('inputTextField',text='', p=CL)
    cmds.button(label = u"取得", c=functools.partial(getTextField, 'inputTextField'), p=CL)
    cmds.text(label='', p=CL)
    
    RC = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 112.5), (2, 112.5), (3, 112.5)])
    cmds.checkBox('ScaleX', label = u"ScaleX", onCommand=functools.partial(editCheckBox, 'ScaleX'), p=RC)
    cmds.checkBox('ScaleY', label = u"ScaleY", onCommand=functools.partial(editCheckBox, 'ScaleY'), p=RC)
    cmds.checkBox('ScaleZ', label = u"ScaleZ", onCommand=functools.partial(editCheckBox, 'ScaleZ'), p=RC)

    cmds.button(label = u"実行",c=functools.partial(main), p=CL)
    cmds.showWindow()

mainWindow()