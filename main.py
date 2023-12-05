#!/usr/bin/env python
# -*- coding: shift_jis -*-
import maya.cmds as mc
import maya.mel as mm

class weightRebalance():
	def __init__(self):
		#�}�b�N�X�C���t���G���X���w�肵�܂�
		global MaxInfl	
		#�l�̌ܓ����錅��ݒ肵�܂�
		global roundPoint	
		##��ł܂Ƃ߂Đ��K������̂ŁA���X�g�ɓ���Ƃ��܂�
		global skinClusterList	
		#�G���[���N�����Ă��钸�_�����X�g���܂�
		global errorVertex		
				
		#�}�b�N�X�C���t���G���X���w�肵�܂�
		MaxInfl = 3
		
		#�l�̌ܓ����錅��ݒ肵�܂�
		roundPoint = 2
		
		##��ł܂Ƃ߂Đ��K������̂ŁA���X�g�ɓ���Ƃ��܂�
		skinClusterList = []
		
		#�G���[���N�����Ă��钸�_�����X�g���܂�
		errorVertex = []
	
	#---------------------------------------------------------------------------------------------------------------------	
	def createUI(self, *args):
		if mc.window( 'weightRoundWindow', q=True, ex=True):
			mc.deleteUI( 'weightRoundWindow' )
		mc.window( 'weightRoundWindow' )
		mc.frameLayout( 'mainFrame', p='weightRoundWindow', l='weightRound' )
		mc.rowColumnLayout( 'mainLay', p='mainFrame', nc=2 )
		mc.intField( 'roundWeightFields',p='mainLay', value=3, ann='ex)3-->0.001, 2-->0.01, 1-->0.1' )
		mc.button( 'roundButton', p='mainLay', l='round vtx weight', c= self.roundSkinWeights  )
		mc.intField( 'maxInflFields',p='mainLay', value=3, ann='�ő�C���t���G���X���ł��B�w�肷�邱�ƂŁA���_�E�F�C�g�ɑ΂���W���C���g�̐������������܂�')
		mc.button( 'maxButton', p='mainLay', l='force max influence', c=self.maxInfllenceAdjustment )
		mc.button( 'selectErrorVtxButton', p='mainLay', l='error weight vtx', c= self.thresholdDetermination )
		mc.showWindow( 'weightRoundWindow' )
	#---------------------------------------------------------------------------------------------------------------------
	def weightBalanceList(self, vtx, connectSkinsName, *args):

		#�I���������_�̃C���t���G���V�����Ȋe�W���C���g�����X�g���܂�
		listWeightJoint = mc.skinPercent( connectSkinsName, vtx, q=True , t=None )
		#���X�g�����W���C���g���x�z���Ă���p�[�Z���e�[�W���擾���܂�
		listWeightValue = mc.skinPercent( connectSkinsName, vtx, q=True , v=True )
		
		
		#�E�F�C�g�������Ă���W���C���g���s�b�N�A�b�v���A���E���h���Ċi�[���܂�
		haveWeightDicBuf = {}
		for i,v in enumerate(listWeightJoint):
			if listWeightValue[i] > 0:		
				roundNum = 	round(listWeightValue[i], roundPoint)
				haveWeightDicBuf[v] = roundNum
		
		return haveWeightDicBuf
	
	#---------------------------------------------------------------------------------------------------------------------	
	def roundSkinWeights(self, *args):
		#�}�b�N�X�C���t���G���X���w�肵�܂�
		global MaxInfl
		MaxInfl = mc.intField( 'roundWeightFields', q=True, value=True )		
		#�l�̌ܓ����錅��ݒ肵�܂�
		global roundPoint
		roundPoint = mc.intField( 'maxInflFields', q=True, value=True )
				
		##��ł܂Ƃ߂Đ��K������̂ŁA���X�g�ɓ���Ƃ��܂�
		global skinClusterList
		
		#�G���[���N�����Ă��钸�_�����X�g���܂�
		global errorVertex
		
		
		#�I���������_���t���b�g�Ŏ擾���܂��B
		selectVert = mc.ls(sl=True,fl=True)

		#�v���O���X�E�B���h�E����
		numberVtx = len(selectVert)
		amount = 0
		mc.progressWindow( title='please weight...', progress=amount, status='now check: 0%', isInterruptable=True )
		#�v���O���X�E�B���h�E����
				
		for vtx in selectVert:
			#�擾�������_���x�z���Ă���X�L���N���X�^�[���擾���܂��B
			objSkinName = vtx.split('.')
			connectSkinsName = mm.eval('findRelatedSkinCluster %s' % objSkinName[0])
			
			#��ł܂Ƃ߂Đ��K������̂ŁA���X�g�ɓ���Ƃ��܂�
			skinClusterList.append(connectSkinsName)
			
			#�X�L���N���X�^�̃E�F�C�g�l���K������
			mc.setAttr (connectSkinsName +".normalizeWeights", 0)
			
			#�I���������_�̃C���t���G���V�����Ȋe�W���C���g�����X�g���܂�
			listWeightJoint = mc.skinPercent( connectSkinsName, vtx, q=True , t=None )
			#���X�g�����W���C���g���x�z���Ă���p�[�Z���e�[�W���擾���܂�
			listWeightValue = mc.skinPercent( connectSkinsName, vtx, q=True , v=True )
			
			
			#�E�F�C�g�������Ă���W���C���g���s�b�N�A�b�v���A���E���h���Ċi�[���܂�
			haveWeightDic = {}
			for i,v in enumerate(listWeightJoint):
				if listWeightValue[i] > 0:		
					roundNum = 	round(listWeightValue[i], roundPoint)
					haveWeightDic[v] = roundNum
			
				
			#���E���h�����E�F�C�g�����ׂđ����ƁA1�ȊO�ɂȂ�ꍇ
			weightPointList = haveWeightDic.values()
			totalPoint = sum(weightPointList)
			if totalPoint != 1:
				print weightPointList
				#���X�g���̈�ԑ傫�Ȓl�ƁA������i�[���Ă��郊�X�g�ԍ����擾���܂�
				mx = max(weightPointList)
				mxIndex = weightPointList.index(mx)
					
				#1����A���v���������āA��������ԑ傫�Ȓl�����W���C���g�ɑ�������ŁA������E�F�C�g���X�g�ɍĊi�[���܂�
				diff = 1 - totalPoint
				weightPointList[mxIndex] = mx + diff
			
				weightedJoints = haveWeightDic.keys()
				for i,v in enumerate(weightedJoints):
					haveWeightDic[v] = weightPointList[i]
			
			
			#�E�F�C�g�̃C���t���G���X���K��l�𒴂��Ă���ꍇ�̓G���[��\�����܂�
			if len(haveWeightDic) > MaxInfl:
				errorVertex.append(vtx)
				print vtx + u'<---���̒��_�̓}�b�N�X�C�t���G���X���K��l�𒴂��Ă��܂�'
			
			
			#���ʂ��E�F�C�g�l�ɖ߂��܂�
			weightedJoints = haveWeightDic.keys()
			for v in weightedJoints:
				mc.skinPercent( connectSkinsName, vtx, tv=(v, haveWeightDic[v]), normalize=False )
		

			#�v���O���X�E�B���h�E����
			if mc.progressWindow( q=True, isCancelled=True ):
				break
			
			adoptNum = str(amount/numberVtx)
			mc.progressWindow( e=True, progress=(int((amount*1.0)/numberVtx*100)), status=('now check:' + adoptNum + '%') )
			amount = amount +1
			
		mc.progressWindow( endProgress=True )		
		#�v���O���X�E�B���h�E����
				
		#�X�L���N���X�^�̃E�F�C�g�l���K���Đݒ�
		for skinCls in skinClusterList:
			mc.setAttr (skinCls +".normalizeWeights", 1)
		
		skinClusterList = []
	#---------------------------------------------------------------------------------------------------------------------
	
	#---------------------------------------------------------------------------------------------------------------------	
	def maxInfllenceAdjustment(self, *args):
	
		#�}�b�N�X�C���t���G���X���w�肵�܂�
		global MaxInfl
		MaxInfl = mc.intField( 'roundWeightFields', q=True, value=True )		
		#�l�̌ܓ����錅��ݒ肵�܂�
		global roundPoint
		roundPoint = mc.intField( 'maxInflFields', q=True, value=True )
				
		##��ł܂Ƃ߂Đ��K������̂ŁA���X�g�ɓ���Ƃ��܂�
		global skinClusterList
		
		#�G���[���N�����Ă��钸�_�����X�g���܂�
		global errorVertex
	
		#maxInflence�𒴂��ăE�F�C�g�������Ă��钸�_�𒲐����܂�
		selectVert = mc.ls(errorVertex,fl=True)
		
		#�v���O���X�E�B���h�E����
		numberVtx = len(selectVert)
		amount = 0
		mc.progressWindow( title='please weight...', progress=amount, status='now check: 0%', isInterruptable=True )
		#�v���O���X�E�B���h�E����
		
		for vtx in selectVert:
			#�擾�������_���x�z���Ă���X�L���N���X�^�[���擾���܂��B
			objSkinName = vtx.split('.')
			connectSkinsName = mm.eval('findRelatedSkinCluster %s' % objSkinName[0])
			
			#��ł܂Ƃ߂Đ��K������̂ŁA���X�g�ɓ���Ƃ��܂�
			skinClusterList.append(connectSkinsName)
			
			#�X�L���N���X�^�̃E�F�C�g�l���K������
			mc.setAttr (connectSkinsName +".normalizeWeights", 0)
			
			#�E�F�C�g�������Ă���W���C���g���s�b�N�A�b�v���A���E���h���Ċi�[���܂�
			haveWeightDic = self.weightBalanceList(vtx,connectSkinsName)			
			
			
			#maxInfllence����ǂ̂��炢�I�[�o�[���Ă��邩���J�E���g���܂�
			subPoint = len( haveWeightDic ) - MaxInfl
			
			getMiniPoint = 0.0
			
			#maxInfllence�𒴂��ăE�F�C�g���Ȃ���Ă����ꍇ�A��������
			if subPoint > 0:
				#�E�F�C�g�̏�����������\�[�g�����������X�g���쐬���܂�
				sortWeightlist = haveWeightDic.items()
				sortWeightlist.sort(key=lambda a: a[1])
				
				#�W���C���g�ƃE�F�C�g�̃��X�g���쐬���܂�
				jointSortList = []
				pointSortList = []
				for i in sortWeightlist:
					jointSortList.append(i[0])
					pointSortList.append(i[1])
				
				#�������E�F�C�g���I�[�o�[���Ă��鐔�������܂�
				#�I�[�o�[���Ă���C���t���G���X�𒲐����邽�߂ɁA�������E�F�C�g���珇�ԂɃE�F�C�g��0�ɂ��Ă����܂�
				for i in range(0,subPoint):
					getMiniPoint = getMiniPoint + pointSortList[i]
					pointSortList[i] = 0
				
				#���ς��v�Z���āAfor���Ń��X�g�𑫂��Z
				avg = round( getMiniPoint / MaxInfl, roundPoint)
				n = -1
				
				for i in range(0,subPoint):
					pointSortList[n] = round( pointSortList[n] + avg, roundPoint) 
					n = n -1
				
				
				#���v������ȊO�̏ꍇ�̏���
				total = sum(pointSortList)
				if total != 1:
					sub =  round( 1 - total, roundPoint) 
					pointSortList[n] = pointSortList[n] + sub
					
			
				#���ʂ��E�F�C�g�l�ɖ߂��܂�
				for i,v in enumerate(jointSortList):
					mc.skinPercent( connectSkinsName, vtx, tv=(v, pointSortList[i]), normalize=False )
			
			#�v���O���X�E�B���h�E����
			if mc.progressWindow( q=True, isCancelled=True ):
				break
			
			adoptNum = str(amount/numberVtx)
			mc.progressWindow( e=True, progress=(int((amount*1.0)/numberVtx*100)), status=('now check:' + adoptNum + '%') )
			amount = amount +1
			
		mc.progressWindow( endProgress=True )		
		#�v���O���X�E�B���h�E����
		
		#�X�L���N���X�^�̃E�F�C�g�l���K���Đݒ�
		for skinCls in skinClusterList:
			mc.setAttr (skinCls +".normalizeWeights", 1)
		
	#---------------------------------------------------------------------------------------------------------------------
		
	
	
	#---------------------------------------------------------------------------------------------------------------------	
	def thresholdDetermination(self, *args):
		#�I���������_���t���b�g�Ŏ擾���܂��B
		selectVert = mc.ls(sl=True,fl=True)
		
		#�G���[���N�����Ă��钸�_���i�[���܂�
		
		errorVertex = []
		
		numberVtx = len(selectVert)
		amount = 0
		mc.progressWindow( title='please weight...', progress=amount, status='now check: 0%', isInterruptable=True )
		
		for vtx in selectVert:
			#�擾�������_���x�z���Ă���X�L���N���X�^�[���擾���܂��B
			objSkinName = vtx.split('.')
			connectSkinsName = mm.eval('findRelatedSkinCluster %s' % objSkinName[0])
						
			#�E�F�C�g�������Ă���W���C���g���s�b�N�A�b�v���A���E���h���Ċi�[���܂�
			haveWeightDic = self.weightBalanceList(vtx,connectSkinsName)
			
			#�E�F�C�g�̃C���t���G���X���K��l�𒴂��Ă���ꍇ�̓G���[��\�����܂�
			if len(haveWeightDic) > MaxInfl:
				errorVertex.append(vtx)
				print vtx + u'<---���̒��_�̓}�b�N�X�C�t���G���X���K��l�𒴂��Ă��܂�'		
			
			
			if mc.progressWindow( q=True, isCancelled=True ):
				break
			
			adoptNum = str(amount/numberVtx)
			mc.progressWindow( e=True, progress=(int((amount*1.0)/numberVtx*100)), status=('now check:' + adoptNum + '%') )
			amount = amount +1
			
		mc.progressWindow( endProgress=True )	
		
		if errorVertex != []:
			mc.select(errorVertex,r=True)
			mc.confirmDialog(m='���I�����Ă��钸�_�̓}�b�N�X�C���t���G���X���I�[�o�[���Ă��܂�')
		else:
			mc.select(clear=True)
			mc.confirmDialog(m='�}�b�N�X�C���t���G���X���z���Ă��钸�_�͑��݂��܂���')


weightRebalance().createUI()
