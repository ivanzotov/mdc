# import maya
# maya.cmds.sphere()
# maya.cmds.deformer( type='cacheNode' )

import math, sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeTypeName = "cacheNode"

cacheNodeId = OpenMaya.MTypeId(0x8703)

# Node definition
class cacheNode(OpenMayaMPx.MPxDeformerNode):
        # class variables
        angle = OpenMaya.MObject()
        # constructor
        def __init__(self):
                OpenMayaMPx.MPxDeformerNode.__init__(self)
        # deform
        def deform(self,dataBlock,geomIter,matrix,multiIndex):
                #
                # get the angle from the datablock
                angleHandle = dataBlock.inputValue( self.angle )
                angleValue = angleHandle.asDouble()
                #
                # get the envelope
                envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
                envelopeHandle = dataBlock.inputValue( envelope )
                envelopeValue = envelopeHandle.asFloat()
                #
                # iterate over the object and change the angle
                while geomIter.isDone() == False:
                        point = geomIter.position()
                        ff = angleValue * point.y * envelopeValue
                        if ff != 0.0:
                                cct= math.cos(ff)
                                cst= math.sin(ff)
                                tt= point.x*cct-point.z*cst
                                point.z= point.x*cst + point.z*cct
                                point.x=tt
                        geomIter.setPosition( point )
                        geomIter.next()
                                
# creator
def nodeCreator():
        return OpenMayaMPx.asMPxPtr( cacheNode() )

# initializer
def nodeInitializer():
        # angle
        nAttr = OpenMaya.MFnNumericAttribute()
        cacheNode.angle = nAttr.create( "angle", "fa", OpenMaya.MFnNumericData.kDouble, 0.0 )
        #nAttr.setDefault(0.0)
        nAttr.setKeyable(True)
        # add attribute
        try:
                cacheNode.addAttribute( cacheNode.angle )
                outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
                cacheNode.attributeAffects( cacheNode.angle, outputGeom )
        except:
                sys.stderr.write( "Failed to create attributes of %s node\n", kPluginNodeTypeName )
        
# initialize the script plug-in
def initializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.registerNode( kPluginNodeTypeName, cacheNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kDeformerNode )
        except:
                sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.deregisterNode( cacheNodeId )
        except:
                sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )

